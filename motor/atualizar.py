#!/usr/bin/env python3
"""Atualização do painel SOMA (vendas e estoque Shopify) — usado pela tarefa agendada e à mão.

Passo a passo:
  1) python3 motor/atualizar.py --consultas      -> imprime as consultas Shopify, já com as datas
  2) rodar as consultas no conector da Shopify e salvar os resultados em motor/entrada.json
     (formato abaixo, números exatamente como vieram da Shopify)
  3) python3 motor/atualizar.py motor/entrada.json
     -> valida, atualiza os JSON desta pasta e regenera index.html e teste.html na raiz do repositório.
     Sai com código 0 e a linha "OK PARA PUBLICAR" só se tudo passou. Com erro, nada é gravado.

Formato de motor/entrada.json:
{
  "pedidos": [["2026-11-01", 1111, 2562], ...],          # consulta 1: dia, orders, net_items_sold
  "skus":    [["2026-11-01", "SOMAPINA", 1308], ...],      # consulta 2: dia, product_variant_sku, net_items_sold (inclui SOMAROJO)
  "estoque": [["SOMAPINA", "Melonn Bogota", 0, 874], ...], # consulta 3: sku, local, available, committed (uma linha por produto e local; SOMAROJO vem de 4 produtos)
  "link":    [["2026-11-01", 2, 2, 199800], ...],          # consulta 4: dia, orders, net_items_sold, gross_sales
  "dist":    {"d30": [["Bogotá, D.C.", "SOMAPINA", 6435], ...],   # consultas 5 e 6 (só quando pedidas)
              "d7":  [["Bogotá, D.C.", "SOMAPINA", 1923], ...]}
}
"""
import json, os, sys, subprocess, unicodedata, datetime as dt
from zoneinfo import ZoneInfo

BASE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(BASE)
TZ_LOJA = ZoneInfo("America/Bogota")      # fuso da loja (dias da ShopifyQL)
TZ_USER = ZoneInfo("America/Sao_Paulo")   # horário mostrado em "atualizado"
DIAS_ATRAS = 10
SKUS = {"SOMAPINA": "p", "SOMANARANJA": "n", "SHAKER": "s", "SOMAROJO": "r"}
KS = "pnsr"   # r = Frutos Rojos (SOMAROJO), desde 10/11/2026
BODS = ["Bogotá", "Medellín", "Cali", "Barranquilla"]
LINK_PRODUCT_ID = 8311531339833
VARIANTES = ["gid://shopify/ProductVariant/45650513920057",   # SOMAPINA (Soma Sculpt Piña)
             "gid://shopify/ProductVariant/45650513952825",   # SOMANARANJA (Soma Sculpt Naranja)
             "gid://shopify/ProductVariant/46302938300473",   # Shaker (Shaker Termo Gratis)
             # SOMAROJO (Frutos Rojos): 4 produtos com o mesmo SKU; disponível igual, comprometido somado
             "gid://shopify/ProductVariant/51133011329081",   # Soma Sculpt - Limitado · Rojos
             "gid://shopify/ProductVariant/51156236206137",   # Soma Sculpt · Rojos
             "gid://shopify/ProductVariant/51054710620217",   # SOMA ROJO
             "gid://shopify/ProductVariant/51133477191737"]   # REGALO DE CREATORS BIENVENIDA - ROJO


def p(path):
    return os.path.join(BASE, path)


def load(name):
    with open(p(name), encoding="utf-8") as f:
        return json.load(f)


def save(name, obj, compact=True):
    with open(p(name), "w", encoding="utf-8") as f:
        if compact:
            json.dump(obj, f, ensure_ascii=False, separators=(",", ":"))
        else:
            json.dump(obj, f, ensure_ascii=False, indent=1)


def norm(s):
    s = unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode().lower()
    return " ".join(s.split())


def n_int(v):
    return int(round(float(str(v).replace(",", ""))))


def hoje_loja():
    return dt.datetime.now(TZ_LOJA).date()


def precisa_dist():
    dist = load("dist.json")
    fim = dist.get("vendas_periodo", {}).get("d30", "").split("–")[-1].strip()  # "08/11"
    ontem = hoje_loja() - dt.timedelta(days=1)
    return fim != ontem.strftime("%d/%m")


def lista_consultas():
    """[(chave, tipo, consulta)] — tipo "shopifyql" ou "graphql". Usado pelo auto_shopify.py (GitHub Actions)."""
    d0 = hoje_loja() - dt.timedelta(days=DIAS_ATRAS)
    ontem = hoje_loja() - dt.timedelta(days=1)
    q = [("pedidos", "shopifyql", f"FROM sales SHOW orders, net_items_sold WHERE order_payment_status = 'Paid' TIMESERIES day SINCE {d0} UNTIL today"),
         ("skus", "shopifyql", f"FROM sales SHOW orders, net_items_sold WHERE order_payment_status = 'Paid' AND product_variant_sku IN ('SOMAPINA','SOMANARANJA','Shaker','SOMAROJO') GROUP BY product_variant_sku TIMESERIES day SINCE {d0} UNTIL today"),
         ("estoque", "graphql", '{ nodes(ids: ' + json.dumps(VARIANTES) + ') { ... on ProductVariant { sku inventoryItem { inventoryLevels(first: 10) { nodes { location { name } quantities(names: ["available","committed","on_hand"]) { name quantity } } } } } } }'),
         ("link", "shopifyql", f"FROM sales SHOW orders, net_items_sold, gross_sales WHERE product_id = {LINK_PRODUCT_ID} AND order_payment_status = 'Paid' TIMESERIES day SINCE {d0} UNTIL today")]
    if precisa_dist():
        for k, n in (("d30", 30), ("d7", 7)):
            ini = ontem - dt.timedelta(days=n - 1)
            q.append(("dist_" + k, "shopifyql", f"FROM sales SHOW net_items_sold WHERE order_payment_status = 'Paid' AND product_variant_sku IN ('SOMAPINA','SOMANARANJA','Shaker','SOMAROJO') GROUP BY shipping_region, product_variant_sku SINCE {ini} UNTIL {ontem} LIMIT 300"))
    return q


def consultas():
    d0 = hoje_loja() - dt.timedelta(days=DIAS_ATRAS)
    ontem = hoje_loja() - dt.timedelta(days=1)
    q = []
    q.append(("1 pedidos (run-analytics-query)",
              f"FROM sales SHOW orders, net_items_sold WHERE order_payment_status = 'Paid' TIMESERIES day SINCE {d0} UNTIL today"))
    q.append(("2 skus (run-analytics-query)",
              f"FROM sales SHOW orders, net_items_sold WHERE order_payment_status = 'Paid' AND product_variant_sku IN ('SOMAPINA','SOMANARANJA','Shaker','SOMAROJO') GROUP BY product_variant_sku TIMESERIES day SINCE {d0} UNTIL today"))
    q.append(("3 estoque (graphql_query)",
              '{ nodes(ids: ' + json.dumps(VARIANTES) + ') { ... on ProductVariant { sku inventoryItem { inventoryLevels(first: 10) { nodes { location { name } quantities(names: ["available","committed","on_hand"]) { name quantity } } } } } } }'))
    q.append(("4 link de oferta (run-analytics-query)",
              f"FROM sales SHOW orders, net_items_sold, gross_sales WHERE product_id = {LINK_PRODUCT_ID} AND order_payment_status = 'Paid' TIMESERIES day SINCE {d0} UNTIL today"))
    if precisa_dist():
        for k, n in (("d30", 30), ("d7", 7)):
            ini = ontem - dt.timedelta(days=n - 1)
            q.append((f"{5 if k == 'd30' else 6} dist {k} (run-analytics-query)",
                      f"FROM sales SHOW net_items_sold WHERE order_payment_status = 'Paid' AND product_variant_sku IN ('SOMAPINA','SOMANARANJA','Shaker','SOMAROJO') GROUP BY shipping_region, product_variant_sku SINCE {ini} UNTIL {ontem} LIMIT 300"))
    else:
        q.append(("5/6 dist", "NÃO PRECISA hoje (distribuição já está até ontem) — não inclua \"dist\" na entrada"))
    for t, s in q:
        print(f"### {t}\n{s}\n")


class Erro(Exception):
    pass


def validar_e_mesclar(E):
    rows = load("rows.json")
    by = {r["d"]: dict(r) for r in rows}
    ult_ant = rows[-1]["d"]

    # ---------- pedidos + skus ----------
    if not E.get("pedidos"):
        raise Erro("entrada sem 'pedidos'")
    ped = {}
    for x in E["pedidos"]:
        d = str(x[0])[:10]
        dt.date.fromisoformat(d)
        ped[d] = (n_int(x[1]), n_int(x[2]))
    dias = sorted(ped)
    for a, b in zip(dias, dias[1:]):
        if (dt.date.fromisoformat(b) - dt.date.fromisoformat(a)).days != 1:
            raise Erro(f"pedidos: falta o dia entre {a} e {b}")
    if dias[0] > (dt.date.fromisoformat(ult_ant) + dt.timedelta(days=1)).isoformat():
        raise Erro(f"pedidos começam em {dias[0]}, mas o painel termina em {ult_ant}: ficaria um buraco")
    if dias[-1] < ult_ant:
        raise Erro(f"pedidos terminam em {dias[-1]}, antes do último dia do painel ({ult_ant})")
    hoje = dias[-1]

    sk = {d: {k: 0 for k in KS} for d in dias}
    vistos = set()
    for x in E.get("skus", []):
        d = str(x[0])[:10]
        k = SKUS.get(str(x[1]).strip().upper())
        if k is None or d not in sk:
            continue
        sk[d][k] += n_int(x[2])
        vistos.add(k)
    if not {"p", "n", "s"} <= vistos:   # Frutos Rojos (r) pode faltar em dias sem venda
        raise Erro(f"skus: faltam linhas de {sorted({'p','n','s'} - vistos)} — confira a consulta 2")

    # base para checar faixas: últimos 14 dias completos já publicados
    hist = [r for r in rows if r["d"] < dias[0] and r["d"] != ult_ant][-14:] or rows[-15:-1]
    med = lambda k: sorted(r[k] for r in hist)[len(hist) // 2]
    avisos = []
    for d in dias:
        o, i = ped[d]
        v = sk[d]
        novo = {"d": d, "o": o, "i": i, "p": v["p"], "n": v["n"], "s": v["s"], "r": v["r"]}
        parcial = d == hoje
        if i < o:
            raise Erro(f"{d}: itens ({i}) menor que pedidos ({o})")
        if sum(v.values()) > i + 5:
            raise Erro(f"{d}: Piña+Naranja+Shaker+Rojo ({sum(v.values())}) maior que itens ({i})")
        if d in by and d < (dt.date.fromisoformat(hoje) - dt.timedelta(days=2)).isoformat():
            for k in ("o", "p", "n", "s"):
                a, b = by[d][k], novo[k]
                if abs(b - a) > max(25, 0.04 * a):
                    raise Erro(f"{d}: {k} mudou de {a} para {b} num dia já fechado — provável erro de transcrição")
        if not parcial:
            for k in ("o", "p", "n"):
                m = med(k)
                if m and not (0.3 * m <= novo[k] <= 3.0 * m):
                    raise Erro(f"{d}: {k}={novo[k]} fora da faixa normal (mediana 14 d = {m})")
        if d in by and by[d] != novo:
            avisos.append(f"{d}: {by[d]} -> {novo}")
        by[d] = novo
    rows2 = [by[d] for d in sorted(by)]

    # ---------- estoque ----------
    if not E.get("estoque"):
        raise Erro("entrada sem 'estoque'")
    st = load("estoque.json")
    loc_map = {"bogota": "Bogotá", "medellin": "Medellín", "cali": "Cali", "barranquilla": "Barranquilla", "barranquillia": "Barranquilla"}
    novos = {}
    for x in E["estoque"]:
        k = SKUS.get(str(x[0]).strip().upper())
        ln = norm(x[1]).replace("melonn", "").strip()
        b = loc_map.get(ln)
        if k is None or b is None:
            continue
        av, cm = n_int(x[2]), n_int(x[3])
        if av < 0 or cm < 0:
            raise Erro(f"estoque negativo em {x}")
        if (k, b) in novos:   # mesmo SKU em vários produtos: disponível é o mesmo, comprometido soma
            novos[(k, b)] = [max(av, novos[(k, b)][0]), novos[(k, b)][1] + cm]
        else:
            novos[(k, b)] = [av, cm]
    falta = [(k, b) for k in KS for b in BODS if (k, b) not in novos]
    if falta:
        raise Erro(f"estoque: faltam {falta}")
    mud_est = []
    for (k, b), v in novos.items():
        ant = st[k]["bod"].get(b)
        if ant != v:
            mud_est.append(f"{st[k]['nome']} {b}: {ant} -> {v}")
        st[k]["bod"][b] = v

    # ---------- link de oferta ----------
    lk = load("links.json")
    for x in E.get("link", []) or []:
        d = str(x[0])[:10]
        o, u, g = n_int(x[1]), n_int(x[2]), n_int(x[3])
        if o == 0 and u == 0:
            lk["d"].pop(d, None)
        else:
            if g != u * lk["preco"] and g > u * lk["cheio"]:
                raise Erro(f"link {d}: faturamento {g} incompatível com {u} un.")
            lk["d"][d] = [o, u, g]
    lk["d"] = dict(sorted(lk["d"].items()))

    # ---------- distribuição ----------
    dist = load("dist.json")
    if E.get("dist"):
        D = E["dist"]
        ontem = dt.date.fromisoformat(hoje) - dt.timedelta(days=1)
        for k, n in (("d30", 30), ("d7", 7)):
            if not D.get(k):
                raise Erro(f"dist: falta {k}")
            out = {}
            for x in D[k]:
                reg, kk = str(x[0]), SKUS.get(str(x[1]).strip().upper())
                if not kk or not reg:
                    continue
                out.setdefault(reg, {k: 0 for k in KS})[kk] += n_int(x[2])
            if len(out) < 15:
                raise Erro(f"dist {k}: só {len(out)} departamentos — consulta incompleta")
            dist[k] = dict(sorted(out.items(), key=lambda kv: -(kv[1]["p"] + kv[1]["n"] + kv[1]["s"])))
            ini = ontem - dt.timedelta(days=n - 1)
            dist.setdefault("vendas_periodo", {})[k] = f"{ini.strftime('%d/%m')}–{ontem.strftime('%d/%m')}"
        t30 = sum(v["p"] for v in dist["d30"].values())
        t7 = sum(v["p"] for v in dist["d7"].values())
        if not (0.12 <= t7 / max(t30, 1) <= 0.40):
            raise Erro(f"dist: Piña 7 d ({t7}) incoerente com 30 d ({t30})")

    agora = dt.datetime.now(TZ_USER)
    meta = load("meta.json")
    meta.update({"atualizado": agora.strftime("%d/%m/%Y %H:%M"), "hoje": hoje, "parcial": hoje})
    if E.get("link"):
        lk["lido_em"] = agora.strftime("%d/%m/%Y %H:%M")
    return rows2, st, lk, dist, meta, avisos, mud_est


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--consultas":
        consultas()
        return 0
    if len(sys.argv) > 1 and sys.argv[1] == "--precisa-dist":
        print("SIM" if precisa_dist() else "NAO")
        return 0
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    with open(sys.argv[1], encoding="utf-8") as f:
        E = json.load(f)
    try:
        rows2, st, lk, dist, meta, avisos, mud_est = validar_e_mesclar(E)
    except Erro as e:
        print("ERRO — nada foi gravado:", e)
        return 1
    # grava (com cópia para desfazer se a geração falhar)
    nomes = ["rows.json", "estoque.json", "links.json", "dist.json", "meta.json"]
    bk = {n: open(p(n), encoding="utf-8").read() for n in nomes}
    save("rows.json", rows2); save("estoque.json", st, compact=False); save("links.json", lk)
    save("dist.json", dist); save("meta.json", meta, compact=False)
    try:
        for s in ("gen.py", "oc_addon.py"):
            subprocess.run([sys.executable, p(s)], check=True, cwd=REPO)
    except subprocess.CalledProcessError as e:
        for n, t in bk.items():
            open(p(n), "w", encoding="utf-8").write(t)
        print("ERRO na geração do HTML — dados restaurados:", e)
        return 1
    r = rows2[-1]
    tot = {k: (sum(v[0] for v in st[k]["bod"].values()), sum(v[1] for v in st[k]["bod"].values())) for k in KS}
    print("Resumo:")
    print(f"  hoje {r['d']} (parcial): {r['o']} pedidos pagos · Piña {r['p']} · Naranja {r['n']} · Shaker {r['s']}")
    for k in KS:
        print(f"  {st[k]['nome']}: disponível {tot[k][0]} · comprometido {tot[k][1]}")
    if avisos:
        print("  dias revisados:", len(avisos))
    if mud_est:
        print("  estoque mudou:", "; ".join(mud_est))
    print("OK PARA PUBLICAR", meta["atualizado"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
