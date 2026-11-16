# Stage 5 — a site's options

**A site file lists the systems on hand at one site and the consumers it wants
to feed. `goat-options site` answers every `feed` line and marks each path on
hand or not. Three notional sites have different systems on hand, and one of
them does not have the library.**

| Site | Owner | Shape | The library |
|---|---|---|---|
| [`ridge-camp`](../../sites/ridge-camp.site) | Velmora | a sensor node: one decoder per sensor, then a translator | on hand |
| [`harbor-east`](../../sites/harbor-east.site) | Kastreni | an edge gateway that captures every feed, and a dictionary-driven binary decoder | not on hand |
| [`depot-lake`](../../sites/depot-lake.site) | Velmora | applications on a Zenoh data fabric, and a Kastreni liaison cell | on hand |

A `feed` line without `from=` asks for every system on hand that emits
anything. A path is on hand when its source, its consumer and every converter
it uses are listed as `have`; `have goat-transformers` says the library is
deployed.

```bash
bin/hello-options 5
```

At harbor east no path that uses the library is on hand. The AIS receiver
Velmora lent the site reaches nothing: its record writes `NMEA 0183 AIS`, and
the gateway's record writes `nmea0183-ais`. The tool matches format names
exactly (case and spacing aside); it has no aliases.

## What you should see

Run against goat-transformers with `fix/options-proving` merged.

The files the stage prints first are left out here; they are in the repository.

```text
== Stage 5: a site's options ==
A site file lists what is on hand and what the site wants to feed. Each path is marked on hand or not.

[1] Site ridge-camp
    $ goat-options site --store stores/tessaline --store stores/velmora --store stores/kastreni sites/ridge-camp.site --keys count
    feed                         from                        paths  on hand
    velmora/map-display          tessaline/eo-7                  9        9
    velmora/map-display          tessaline/jx-2                  3        3
    velmora/map-display          tessaline/rf-9                  6        6
    velmora/map-display          tessaline/tr-40                21       21
    velmora/map-display          velmora/c2-air                  3        3
    velmora/map-display          velmora/node-decoder-eo7        3        3
    velmora/map-display          velmora/node-decoder-rf9        3        3
    velmora/map-display          velmora/node-decoder-tr40       3        3
    velmora/map-display          velmora/node-translator         6        6
    velmora/c2-air               tessaline/tr-40                12       12
    tessaline/jx-2               tessaline/rf-9                  4        4

[2] Site harbor-east
    $ goat-options site --store stores/tessaline --store stores/velmora --store stores/kastreni sites/harbor-east.site --keys count
    feed                         from                        paths  on hand
    kastreni/tactical-display    kastreni/binary-decoder         4        1
    kastreni/tactical-display    kastreni/coastal-ais            2        0
    kastreni/tactical-display    kastreni/edge-capture          11        2
    kastreni/tactical-display    kastreni/lr-5                   6        1
    kastreni/tactical-display    kastreni/patrol-boat-nav        2        0
    kastreni/tactical-display    tessaline/ha-3                  4        0
    kastreni/tactical-display    velmora/harbor-ais              0        0
    kastreni/fabric-picture      kastreni/lr-5                   9        3
    kastreni/edge-capture        velmora/harbor-ais              0        0

[3] Site depot-lake
    $ goat-options site --store stores/tessaline --store stores/velmora --store stores/kastreni sites/depot-lake.site --keys count
    feed                         from                        paths  on hand
    velmora/fabric-tracks        velmora/adsb-ground             2        2
    velmora/fabric-tracks        velmora/fabric-alerts           0        0
    velmora/fabric-tracks        velmora/fabric-bridge           4        4
    velmora/fabric-tracks        velmora/map-display             2        2
    velmora/fabric-tracks        velmora/uas-gcs                 4        4
    kastreni/air-c2              velmora/adsb-ground             3        3
    kastreni/air-c2              velmora/fabric-alerts           0        0
    kastreni/air-c2              velmora/fabric-bridge           6        6
    kastreni/air-c2              velmora/fabric-tracks           3        3
    kastreni/air-c2              velmora/map-display             3        3
    kastreni/air-c2              velmora/uas-gcs                 6        6
    velmora/map-display          velmora/uas-gcs                 6        6
    warning: velmora/weather-mast: on hand at the site and in no record

[4] Verify
    PASS  all three site queries exit 0
    PASS  harbor east does not have the library: no path that uses it is on hand there
    PASS  at harbor east the LR-5 reaches the common picture on hand through the binary decoder only
    PASS  harbor east: the AIS receiver writes `NMEA 0183 AIS`, the gateway reads `nmea0183-ais`: no path
    PASS  ridge camp: every path from the RF-9 to the JX-2 is on hand
    PASS  depot lake: velmora/weather-mast is on hand and has no record, and the site is told
    PASS  depot lake: three feed lines become 12 source and consumer pairs

stage complete: every check held
```
