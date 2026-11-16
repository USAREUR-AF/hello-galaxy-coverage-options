# Stage 3 — read the evidence of a path

**Each `proven` claim points at a file in its owner's store. This stage
follows the pointers of one proven path, opens the library run that one of
them names, and then checks every proven claim in the repository again with
`tools/prove.py`.**

In this repository nothing is `proven` by assertion alone. A proven claim
needs `evidence=` that resolves in the owner's store directory and `sample=`
naming a message. Where the format has a pack, the goat-transformers Python
engine decodes the sample. Where the claim is a library conversion
(`converts ... via=goat-transformers`), `tools/prove.py --write` runs it and
writes the run file the claim points to; `tools/prove.py` runs it again and
fails if the result differs.

```bash
bin/hello-options 3
bin/hello-options prove          # every proven claim, on its own
```

Where a format has no pack (the LR-5's binary format, the EO-7's own JSON),
the capture is kept and the library cannot read it. Those claims rest on the
capture only; `tools/prove.py` says so on their line.

## What you should see

Run against goat-transformers with `fix/options-proving` merged.

```text
== Stage 3: read the evidence of a path ==
A path's status comes from claims; each proven claim points at a file in its owner's store.

[1] The paths from the TR-40 to the depot lake track picture that are proven
    $ goat-options paths --store stores/tessaline --store stores/velmora --store stores/kastreni --from tessaline/tr-40 --to velmora/fabric-tracks --keys count
    asterix-cat062 --[goat-transformers]--> canonical-track-v2
    source   tessaline/tr-40          emits    proven    evidence=evidence/fat-tr40-0311.md  (stores/tessaline/systems/tr-40.rec:11, by tessaline)
    step     velmora/node-decoder-tr40 converts proven    evidence=evidence/runs/node-decoder-tr40.json  (stores/velmora/systems/node-decoder-tr40.rec:11, by velmora)
    consumer velmora/fabric-tracks    accepts  proven    evidence=evidence/bench-n1-0412.md  (stores/velmora/systems/fabric-tracks.rec:10, by velmora)

[2] Follow the step's evidence: a run of the library, kept in Velmora's store
    velmora/node-decoder-tr40 converted evidence/captures/ax26-track-0927.hex to canonical-track-v2 with the keys time_ms, track.generation, track.source_id, uid supplied by the caller
    | {"apiVersion":"billie.dev/track-v2","kind":"Track","trackId":"n1-tr40-2210","sourceId":"velmora-n1-tr40","trackGeneration":"gen-1","simulated":false,"confirmed":true,"coasting":false,"finalUpdate":false,"observedAt":"2026-09-27T13:01:31.250Z","position":{"latitudeDeg":44.59869861602783,"longitudeDeg":-30.330199599266052,"altitudeM":609.6},"velocity":{"eastMps":14,"northMps":-3.5}}

[3] Run every proven claim of every store again: tools/prove.py
    $ tools/prove.py
    | 36 proven claim(s), 0 failed

[4] Verify
    PASS  one path is proven: asterix-cat062 --[goat-transformers]--> canonical-track-v2
    PASS  its source claim is Tessaline's, for version 3.2
    PASS  every evidence pointer on the path resolves in its owner's store
    PASS  the run names the sample it converted, and the sample is unchanged
    PASS  the run needed four keys the caller supplied
    PASS  tools/prove.py: every proven claim resolves, decodes or runs (exit 0)
    PASS  tools/prove.py checked 36 proven claims

stage complete: every check held
```
