#!/usr/bin/env python3
"""Stage 1: read one record, and what the tool makes of it."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "lib"))
import hello as h  # noqa: E402

h.title("Stage 1: read one record", "A record is a text file: one system, what it emits and accepts, and the status of each claim.")

h.step("The record Tessaline wrote about its TR-40 radar")
path = os.path.join(h.ROOT, "stores/tessaline/systems/tr-40.rec")
text = open(path, encoding="utf-8").read()
h.show(text)

h.step("The same system as the tool reads it, from all three stores")
code, r = h.options("systems", *h.stores())
tr40 = [s for s in r["systems"] if s["system"] == "tessaline/tr-40"][0]
for c in tr40["claims"]:
    h.say("%-8s %-24s %-12s %-10s by %s" % (c["claim"], " -> ".join(c["formats"]), c["status"],
                                             c.get("version", ""), c["source"]["by"]))
h.say("records: " + ", ".join("%s (%s)" % (x["file"], x["by"]) for x in tr40["records"]))

h.step("Verify")
own = [c for c in tr40["claims"] if c["source"]["by"] == "tessaline"]
h.check("the query exits 0", code == 0)
h.check("Tessaline's record gives 6 claims", len(own) == 6)
h.check("two owners have a record of the TR-40: tessaline and velmora",
        sorted(x["by"] for x in tr40["records"]) == ["tessaline", "velmora"])
h.check("every claim keeps its store, file and line",
        all({"store", "file", "line", "by"} <= set(c["source"]) for c in tr40["claims"]))
h.check("the keyword `contact`, which the tool does not read, is kept",
        any(e["tokens"][0] == "contact" for x in tr40["records"] for e in x["extra"]))
h.check("the attribute `port=8600`, which the tool does not read, is kept",
        any(c.get("other", {}).get("port") == "8600" for c in own))
h.check("a claim on a format with a pack is marked as having one",
        [c["packs"] for c in own if c["formats"] == ["asterix-cat062"]] == [[True]])
h.check("a claim on a format with no pack is kept and marked as having none",
        [c["packs"] for c in own if c["formats"] == ["tessaline control json"]] == [[False]])
h.done()
