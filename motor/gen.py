# Monta motor/_build/painel_ruptura_soma.html a partir de template.html + dados (JSON desta pasta).
# Normalmente não é chamado sozinho: use  python3 motor/atualizar.py  (que chama gen.py e oc_addon.py).
import json, os

BASE = os.path.dirname(os.path.abspath(__file__))
BUILD = os.path.join(BASE, "_build")
os.makedirs(BUILD, exist_ok=True)

def load(name):
    with open(os.path.join(BASE, name), encoding="utf-8") as f:
        return json.load(f)

def raw(name):
    with open(os.path.join(BASE, name), encoding="utf-8") as f:
        return f.read()

rows = load("rows.json")
for _r in rows:
    _r.setdefault("r", 0)
stock = load("estoque.json")
meta = load("meta.json")

# Pedidos esgotados na Melonn (pagos, sem estoque na bodega): descontados do disponível de cada bodega,
# para a cobertura e o ponto de ruptura já considerarem essa fila. O desconto de uma bodega deixa de valer
# quando o disponível dela sobe mais de 20 un. acima da base (a Melonn recebeu mercadoria e atendeu a fila).
esg_aplicado = {}
if os.path.exists(os.path.join(BASE, "esgotados.json")):
    esg = load("esgotados.json")
    for k, bods in esg.get("skus", {}).items():
        for b, (q, base) in bods.items():
            if q <= 0 or k not in stock or b not in stock[k]["bod"]:
                continue
            agora = stock[k]["bod"][b][0]
            if agora - base > 20:
                continue
            stock[k]["bod"][b] = [agora - q, stock[k]["bod"][b][1]]
            esg_aplicado["%s %s" % (k, b)] = q
    # esgotados que não saem com a chegada de mercadoria (ex.: SKU SOMAROJOS sem ligação ao estoque SOMAROJO)
    for k, bods in esg.get("fixos", {}).items():
        for b, q in bods.items():
            if q > 0 and k in stock and b in stock[k]["bod"]:
                stock[k]["bod"][b] = [stock[k]["bod"][b][0] - q, stock[k]["bod"][b][1]]
                esg_aplicado["%s %s fixo" % (k, b)] = q
melj = load("melonn.json")
mel = {b: {"bodega": b, "lido_em": melj["lido_em"],
           "skus": {k: {"disp": v[0], "esp": v[1], "res": v[2], "al": v[3]} for k, v in d.items()}}
       for b, d in melj["bodegas"].items()}

# sanidade mínima: dias contíguos, último dia = parcial
import datetime as _dt
ds = [r["d"] for r in rows]
assert ds == sorted(ds) and len(set(ds)) == len(ds), "rows.json fora de ordem ou com dia repetido"
for a, b in zip(ds, ds[1:]):
    assert (_dt.date.fromisoformat(b) - _dt.date.fromisoformat(a)).days == 1, "falta dia entre %s e %s" % (a, b)
assert meta["parcial"] == ds[-1], "meta.parcial deve ser o último dia de rows.json"

html = raw("template.html")
assert html.count("/*__DATA__*/") == 1
html = html.replace("/*__DATA__*/", "const ROWS=%s;const STOCK=%s;const META=%s;const DIST=%s;const FECHS=%s;const DRIVE_FOLDER=%s;const MEL0=%s;const LOTES0=%s;const LINKS=%s;" % (
    json.dumps(rows, separators=(",", ":")),
    json.dumps(stock, ensure_ascii=False, separators=(",", ":")),
    json.dumps(meta, separators=(",", ":")),
    raw("dist.json"), raw("fechs.json"),
    json.dumps("https://drive.google.com/drive/folders/1qoPjeOugGa_uQYzBN-GTKjfAbnvf2EaC"),
    json.dumps(mel, ensure_ascii=False, separators=(",", ":")),
    raw("lotes_embed.json"), raw("links.json")))
with open(os.path.join(BUILD, "painel_ruptura_soma.html"), "w", encoding="utf-8") as f:
    f.write(html)
print("gen ok", len(html), "esgotados descontados:", esg_aplicado or "nenhum")
