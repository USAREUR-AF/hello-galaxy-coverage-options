#!/usr/bin/env python3
"""Stage 7: a forthcoming option, from a vendor's announced version."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "lib"))
import hello as h  # noqa: E402

h.title("Stage 7: a forthcoming option",
        "A claim for a version announced and not in hand is `forthcoming`. A path is as forthcoming as its least established step.")

h.step("What Tessaline's release plan announces")
h.show(open(os.path.join(h.ROOT, "stores/tessaline/evidence/rp-24-release-plan.md"), encoding="utf-8").read())

h.step("Every forthcoming claim in the stores")
code, r = h.options("systems", *h.stores())
fc = [(s["system"], c) for s in r["systems"] for c in s["claims"] if c["status"] == "forthcoming"]
for sid, c in fc:
    h.say("%-16s %-8s %-20s version %-4s evidence=%s" % (sid, c["claim"], " -> ".join(c["formats"]), c.get("version"), c.get("evidence")))

h.step("At ridge camp: the RF-9 to the JX-2 effector")
code, t = h.options("paths", *h.stores(), "--from", "tessaline/rf-9", "--to", "tessaline/jx-2", table=True)
h.show(t)
code, p = h.options("paths", *h.stores(), "--from", "tessaline/rf-9", "--to", "tessaline/jx-2")

h.step("Verify")
h.check("5 forthcoming claims, all by Tessaline", len(fc) == 5 and all(c["source"]["by"] == "tessaline" for _, c in fc))
h.check("every forthcoming claim points at the release plan, and it resolves",
        all(c.get("evidence") == "evidence/rp-24-release-plan.md" and
            os.path.isfile(os.path.join(h.ROOT, c["source"]["store"], c["evidence"])) for _, c in fc))
fp = [x for x in p["paths"] if x["status"] == "forthcoming"]
h.check("two paths from the RF-9 to the JX-2 are forthcoming, both ending in the JX-2's announced cot-xml",
        len(fp) == 2 and all(x["to"]["format"] == "cot-xml" and x["to"]["claim"]["version"] == "2.0" for x in fp))
h.check("the paths in hand today are listed beside them, as available",
        sorted(x["status"] for x in p["paths"]) == ["available", "available", "forthcoming", "forthcoming"])
h.done()
