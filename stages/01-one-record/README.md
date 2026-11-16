# Stage 1 — read one record

**A record is a plain text file about one system: what it emits, accepts or
converts, in which version and over which transport, and the status and
evidence of each claim. This stage reads one record, then shows the same
system as `goat-options` reads it from all three stores.**

The record is [`stores/tessaline/systems/tr-40.rec`](../../stores/tessaline/systems/tr-40.rec),
written by the notional vendor Tessaline Instruments about its TR-40 radar.
It holds things the tool does not read: a `contact` line and attributes such
as `port=` and `sample=`. The tool keeps them and says so; it refuses
nothing it can tokenize.

```bash
bin/hello-options 1
```

Velmora also holds a record of the TR-40, in its own store. The tool shows
both, each claim with the store, file, line and author it came from. Stage 6
looks at where the two disagree.

## What you should see

Run against goat-transformers with `fix/options-proving` merged.

The files the stage prints first are left out here; they are in the repository.

```text
== Stage 1: read one record ==
A record is a text file: one system, what it emits and accepts, and the status of each claim.

[1] The record Tessaline wrote about its TR-40 radar

[2] The same system as the tool reads it, from all three stores
    $ goat-options systems --store stores/tessaline --store stores/velmora --store stores/kastreni
    emits    asterix-cat048           proven       3.2        by tessaline
    emits    asterix-cat062           proven       3.2        by tessaline
    emits    asterix-cat034           available    3.2        by tessaline
    emits    sapient                  forthcoming  4.0        by tessaline
    emits    canonical-track-v2       forthcoming  4.0        by tessaline
    accepts  tessaline control json   available    3.2        by tessaline
    emits    asterix-cat048           proven       3.1        by velmora
    emits    asterix-cat062           available    3.1        by velmora
    emits    sapient                  unknown      4.0        by velmora
    records: systems/tr-40.rec (tessaline), received/tessaline-tr-40.rec (velmora)

[3] Verify
    PASS  the query exits 0
    PASS  Tessaline's record gives 6 claims
    PASS  two owners have a record of the TR-40: tessaline and velmora
    PASS  every claim keeps its store, file and line
    PASS  the keyword `contact`, which the tool does not read, is kept
    PASS  the attribute `port=8600`, which the tool does not read, is kept
    PASS  a claim on a format with a pack is marked as having one
    PASS  a claim on a format with no pack is kept and marked as having none

stage complete: every check held
```
