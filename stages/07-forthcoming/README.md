# Stage 7 — a forthcoming option

**A claim for a version its owner has announced and not delivered is
`forthcoming`. A path through it is listed beside the paths in hand today,
with that status, so a planner sees both.**

Tessaline's notional release plan RP-24 announces SAPIENT and Canonical
Track v2 for the TR-40 at version 4.0, and Cursor-on-Target input for the
EO-7 and the JX-2 effector. Each forthcoming claim points at the plan.

```bash
bin/hello-options 7
```

Velmora's own record of the TR-40 says `unknown` for the SAPIENT output of
version 4.0: it has seen the announcement and has no date. Both claims are
listed, so the same path appears once as `forthcoming` and once as `unknown`.

## What you should see

Run against goat-transformers with `fix/options-proving` merged.

```text
== Stage 7: a forthcoming option ==
A claim for a version announced and not in hand is `forthcoming`. A path is as forthcoming as its least established step.

[1] What Tessaline's release plan announces
    | # Release plan RP-24 (notional)
    | 
    | Tessaline Instruments, 2026-09-15. Announced, not delivered.
    | 
    | | Product | Version | Adds |
    | |---|---|---|
    | | TR-40 | 4.0 | SAPIENT detection reports; Canonical Track v2 on Zenoh |
    | | EO-7 | 3.0 | slew to a Cursor-on-Target position |
    | | HA-3 | 3 | SAPIENT detection reports |
    | | JX-2 | 2.0 | Cursor-on-Target cue |
    | 
    | Notional document, written for this demonstration.

[2] Every forthcoming claim in the stores
    $ goat-options systems --store stores/tessaline --store stores/velmora --store stores/kastreni
    tessaline/eo-7   accepts  cot-xml              version 3.0  evidence=evidence/rp-24-release-plan.md
    tessaline/ha-3   emits    sapient              version 3    evidence=evidence/rp-24-release-plan.md
    tessaline/jx-2   accepts  cot-xml              version 2.0  evidence=evidence/rp-24-release-plan.md
    tessaline/tr-40  emits    sapient              version 4.0  evidence=evidence/rp-24-release-plan.md
    tessaline/tr-40  emits    canonical-track-v2   version 4.0  evidence=evidence/rp-24-release-plan.md

[3] At ridge camp: the RF-9 to the JX-2 effector
    $ goat-options paths --store stores/tessaline --store stores/velmora --store stores/kastreni --from tessaline/rf-9 --to tessaline/jx-2 --table
    | tessaline/rf-9 -> tessaline/jx-2
    |   conv  status       route                                                                                                    keys                on hand  claims by                      marks
    |   1     forthcoming  remote-id --[goat-transformers]--> cot-xml                                                               4 carried, 49 lost           tessaline 1.4 / tessaline 2.0
    |   1     available    remote-id --[goat-transformers]--> sapient                                                               3 carried, 50 lost           tessaline 1.4 / tessaline 1.8
    |   2     forthcoming  tessaline rf-9 json --[velmora/node-decoder-rf9]--> canonical-track-v2 --[goat-transformers]--> cot-xml  not stated                   tessaline 1.4 / tessaline 2.0
    |   2     available    tessaline rf-9 json --[velmora/node-decoder-rf9]--> canonical-track-v2 --[goat-transformers]--> sapient  not stated                   tessaline 1.4 / tessaline 1.8
    | 
    | Paths are listed by number of conversions, then by format and converter name, so the output is stable. The order is not a preference. Each path's status is the least established status among its own steps.
    | 
    | 0 error(s), 0 warning(s), 53 note(s) from reading the files; run `check` to list them
    $ goat-options paths --store stores/tessaline --store stores/velmora --store stores/kastreni --from tessaline/rf-9 --to tessaline/jx-2

[4] Verify
    PASS  5 forthcoming claims, all by Tessaline
    PASS  every forthcoming claim points at the release plan, and it resolves
    PASS  two paths from the RF-9 to the JX-2 are forthcoming, both ending in the JX-2's announced cot-xml
    PASS  the paths in hand today are listed beside them, as available

stage complete: every check held
```
