#!/usr/bin/env python3
"""Stage 5: a site's options. Three sites, each with its own systems on hand and its own consumers to feed."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "lib"))
import hello as h  # noqa: E402

h.title("Stage 5: a site's options",
        "A site file lists what is on hand and what the site wants to feed. Each path is marked on hand or not.")

results = {}
for site in ("ridge-camp", "harbor-east", "depot-lake"):
    h.step("Site %s" % site)
    h.show(open(os.path.join(h.ROOT, "sites", site + ".site"), encoding="utf-8").read(), limit=40)
    code, r = h.options("site", *h.stores(), "sites/%s.site" % site, "--keys", "count")
    results[site] = (code, r)
    h.say("%-28s %-26s %6s %8s" % ("feed", "from", "paths", "on hand"))
    for it in r["intents"]:
        h.say("%-28s %-26s %6d %8d" % (it["consumer"], it["source"], it["counts"]["paths"], it["paths_on_hand"]))
    for p in r["problems"]:
        if p["level"] != "info":
            h.say("%s: %s: %s" % (p["level"], p["where"], p["text"]))


def intent(site, consumer, source):
    return [i for i in results[site][1]["intents"] if i["consumer"] == consumer and i["source"] == source][0]


h.step("Verify")
h.check("all three site queries exit 0", all(c == 0 for c, _ in results.values()))
he = results["harbor-east"][1]
lib_paths = [p for i in he["intents"] for p in i["paths"] if any(s["via"] == "goat-transformers" for s in p["steps"])]
h.check("harbor east does not have the library: no path that uses it is on hand there",
        lib_paths and all(s["on_hand"] is False for p in lib_paths for s in p["steps"] if s["via"] == "goat-transformers"))
lr5 = intent("harbor-east", "kastreni/fabric-picture", "kastreni/lr-5")
on = [h.route(p) for p in lr5["paths"] if all(x is not False for x in
      [p["from"].get("on_hand"), p["to"].get("on_hand")] + [s.get("on_hand") for s in p["steps"]])]
h.check("at harbor east the LR-5 reaches the common picture on hand through the binary decoder only",
        on == ["asterix-cat062", "kastreni lr-5 binary --[kastreni/binary-decoder]--> cot-xml",
               "kastreni lr-5 binary --[kastreni/binary-decoder]--> geojson"])
h.check("harbor east: the AIS receiver writes `NMEA 0183 AIS`, the gateway reads `nmea0183-ais`: no path",
        intent("harbor-east", "kastreni/edge-capture", "velmora/harbor-ais")["counts"]["paths"] == 0)
rc = intent("ridge-camp", "tessaline/jx-2", "tessaline/rf-9")
h.check("ridge camp: every path from the RF-9 to the JX-2 is on hand",
        rc["counts"]["paths"] == 4 and rc["paths_on_hand"] == 4)
h.check("depot lake: velmora/weather-mast is on hand and has no record, and the site is told",
        any(p["where"] == "velmora/weather-mast" for p in results["depot-lake"][1]["problems"]))
h.check("depot lake: three feed lines become %d source and consumer pairs" % len(results["depot-lake"][1]["intents"]),
        len(results["depot-lake"][1]["intents"]) == 12)
h.done()
