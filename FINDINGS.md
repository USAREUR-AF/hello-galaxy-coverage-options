# Findings — what proving it out showed

Status: Measured. Every finding below was seen in a run of this repository
against goat-transformers at commit `12a205e` (before the fixes of section 3)
or `8845949` (with them), and each names the record, file or command
that shows it. Commands run from the repository root; `S` stands for
`--store stores/tessaline --store stores/velmora --store stores/kastreni`.

The stores are notional, so these findings are about the record format and
the tool, not about any real system. They are the first use of the format by
more than one notional owner, and they are not a substitute for records
written by real owners.

## Summary

| | Count |
|---|---|
| Worked as designed | 7 |
| The format could not express it | 9 |
| The tool got it wrong or made it awkward, fixed in goat-transformers pull request 11 | 5 |
| The tool or the library made it awkward, not fixed | 7 |

The fixes are in goat-transformers `main` at commit `8845949` (pull request
11), with tests (26 pass). Stage 4 needs them; this repository pins that
commit.

## 1. What worked

| # | What | Shown by |
|---|---|---|
| W1 | 29 records in three owners' styles were read with nothing refused. Keywords the tool does not read (`contact`, `topic`, `retention`) and attributes (`port=`, `icd=`, `bus=`, `dictionary=`, `sample=`, `set=`) were kept and appear in the JSON. This repository used two of them, `sample=` and `set=`, as its own convention without any change to the tool. | stage 1; `goat-options systems $S` |
| W2 | Merging by identifier kept both owners' claims about the TR-40 and the EO-7, each with store, file, line, author and version, and the answer did not depend on the order of the stores. | stage 6 |
| W3 | A site without the library: every path that uses a library step is marked not on hand at harbor east, and the three paths through the binary decoder are marked on hand. | stage 5; `goat-options site $S sites/harbor-east.site --table` |
| W4 | The JSON was enough to build two consumers without reading the tool's code: `consumer/site-grid.py` (32 lines) and `tools/prove.py`, which reads `goat-options systems` to find every proven claim. | stage 9; `tools/prove.py` |
| W5 | All five library conversions claimed `proven` ran on their samples. For the keys the capability report counts, the keys carried in each run equal the report's `carried` list. | `stores/*/evidence/runs/*.json`, keys `carried` and `capability.carried` |
| W6 | `check --strict` caught the five mistakes of a first draft: an unclosed quote, no `system` line, `proven` with no evidence, a status outside the four, `converts` with one format. | stage 8 |
| W7 | `forthcoming` paths from an announced version are listed beside the paths in hand today, so both are seen in one answer. | stage 7 |

## 2. What the format could not express

| # | What | Shown by | What would change it |
|---|---|---|---|
| F1 | **Two names for one format.** Velmora's AIS receiver writes `"NMEA 0183 AIS"`; Kastreni's gateway writes `nmea0183-ais`. They do not match, and the receiver reaches nothing at harbor east. `check` lists both as names with no pack, which is the only hint. | `stores/velmora/systems/harbor-ais.rec`, `stores/kastreni/systems/edge-capture.rec`; stage 5 | an alias list beside the stores, or a rule that a format with a pack is written by its pack name. A format with no pack has no such name to agree on. |
| F2 | **A gateway that carries a feed unchanged.** The edge capture gateway reads each feed on UDP and republishes it on Zenoh. A record can say it accepts and emits the same format, but not that the one is carried to the other; `converts X X` is not a step because a format does not repeat within a path. So the AIS receiver, the coalition radar and the LR-5 cannot reach the harbor fabric *through* the gateway in any answer. The gateway appears only as a producer of everything it captures. | `stores/kastreni/systems/edge-capture.rec`; stage 5, `feed kastreni/tactical-display from kastreni/edge-capture` | a claim kind such as `carries <format> from=<transport> to=<transport>`, read as a step that keeps the format. This is the transport bridging the design leaves out. |
| F3 | **Which messages of a format a system takes.** The JX-2 effector accepts SAPIENT task and alert messages only (its note says so). The tool lists remote identification to SAPIENT through the library as `available`; the library writes a SAPIENT detection report, which the JX-2 does not take. | `stores/tessaline/systems/jx-2.rec`; stage 7 table | a `kinds=` attribute on a claim, matched against the pack's kinds. Coverage per message kind is listed in the design as left out; this is its first concrete cost. |
| F4 | **Keys a converter supplies.** Category 062 to Canonical Track v2 runs only when the caller supplies `uid`, `track.source_id`, `track.generation` and `time_ms`. A record has nowhere to say that a decoder supplies them, or how. This repository wrote `set="..."` on the claim, which the tool keeps and does not read. | `stores/velmora/systems/node-decoder-tr40.rec`; `stores/velmora/evidence/runs/node-decoder-tr40.json` key `supplied` | a recognized attribute on a `converts ... via=goat-transformers` claim naming the keys the converter supplies, so `needs` can be met by a claim |
| F5 | **Which system runs a library conversion.** Velmora's translator and fabric bridge each claim `converts ... via=goat-transformers`. The path shows the step as the library's, and at a site the step is on hand only when the site file says `have goat-transformers`. That the translator, which embeds the library, is on hand does not count. | `stores/velmora/systems/node-translator.rec`; `sites/ridge-camp.site` | count a library step on hand when a system on hand claims that conversion via the library |
| F6 | **A library conversion's evidence is shared by every path.** The decoder's proven claim for Category 062 to Canonical Track v2 makes that step `proven` in every path, including paths from Kastreni's edge gateway. The run that proved it needed four keys supplied by the decoder. | stage 3: `tessaline/tr-40 -> velmora/fabric-tracks`, the one proven path | read the claim as evidence for its own system's steps only, or show the claiming system on the step |
| F7 | **What evidence points to.** `evidence=` is free text. This repository made every pointer a path relative to the owner's store directory and checks it with `tools/prove.py`; the tool cannot, and `check` passes `proven` with a pointer to nothing. | stage 3; stage 8 notes | owners agreeing a form for evidence (a path in the owner's store, a document number) that `check` can test |
| F8 | **A status between `available` and `proven`.** Kastreni's trial of the EO-7 received detections with an empty classification. That is more than `available` and less than working; it went into a note. A first draft that wrote `status=partly` was read as `unknown`. | `stores/kastreni/received/tessaline-eo-7.rec`; stage 8 | nothing, if notes are enough; otherwise a way to qualify `proven` (which fields were seen) rather than a fifth word |
| F9 | **Direction from `speaks` only.** The coastal AIS station has two `speaks` lines and nothing else. It accounts for 36 of the 466 producer and consumer pairs, and every path of those 36 rests on an unstated direction. One record from an equipment list moves the counts by 8 percent. | `stores/kastreni/systems/coastal-ais.rec`; `goat-options summary $S`, `pairs_whose_every_path_rests_on_an_unstated_direction` | sources that state direction; until then, read the summary with and without such systems |

## 3. What the tool got wrong or made awkward, and is fixed

In goat-transformers commit `8845949` (pull request 11), in
`tools/goat-options`, with tests in `tools/tests/test_goat_options.py` and the
design in `docs/system-records.md` updated.

| # | What was wrong | Shown by | The fix |
|---|---|---|---|
| D1 | **A library step was `available` when the library refuses it.** Canonical Track v2 requires `uid`, `track.source_id`, `track.generation` and `time_ms`; Category 062 maps none of them, and the engine raises `no-kind`. The tool listed the step as available with "9 carried". Before the stores were written, 56 ordered pairs of the formats used here were tried on every pack vector of the source: for 22 pairs the library refused every vector, most with `no-kind` on the target. | stage 4; `goat-options paths $S --from tessaline/tr-40 --to velmora/fabric-tracks` | a library step carries `needs`: for each kind of the target, the required keys the source does not supply, counting what the model derives; `null` when some kind can be written. The table marks it. The step is still listed, because a caller can supply the keys. |
| D2 | **`check` did not list unknown attributes**, though the design says it does. The existing test asserted the old behavior. | `goat-options check $S` at `12a205e` lists `contact` and `topic` and not `port=` or `sample=` | each is listed as `info` |
| D3 | **`transports_differ` marked every path**, though it is documented for a direct path. On a path with a converter the mark compared the source's transport with the consumer's, which the converter changes anyway: 31 of the 38 paths in the harbor east answer carried it, 29 of them paths with a conversion. | `goat-options site $S sites/harbor-east.site` at `12a205e` | only direct paths are marked |
| D4 | **Identical rows.** Two owners' claims about the TR-40 gave pairs of rows that looked the same in the table; only the JSON told them apart. The table also hid an unstated direction and a differing transport. | stage 2 table at `12a205e` | two columns: `claims by` (author and version of each end's claim) and `marks` |
| D5 | **Every table ended with "N problem(s)"**, counting the notes about kept keywords as problems (53 with the stores here). | any `--table` | the footer counts errors, warnings and notes apart |

## 4. What is awkward and not fixed

| # | What | Shown by | Where it belongs |
|---|---|---|---|
| A1 | **The capability report does not count derived keys.** Category 062 to GeoJSON writes `course` and `speed_ms`, derived from the velocity the report counts as lost. Canonical Track v2 to CoT XML writes `ce`, `le`, `course` and `speed_ms` the same way. The report under-counts what carries. | stage 4; `stores/kastreni/evidence/runs/fabric-picture-geojson.json`, `stores/velmora/evidence/runs/node-translator-cot.json` | the engines' `capability` (engine specification). `needs` already counts derivations, so the two now differ in this. |
| A2 | **A conversion with nothing required succeeds with nothing in it.** A Category 048 plot (range and bearing, no position) converts to CoT XML as `<event version="2.0" type="a-u-X"><point hae="9999999" .../></event>`. CoT XML has no `requires` line, so nothing refuses it. The step's "1 carried, 143 lost" is the only sign. | stage 4 | the packs: whether CoT XML, GeoJSON and NVG require a position |
| A3 | **Answers are long.** The ridge camp site gives 73 paths over 11 source and consumer pairs; one pair, the TR-40 to the map display, has 21. Every claim by a second owner doubles a row. Reading needs filters (by status, by on hand, by owner). | stage 5 | consumers of the JSON (stage 9 shows one); filters in the tool would not rank, but would add options to keep simple |
| A4 | **A `feed` line with no `from=` asks every system on hand that emits anything**, including displays and the effector's status reports: at ridge camp, "map display from the JX-2" lists three paths of the effector's status reports. | stage 5 | the site file: a way to say which systems are sources, or `from=` on every line |
| A5 | **The summary hides forthcoming options.** Each pair counts at its strongest path, so 5 forthcoming claims give 0 pairs "forthcoming": every such pair also has an available path. | `goat-options summary $S --table` | nothing, if read as designed; a second count of pairs with any forthcoming path would show them |
| A6 | **One bad line in any store makes every command exit 1.** An unclosed quote is an `error`, and an error fails `paths`, `site` and `summary` even when the bad record is not on the path. A store received from another owner can stop a site's queries. | stage 8, the draft | the tool: make a line that cannot be read a warning outside `check` |
| A7 | **Proof in a notional repository is partly circular.** The binary samples here are encoded by the library from notional values, so decoding them shows that the record, the sample and the pack agree, not that a real system sends such a message. The MAVLink sample carries the checksum of the pack's vector: the pack neither verifies nor writes it (its `pack.md`), so the sample is not a transmittable frame. For 5 claims on formats with no pack, a capture is kept and nothing can read it. | `tools/make-captures.py`; `tools/prove.py` lines "no pack for ..." | the first real use: captures from real systems, in private stores |

## 5. What needs a decision, not code

1. **How formats with no pack are named across owners** (F1). Without an
   agreement, records from different owners do not join on those formats.
2. **Whether the format grows a claim kind for a gateway that carries a feed
   unchanged** (F2), or such gateways stay outside the answer. Three of the
   four consumer shapes here sit near one.
3. **What counts as evidence** (F7, F8, A7). This repository's rule (a file in
   the owner's store, a sample that decodes, a run that repeats) is one
   choice, and strict; real owners will hold trial reports that are not
   machine-checkable.
