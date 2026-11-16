# Stage 2 — ask one question

**From one producing system to one consuming system, `goat-options paths`
lists every path: a direct one where both ends name the same format, and
paths with one or two conversions. Each path has a status, and the table says
whose claims it rests on.**

The question: in which ways can the TR-40 radar's data reach Velmora's air
command application, `velmora/c2-air`?

```bash
bin/hello-options 2
```

The same answer comes as a table for a person and as JSON for a program.
Paths are listed by number of conversions and then by name, so the output is
stable from run to run; the order says nothing about which path to use.

A path's status is the least established status among its own claims: the
source's `emits`, each conversion, and the consumer's `accepts`. Rows that
look the same differ in whose claim they rest on: the `claims by` column
gives the author and version of each end's claim.

## What you should see

Run against goat-transformers at commit `8845949`.

```text
== Stage 2: ask one question ==
From one producing system to one consuming system: every path, with the status of each.

[1] Every path from tessaline/tr-40 to velmora/c2-air, as a table
    $ goat-options paths --store stores/tessaline --store stores/velmora --store stores/kastreni --from tessaline/tr-40 --to velmora/c2-air --table
    | tessaline/tr-40 -> velmora/c2-air
    |   conv  status       route                                                       keys                 on hand  claims by                    marks
    |   0     proven       asterix-cat062                                              unchanged                     tessaline 3.2 / velmora 5.1
    |   0     available    asterix-cat062                                              unchanged                     velmora 3.1 / velmora 5.1
    |   1     available    asterix-cat048 --[goat-transformers]--> cot-xml             1 carried, 143 lost           tessaline 3.2 / velmora 5.1
    |   1     available    asterix-cat048 --[goat-transformers]--> cot-xml             1 carried, 143 lost           velmora 3.1 / velmora 5.1
    |   1     available    asterix-cat062 --[goat-transformers]--> cot-xml             3 carried, 15 lost            tessaline 3.2 / velmora 5.1
    |   1     available    asterix-cat062 --[goat-transformers]--> cot-xml             3 carried, 15 lost            velmora 3.1 / velmora 5.1
    |   1     forthcoming  canonical-track-v2 --[goat-transformers]--> asterix-cat062  9 carried, 16 lost            tessaline 4.0 / velmora 5.1  asterix-cat062 needs cat062.sac cat062.sic
    |   1     forthcoming  canonical-track-v2 --[goat-transformers]--> cot-xml         6 carried, 19 lost            tessaline 4.0 / velmora 5.1
    |   1     forthcoming  sapient --[goat-transformers]--> asterix-cat062             5 carried, 462 lost           tessaline 4.0 / velmora 5.1  asterix-cat062 needs cat062.sac cat062.sic cat062.time_of_day_s cat062.track_number track.confirmed
    |   1     unknown      sapient --[goat-transformers]--> asterix-cat062             5 carried, 462 lost           velmora 4.0 / velmora 5.1    asterix-cat062 needs cat062.sac cat062.sic cat062.time_of_day_s cat062.track_number track.confirmed
    |   1     forthcoming  sapient --[goat-transformers]--> cot-xml                    3 carried, 464 lost           tessaline 4.0 / velmora 5.1
    |   1     unknown      sapient --[goat-transformers]--> cot-xml                    3 carried, 464 lost           velmora 4.0 / velmora 5.1
    | 
    | Paths are listed by number of conversions, then by format and converter name, so the output is stable. The order is not a preference. Each path's status is the least established status among its own steps.
    | 
    | 0 error(s), 0 warning(s), 53 note(s) from reading the files; run `check` to list them

[2] The same answer as JSON, for a program
    $ goat-options paths --store stores/tessaline --store stores/velmora --store stores/kastreni --from tessaline/tr-40 --to velmora/c2-air --keys count
    0 conversion(s)  proven      asterix-cat062
    0 conversion(s)  available   asterix-cat062
    1 conversion(s)  available   asterix-cat048 --[goat-transformers]--> cot-xml
    1 conversion(s)  available   asterix-cat048 --[goat-transformers]--> cot-xml
    1 conversion(s)  available   asterix-cat062 --[goat-transformers]--> cot-xml
    1 conversion(s)  available   asterix-cat062 --[goat-transformers]--> cot-xml
    1 conversion(s)  forthcoming canonical-track-v2 --[goat-transformers]--> asterix-cat062
    1 conversion(s)  forthcoming canonical-track-v2 --[goat-transformers]--> cot-xml
    1 conversion(s)  forthcoming sapient --[goat-transformers]--> asterix-cat062
    1 conversion(s)  unknown     sapient --[goat-transformers]--> asterix-cat062
    1 conversion(s)  forthcoming sapient --[goat-transformers]--> cot-xml
    1 conversion(s)  unknown     sapient --[goat-transformers]--> cot-xml
    counts: {'paths': 12, 'by_status': {'proven': 1, 'available': 5, 'forthcoming': 4, 'unknown': 2}}

[3] Verify
    PASS  the query exits 0
    PASS  12 paths
    PASS  two direct paths in asterix-cat062, one per owner's claim about the radar
    PASS  each path's status is one of the four
    PASS  no path is longer than two conversions
    PASS  the output says the order is not a preference

stage complete: every check held
```
