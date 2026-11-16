#!/usr/bin/env python3
"""Stage 4: what carries and what is lost, as the library reports it and as a run measures it."""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "lib"))
import hello as h  # noqa: E402

h.use_engine()
from goat_transformers import Engine  # noqa: E402

h.title("Stage 4: what carries and what is lost",
        "A library step carries the keys both packs map. The report is per format; a run is per message.")

h.step("Three library steps from the TR-40 to the depot lake track picture")
code, r = h.options("paths", *h.stores(), "--from", "tessaline/tr-40", "--to", "velmora/fabric-tracks")
steps = {}
for p in r["paths"]:
    for s in p["steps"]:
        steps.setdefault((s["from"], s["to"]), s)
for key in [("asterix-cat048", "cot-protobuf"), ("asterix-cat062", "cot-protobuf"), ("asterix-cat062", "canonical-track-v2")]:
    s = steps[key]
    h.say("%s -> %s  grade %s" % (key[0], key[1], s["grade"]))
    h.say("    carried: %s" % ", ".join(s["carried"]))
    h.say("    lost:    %d keys, for example %s" % (len(s["lost"]), ", ".join(s["lost"][:4])))
    h.say("    needs:   %s" % (json.dumps(s.get("needs")) if s.get("needs") else "nothing beyond what the source maps"))

if not any("needs" in s for s in steps.values()):
    h.say("This goat-transformers gives no `needs` on a library step: the two checks on it below need")
    h.say("goat-transformers with fix/options-proving merged (see README, What is pinned).")

h.step("Run one: the TR-40's plot (Category 048) to Cursor-on-Target XML")
eng = Engine.from_dir(os.path.join(h.GT, "packs"), None, "controlled",
                      packs_only=["asterix-cat048", "asterix-cat062", "cot-xml", "geojson"])
plot = open(os.path.join(h.ROOT, "stores/tessaline/evidence/captures/tr40-plot-0311.hex"), "rb").read().strip()
event = eng.convert("asterix-cat048", "cot-xml", plot).decode()
h.show(event)
h.say("A plot is a range and a bearing from the radar. With no position in the model, the event has none.")

h.step("Run two: a Category 062 track to GeoJSON, against the report")
run = json.load(open(os.path.join(h.ROOT, "stores/kastreni/evidence/runs/fabric-picture-geojson.json")))
extra = sorted(set(run["keys_out"]) - set(run["capability"]["carried"]))
h.say("report carried:  %s" % ", ".join(run["capability"]["carried"]))
h.say("the run wrote:   %s" % ", ".join(run["keys_out"]))
h.say("written and not in the report: %s (derived from the velocity the report counts as lost)" % ", ".join(extra))

h.step("Verify")
c48 = steps[("asterix-cat048", "cot-protobuf")]
h.check("Category 048 to CoT Protobuf: the report carries one key, speed_ms", c48["carried"] == ["speed_ms"])
h.check("the plot converts to cot-xml without an error", event.startswith("<event"))
h.check("and the event it gives has no latitude or longitude", "lat=" not in event and "lon=" not in event)
h.check("goat-options lists what Canonical Track v2 needs that Category 062 does not map",
        steps[("asterix-cat062", "canonical-track-v2")].get("needs") ==
        [{"kind": "Track", "missing": ["uid", "track.source_id", "track.generation", "time_ms"]}])
h.check("CoT Protobuf from Category 048 needs lat and lon for its event kind",
        any(n["kind"] == "cot_event" and n["missing"] == ["lat", "lon"] for n in (c48.get("needs") or [])))
h.check("the run of Category 062 to GeoJSON wrote course and speed_ms, which the report does not count",
        extra == ["course", "speed_ms"])
h.done()
