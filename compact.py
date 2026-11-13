"""graph.json (from extract.py) -> data.json, the compact form embedded in the page."""
import json, pathlib
d = pathlib.Path(__file__).parent
g = json.load(open(d / "graph.json"))
idx = {n["id"]: i for i, n in enumerate(g["nodes"])}
def t(s):
    s = (s or "Untitled").strip()
    return s if len(s) <= 220 else s[:217] + "…"
def papers(rows):
    """[[year, title, copies], ...] from extract.py -> same rows, titles trimmed, oldest first."""
    return sorted(([y, t(title), c] for y, title, c in rows), key=lambda r: (r[0] or "9999", r[1]))
out = {"n": [[n["name"], n["papers"], papers(n["titles"])] for n in g["nodes"]],
       "l": [[idx[l["source"]], idx[l["target"]], l["w"]] for l in g["links"]],
       "s": g["stats"]}
json.dump(out, open(d / "data.json", "w"), separators=(",", ":"), ensure_ascii=False)
