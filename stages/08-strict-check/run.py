#!/usr/bin/env python3
"""Stage 8: a store that fails `check --strict`, and how to fix it."""
import os
import shutil
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "lib"))
import hello as h  # noqa: E402

HERE = os.path.relpath(os.path.dirname(os.path.abspath(__file__)), h.ROOT)
FIXED = os.path.join(h.RUN, "08-store")

# What a writer changes, line by line: each pair is (what was written, what fixes it).
FIXES = {
    "mast-camera.rec": [
        ('name     "Mast camera at the trials range (first draft)\n',
         'name     "Mast camera at the trials range (first draft)"\n'),
        ("emits    sapient   status=proven\n",
         "emits    sapient   status=proven  evidence=evidence/range-log-1110.md\n"),
        ('emits    cot-xml   status=partly  note="seen on one display only"\n',
         'emits    cot-xml   status=available  note="seen on one display only"\n'),
        ("converts sapient   status=available\n", "converts sapient  cot-xml  status=available\n"),
    ],
    "range-radar.rec": [("record   1\n", "record   1\nsystem   trials-cell/range-radar\n")],
}

h.title("Stage 8: a store that fails `check --strict`",
        "The reader refuses nothing it can tokenize. `check` lists what it could not use; `--strict` makes a warning fail.")

h.step("A first draft from a new writer, the trials cell")
for name in sorted(os.listdir(os.path.join(h.ROOT, HERE, "store"))):
    h.say(name)
    h.show(open(os.path.join(h.ROOT, HERE, "store", name), encoding="utf-8").read())

h.step("check --strict on the draft")
code1, t1 = h.options("check", "--store", HERE + "/store", "--strict", table=True)
h.show(t1)
h.say("exit code %d" % code1)

h.step("The fixes, applied to a copy in .run/08-store")
shutil.rmtree(FIXED, ignore_errors=True)
shutil.copytree(os.path.join(h.ROOT, HERE, "store"), FIXED)
os.makedirs(os.path.join(FIXED, "evidence"))
with open(os.path.join(FIXED, "evidence", "range-log-1110.md"), "w", encoding="utf-8") as f:
    f.write("# Range log 1110 (notional)\n\nSAPIENT detections from the mast camera were recorded.\n")
applied = 0
for name, pairs in FIXES.items():
    path = os.path.join(FIXED, name)
    text = open(path, encoding="utf-8").read()
    for old, new in pairs:
        if old in text:
            text = text.replace(old, new, 1)
            applied += 1
        h.say("%s: %s" % (name, new.strip().replace("\n", " / ")))
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)

h.step("check --strict on the fixed copy")
code2, t2 = h.options("check", "--store", ".run/08-store", "--strict", table=True)
h.show(t2 or "(nothing to report)")
h.say("exit code %d" % code2)

h.step("check --strict on the three example stores")
code3, r3 = h.options("check", *h.stores(), "--strict")
h.say("%d systems; %s" % (r3["systems"], ", ".join("%d %s" % (sum(1 for p in r3["problems"] if p["level"] == lv), lv)
                                                 for lv in ("error", "warning", "info"))))

h.step("Verify")
h.check("the draft fails check --strict (exit 1)", code1 == 1)
h.check("an unclosed quote is an error, and the line is not used", "error   mast-camera.rec:3: line not read" in t1)
h.check("a record with no `system` line is not used", "range-radar.rec: no `system` line; record not used" in t1)
h.check("`proven` with no evidence is a warning", "mast-camera.rec:8: status proven with no evidence" in t1)
h.check("a status outside the four is read as unknown, with a warning", "status `partly` is not one of" in t1)
h.check("`converts` with one format is kept and not used", "`converts` needs 2 format names; kept, not used" in t1)
h.check("all %d fixes applied to the copy" % sum(len(v) for v in FIXES.values()), applied == sum(len(v) for v in FIXES.values()))
h.check("the fixed copy passes check --strict (exit 0)", code2 == 0)
h.check("the three example stores pass check --strict (exit 0)", code3 == 0)
h.done()
