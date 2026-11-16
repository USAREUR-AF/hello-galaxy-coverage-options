# Stage 10 — a private store beside this one

**Records of real systems never go into a public repository: which system
speaks what, in which version, is itself the sensitive fact. A private store
is a directory of records kept elsewhere, and it joins the query at run time
with one more `--store`. This stage writes a stand-in private store under
`.run/` (ignored by git), queries it with the public stores, prints the
counts that may leave the private side, and checks a needle list against the
tracked files.**

```bash
bin/hello-options 10
```

To keep a real private store:

- Put it in a private repository, one directory per owner
  (goat-transformers `docs/private-store.md`). Pass it with `--store`, beside
  or instead of these.
- Never copy its records, site files or identifiers into a public
  repository, issue, pull request or commit message.
- Keep a needle list of its identifiers outside the public repository, and
  refuse a push when a tracked file holds one: `git grep -i -w -F -f <list>`
  here, or goat-transformers `tools/boundary-gate --needles <list>`.
- Share counts (`goat-options summary`) where the records may not go.

## What you should see

Run against goat-transformers at commit `8845949`.

```text
== Stage 10: a private store beside this one ==
Records of real systems never go into a public repository. They live in a private store and join the query at run time.

[1] A private store, written outside the tracked tree (.run/ is ignored by git)
    | record   1
    | system   our-maker/our-sensor-a
    | name     "A system only our organization may know about"
    | kind     sensor
    | by       our-org
    | date     2026-11-16
    | note     "In a real private store this file holds a real system. Here it is a stand-in."
    | 
    | emits    cot-xml  transport=udp  status=available
    git check-ignore: ignored

[2] The public stores and the private one in one query
    $ goat-options paths --store stores/tessaline --store stores/velmora --store stores/kastreni --store .run/private-store --from our-maker/our-sensor-a --to kastreni/tactical-display --table
    | our-maker/our-sensor-a -> kastreni/tactical-display
    |   conv  status     route                                 keys                on hand
    |   0     available  cot-xml                               unchanged
    |   1     available  cot-xml --[goat-transformers]--> nvg  4 carried, 10 lost
    | 
    | Paths are listed by number of conversions, then by format and converter name, so the output is stable. The order is not a preference. Each path's status is the least established status among its own steps.
    | 
    | 4 problem(s); run `check` to list them
    $ goat-options paths --store stores/tessaline --store stores/velmora --store stores/kastreni --store .run/private-store --from our-maker/our-sensor-a --to kastreni/tactical-display

[3] What may leave the private side: counts only
    $ goat-options summary --store stores/tessaline --store stores/velmora --store stores/kastreni --store .run/private-store --table
    | systems              28
    | producers            24
    | consumers            21
    | formats_named        24
    | formats_with_pack    14
    | pairs                487
    | pairs, strongest path proven       25
    | pairs, strongest path available    305
    | pairs, strongest path forthcoming  0
    | pairs, strongest path unknown      37
    | pairs, strongest path none         120
    | 
    | 4 problem(s); run `check` to list them

[4] A needle list: the private store's identifiers must appear in no tracked file
    $ git grep -i -w -F -f .run/private-needles.txt
    0 tracked line(s) hold a needle

[5] Verify
    PASS  the private store is ignored by git
    PASS  the query merges it: paths from the private system exist
    PASS  every path from it names the private store as the source of its claim
    PASS  the summary holds counts and no identifier
    PASS  no tracked file outside this stage's directory names the private system

stage complete: every check held
```
