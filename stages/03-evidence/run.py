#!/usr/bin/env python3
"""Stage 3: read the evidence of a path, and run it again."""
import hashlib
import json
import os
import subprocess
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "lib"))
import hello as h  # noqa: E402

h.title("Stage 3: read the evidence of a path", "A path's status comes from claims; each proven claim points at a file in its owner's store.")

h.step("The paths from the TR-40 to the depot lake track picture that are proven")
code, r = h.options("paths", *h.stores(), "--from", "tessaline/tr-40", "--to", "velmora/fabric-tracks", "--keys", "count")
proven = [p for p in r["paths"] if p["status"] == "proven"]
for p in proven:
    h.say(h.route(p))
p = proven[0]
claims = [("source", p["from"]["claim"])] + [("step", c) for s in p["steps"] for c in s["claims"]] + \
         [("consumer", p["to"]["claim"])]
for part, c in claims:
    h.say("%-8s %-24s %-8s %-9s evidence=%s  (%s/%s:%d, by %s)" % (
        part, c["system"], c["claim"], c["status"], c.get("evidence"), c["source"]["store"], c["source"]["file"],
        c["source"]["line"], c["source"]["by"]))

h.step("Follow the step's evidence: a run of the library, kept in Velmora's store")
step_claim = p["steps"][0]["claims"][0]
store = os.path.join(h.ROOT, step_claim["source"]["store"])
run_path = os.path.join(store, step_claim["evidence"])
run = json.load(open(run_path, encoding="utf-8"))
h.say("%s converted %s to %s with the keys %s supplied by the caller" % (
    run["claim"]["system"], run["sample"], run["to"], ", ".join(sorted(run["set"]))))
h.show(run["output"])

h.step("Run every proven claim of every store again: tools/prove.py")
print("    $ tools/prove.py")
proc = subprocess.run([sys.executable, "-I", os.path.join(h.ROOT, "tools", "prove.py")], capture_output=True, text=True)
h.show(proc.stdout.strip().split("\n")[-1])

h.step("Verify")
h.check("one path is proven: asterix-cat062 --[goat-transformers]--> canonical-track-v2",
        [x["formats"] for x in proven] == [["asterix-cat062", "canonical-track-v2"]])
h.check("its source claim is Tessaline's, for version 3.2",
        (p["from"]["claim"]["source"]["by"], p["from"]["claim"].get("version")) == ("tessaline", "3.2"))
h.check("every evidence pointer on the path resolves in its owner's store",
        all(os.path.isfile(os.path.join(h.ROOT, c["source"]["store"], c["evidence"])) for _, c in claims))
sample = os.path.join(store, run["sample"])
h.check("the run names the sample it converted, and the sample is unchanged",
        hashlib.sha256(open(sample, "rb").read().strip()).hexdigest() == run["sample_sha256"])
h.check("the run needed four keys the caller supplied",
        run["supplied"] == ["time_ms", "track.generation", "track.source_id", "uid"])
h.check("tools/prove.py: every proven claim resolves, decodes or runs (exit 0)", proc.returncode == 0)
h.check("tools/prove.py checked 36 proven claims", "36 proven claim(s), 0 failed" in proc.stdout)
h.done()
