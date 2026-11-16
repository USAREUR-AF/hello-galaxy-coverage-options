#!/usr/bin/env python3
"""Stage 9: a program of your own reads the JSON and draws its own view."""
import ast
import json
import os
import subprocess
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "lib"))
import hello as h  # noqa: E402

PROGRAM = os.path.join(h.ROOT, "consumer", "site-grid.py")

h.title("Stage 9: your own view",
        "goat-options prints JSON. What to draw from it, and how, is the reader's choice; this is one small example.")

h.step("The program: consumer/site-grid.py")
source = open(PROGRAM, encoding="utf-8").read()
h.show(source)

grids = {}
for site in ("ridge-camp", "harbor-east", "depot-lake"):
    h.step("Site %s, drawn by the program" % site)
    code, answer = h.options("site", *h.stores(), "sites/%s.site" % site, "--keys", "count", table=False)
    print("    $ goat-options site ... sites/%s.site | consumer/site-grid.py" % site)

    p = subprocess.run([sys.executable, "-I", PROGRAM], input=json.dumps(answer), capture_output=True, text=True)
    grids[site] = p
    h.show(p.stdout)

h.step("Verify")
lines = source.rstrip("\n").split("\n")
imports = sorted({a.name for n in ast.walk(ast.parse(source)) if isinstance(n, ast.Import) for a in n.names})
h.check("the program is %d lines, between 20 and 40" % len(lines), 20 <= len(lines) <= 40)
h.check("it imports json and sys only", imports == ["json", "sys"])
h.check("it ran on every site with exit 0", all(p.returncode == 0 for p in grids.values()))
he = grids["harbor-east"].stdout.split("\n")
h.check("harbor east: the LR-5 row shows 1 proven, 1 available and 1 unknown path on hand to the picture",
        any(ln.startswith("kastreni/lr-5") and "1P 1A 1U" in ln for ln in he))
h.check("harbor east: the AIS receiver has no path on hand",
        any(ln.split()[0] == "velmora/harbor-ais" and set(ln.split()[1:]) == {"."} for ln in he))
rc = grids["ridge-camp"].stdout.split("\n")
h.check("ridge camp: the RF-9 row shows its 4 paths to the JX-2",
        any(ln.startswith("tessaline/rf-9") and "2A 2F" in ln for ln in rc))
h.done()
