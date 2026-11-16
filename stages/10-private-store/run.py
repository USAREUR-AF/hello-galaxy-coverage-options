#!/usr/bin/env python3
"""Stage 10: keep a private store beside this public example."""
import os
import shutil
import subprocess
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "lib"))
import hello as h  # noqa: E402

PRIVATE = os.path.join(h.RUN, "private-store")
REC = """record   1
system   our-maker/our-sensor-a
name     "A system only our organization may know about"
kind     sensor
by       our-org
date     2026-11-16
note     "In a real private store this file holds a real system. Here it is a stand-in."

emits    cot-xml  transport=udp  status=available
"""
NEEDLE = "our-maker/our-sensor-a"

h.title("Stage 10: a private store beside this one",
        "Records of real systems never go into a public repository. They live in a private store and join the query at run time.")

h.step("A private store, written outside the tracked tree (.run/ is ignored by git)")
shutil.rmtree(PRIVATE, ignore_errors=True)
os.makedirs(os.path.join(PRIVATE, "our-maker"))
with open(os.path.join(PRIVATE, "our-maker", "our-sensor-a.rec"), "w", encoding="utf-8") as f:
    f.write(REC)
h.show(REC)
ignored = subprocess.run(["git", "-C", h.ROOT, "check-ignore", "-q", ".run/private-store/our-maker/our-sensor-a.rec"])
h.say("git check-ignore: %s" % ("ignored" if ignored.returncode == 0 else "NOT ignored"))

h.step("The public stores and the private one in one query")
code, t = h.options("paths", *h.stores(), "--store", ".run/private-store", "--from", NEEDLE,
                    "--to", "kastreni/tactical-display", table=True)
h.show(t)
code, r = h.options("paths", *h.stores(), "--store", ".run/private-store", "--from", NEEDLE, "--to", "kastreni/tactical-display")

h.step("What may leave the private side: counts only")
code_s, s = h.options("summary", *h.stores(), "--store", ".run/private-store", table=True)
h.show(s)

h.step("A needle list: the private store's identifiers must appear in no tracked file")
needles = os.path.join(h.RUN, "private-needles.txt")
with open(needles, "w", encoding="utf-8") as f:
    f.write(NEEDLE + "\n")
print("    $ git grep -i -w -F -f .run/private-needles.txt")
hits = subprocess.run(["git", "-C", h.ROOT, "grep", "-i", "-w", "-F", "-f", needles], capture_output=True, text=True)
h.say("%d tracked line(s) hold a needle" % len([ln for ln in hits.stdout.split("\n") if ln and not ln.startswith("stages/10-private-store/")]))

h.step("Verify")
h.check("the private store is ignored by git", ignored.returncode == 0)
h.check("the query merges it: paths from the private system exist", code == 0 and r["counts"]["paths"] >= 1)
h.check("every path from it names the private store as the source of its claim",
        all(p["from"]["claim"]["source"]["store"] == ".run/private-store" for p in r["paths"]))
h.check("the summary holds counts and no identifier", code_s == 0 and NEEDLE not in s)
h.check("no tracked file outside this stage's directory names the private system",
        all(ln.startswith("stages/10-private-store/") for ln in hits.stdout.split("\n") if ln))
h.done()
