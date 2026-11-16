"""Shared by every stage: where goat-transformers is, how goat-options is run,
narration and checks. Standard library only."""

import glob
import json
import os
import shlex
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GT = os.environ.get("GOAT_TRANSFORMERS_DIR") or os.path.join(ROOT, ".cache", "goat-transformers")
OPTIONS = os.path.join(GT, "tools", "goat-options")
RUN = os.path.join(ROOT, ".run")
STORES = ["stores/tessaline", "stores/velmora", "stores/kastreni"]

_TTY = sys.stdout.isatty() and not os.environ.get("NO_COLOR")
_failed = []


def _c(code, s):
    return "\033[%sm%s\033[0m" % (code, s) if _TTY else s


def need_library():
    if not os.path.isfile(OPTIONS):
        sys.exit("goat-transformers is not at %s: run `bin/hello-options fetch` first" % GT)


def use_engine():
    """Put goat-transformers' Python engine on the import path: the directory
    under engines/python that holds the goat_transformers package."""
    need_library()
    found = glob.glob(os.path.join(GT, "engines", "python", "*", "goat_transformers"))
    if not found:
        sys.exit("no Python engine under %s/engines/python" % GT)
    sys.path.insert(0, os.path.dirname(found[0]))


def title(text, sub=None):
    print("\n" + _c("1", "== %s ==" % text))
    if sub:
        print(_c("2", sub))


_n = [0]


def step(text):
    _n[0] += 1
    print("\n" + _c("1;36", "[%d] %s" % (_n[0], text)))


def say(text):
    print("    " + text)


def show(text, limit=None):
    lines = text.rstrip("\n").split("\n")
    if limit and len(lines) > limit:
        lines = lines[:limit] + ["... (%d more lines)" % (len(lines) - limit)]
    for ln in lines:
        print("    | " + ln)


def options(*args, table=False, quiet=False):
    """Run goat-options from the repository root. Returns (exit code, output);
    JSON output is parsed."""
    need_library()
    argv = ["python3", "-I", OPTIONS] + list(args) + (["--table"] if table else [])
    shown = "goat-options " + " ".join(shlex.quote(a) for a in args) + (" --table" if table else "")
    if not quiet:
        print("    " + _c("32", "$ " + shown))
    p = subprocess.run(argv, cwd=ROOT, capture_output=True, text=True)
    if p.stderr.strip():
        show(p.stderr)
    out = p.stdout
    if not table:
        try:
            out = json.loads(out)
        except ValueError:
            pass
    return p.returncode, out


def stores(*names):
    """--store arguments for the named owner stores (default: all three)."""
    out = []
    for s in (["stores/" + n for n in names] if names else STORES):
        out += ["--store", s]
    return out


def check(label, ok):
    print("    " + (_c("32", "PASS") if ok else _c("31", "FAIL")) + "  " + label)
    if not ok:
        _failed.append(label)
    return ok


def done():
    if _failed:
        print("\n" + _c("31", "stage failed: %d check(s) did not hold" % len(_failed)))
        sys.exit(1)
    print("\n" + _c("32", "stage complete: every check held"))


def route(p):
    """A path as one line: format --[converter]--> format ..."""
    parts = [p["formats"][0]]
    for s in p["steps"]:
        parts += ["--[%s]-->" % s["via"], s["to"]]
    return " ".join(parts)
