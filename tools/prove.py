#!/usr/bin/env python3
"""prove.py: no claim in this repository is `proven` by assertion alone.

For every claim whose status is `proven`, in every store:

  1. `evidence=` is present and names a file in the owner's store directory.
  2. `sample=` names a message in the store. Where the format has a pack, the
     goat-transformers Python engine decodes it: for `emits`, `accepts` and
     `speaks` the claim's format; for a system's own `converts`, the format it
     writes.
  3. A `converts ... via=goat-transformers` claim is run: the library converts
     the sample, with the keys of `set=` given as caller-supplied keys, and
     the result is the run file `evidence=` points to.

  tools/prove.py           check: run everything, compare with the files, write nothing
  tools/prove.py --write   write the run files of step 3

Exits 1 when any claim fails. Standard library and the pinned goat-transformers.
"""
import hashlib
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "lib"))
import hello  # noqa: E402

hello.use_engine()
from goat_transformers import Engine  # noqa: E402

LIBRARY = "goat-transformers"


def parse_set(text):
    out = {}
    for item in (text or "").split(","):
        if item.strip():
            k, _, v = item.partition("=")
            out[k.strip()] = v.strip()
    return out


def keys(entity):
    return sorted(entity.fields)


def main():
    write = "--write" in sys.argv[1:]
    code, systems = hello.options("systems", *hello.stores(), quiet=True)
    if code != 0:
        sys.exit("goat-options systems failed")
    packs = sorted(set(systems["query"]["library_formats"]))
    eng = Engine.from_dir(os.path.join(hello.GT, "packs"), None, "controlled", packs_only=packs)
    rows, failed = [], 0
    for s in systems["systems"]:
        for c in s["claims"]:
            if c["status"] != "proven":
                continue
            origin = c["source"]
            where = "%s/%s:%d" % (origin["store"], origin["file"], origin["line"])
            store = os.path.join(hello.ROOT, origin["store"])
            other = c.get("other", {})
            fmts = [f.lower() for f in c["formats"]]
            problems, did = [], ""

            ev = c.get("evidence")
            ev_path = os.path.join(store, ev) if ev else None
            library = c["claim"] == "converts" and other.get("via") == LIBRARY
            if not ev:
                problems.append("no evidence=")
            elif not library and not os.path.isfile(ev_path):
                problems.append("evidence %s does not resolve" % ev)

            sample = other.get("sample")
            sample_path = os.path.join(store, sample) if sample else None
            read_fmt = fmts[-1] if c["claim"] == "converts" and not library else fmts[0]
            if not sample:
                problems.append("no sample=")
            elif not os.path.isfile(sample_path):
                problems.append("sample %s does not resolve" % sample)
            elif read_fmt not in eng.formats():
                did = "no pack for %s: the capture is kept, the library cannot read it" % read_fmt
            else:
                data = open(sample_path, "rb").read().strip()
                try:
                    ent = eng.decode(read_fmt, data)
                    did = "decoded as %s: %d keys" % (read_fmt, len(ent.fields))
                except Exception as e:  # any refusal by the engine is a failed proof
                    problems.append("the library does not decode the sample as %s: %s" % (read_fmt, e))
                    ent = None
                if library and ent is not None:
                    given = parse_set(other.get("set"))
                    try:
                        out = eng.convert(fmts[0], fmts[1], data, given or None).decode()
                    except Exception as e:
                        problems.append("the conversion %s -> %s does not run: %s" % (fmts[0], fmts[1], e))
                        out = None
                    if out is not None:
                        back = eng.decode(fmts[1], out.encode())
                        cap = eng.capability(fmts[0], fmts[1])
                        run = {
                            "what": "a conversion run with the goat-transformers Python engine, for a proven claim",
                            "claim": {"system": s["system"], "store": origin["store"], "file": origin["file"],
                                      "line": origin["line"], "by": origin["by"]},
                            "from": fmts[0], "to": fmts[1], "sample": sample,
                            "sample_sha256": hashlib.sha256(data).hexdigest(),
                            "set": given, "output": out,
                            "keys_in": keys(ent), "keys_out": keys(back),
                            "carried": sorted(set(ent.fields) & set(back.fields)),
                            "supplied": sorted(k for k in given if k in back.fields),
                            "capability": {"grade": cap["grade"], "carried": cap["carried"], "dropped": cap["dropped"]},
                        }
                        text = json.dumps(run, indent=1) + "\n"
                        if not ev or not ev.startswith("evidence/runs/"):
                            problems.append("a library run is written under evidence/runs/, not %s" % ev)
                        elif write:
                            os.makedirs(os.path.dirname(ev_path), exist_ok=True)
                            with open(ev_path, "w", encoding="utf-8") as f:
                                f.write(text)
                            did = "ran %s -> %s, wrote %s" % (fmts[0], fmts[1], ev)
                        elif not os.path.isfile(ev_path):
                            problems.append("run file %s does not exist: run tools/prove.py --write" % ev)
                        elif open(ev_path, encoding="utf-8").read() != text:
                            problems.append("run file %s differs from this run" % ev)
                        else:
                            did = "ran %s -> %s; equals %s" % (fmts[0], fmts[1], ev)
            ok = not problems
            failed += not ok
            rows.append(("PASS" if ok else "FAIL", where, "%s %s" % (c["claim"], " -> ".join(c["formats"])),
                         did if ok else "; ".join(problems)))
    for r in rows:
        print("%s  %-44s %-46s %s" % r)
    print("\n%d proven claim(s), %d failed" % (len(rows), failed))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
