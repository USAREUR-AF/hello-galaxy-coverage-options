#!/usr/bin/env python3
"""A consumer of goat-options JSON: one site's answer drawn as a grid of
sources by consumers. Each cell counts the paths that are on hand, by status
(P proven, A available, F forthcoming, U unknown); `.` means none on hand.
This view is one choice among many. Standard library only.

  goat-options site --store ... FILE.site | consumer/site-grid.py
"""
import json
import sys

answer = json.load(sys.stdin)
cells, sources, consumers = {}, [], []
for it in answer["intents"]:
    source, consumer = it["source"], it["consumer"]
    sources += [source] if source not in sources else []
    consumers += [consumer] if consumer not in consumers else []
    for p in it["paths"]:
        parts = [p["from"], p["to"]] + p["steps"]
        if all(x.get("on_hand") is not False for x in parts):
            count = cells.setdefault((source, consumer), {})
            count[p["status"]] = count.get(p["status"], 0) + 1
width = max(len(s) for s in sources) + 2
print("site %s" % answer["site"]["site"])
print((" " * width + "".join(c.split("/")[-1][:16].ljust(18) for c in consumers)).rstrip())
for s in sources:
    row = []
    for c in consumers:
        n = cells.get((s, c), {})
        text = " ".join("%d%s" % (n[k], k[0].upper()) for k in ("proven", "available", "forthcoming", "unknown") if n.get(k))
        row.append((text or ".").ljust(18))
    print(s.ljust(width) + "".join(row).rstrip())
