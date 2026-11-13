"""Fill template.html with data.json -> index.html (self-contained page)."""
import pathlib
d = pathlib.Path(__file__).parent
data = (d / "data.json").read_text().replace("</", "<\\/")
body = (d / "template.html").read_text().replace("__DATA__", data)
head = '<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
title_end = body.index("</style>") + len("</style>")
(d / "index.html").write_text(head + body[:title_end] + "\n</head><body>\n" + body[title_end:] + "\n</body></html>\n")
