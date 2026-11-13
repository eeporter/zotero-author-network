"""graph.json (from extract.py) -> data.json, the compact form embedded in the page."""
import json, pathlib
d = pathlib.Path(__file__).parent
g = json.load(open(d / "graph.json"))
idx = {n["id"]: i for i, n in enumerate(g["nodes"])}
def t(s):
    s = (s or "Untitled").strip()
    return s if len(s) <= 110 else s[:107] + "…"
out = {"n": [[n["name"], n["papers"], [t(x) for x in n["titles"][:6]]] for n in g["nodes"]],
       "l": [[idx[l["source"]], idx[l["target"]], l["w"]] for l in g["links"]],
       "s": g["stats"]}
json.dump(out, open(d / "data.json", "w"), separators=(",", ":"), ensure_ascii=False)
