#!/usr/bin/env python3
"""Stage 2: ask one question. Which ways can the TR-40's data reach Velmora's air C2?"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "lib"))
import hello as h  # noqa: E402

h.title("Stage 2: ask one question", "From one producing system to one consuming system: every path, with the status of each.")

h.step("Every path from tessaline/tr-40 to velmora/c2-air, as a table")
code, table = h.options("paths", *h.stores(), "--from", "tessaline/tr-40", "--to", "velmora/c2-air", table=True)
h.show(table)

h.step("The same answer as JSON, for a program")
code, r = h.options("paths", *h.stores(), "--from", "tessaline/tr-40", "--to", "velmora/c2-air", "--keys", "count")
for p in r["paths"]:
    h.say("%d conversion(s)  %-11s %s" % (p["conversions"], p["status"], h.route(p)))
h.say("counts: %s" % r["counts"])

h.step("Verify")
h.check("the query exits 0", code == 0)
h.check("12 paths", r["counts"]["paths"] == 12)
direct = [p for p in r["paths"] if p["conversions"] == 0]
h.check("two direct paths in asterix-cat062, one per owner's claim about the radar",
        [p["formats"] for p in direct] == [["asterix-cat062"], ["asterix-cat062"]]
        and sorted(p["from"]["claim"]["source"]["by"] for p in direct) == ["tessaline", "velmora"])
h.check("each path's status is one of the four", all(p["status"] in ("proven", "available", "forthcoming", "unknown")
                                                     for p in r["paths"]))
h.check("no path is longer than two conversions", max(p["conversions"] for p in r["paths"]) <= 2)
h.check("the output says the order is not a preference", "not a preference" in r["note"])
h.done()
