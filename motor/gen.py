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
stock = load("estoque.json")
meta = load("meta.json")
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
print("gen ok", len(html))
