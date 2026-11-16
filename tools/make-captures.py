#!/usr/bin/env python3
"""Write the notional sample messages under stores/*/evidence/captures/.

Every system in this repository is notional, so no message here was captured
from real equipment. The binary samples are encoded by the goat-transformers
Python engine from notional values; the text samples are written below as
text. Each owner's samples sit in that owner's store, so a store copied on its
own keeps its evidence.

Run from anywhere: tools/make-captures.py [--check]
--check writes nothing and exits 1 when a file on disk differs.
"""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "lib"))
import hello  # noqa: E402

hello.use_engine()
from goat_transformers import Engine  # noqa: E402
from goat_transformers.entity import Entity  # noqa: E402

PACKS = os.path.join(hello.GT, "packs")
FORMATS = ["asterix-cat048", "asterix-cat062", "asterix-cat021", "sapient", "remote-id",
           "mavlink2", "nmea2000"]
eng = Engine.from_dir(PACKS, None, "controlled", packs_only=FORMATS)


def from_vector(fmt, vector, **changes):
    """Decode a pack's own test vector, change the notional values, encode."""
    with open(os.path.join(PACKS, fmt, "vectors", vector + ".json"), encoding="utf-8") as f:
        v = json.load(f)
    ent = eng.decode(fmt, v["input"].encode())
    for k, val in changes.items():
        ent.fields[k.replace("__", ".")] = val
    ent.residue = {}
    return eng.encode(fmt, ent).decode() + "\n"


def fresh(fmt, kind, **fields):
    ent = Entity(fields={k.replace("__", "."): v for k, v in fields.items()}, kind=(fmt, kind))
    return eng.encode(fmt, ent).decode() + "\n"


def cat062(sac, sic, tn, tod, lat, lon, hae, ve, vn):
    return from_vector("asterix-cat062", "01-open-billie-sample-roundtrip",
                       cat062__sac=sac, cat062__sic=sic, cat062__track_number=tn, cat062__time_of_day_s=tod,
                       lat=lat, lon=lon, hae=hae, track__vel_east_ms=ve, track__vel_north_ms=vn)


def ctv2(track, source, gen, when, lat, lon, alt, cls, conf):
    return json.dumps({
        "apiVersion": "billie.dev/track-v2", "kind": "Track", "trackId": track, "sourceId": source,
        "trackGeneration": gen, "testData": False, "headerSimulated": False, "simulated": False,
        "confirmed": True, "coasting": False, "finalUpdate": False, "observedAt": when,
        "position": {"latitudeDeg": lat, "longitudeDeg": lon, "altitudeM": alt},
        "velocity": {"eastMps": -6.5, "northMps": 11.25, "upMps": 0.0},
        "classification": cls, "confidence": conf,
        "positionUncertainty": {"sigmaEastM": 20, "sigmaNorthM": 20, "sigmaUpM": 35},
    }, separators=(",", ":")) + "\n"


def cot(uid, typ, when, stale, lat, lon, hae, callsign, course, speed):
    return ('<?xml version="1.0"?><event version="2.0" uid="%s" type="%s" time="%s" start="%s" stale="%s" '
            'how="m-g"><point lat="%s" lon="%s" hae="%s" ce="25.0" le="40.0"/><detail><contact callsign="%s"/>'
            '<track course="%s" speed="%s"/></detail></event>\n'
            % (uid, typ, when, when, stale, lat, lon, hae, callsign, course, speed))


def geojson(fid, lat, lon, typ, when_ms, callsign):
    return json.dumps({"type": "Feature", "geometry": {"type": "Point", "coordinates": [lon, lat]},
                       "properties": {"type": typ, "time_ms": when_ms, "callsign": callsign}, "id": fid},
                      separators=(",", ":")) + "\n"


CAPTURES = {
    # Tessaline Instruments: factory acceptance of the TR-40, bench runs of the EO-7 and RF-9
    "stores/tessaline/evidence/captures/tr40-plot-0311.hex": lambda: from_vector(
        "asterix-cat048", "07-sample-plot", cat048__i010_sac=61, cat048__i010_sic=12,
        cat048__i040_rho=8.25, cat048__i040_theta=131.5, cat048__i070_mode3a=1234),
    "stores/tessaline/evidence/captures/tr40-track-0311.hex": lambda: cat062(
        61, 12, 1047, 51234.5, 44.6121, -30.2874, 450.0, -6.5, 11.25),
    "stores/tessaline/evidence/captures/eo7-detection-0412.hex": lambda: fresh(
        "sapient", "detection_report", lat=44.6188, lon=-30.2712, hae=95.0,
        sapient__location_coordinate_system=1, sapient__location_datum=1),
    "stores/tessaline/evidence/captures/rf9-location-0419.hex": lambda: from_vector(
        "remote-id", "02-location-roundtrip", lat=44.6302, lon=-30.2655, hae=140.0, rid__height=120.0),
    # Velmora: ridge camp sensor node, exercise captures, the fabric at depot lake
    "stores/velmora/evidence/captures/ax26-track-0927.hex": lambda: cat062(
        61, 12, 2210, 47011.25, 44.5987, -30.3302, 610.0, 14.0, -3.5),
    "stores/velmora/evidence/captures/ax26-plot-0927.hex": lambda: from_vector(
        "asterix-cat048", "07-sample-plot", cat048__i010_sac=61, cat048__i010_sic=12,
        cat048__i040_rho=14.0, cat048__i040_theta=287.25, cat048__i070_mode3a=0),
    "stores/velmora/evidence/captures/n1-eo7-input-0412.json": lambda: json.dumps({
        "msg": "det", "cam": "EO7-0193", "seq": 88213, "utc": "2026-04-12T09:14:07.250Z",
        "az_deg": 41.7, "el_deg": 3.2, "range_m": 1840, "lat": 44.6188, "lon": -30.2712, "alt_m": 95.0,
        "cls": "uas", "conf": 0.81}, separators=(",", ":")) + "\n",
    "stores/velmora/evidence/captures/n1-eo7-track-0412.json": lambda: ctv2(
        "n1-eo7-0042", "velmora-n1-eo7", "gen-3", "2026-04-12T09:14:07.250Z",
        44.6188, -30.2712, 95.0, "uas", 0.81),
    "stores/velmora/evidence/captures/ax26-cot-0927.xml": lambda: cot(
        "VEL-N1-0042", "a-u-A-M-F-Q", "2026-09-27T13:03:31.000Z", "2026-09-27T13:05:31.000Z",
        "44.6188", "-30.2712", "95.0", "N1-0042", "302.5", "12.9"),
    "stores/velmora/evidence/captures/gcs-position-0605.hex": lambda: from_vector(
        "mavlink2", "rt-00033-global_position_int", lat=44.5531, lon=-30.4127,
        mavlink__alt_mm=212000, mavlink__relative_alt_mm=120000, mavlink__sysid=7, mavlink__compid=1),
    "stores/velmora/evidence/captures/adsb-ground-0605.hex": lambda: from_vector(
        "asterix-cat021", "01-every-mapped-item-roundtrip", cat021__i010_sac=61, cat021__i010_sic=40,
        lat=44.7012, lon=-30.1179, cat021__i131_lat=44.7012, cat021__i131_lon=-30.1179),
    # Kastreni: harbor east edge capture, the decoder bench, the patrol boat
    "stores/kastreni/evidence/captures/edge-cat048-0802.hex": lambda: from_vector(
        "asterix-cat048", "07-sample-plot", cat048__i010_sac=72, cat048__i010_sic=3,
        cat048__i040_rho=21.5, cat048__i040_theta=12.75, cat048__i070_mode3a=4021),
    "stores/kastreni/evidence/captures/edge-cat062-0802.hex": lambda: cat062(
        72, 9, 388, 30402.0, 44.4415, -30.0861, 1520.0, 120.5, 33.0),
    "stores/kastreni/evidence/captures/bd-lr5-0907.hex": lambda: "4b52050300a1c4f2000f6c3a1b8e2f40c3ff\n",
    "stores/kastreni/evidence/captures/bd-lr5-decoded-0907.geojson": lambda: geojson(
        "KR-LR5-0161", 44.4402, -30.0915, "a-u-A", 1789389720000, "LR5-0161"),
    "stores/kastreni/evidence/captures/fc-0814.hex": lambda: "46430102000000a10b2c0e7f00\n",
    "stores/kastreni/evidence/captures/td-nvg-0814.xml": lambda:
        '<nvg><point x="-30.0861" y="44.4415" label="HE-PATROL-2" symbol="app6a:SFSPXR----D"/></nvg>\n',
    "stores/kastreni/evidence/captures/td-cot-0814.xml": lambda: cot(
        "KAS-HE-0388", "a-u-A", "2026-08-14T08:26:42.000Z", "2026-08-14T08:28:42.000Z",
        "44.4415", "-30.0861", "1520.0", "HE-0388", "74.7", "124.9"),
    "stores/kastreni/evidence/captures/boat-position-0730.hex": lambda: from_vector(
        "nmea2000", "x01-pgn129025-to-geojson", lat=44.4318, lon=-30.0544),
}


def main():
    check = "--check" in sys.argv[1:]
    differ = 0
    for rel, make in sorted(CAPTURES.items()):
        path = os.path.join(hello.ROOT, rel)
        text = make()
        old = open(path, encoding="utf-8").read() if os.path.exists(path) else None
        if old == text:
            continue
        differ += 1
        if check:
            print("differs: %s" % rel)
            continue
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)
        print("wrote %s" % rel)
    print("%d sample(s), %d %s" % (len(CAPTURES), differ, "differ" if check else "written"))
    return 1 if check and differ else 0


if __name__ == "__main__":
    sys.exit(main())
