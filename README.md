# Zotero Co-author Network

Interactive co-authorship graph of every author in my personal Zotero library ("My Library" only; group libraries are excluded).

**Live page:** https://eeporter.github.io/zotero-author-network/

- Nodes are authors; size = number of papers in the library that list them as an author (any position).
- Edges join authors who share a paper; thicker edges = more shared papers.
- Duplicate Zotero items (same title and first author) are merged into one paper before counting.
- Colors mark the eight largest connected clusters.
- Only the `author` creator role is used (no editors, translators, etc.). Deleted items are skipped.
- Names are matched on last name + first name; an initial-only form is merged into a full first name when exactly one person fits.

## Rebuild

```bash
cp ~/Zotero/zotero.sqlite /tmp/z.sqlite        # copy so a running Zotero doesn't lock it
python3 extract.py /tmp/z.sqlite .             # writes graph.json
python3 compact.py                             # graph.json -> data.json
python3 build.py                               # template.html + data.json -> index.html
```
