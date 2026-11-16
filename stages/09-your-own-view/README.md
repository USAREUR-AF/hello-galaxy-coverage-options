# Stage 9 — your own view

**`goat-options` prints JSON. What a reader draws from it is the reader's
choice. [`consumer/site-grid.py`](../../consumer/site-grid.py), 32 lines of
standard-library Python, reads one site's answer and draws a grid of sources
by consumers, each cell counting the paths on hand by status.**

```bash
bin/hello-options 9
# or, by hand:
python3 -I .cache/goat-transformers/tools/goat-options site \
    --store stores/tessaline --store stores/velmora --store stores/kastreni \
    sites/harbor-east.site | consumer/site-grid.py
```

The grid is one view among many. A map, a matrix of formats, a list of what
is missing at a site, or a feed into another planning tool read the same
JSON.

## What you should see

Run against goat-transformers at commit `8845949`.

The files the stage prints first are left out here; they are in the repository.

```text
== Stage 9: your own view ==
goat-options prints JSON. What to draw from it, and how, is the reader's choice; this is one small example.

[1] The program: consumer/site-grid.py

[2] Site ridge-camp, drawn by the program
    $ goat-options site --store stores/tessaline --store stores/velmora --store stores/kastreni sites/ridge-camp.site --keys count
    $ goat-options site ... sites/ridge-camp.site | consumer/site-grid.py
    | site ridge-camp
    |                            map-display       c2-air            jx-2
    | tessaline/eo-7             9A                .                 .
    | tessaline/jx-2             3A                .                 .
    | tessaline/rf-9             6A                .                 2A 2F
    | tessaline/tr-40            12A 6F 3U         1P 5A 4F 2U       .
    | velmora/c2-air             3A                .                 .
    | velmora/node-decoder-eo7   1P 2A             .                 .
    | velmora/node-decoder-rf9   3A                .                 .
    | velmora/node-decoder-tr40  3A                .                 .
    | velmora/node-translator    1P 5A             .                 .

[3] Site harbor-east, drawn by the program
    $ goat-options site --store stores/tessaline --store stores/velmora --store stores/kastreni sites/harbor-east.site --keys count
    $ goat-options site ... sites/harbor-east.site | consumer/site-grid.py
    | site harbor-east
    |                           tactical-display  fabric-picture    edge-capture
    | kastreni/binary-decoder   1A                .                 .
    | kastreni/coastal-ais      .                 .                 .
    | kastreni/edge-capture     2A                .                 .
    | kastreni/lr-5             1A                1P 1A 1U          .
    | kastreni/patrol-boat-nav  .                 .                 .
    | tessaline/ha-3            .                 .                 .
    | velmora/harbor-ais        .                 .                 .

[4] Site depot-lake, drawn by the program
    $ goat-options site --store stores/tessaline --store stores/velmora --store stores/kastreni sites/depot-lake.site --keys count
    $ goat-options site ... sites/depot-lake.site | consumer/site-grid.py
    | site depot-lake
    |                        fabric-tracks     air-c2            map-display
    | velmora/adsb-ground    2A                3A                .
    | velmora/fabric-alerts  .                 .                 .
    | velmora/fabric-bridge  4A                6A                .
    | velmora/map-display    2A                3A                .
    | velmora/uas-gcs        4A                6A                6A
    | velmora/fabric-tracks  .                 3A                .

[5] Verify
    PASS  the program is 32 lines, between 20 and 40
    PASS  it imports json and sys only
    PASS  it ran on every site with exit 0
    PASS  harbor east: the LR-5 row shows 1 proven, 1 available and 1 unknown path on hand to the picture
    PASS  harbor east: the AIS receiver has no path on hand
    PASS  ridge camp: the RF-9 row shows its 4 paths to the JX-2

stage complete: every check held
```
