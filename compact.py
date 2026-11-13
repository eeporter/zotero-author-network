"""graph.json (from extract.py) -> data.json, the compact form embedded in the page."""
import json, pathlib
d = pathlib.Path(__file__).parent
g = json.load(open(d / "graph.json"))
idx = {n["id"]: i for i, n in enumerate(g["nodes"])}
def t(s):
    s = (s or "Untitled").strip()
    return s if len(s) <= 220 else s[:217] + "…"
def papers(items):
    """[[year, title], ...] -> [[year, title, copies], ...], one row per distinct title, oldest first."""
    seen = {}
    for year, title in items:
        key = " ".join((title or "").lower().split())
        if key in seen:
            seen[key][2] += 1
            seen[key][0] = seen[key][0] or year
        else:
            seen[key] = [year, t(title), 1]
    return sorted(seen.values(), key=lambda r: (r[0] or "9999", r[1]))
out = {"n": [[n["name"], n["papers"], papers(n["titles"])] for n in g["nodes"]],
       "l": [[idx[l["source"]], idx[l["target"]], l["w"]] for l in g["links"]],
       "s": g["stats"]}
json.dump(out, open(d / "data.json", "w"), separators=(",", ":"), ensure_ascii=False)
