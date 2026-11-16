# AGENTS.md

Instructions for AI coding agents, and a short version for anyone working here. [CONTRIBUTING.md](CONTRIBUTING.md) is the full process.

## What this repository is

hello-galaxy-coverage-options shows how to use system records and `goat-options` from [goat-transformers](https://github.com/USAREUR-AF/goat-transformers) in ten stages, on notional stores of 27 systems from three owners. It is also the proof that the tool works on data shaped like real records: [FINDINGS.md](FINDINGS.md) says what that showed.

It is one of the Hello Galaxy demonstrations. It holds no goat-transformers source code; `tools/fetch-goat-transformers.sh` fetches it at the commit in `GOAT_TRANSFORMERS_REF`.

## Layout

| Path | What |
|---|---|
| `stages/` | one directory per stage: `README.md` and `run.py` |
| `bin/hello-options` | the runner: `fetch`, `prove`, one stage, `all`, `list`, `clean` |
| `lib/hello.py` | shared by the stages |
| `stores/<owner>/` | each owner's records and the evidence they point to |
| `sites/` | three site files |
| `tools/` | `prove.py`, `make-captures.py`, `fetch-goat-transformers.sh` |
| `consumer/` | the program of stage 9 |

## Before you push

CI (`.github/workflows/ci.yml`) runs these:

```bash
shellcheck bin/hello-options tools/fetch-goat-transformers.sh
bin/hello-options fetch
python3 -I tools/make-captures.py --check
NO_COLOR=1 bin/hello-options all
```

A change to a record or a sample is followed by `tools/prove.py --write` when it touches a library conversion, and by a run of the stages; the "What you should see" block of a stage's README is pasted from a run, never written by hand.

## Rules

1. **Notional only.** No real vendor, product, unit, site, nation, person or program, and no record of a real system, goes into a file or a commit message. Real records live in private stores (stage 10). Example mail addresses end in `.internal`.
2. **Not prescriptive.** No stage, README or output says which path to use. The tool lists options; so does this repository.
3. **Nothing is `proven` by assertion.** A proven claim has `evidence=` that resolves in its owner's store and a `sample=`; `tools/prove.py` must pass.
4. **Commits.** Conventional Commits subject of 100 characters or fewer, with a scope. Every commit is signed off (`git commit -s`) and signed with a key GitHub verifies.
5. **Vulnerabilities** go through [SECURITY.md](SECURITY.md), never a public issue.
