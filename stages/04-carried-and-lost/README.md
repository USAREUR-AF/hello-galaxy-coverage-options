# Stage 4 — what carries and what is lost

**For a conversion the library makes, `goat-options` gives the keys that
carry and the keys that are lost, from the library's capability report, and
the keys the target requires that the source does not supply (`needs`). This
stage puts the report beside two conversions that were run.**

The capability report is per format: the keys both packs map. A run is per
message. The two can differ, and this stage shows two ways:

- A Category 048 plot is a range and a bearing from the radar. It has no
  latitude or longitude, so a conversion to Cursor-on-Target XML runs without
  an error and gives an event with no position. Cursor-on-Target XML has no
  `requires` line, so nothing refuses it.
- A Category 062 track converted to GeoJSON also gets `course` and
  `speed_ms`, which the library derives from the velocity. The report counts
  the velocity as lost and does not count the derived keys.

```bash
bin/hello-options 4
```

**This stage needs goat-transformers with the branch `fix/options-proving`
merged**: `needs` is part of that change. Against the pinned commit the two
checks on `needs` fail and the stage says why. See the README's
[What is pinned](../../README.md#what-is-pinned).

## What you should see

Run against goat-transformers with `fix/options-proving` merged.

```text
== Stage 4: what carries and what is lost ==
A library step carries the keys both packs map. The report is per format; a run is per message.

[1] Three library steps from the TR-40 to the depot lake track picture
    $ goat-options paths --store stores/tessaline --store stores/velmora --store stores/kastreni --from tessaline/tr-40 --to velmora/fabric-tracks
    asterix-cat048 -> cot-protobuf  grade partial
        carried: speed_ms
        lost:    143 keys, for example cat048.i010_sac, cat048.i010_sic, cat048.i140, cat048.i020_typ
        needs:   [{"kind": "cot_event", "missing": ["lat", "lon"]}, {"kind": "tak_control", "missing": ["takproto.tak_control_min_proto_version"]}]
    asterix-cat062 -> cot-protobuf  grade partial
        carried: lat, lon, hae
        lost:    15 keys, for example cat062.sac, cat062.sic, cat062.time_of_day_s, track.vel_east_ms
        needs:   nothing beyond what the source maps
    asterix-cat062 -> canonical-track-v2  grade partial
        carried: lat, lon, track.vel_east_ms, track.vel_north_ms, track.confirmed, track.simulated, track.final_update, track.coasting, hae
        lost:    9 keys, for example cat062.sac, cat062.sic, cat062.time_of_day_s, cat062.track_number
        needs:   [{"kind": "Track", "missing": ["uid", "track.source_id", "track.generation", "time_ms"]}]

[2] Run one: the TR-40's plot (Category 048) to Cursor-on-Target XML
    | <event version="2.0" type="a-u-X"><point hae="9999999" ce="9999999" le="9999999"/></event>
    A plot is a range and a bearing from the radar. With no position in the model, the event has none.

[3] Run two: a Category 062 track to GeoJSON, against the report
    report carried:  lat, lon, hae
    the run wrote:   course, hae, lat, lon, speed_ms
    written and not in the report: course, speed_ms (derived from the velocity the report counts as lost)

[4] Verify
    PASS  Category 048 to CoT Protobuf: the report carries one key, speed_ms
    PASS  the plot converts to cot-xml without an error
    PASS  and the event it gives has no latitude or longitude
    PASS  goat-options lists what Canonical Track v2 needs that Category 062 does not map
    PASS  CoT Protobuf from Category 048 needs lat and lon for its event kind
    PASS  the run of Category 062 to GeoJSON wrote course and speed_ms, which the report does not count

stage complete: every check held
```
