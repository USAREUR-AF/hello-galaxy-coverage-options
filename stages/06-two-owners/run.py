#!/usr/bin/env python3
"""Stage 6: two owners hold records for the same system and disagree."""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "lib"))
import hello as h  # noqa: E402

h.title("Stage 6: two owners, merged, disagreeing",
        "Stores merge by system identifier. Nothing one owner writes replaces what another wrote.")

h.step("Two records of tessaline/tr-40, in two stores")
for f in ("stores/tessaline/systems/tr-40.rec", "stores/velmora/received/tessaline-tr-40.rec"):
    h.say(f)
    h.show("\n".join(ln for ln in open(os.path.join(h.ROOT, f), encoding="utf-8").read().split("\n")
                     if ln.startswith(("by", "emits    asterix-cat062"))))

h.step("Merged: both claims about Category 062 are kept, each with its owner and version")
code, r = h.options("systems", *h.stores())
tr40 = [s for s in r["systems"] if s["system"] == "tessaline/tr-40"][0]
c062 = [c for c in tr40["claims"] if c["formats"] == ["asterix-cat062"]]
for c in c062:
    h.say("%-10s version %-4s %-10s %s" % (c["source"]["by"], c.get("version"), c["status"], c.get("other", {}).get("note", "")))

h.step("The direct paths to Velmora's air C2: one per claim")
code, t = h.options("paths", *h.stores(), "--from", "tessaline/tr-40", "--to", "velmora/c2-air",
                    "--max-conversions", "0", table=True)
h.show(t)

h.step("The same for the EO-7, where Kastreni's record disagrees with Tessaline's")
code, r2 = h.options("systems", *h.stores())
eo7 = [s for s in r2["systems"] if s["system"] == "tessaline/eo-7"][0]
for c in eo7["claims"]:
    if c["formats"] == ["sapient"]:
        h.say("%-10s %-8s %-10s %s" % (c["source"]["by"], c["claim"], c["status"], c.get("other", {}).get("note", "")))

h.step("The answer does not depend on the order of the stores")
_, a = h.options("paths", *h.stores("tessaline", "velmora", "kastreni"), "--from", "tessaline/tr-40", "--to", "velmora/fabric-tracks")
_, b = h.options("paths", *h.stores("kastreni", "velmora", "tessaline"), "--from", "tessaline/tr-40", "--to", "velmora/fabric-tracks")

h.step("Verify")
h.check("the TR-40 has 9 claims from 2 owners", len(tr40["claims"]) == 9 and len(tr40["records"]) == 2)
h.check("Tessaline says Category 062 is proven at 3.2; Velmora says available at 3.1; both are shown",
        sorted((c["source"]["by"], c.get("version"), c["status"]) for c in c062) ==
        [("tessaline", "3.2", "proven"), ("velmora", "3.1", "available")])
h.check("the two direct paths carry the two statuses", "proven" in t and "available" in t)
h.check("the EO-7 has records from tessaline and kastreni",
        sorted(x["by"] for x in eo7["records"]) == ["kastreni", "tessaline"])
h.check("both names the two owners gave the EO-7 are kept",
        sorted(eo7["names"]) == sorted(["Tessaline EO-7 electro-optical and infrared camera", "EO-7 camera"]))
h.check("store order changes nothing but the list of stores in the query",
        json.dumps(a["paths"], sort_keys=True) == json.dumps(b["paths"], sort_keys=True))
h.done()
