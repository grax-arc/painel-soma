#!/usr/bin/env python3
"""Atualização automática do painel direto da Shopify (roda no GitHub Actions a cada 15 min).

Lê as mesmas consultas de motor/atualizar.py pela Admin API da Shopify, grava motor/entrada.json
e chama atualizar.py, que valida e só gera o painel se tudo bater.

Credenciais (segredos do repositório no GitHub):
  SHOPIFY_CLIENT_ID e SHOPIFY_CLIENT_SECRET  -> app do Dev Dashboard instalado na loja (client credentials grant)
  ou SHOPIFY_ACCESS_TOKEN                    -> token fixo de um app antigo, se existir
Escopos do app: read_reports (ShopifyQL), read_products e read_inventory.
Sem credenciais, sai sem mexer em nada.
"""
import json, os, subprocess, sys, time, urllib.parse, urllib.request

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)
import atualizar as A  # noqa: E402

SHOP = os.environ.get("SHOPIFY_SHOP", "dw1rtx-dm").replace(".myshopify.com", "")
API = os.environ.get("SHOPIFY_API_VERSION", "2026-10")


def post(url, data, headers):
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    for tentativa in range(4):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.loads(r.read().decode())
        except urllib.error.HTTPError as e:
            corpo = e.read().decode()[:500]
            if e.code in (429, 500, 502, 503, 504) and tentativa < 3:
                time.sleep(3 * (tentativa + 1)); continue
            raise SystemExit(f"Shopify respondeu {e.code} em {url.split('/admin')[1] if '/admin' in url else url}: {corpo}")
        except urllib.error.URLError as e:
            if tentativa < 3:
                time.sleep(3 * (tentativa + 1)); continue
            raise SystemExit(f"Sem conexão com a Shopify: {e}")


def token():
    t = os.environ.get("SHOPIFY_ACCESS_TOKEN", "").strip()
    if t:
        return t
    cid, sec = os.environ.get("SHOPIFY_CLIENT_ID", "").strip(), os.environ.get("SHOPIFY_CLIENT_SECRET", "").strip()
    if not (cid and sec):
        return None
    r = post(f"https://{SHOP}.myshopify.com/admin/oauth/access_token",
             urllib.parse.urlencode({"grant_type": "client_credentials", "client_id": cid, "client_secret": sec}).encode(),
             {"Content-Type": "application/x-www-form-urlencoded"})
    if "access_token" not in r:
        raise SystemExit(f"A Shopify não devolveu token: {r}")
    return r["access_token"]


def gql(tok, query, variables=None):
    r = post(f"https://{SHOP}.myshopify.com/admin/api/{API}/graphql.json",
             json.dumps({"query": query, "variables": variables or {}}).encode(),
             {"Content-Type": "application/json", "X-Shopify-Access-Token": tok})
    if r.get("errors"):
        raise SystemExit(f"Erro GraphQL: {json.dumps(r['errors'], ensure_ascii=False)[:800]}")
    return r["data"]


def shopifyql(tok, q):
    d = gql(tok, "query($q: String!) { shopifyqlQuery(query: $q) { tableData { columns { name } rows } parseErrors } }", {"q": q})["shopifyqlQuery"]
    if d.get("parseErrors"):
        raise SystemExit(f"ShopifyQL recusou a consulta: {d['parseErrors']}\n{q}")
    return (d.get("tableData") or {}).get("rows") or []


def main():
    tok = token()
    if not tok:
        print("Sem credenciais da Shopify (SHOPIFY_CLIENT_ID/SHOPIFY_CLIENT_SECRET): nada a fazer.")
        return 0
    E = {}
    for chave, tipo, q in A.lista_consultas():
        if tipo == "graphql":
            nodes = gql(tok, q)["nodes"]
            est = []
            for n in nodes:
                if not n:
                    continue
                for lv in n["inventoryItem"]["inventoryLevels"]["nodes"]:
                    qt = {x["name"]: x["quantity"] for x in lv["quantities"]}
                    est.append([n["sku"], lv["location"]["name"], qt.get("available", 0), qt.get("committed", 0)])
            E["estoque"] = est
            continue
        rows = shopifyql(tok, q)
        if chave == "pedidos":
            E["pedidos"] = [[r["day"], r["orders"], r["net_items_sold"]] for r in rows]
        elif chave == "skus":
            E["skus"] = [[r["day"], r["product_variant_sku"], r["net_items_sold"]] for r in rows if r.get("product_variant_sku")]
        elif chave == "link":
            E["link"] = [[r["day"], r["orders"], r["net_items_sold"], r["gross_sales"]] for r in rows]
        elif chave.startswith("dist_"):
            E.setdefault("dist", {})[chave[5:]] = [[r["shipping_region"], r["product_variant_sku"], r["net_items_sold"]] for r in rows if r.get("shipping_region")]
    with open(os.path.join(BASE, "entrada.json"), "w", encoding="utf-8") as f:
        json.dump(E, f, ensure_ascii=False)
    print("Consultas ok:", {k: len(v) if isinstance(v, list) else {kk: len(vv) for kk, vv in v.items()} for k, v in E.items()})
    return subprocess.run([sys.executable, os.path.join(BASE, "atualizar.py"), os.path.join(BASE, "entrada.json")]).returncode


if __name__ == "__main__":
    sys.exit(main())
