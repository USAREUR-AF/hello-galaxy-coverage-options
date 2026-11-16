# Stage 6 — two owners, merged, disagreeing

**Stores merge by system identifier. Two owners who describe one system use
the same identifier, and the tool keeps every claim from both, each with its
author. Nothing one owner writes replaces what another wrote.**

Two systems have two records here:

| System | Its maker's record | The other record | They disagree on |
|---|---|---|---|
| `tessaline/tr-40` | Tessaline: Category 062 `proven` at version 3.2 | Velmora: Category 062 `available` at version 3.1, tracks dropped in an exercise | status, and version |
| `tessaline/eo-7` | Tessaline: SAPIENT `proven` | Kastreni: SAPIENT `available`, classification empty in a trial | status |

```bash
bin/hello-options 6
```

The stage also runs one query with the stores in two orders and checks that
the paths are the same.

## What you should see

Run against goat-transformers at commit `8845949`.

```text
== Stage 6: two owners, merged, disagreeing ==
Stores merge by system identifier. Nothing one owner writes replaces what another wrote.

[1] Two records of tessaline/tr-40, in two stores
    stores/tessaline/systems/tr-40.rec
    | by       tessaline
    | emits    asterix-cat062  version=3.2  transport=udp  port=8601  status=proven  evidence=evidence/fat-tr40-0311.md  sample=evidence/captures/tr40-track-0311.hex
    stores/velmora/received/tessaline-tr-40.rec
    | by       velmora
    | emits    asterix-cat062  version=3.1  transport=udp  status=available  evidence=evidence/exercise-ax26.md  note="exercise AX-26: tracks dropped above 60 targets; the vendor's fix in 3.2 not yet received"

[2] Merged: both claims about Category 062 are kept, each with its owner and version
    $ goat-options systems --store stores/tessaline --store stores/velmora --store stores/kastreni
    tessaline  version 3.2  proven     
    velmora    version 3.1  available  exercise AX-26: tracks dropped above 60 targets; the vendor's fix in 3.2 not yet received

[3] The direct paths to Velmora's air C2: one per claim
    $ goat-options paths --store stores/tessaline --store stores/velmora --store stores/kastreni --from tessaline/tr-40 --to velmora/c2-air --max-conversions 0 --table
    | tessaline/tr-40 -> velmora/c2-air
    |   conv  status     route           keys       on hand  claims by                    marks
    |   0     proven     asterix-cat062  unchanged           tessaline 3.2 / velmora 5.1
    |   0     available  asterix-cat062  unchanged           velmora 3.1 / velmora 5.1
    | 
    | Paths are listed by number of conversions, then by format and converter name, so the output is stable. The order is not a preference. Each path's status is the least established status among its own steps.
    | 
    | 0 error(s), 0 warning(s), 53 note(s) from reading the files; run `check` to list them

[4] The same for the EO-7, where Kastreni's record disagrees with Tessaline's
    $ goat-options systems --store stores/tessaline --store stores/velmora --store stores/kastreni
    tessaline  emits    proven     
    tessaline  accepts  available  task messages: slew, zoom, track
    kastreni   emits    available  detections received; the classification field was empty in every report
    kastreni   accepts  unknown    tasking not tried

[5] The answer does not depend on the order of the stores
    $ goat-options paths --store stores/tessaline --store stores/velmora --store stores/kastreni --from tessaline/tr-40 --to velmora/fabric-tracks
    $ goat-options paths --store stores/kastreni --store stores/velmora --store stores/tessaline --from tessaline/tr-40 --to velmora/fabric-tracks

[6] Verify
    PASS  the TR-40 has 9 claims from 2 owners
    PASS  Tessaline says Category 062 is proven at 3.2; Velmora says available at 3.1; both are shown
    PASS  the two direct paths carry the two statuses
    PASS  the EO-7 has records from tessaline and kastreni
    PASS  both names the two owners gave the EO-7 are kept
    PASS  store order changes nothing but the list of stores in the query

stage complete: every check held
```
