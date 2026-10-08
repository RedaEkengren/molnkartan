"""Gör om SCB:s kommun- och länsgränser till förenklade SVG-vägar: docs/karta.json.

Källa: SCB, Digitala gränser (shape_svenska_260225.zip), licens CC0.
https://scb.se/hitta-statistik/regional-statistik-och-kartor/regionala-indelningar/digitala-granser/

python3 karta_bygg.py <mapp med Kommun_Sweref99TM.shp/.dbf och Lan_Sweref99TM_region.shp/.dbf>

Koordinaterna är SWEREF 99 TM (meter, plant), så ingen projektion behövs.
Shapefilerna läses utan bibliotek: bara polygoner (typ 5) och DBF med teckenfält.
"""

import json
import struct
import sys
from pathlib import Path

ROT = Path(__file__).parent
BREDD = 400          # SVG-enheter; höjden följer Sveriges proportioner
TOLERANS_M = 900     # Douglas–Peucker i meter: lagom för en temakarta i webbläsarstorlek


def las_dbf(fil):
    b = fil.read_bytes()
    antal, huvud, radlangd = struct.unpack("<IHH", b[4:12])
    falt, i = [], 32
    while b[i] != 0x0D:
        falt.append((b[i:i + 11].split(b"\0")[0].decode(), b[i + 16]))
        i += 32
    rader = []
    for n in range(antal):
        post, o, rad = b[huvud + n * radlangd + 1:huvud + (n + 1) * radlangd], 0, {}
        for namn, langd in falt:
            rad[namn] = post[o:o + langd].decode("latin-1").strip()
            o += langd
        rader.append(rad)
    return rader


def las_shp(fil):
    b, pos, former = fil.read_bytes(), 100, []
    while pos < len(b):
        _, langd = struct.unpack(">ii", b[pos:pos + 8])
        innehall = b[pos + 8:pos + 8 + langd * 2]
        pos += 8 + langd * 2
        typ = struct.unpack("<i", innehall[:4])[0]
        if typ != 5:
            raise ValueError(f"bara polygoner stöds, fick typ {typ}")
        delar, punkter = struct.unpack("<ii", innehall[36:44])
        start = list(struct.unpack(f"<{delar}i", innehall[44:44 + 4 * delar])) + [punkter]
        xy = struct.unpack(f"<{2 * punkter}d", innehall[44 + 4 * delar:44 + 4 * delar + 16 * punkter])
        pts = list(zip(xy[::2], xy[1::2]))
        former.append([pts[start[i]:start[i + 1]] for i in range(delar)])
    return former


def forenkla(pts, tol):
    """Douglas–Peucker, iterativ."""
    if len(pts) < 4:
        return pts
    behall = [False] * len(pts)
    behall[0] = behall[-1] = True
    stack = [(0, len(pts) - 1)]
    while stack:
        a, b = stack.pop()
        (x1, y1), (x2, y2) = pts[a], pts[b]
        dx, dy = x2 - x1, y2 - y1
        langd = (dx * dx + dy * dy) ** 0.5
        storst, idx = 0, None
        for i in range(a + 1, b):
            if langd == 0:  # sluten ring: första och sista punkten är samma, mät avståndet till den
                d = ((pts[i][0] - x1) ** 2 + (pts[i][1] - y1) ** 2) ** 0.5
            else:
                d = abs(dy * pts[i][0] - dx * pts[i][1] + x2 * y1 - y2 * x1) / langd
            if d > storst:
                storst, idx = d, i
        if idx is not None and storst > tol:
            behall[idx] = True
            stack += [(a, idx), (idx, b)]
    return [p for p, k in zip(pts, behall) if k]


def main():
    mapp = Path(sys.argv[1])
    kommuner = list(zip(las_dbf(next(mapp.rglob("Kommun_Sweref99TM.dbf"))), las_shp(next(mapp.rglob("Kommun_Sweref99TM.shp")))))
    lan = list(zip(las_dbf(next(mapp.rglob("Lan_Sweref99TM_region.dbf"))), las_shp(next(mapp.rglob("Lan_Sweref99TM_region.shp")))))
    alla = [p for _, form in kommuner for ring in form for p in ring]
    minx, maxx = min(x for x, _ in alla), max(x for x, _ in alla)
    miny, maxy = min(y for _, y in alla), max(y for _, y in alla)
    skala = BREDD / (maxx - minx)
    hojd = round((maxy - miny) * skala, 1)

    def vag(form, minsta_ring_m2=0):
        delar = []
        for ring in form:
            # Små öar under gränsen tas bort; de syns ändå inte i den här storleken.
            yta = abs(sum(x1 * y2 - x2 * y1 for (x1, y1), (x2, y2) in zip(ring, ring[1:] + ring[:1]))) / 2
            if yta < minsta_ring_m2:
                continue
            f = forenkla(ring, TOLERANS_M)
            if len(f) < 4:
                continue
            delar.append("M" + "L".join(f"{(x - minx) * skala:.1f},{(maxy - y) * skala:.1f}" for x, y in f[:-1]) + "Z")
        return "".join(delar)

    ut = {
        "kalla": "SCB, Digitala gränser (shape_svenska_260225), CC0",
        "viewBox": f"0 0 {BREDD} {hojd}",
        "kommuner": {r["KnKod"]: {"namn": r["KnNamn"], "d": vag(f, 4e6)} for r, f in kommuner},
        "lan": {r["LnKod"]: {"namn": r["LnNamn"], "d": vag(f, 4e6)} for r, f in lan},
    }
    fil = ROT / "docs" / "karta.json"
    fil.write_text(json.dumps(ut, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")
    tomma = [k for k, v in ut["kommuner"].items() if not v["d"]]
    print(f"{fil.relative_to(ROT)}: {len(ut['kommuner'])} kommuner, {len(ut['lan'])} län, "
          f"{fil.stat().st_size // 1024} kB, viewBox {ut['viewBox']}, utan form: {tomma}")


if __name__ == "__main__":
    main()
