# Stage 8 — a store that fails `check --strict`

**The reader keeps everything it can tokenize and reads what it does not
understand as `unknown`. `check` lists what it could not use; `--strict`
makes any warning fail, for use before a commit. This stage runs it on a
first draft with five mistakes, fixes them in a copy, and runs it again.**

The draft is in [`store/`](store/), written by a notional trials cell:

| Mistake | What `check` says |
|---|---|
| an unclosed quote | error: the line is not read |
| a record with no `system` line | warning: the record is not used |
| `proven` with no `evidence=` | warning |
| a status that is not one of the four (`partly`) | warning: read as `unknown` |
| `converts` with one format | warning: kept, not used |

```bash
bin/hello-options 8
```

The three example stores pass `check --strict`. Their `info` lines are the
keywords and attributes the tool keeps without reading, and the format names
that have no pack.

`check` does not look at what `evidence=` points to: the record format leaves
evidence as free text. In this repository `tools/prove.py` does that check
(stage 3).

## What you should see

Run against goat-transformers at commit `8845949`.

```text
== Stage 8: a store that fails `check --strict` ==
The reader refuses nothing it can tokenize. `check` lists what it could not use; `--strict` makes a warning fail.

[1] A first draft from a new writer, the trials cell
    mast-camera.rec
    | record   1
    | system   trials-cell/mast-camera
    | name     "Mast camera at the trials range (first draft)
    | kind     sensor
    | by       trials-cell
    | date     2026-11-10
    | 
    | emits    sapient   status=proven
    | emits    cot-xml   status=partly  note="seen on one display only"
    | converts sapient   status=available
    range-radar.rec
    | record   1
    | name     "Range radar"
    | kind     sensor
    | by       trials-cell
    | date     2026-11-10
    | 
    | emits    asterix-cat062  transport=udp  status=available

[2] check --strict on the draft
    $ goat-options check --store stages/08-strict-check/store --strict --table
    | error   mast-camera.rec:3: line not read: unbalanced double quote
    | warning mast-camera.rec:8: status proven with no evidence
    | warning mast-camera.rec:9: status `partly` is not one of proven, available, forthcoming, unknown; read as unknown
    | warning mast-camera.rec:10: `converts` needs 2 format names; kept, not used
    | warning range-radar.rec: no `system` line; record not used
    exit code 1

[3] The fixes, applied to a copy in .run/08-store
    mast-camera.rec: name     "Mast camera at the trials range (first draft)"
    mast-camera.rec: emits    sapient   status=proven  evidence=evidence/range-log-1110.md
    mast-camera.rec: emits    cot-xml   status=available  note="seen on one display only"
    mast-camera.rec: converts sapient  cot-xml  status=available
    range-radar.rec: record   1 / system   trials-cell/range-radar

[4] check --strict on the fixed copy
    $ goat-options check --store .run/08-store --strict --table
    | (nothing to report)
    exit code 0

[5] check --strict on the three example stores
    $ goat-options check --store stores/tessaline --store stores/velmora --store stores/kastreni --strict
    27 systems; 0 error, 0 warning, 63 info

[6] Verify
    PASS  the draft fails check --strict (exit 1)
    PASS  an unclosed quote is an error, and the line is not used
    PASS  a record with no `system` line is not used
    PASS  `proven` with no evidence is a warning
    PASS  a status outside the four is read as unknown, with a warning
    PASS  `converts` with one format is kept and not used
    PASS  all 5 fixes applied to the copy
    PASS  the fixed copy passes check --strict (exit 0)
    PASS  the three example stores pass check --strict (exit 0)

stage complete: every check held
```
