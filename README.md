# hello-galaxy-coverage-options

**A system produces data and another system needs it. In which ways can the
data get there today or soon, and what is the evidence for each? Ten runnable
stages use system records and `goat-options` from
[goat-transformers](https://github.com/USAREUR-AF/goat-transformers) on
notional stores of 27 systems from three owners, and say what each answer
shows and what it does not.**

This is a repository in the **Hello Galaxy** series: small, self-contained,
runnable examples, each about one part of goat. Every system, owner, site,
document and message here is notional. The tool and the library are the real
ones, fetched at a pinned commit.

---

## The question this repository answers

Coverage planning asks which sensors can feed which consumers, and how. The
answer depends on facts held by many owners: which formats a system emits or
accepts, in which version, over which transport, and how well that is
established. A **system record** states those facts for one system, in one
plain text file. `goat-options` reads records from any number of stores,
joins them with the conversions the goat-transformers library can make, and
lists every path from a producer to a consumer with the status and evidence
of each step.

It lists options. It does not rank them or name a preferred one, and nor does
anything in this repository: there is no single right path, and the choice
belongs to the person with the context. What the stages show is how to read
the options, and where the records and the tool can and cannot be trusted.

The record format, the site file and the query are specified in
goat-transformers [`docs/system-records.md`](https://github.com/USAREUR-AF/goat-transformers/blob/main/docs/system-records.md);
keeping records of real systems is in
[`docs/private-store.md`](https://github.com/USAREUR-AF/goat-transformers/blob/main/docs/private-store.md).

## The ten stages

| Stage | What it shows | Ends by checking |
|---|---|---|
| [**1 one record**](stages/01-one-record/) | a record as text, and the same system as the tool reads it from three stores | 9 claims from 2 owners; unknown keywords and attributes kept |
| [**2 one question**](stages/02-one-question/) | every path from the TR-40 radar to Velmora's air command application | 12 paths; two direct ones, one per owner's claim |
| [**3 evidence**](stages/03-evidence/) | follow the evidence of a proven path to a library run, and check every proven claim again | 36 proven claims resolve, decode or run |
| [**4 carried and lost**](stages/04-carried-and-lost/) | the library's report of what carries, beside two conversions that were run, and what the target needs | a plot converts to an event with no position; a run writes two keys the report does not count |
| [**5 sites**](stages/05-sites/) | three sites, one without the library, each with its own systems and consumers | no library path on hand where the library is not; an AIS feed lost to a format name written two ways |
| [**6 two owners**](stages/06-two-owners/) | two owners' records of one system, merged and disagreeing | both statuses shown; store order changes nothing |
| [**7 forthcoming**](stages/07-forthcoming/) | options from a vendor's announced version, beside today's | 5 forthcoming claims, each pointing at the release plan |
| [**8 strict check**](stages/08-strict-check/) | a first draft with five mistakes fails `check --strict`; the fixed copy passes | exit 1, then exit 0 |
| [**9 your own view**](stages/09-your-own-view/) | a 32-line program draws its own grid from the JSON | the grid's cells for two sites |
| [**10 private store**](stages/10-private-store/) | a private store joins the query at run time and stays out of git | ignored by git; no tracked file holds its identifier |

Each stage prints what it runs and ends with checks that pass or fail; a
failed check makes the stage exit 1. Each stage's README has the output of a
run.

## Run it

Prerequisites: `bash`, `git` and Python 3.9 or later. Nothing is installed;
everything is the Python standard library and goat-transformers' Python
engine.

```bash
bin/hello-options fetch      # goat-transformers at the pinned commit, into .cache/
bin/hello-options all        # tools/prove.py, then the ten stages in order
```

`bin/hello-options <n>` runs one stage; `bin/hello-options list` names them;
`bin/hello-options prove` checks every proven claim; `bin/hello-options clean`
removes `.run/` and `.cache/`. CI runs the same commands on a GitHub-hosted
Ubuntu runner.

| Measured on one machine | |
|---|---|
| `bin/hello-options all`, goat-transformers already fetched | 15 s |
| `goat-options summary` over the three stores (466 producer and consumer pairs) | 5.4 s |

## What is in the stores

Three owners, each with its own store directory. Every `evidence=` and
`sample=` path is relative to the owner's directory, so a store copied on its
own keeps its evidence.

| Store | Owner | Systems |
|---|---|---|
| [`stores/tessaline`](stores/tessaline/) | Tessaline Instruments, a notional vendor | a short-range radar, a camera, a radio frequency detector, an acoustic array, an effector and a display |
| [`stores/velmora`](stores/velmora/) | Velmora, a notional nation | a sensor node (three decoders and a translator), an air command application, a map display, three fabric applications, a ground control station, an ADS-B station, an AIS receiver; and its own record of the TR-40 |
| [`stores/kastreni`](stores/kastreni/) | Kastreni, a notional nation | an edge capture gateway, a binary decoder, a long-range radar, an air command application, a tactical display, a patrol boat gateway, a coastal AIS station, an interceptor, a fabric application; and its own record of the EO-7 |

| In the stores | Number |
|---|---|
| Records | 29, for 27 systems (two systems have records from two owners) |
| Claims | 100: 44 `emits`, 43 `accepts`, 11 `converts`, 2 `speaks` |
| Status of the claims | 36 `proven`, 52 `available`, 5 `forthcoming`, 5 `unknown`, 2 with none |
| Format names | 24, of which 14 have a pack: ASTERIX Categories 021, 034, 048 and 062, SAPIENT, Cursor-on-Target XML and Protobuf, GeoJSON, NVG, Canonical Track v2, MAVLink 2, NMEA 2000, ADS-B and remote identification |
| Formats with no pack | 10: the vendors' own JSON and binary formats, a national radar's binary format, NMEA 0183 AIS (written two ways), STANAG 4607, a fire control link and an alert format |
| Producer and consumer pairs | 466: 25 with a proven path, 289 with an available path at best, 36 unknown at best, 116 with no path |

The samples under `stores/*/evidence/captures/` are written by
[`tools/make-captures.py`](tools/make-captures.py): the binary ones are
encoded by the library from notional values, so a sample decoding is a check
that the record, the sample and the pack agree, not a proof that any real
system sends it. [FINDINGS.md](FINDINGS.md) says more.

## The four consumer shapes

The stores hold four shapes of consumer that real open-source projects take.
The systems here are notional and are not those projects.

| Shape here | Systems | The open-source project of that shape |
|---|---|---|
| a sensor node: one decoder per sensor, then a translator | `velmora/node-decoder-eo7`, `-rf9`, `-tr40`, `velmora/node-translator` at ridge camp | Open Billie |
| an edge gateway that captures every feed and republishes it unchanged | `kastreni/edge-capture` at harbor east | octo-pod |
| a decoder of fixed-layout binary messages, driven by a dictionary written from the interface document | `kastreni/binary-decoder` at harbor east | first-bite ([hello-galaxy-first-bite](https://github.com/USAREUR-AF/hello-galaxy-first-bite)) |
| applications on a Zenoh data fabric | `velmora/fabric-tracks`, `-alerts`, `-bridge` at depot lake; `kastreni/fabric-picture` | goat |

## What is pinned

| What | Pin | Change it in |
|---|---|---|
| goat-transformers | commit `12a205e881cbdd3dc1295b14bf59ffcdde2081bb`, its `main` with system records and `goat-options` | [`GOAT_TRANSFORMERS_REF`](GOAT_TRANSFORMERS_REF); [`tools/fetch-goat-transformers.sh`](tools/fetch-goat-transformers.sh) fetches it, and CI runs the same script |
| GitHub Actions | by commit SHA | [`.github/workflows/`](.github/workflows) |

Stage 4 needs a change to `goat-options` that is not yet in goat-transformers
`main`: the branch `fix/options-proving`, which adds `needs` to a library step
(the required keys the source does not supply). Against the pinned commit
stage 4 fails two checks and says why; the other nine stages and
`tools/prove.py` pass. When that change merges, put its merge commit in
`GOAT_TRANSFORMERS_REF`. To run against another checkout:

```bash
GOAT_TRANSFORMERS_DIR=/path/to/goat-transformers bin/hello-options all
GOAT_TRANSFORMERS_REF=<commit> GOAT_TRANSFORMERS_URL=<repository> bin/hello-options fetch
```

The tables in the stage READMEs come from a run with that change, which adds
the `claims by` and `marks` columns.

## What is deliberately simplified

| Here | In a real deployment |
|---|---|
| every system, owner, site, document and message is notional | records describe fielded systems and live in private stores (stage 10) |
| samples are written by the library from notional values | a sample is a capture from the real system, which may not decode |
| `proven` means a sample is kept and, where a pack exists, decodes; a library conversion has been run on it | owners decide what counts as proof; the record format leaves evidence as free text |
| three stores side by side in one repository | each owner keeps its own store and shares it by copy, with the parties entitled to it |

## Repository layout

```
bin/hello-options            the runner: fetch, prove, <stage>, all, list, clean
lib/hello.py                 shared by the stages: where goat-transformers is, running goat-options, checks
GOAT_TRANSFORMERS_REF        the goat-transformers commit every stage runs against
stores/<owner>/              one directory per owner: systems/, received/, evidence/
sites/                       three site files
stages/NN-name/              README.md and run.py for each stage
stages/08-strict-check/store a first draft with five mistakes, for stage 8
consumer/site-grid.py        the program of stage 9
tools/prove.py               checks every proven claim; --write writes the library runs
tools/make-captures.py       writes the notional samples; --check compares
tools/fetch-goat-transformers.sh
FINDINGS.md                  what proving it out showed
```

One of the Hello Galaxy series of runnable goat demonstrations.

## Licence

`hello-galaxy-coverage-options` was written by U.S. Federal government employees. In the U.S. it is not subject to copyright and is in the public domain; in countries where copyright is recognized, it is released under the [Apache License 2.0](LICENSE). See [INTENT.md](INTENT.md).
