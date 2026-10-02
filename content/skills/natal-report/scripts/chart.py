#!/usr/bin/env python3
"""
chart.py — natal chart + numerology engine for the natal-report skill.

    python3 chart.py birth.json                    # writes chart.json beside it, prints the summary
    python3 chart.py birth.json -o out/chart.json
    python3 chart.py --example                     # prints a birth.json skeleton to fill in

Input  : birth.json — REPORT-SPEC.md §2. Only `name` and `date` are required; without
         `time` + `utc_offset` + `lat`/`lon` there are no angles, no houses, no sect.
Output : chart.json (schema natal-report/chart.v1 — REPORT-SPEC.md §3), the single
         machine-readable source that build.py, wheel.js and check-report.py all read.
         Plus a human summary on stdout: the writer's working notes.

Conventions: tropical zodiac, whole-sign houses (Placidus cusps reported only where
they disagree). Numerology: Pythagorean on the full birth name, Y as a consonant,
Life Path by the reduce-each-component method (all-digit method reported alongside).

Requires `pip3 install pyswisseph`. Chiron additionally needs ephe/seas_18.se1:
  curl -sL -o ephe/seas_18.se1 https://raw.githubusercontent.com/aloistr/swisseph/master/ephe/seas_18.se1
Looks for an `ephe/` directory next to this script, then in the working directory.
"""
import argparse
import datetime as dt
import json
import math
import os
import sys
import unicodedata
from collections import Counter

try:
    import swisseph as swe
except ImportError:  # pragma: no cover
    sys.exit("chart.py: pyswisseph is not installed — run: pip3 install pyswisseph")

SCHEMA = "natal-report/chart.v1"
HERE = os.path.dirname(os.path.abspath(__file__))

SIGNS = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio",
         "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
SIGN_GLYPH = dict(zip(SIGNS, "♈♉♊♋♌♍♎♏♐♑♒♓"))
RULER = dict(zip(SIGNS, ["Mars", "Venus", "Mercury", "Moon", "Sun", "Mercury", "Venus", "Pluto",
                         "Jupiter", "Saturn", "Uranus", "Neptune"]))
ELEM = {s: e for s, e in zip(SIGNS, ["Fire", "Earth", "Air", "Water"] * 3)}
MODE = {s: m for s, m in zip(SIGNS, ["Cardinal", "Fixed", "Mutable"] * 4)}
ORDINAL = ["First", "Second", "Third", "Fourth", "Fifth", "Sixth", "Seventh", "Eighth",
           "Ninth", "Tenth", "Eleventh", "Twelfth"]

BODIES = [("Sun", swe.SUN, "☉"), ("Moon", swe.MOON, "☽"), ("Mercury", swe.MERCURY, "☿"),
          ("Venus", swe.VENUS, "♀"), ("Mars", swe.MARS, "♂"), ("Jupiter", swe.JUPITER, "♃"),
          ("Saturn", swe.SATURN, "♄"), ("Uranus", swe.URANUS, "♅"), ("Neptune", swe.NEPTUNE, "♆"),
          ("Pluto", swe.PLUTO, "♇"), ("Chiron", swe.CHIRON, "⚷"), ("True Node", swe.TRUE_NODE, "☊"),
          ("Lilith", swe.MEAN_APOG, "⚸")]
GLYPH = {n: g for n, _, g in BODIES}
GLYPH.update({"Ascendant": "AC", "Midheaven": "MC"})
WHEEL_BODIES = [n for n, _, _ in BODIES if n != "Lilith"]       # Lilith is read, not drawn
WHEEL_ASPECT_BODIES = [n for n in WHEEL_BODIES if n != "True Node"]
PERSONAL = {"Sun", "Moon", "Mercury", "Venus", "Mars"}           # drawn heavier on the wheel

# (name, exact angle, wheel kind) — quincunx is reported but never drawn
ASPECTS = [("conjunct", 0, "cnj"), ("sextile", 60, "soft"), ("square", 90, "hard"),
           ("trine", 120, "soft"), ("opposite", 180, "hard"), ("quincunx", 150, None)]
WHEEL_ORB = {"cnj": 6.0, "hard": 5.0, "soft": 4.0}

VEDIC_PLANET = {1: "Sun", 2: "Moon", 3: "Jupiter", 4: "Rahu", 5: "Mercury",
                6: "Venus", 7: "Ketu", 8: "Saturn", 9: "Mars"}
# Golden Dawn attribution of the 22 paths: (letter, card, attribution). Index = total mod 22, 0 → Tav.
KABBALAH = {
    1: ("Aleph", "The Fool", "Air"), 2: ("Beth", "The Magician", "Mercury"),
    3: ("Gimel", "The High Priestess", "Moon"), 4: ("Daleth", "The Empress", "Venus"),
    5: ("Heh", "The Emperor", "Aries"), 6: ("Vav", "The Hierophant", "Taurus"),
    7: ("Zayin", "The Lovers", "Gemini"), 8: ("Chet", "The Chariot", "Cancer"),
    9: ("Tet", "Strength", "Leo"), 10: ("Yod", "The Hermit", "Virgo"),
    11: ("Kaph", "The Wheel of Fortune", "Jupiter"), 12: ("Lamed", "Justice", "Libra"),
    13: ("Mem", "The Hanged Man", "Water"), 14: ("Nun", "Death", "Scorpio"),
    15: ("Samekh", "Temperance", "Sagittarius"), 16: ("Ayin", "The Devil", "Capricorn"),
    17: ("Peh", "The Tower", "Mars"), 18: ("Tzaddi", "The Star", "Aquarius"),
    19: ("Qoph", "The Moon", "Pisces"), 20: ("Resh", "The Sun", "Sun"),
    21: ("Shin", "Judgement", "Fire"), 0: ("Tav", "The World", "Saturn"),
}

EXAMPLE = {
    "_comment": "Fill in and save as birth.json. name = full name AS ON THE BIRTH CERTIFICATE. "
                "time is 24h local clock time; utc_offset must reflect DST for that date, place "
                "and year. Leave time null if unknown — do not guess one.",
    "name": "Full Birth Name",
    "date": "1990-06-15",
    "time": "09:42",
    "utc_offset": -7,
    "tz_label": "PDT",
    "place": "Portland, Oregon",
    "lat": 45.5152,
    "lon": -122.6784,
    "pronouns": None,
    "prepared": dt.date.today().isoformat(),
    "for": "Full Birth Name",
    "from": "a friend",
}


# ── helpers ─────────────────────────────────────────────────────────────────
def sign_of(lon):
    return SIGNS[int(lon // 30) % 12]


def dms(lon):
    d = lon % 30
    dd = int(d)
    mm = int(round((d - dd) * 60))
    if mm == 60:
        dd, mm = dd + 1, 0
    return dd, mm


def fmt(lon):
    dd, mm = dms(lon)
    return "%d°%02d' %s" % (dd, mm, sign_of(lon))


def point(lon, retro=False, house=None):
    dd, mm = dms(lon)
    p = {"lon": round(lon % 360, 4), "sign": sign_of(lon), "deg": dd, "min": mm,
         "fmt": fmt(lon), "decan": dd // 10 + 1, "retrograde": bool(retro)}
    if house is not None:
        p["house"] = house
    return p


def reduce_num(n, keep=(11, 22, 33)):
    while n > 9 and n not in keep:
        n = sum(int(c) for c in str(n))
    return n


def letters_of(name):
    """Uppercase A–Z only: strips diacritics, hyphens, apostrophes, spaces."""
    flat = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode()
    return "".join(c for c in flat.upper() if "A" <= c <= "Z")


def long_date(y, m, d):
    return "%d %s %d" % (d, dt.date(y, m, d).strftime("%B"), y)


def ampm(hh, mm):
    h12 = hh % 12 or 12
    return "%d:%02d %s" % (h12, mm, "a.m." if hh < 12 else "p.m.")


def age_on(birth, when):
    years = when.year - birth.year
    if (when.month, when.day) < (birth.month, birth.day):
        years -= 1
    return years


# ── input ───────────────────────────────────────────────────────────────────
def load_birth(path):
    with open(path, encoding="utf-8") as f:
        b = json.load(f)
    b = {k: v for k, v in b.items() if not k.startswith("_")}
    for k in ("name", "date"):
        if not b.get(k):
            sys.exit("chart.py: birth.json needs `%s`" % k)
    try:
        y, m, d = (int(x) for x in b["date"].split("-"))
        dt.date(y, m, d)
    except (ValueError, TypeError):
        sys.exit("chart.py: `date` must be YYYY-MM-DD")
    has_time = bool(b.get("time"))
    if has_time:
        missing = [k for k in ("utc_offset", "lat", "lon") if b.get(k) is None]
        if missing:
            sys.exit("chart.py: `time` is set, so %s must be too — no houses without a place "
                     "and an offset. Set time to null if the place is unknown." % ", ".join(missing))
        try:
            hh, mm = (int(x) for x in b["time"].split(":"))
            assert 0 <= hh < 24 and 0 <= mm < 60
        except (ValueError, AssertionError):
            sys.exit("chart.py: `time` must be HH:MM (24h local clock)")
    b.setdefault("place", None)
    b.setdefault("tz_label", None)
    b.setdefault("pronouns", None)
    b.setdefault("for", b["name"])
    b.setdefault("from", None)
    if not b.get("prepared"):
        b["prepared"] = dt.date.today().isoformat()
    try:
        dt.date.fromisoformat(b["prepared"])
    except ValueError:
        sys.exit("chart.py: `prepared` must be YYYY-MM-DD")
    return b, (y, m, d), has_time


# ── the chart ───────────────────────────────────────────────────────────────
def compute(b, ymd, has_time):
    Y, M, D = ymd
    unavailable = {}
    for cand in (os.path.join(HERE, "ephe"), os.path.join(os.getcwd(), "ephe")):
        if os.path.isdir(cand):
            swe.set_ephe_path(cand)
            break

    if has_time:
        hh, mm = (int(x) for x in b["time"].split(":"))
        ut = hh + mm / 60.0 - float(b["utc_offset"])
    else:
        hh = mm = None
        ut = 12.0  # noon UT — the convention for an unknown time; Moon uncertain by up to ±7°
    jd = swe.julday(Y, M, D, 0, swe.GREG_CAL) + ut / 24.0  # day rollover across midnight UT included
    FL = swe.FLG_SWIEPH | swe.FLG_SPEED

    pos, retro = {}, {}
    for nm, pl, _ in BODIES:
        try:
            xx, _ = swe.calc_ut(jd, pl, FL)
        except Exception as e:  # Chiron without its ephemeris file, typically
            unavailable[nm] = str(e)
            continue
        pos[nm] = xx[0] % 360
        retro[nm] = xx[3] < 0

    out = {
        "schema": SCHEMA,
        "generated": dt.datetime.now().replace(microsecond=0).isoformat(),
        "birth": dict(b),
        "has_time": has_time,
        "jd_ut": round(jd, 6),
        "labels": {
            "date_long": long_date(Y, M, D),
            "time_label": (ampm(hh, mm) + (" " + b["tz_label"] if b["tz_label"] else
                           " UTC%+g" % float(b["utc_offset"]))) if has_time else "time of birth not known",
            "place": b["place"] or "place of birth not known",
            "prepared_long": long_date(*(int(x) for x in b["prepared"].split("-"))),
            "age_at_prepared": age_on(dt.date(Y, M, D), dt.date.fromisoformat(b["prepared"])),
            "day_month": "%d %s" % (D, dt.date(Y, M, D).strftime("%B")),
        },
        "meta": {"unavailable": unavailable,
                 "moon_uncertain": not has_time,
                 "note": None if has_time else
                 "No birth time: positions are for noon UT, so the Moon may be off by several "
                 "degrees and could even be in the neighbouring sign. No Ascendant, Midheaven, "
                 "houses, sect, Part of Fortune, or angle aspects. Say so in the report."},
    }

    # angles + houses
    ASC = MC = None
    asc_i = None
    if has_time:
        cusps_q, ascmc = swe.houses(jd, float(b["lat"]), float(b["lon"]), b"P")
        ASC, MC = ascmc[0] % 360, ascmc[1] % 360
        asc_i = int(ASC // 30)

    def whole_house(lon):
        return ((int(lon // 30) - asc_i) % 12) + 1 if asc_i is not None else None

    def quad_house(lon):
        for h in range(12, 0, -1):
            start, end = cusps_q[h - 1], cusps_q[h % 12]
            if ((lon - start) % 360) < (((end - start) % 360) or 360):
                return h
        return 12

    out["bodies"] = {}
    for nm in pos:
        p = point(pos[nm], retro[nm], whole_house(pos[nm]))
        p["glyph"] = GLYPH[nm]
        if has_time:
            p["house_quadrant"] = quad_house(pos[nm])
        out["bodies"][nm] = p

    if has_time:
        out["angles"] = {
            "Ascendant": point(ASC), "Midheaven": point(MC),
            "Descendant": point((ASC + 180) % 360), "Imum Coeli": point((MC + 180) % 360),
        }
        out["chart_ruler"] = RULER[sign_of(ASC)]
        out["houses"] = [{"n": i + 1, "sign": SIGNS[(asc_i + i) % 12],
                          "occupants": [n for n in pos if whole_house(pos[n]) == i + 1]}
                         for i in range(12)]
        out["house_disagreements"] = [
            {"body": n, "whole_sign": whole_house(pos[n]), "quadrant": quad_house(pos[n])}
            for n in pos if whole_house(pos[n]) != quad_house(pos[n])]
        stellia = [h for h in out["houses"] if len(h["occupants"]) >= 3]
        out["stellium_houses"] = [{"n": h["n"], "sign": h["sign"], "count": len(h["occupants"]),
                                   "bodies": h["occupants"]} for h in stellia]

        sun, moon = pos["Sun"], pos["Moon"]
        is_day = whole_house(sun) in range(7, 13)
        out["sect"] = "day" if is_day else "night"
        out["saturn_in_sect"] = is_day            # Saturn is diurnal: in sect by day, harsher by night
        out["mars_in_sect"] = not is_day
        pof = (ASC + moon - sun) % 360 if is_day else (ASC + sun - moon) % 360
        out["part_of_fortune"] = point(pof, house=whole_house(pof))
        alts = {}
        for nm, pl in (("Sun", swe.SUN), ("Moon", swe.MOON)):
            xx, _ = swe.calc_ut(jd, pl, swe.FLG_SWIEPH | swe.FLG_EQUATORIAL)
            H = math.radians((swe.sidtime(jd) * 15 + float(b["lon"]) - xx[0]) % 360)
            dec, phi = math.radians(xx[1]), math.radians(float(b["lat"]))
            alts[nm] = round(math.degrees(math.asin(
                math.sin(phi) * math.sin(dec) + math.cos(phi) * math.cos(dec) * math.cos(H))), 2)
        out["altitudes"] = alts
    else:
        out["angles"] = None
        out["chart_ruler"] = None
        out["houses"] = None
        out["house_disagreements"] = None
        out["stellium_houses"] = []
        out["sect"] = None
        out["saturn_in_sect"] = None
        out["mars_in_sect"] = None
        out["part_of_fortune"] = None
        out["altitudes"] = None

    # sign stellia (hold regardless of time)
    sign_count = Counter(sign_of(pos[n]) for n in pos if n not in ("Lilith", "True Node"))
    out["stellium_signs"] = [{"sign": s, "count": c,
                              "bodies": [n for n in pos if n not in ("Lilith", "True Node") and sign_of(pos[n]) == s]}
                             for s, c in sign_count.items() if c >= 3]

    elong = (pos["Moon"] - pos["Sun"]) % 360
    phases = ["New", "Waxing Crescent", "First Quarter", "Waxing Gibbous", "Full",
              "Waning Gibbous", "Last Quarter", "Waning Crescent"]
    out["moon_phase"] = {"name": phases[int(((elong + 22.5) % 360) // 45)],
                         "elongation": round(elong, 2),
                         "illumination": round((1 - math.cos(math.radians(elong))) / 2 * 100, 1),
                         "waxing": elong < 180}

    # aspects
    pts = dict(pos)
    if has_time:
        pts["Ascendant"], pts["Midheaven"] = ASC, MC
    order = [n for n in ["Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Uranus",
                         "Neptune", "Pluto", "Chiron", "True Node", "Ascendant", "Midheaven"] if n in pts]
    found = []
    for i, a in enumerate(order):
        for bname in order[i + 1:]:
            d = abs(pts[a] - pts[bname]) % 360
            if d > 180:
                d = 360 - d
            for rel, ang, kind in ASPECTS:
                lim = 8 if {a, bname} & {"Sun", "Moon"} else 6
                if rel == "quincunx":
                    lim = 3
                if {a, bname} & {"Ascendant", "Midheaven"}:
                    lim = 6
                if abs(d - ang) <= lim:
                    found.append({"a": a, "type": rel, "b": bname, "orb": round(abs(d - ang), 2),
                                  "exact": abs(d - ang) < 1, "kind": kind})
                    break
    found.sort(key=lambda x: x["orb"])
    out["aspects"] = found
    out["tightest_aspect"] = found[0] if found else None

    # balance
    w = {"Sun": 3, "Moon": 3, "Ascendant": 3, "Mercury": 2, "Venus": 2, "Mars": 2, "Midheaven": 2}
    eb, mb = Counter(), Counter()
    for k in order:
        wt = w.get(k, 1)
        eb[ELEM[sign_of(pts[k])]] += wt
        mb[MODE[sign_of(pts[k])]] += wt
    out["balance"] = {"elements": {e: eb.get(e, 0) for e in ("Fire", "Earth", "Air", "Water")},
                      "modalities": {m: mb.get(m, 0) for m in ("Cardinal", "Fixed", "Mutable")},
                      "weights": w}

    out["numerology"] = numerology(b["name"], Y, M, D, int(b["prepared"][:4]),
                                   out["labels"]["age_at_prepared"])
    out["timing"] = timing(jd, pos, Y, out["labels"]["age_at_prepared"])
    out["wheel"] = wheel(pos, found, ASC, MC)
    return out


# ── numerology ──────────────────────────────────────────────────────────────
def numerology(name, Y, M, D, prepared_year, age_now):
    PY = {c: (i % 9) + 1 for i, c in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ")}
    CH = {c: v for v, ls in {1: "AIJQY", 2: "BKR", 3: "CGLS", 4: "DMT", 5: "EHNX",
                             6: "UVW", 7: "OZ", 8: "FP"}.items() for c in ls}
    VOW = set("AEIOU")
    parts = [letters_of(p) for p in name.split()]
    parts = [p for p in parts if p]
    letters = "".join(parts)
    tot = sum(PY[c] for c in letters)
    vowel = sum(PY[c] for c in letters if c in VOW)
    cons = tot - vowel
    rm, rd, ry = reduce_num(M), reduce_num(D), reduce_num(Y)
    lp = reduce_num(rm + rd + ry)
    lp_all = reduce_num(sum(int(c) for c in "%02d%02d%d" % (D, M, Y)))
    expression, soul, pers, bday = reduce_num(tot), reduce_num(vowel), reduce_num(cons), reduce_num(D)
    maturity = reduce_num(lp + expression)
    six = {"life_path": lp, "expression": expression, "soul_urge": soul,
           "personality": pers, "birthday": bday, "maturity": maturity}
    masters = [{"number": v, "where": k} for k, v in six.items() if v in (11, 22, 33)]
    tally = Counter(PY[c] for c in letters)
    mx = max(tally.values()) if tally else 0

    # pinnacles: master Life Paths reduce for the age formula (11→2, 22→4, 33→6)
    lp_r = reduce_num(lp, keep=())
    first = 36 - lp_r
    P1, P2 = rm + rd, rd + ry
    pins_n = [reduce_num(P1), reduce_num(P2), reduce_num(P1 + P2), reduce_num(rm + ry)]
    bounds = [0, first, first + 9, first + 18, None]
    pinnacles = []
    for i in range(4):
        lo, hi = bounds[i], bounds[i + 1]
        pinnacles.append({"n": i + 1, "number": pins_n[i], "from_age": lo, "to_age": hi,
                          "range_label": ("birth to %d" % hi) if i == 0 else
                                         ("%d onward" % lo) if hi is None else "%d to %d" % (lo, hi),
                          "current": (lo <= age_now) and (hi is None or age_now < hi)})
    m1, d1, y1 = reduce_num(M, keep=()), reduce_num(D, keep=()), reduce_num(Y, keep=())
    c1, c2 = abs(m1 - d1), abs(d1 - y1)
    challenges = [c1, c2, abs(c1 - c2), abs(m1 - y1)]

    def personal_year(y):
        return reduce_num(rm + rd + reduce_num(y, keep=()), keep=())
    pys = [{"year": y, "number": personal_year(y), "current": y == prepared_year}
           for y in range(prepared_year - 2, prepared_year + 9)]

    loshu_digits = [int(c) for c in "%d%d%d" % (D, M, Y) if c != "0"]
    loshu = Counter(loshu_digits)
    psychic = reduce_num(D, keep=())
    destiny = reduce_num(sum(int(c) for c in "%d%d%d" % (D, M, Y)), keep=())
    name_vedic = reduce_num(expression, keep=())
    kpath = tot % 22
    kl = KABBALAH[kpath]
    return {
        "system": "Pythagorean, full birth name, Y as consonant",
        "name_used": " ".join(parts),
        "name_parts": [{"part": p, "total": sum(PY[c] for c in p), "reduced": reduce_num(sum(PY[c] for c in p))}
                       for p in parts],
        "totals": {"expression": tot, "vowels": vowel, "consonants": cons,
                   "balance_ok": vowel + cons == tot},
        **six,
        "life_path_all_digit": lp_all,
        "life_path_methods_agree": lp == lp_all,
        "masters": masters,
        "tally": {str(k): tally.get(k, 0) for k in range(1, 10)},
        "karmic_lessons": [k for k in range(1, 10) if not tally.get(k)],
        "hidden_passion": sorted(k for k in tally if tally[k] == mx),
        "balance_number": reduce_num(sum(PY[p[0]] for p in parts)) if parts else None,
        "chaldean": {"total": sum(CH[c] for c in letters), "reduced": reduce_num(sum(CH[c] for c in letters))},
        "kabbalistic": {"path": kpath or 22, "letter": kl[0], "card": kl[1], "attribution": kl[2]},
        "vedic": {"psychic": psychic, "psychic_planet": VEDIC_PLANET[psychic],
                  "destiny": destiny, "destiny_planet": VEDIC_PLANET[destiny],
                  "name": name_vedic, "name_planet": VEDIC_PLANET[name_vedic]},
        "lo_shu": {"grid": {str(k): loshu.get(k, 0) for k in range(1, 10)},
                   "missing": [k for k in range(1, 10) if not loshu.get(k)],
                   "strongest": sorted(k for k in loshu if loshu[k] == max(loshu.values()))},
        "pinnacles": pinnacles,
        "pinnacle_ages": [first, first + 9, first + 18],
        "pinnacle_life_path_reduced": lp_r,
        "challenges": challenges,
        "personal_years": pys,
    }


# ── timing ──────────────────────────────────────────────────────────────────
def timing(jd, pos, Y, age_now):
    def hits(pl, target, a, b, step=2.0):
        out, jd0, prev = [], a, None
        while jd0 < b:
            d = ((swe.calc_ut(jd0, pl, swe.FLG_SWIEPH)[0][0] - target + 180) % 360) - 180
            if prev is not None and prev * d < 0 and abs(d - prev) < 180:
                lo, hi = jd0 - step, jd0
                for _ in range(50):
                    mid = (lo + hi) / 2
                    dm = ((swe.calc_ut(mid, pl, swe.FLG_SWIEPH)[0][0] - target + 180) % 360) - 180
                    if dm * prev < 0:
                        hi = mid
                    else:
                        lo = mid
                out.append((lo + hi) / 2)
            prev = d
            jd0 += step
        return out

    def iso(j):
        y, m, d, _ = swe.revjul(j)
        return "%d-%02d-%02d" % (y, m, d)

    end = swe.julday(Y + 90, 1, 1, 0)
    T = {}
    for key, pl, tgt in [("saturn_returns", swe.SATURN, pos.get("Saturn")),
                         ("jupiter_returns", swe.JUPITER, pos.get("Jupiter")),
                         ("nodal_returns", swe.TRUE_NODE, pos.get("True Node")),
                         ("chiron_return", swe.CHIRON, pos.get("Chiron")),
                         ("uranus_opposition", swe.URANUS, (pos["Uranus"] + 180) % 360 if "Uranus" in pos else None),
                         ("neptune_square", swe.NEPTUNE, (pos["Neptune"] + 90) % 360 if "Neptune" in pos else None),
                         ("pluto_square", swe.PLUTO, (pos["Pluto"] + 90) % 360 if "Pluto" in pos else None)]:
        if tgt is None:
            T[key] = None
            continue
        try:
            hh = hits(pl, tgt, jd, end)
        except Exception:
            T[key] = None
            continue
        T[key] = [{"date": iso(h), "age": int((h - jd) / 365.25)} for h in hh[:8]]
    T["progressed_sun"] = []
    for age in sorted(set([0, 10, 20, 30, 40, 50, 60, 70, age_now])):
        T["progressed_sun"].append({"age": age, **point(swe.calc_ut(jd + age, swe.SUN, swe.FLG_SWIEPH)[0][0])})
    T["progressed_moon_now"] = point(swe.calc_ut(jd + age_now, swe.MOON, swe.FLG_SWIEPH)[0][0])
    return T


# ── wheel data ──────────────────────────────────────────────────────────────
def wheel(pos, aspects, ASC, MC):
    names = [n for n in WHEEL_BODIES if n in pos]
    idx = {n: i for i, n in enumerate(names)}
    bodies = [{"lon": round(pos[n], 2), "g": GLYPH[n], "t": str(dms(pos[n])[0]),
               "w": 1 if n in PERSONAL else 0, "name": n} for n in names]
    asp = []
    for a in aspects:
        if a["kind"] and a["a"] in idx and a["b"] in idx \
                and a["a"] in WHEEL_ASPECT_BODIES and a["b"] in WHEEL_ASPECT_BODIES \
                and a["orb"] <= WHEEL_ORB[a["kind"]]:
            asp.append([idx[a["a"]], idx[a["b"]], a["kind"]])
    return {"asc": round(ASC, 4) if ASC is not None else None,
            "mc": round(MC, 4) if MC is not None else None,
            "bodies": bodies, "aspects": asp}


# ── the human summary ───────────────────────────────────────────────────────
def summary(c):
    L = c["labels"]
    N = c["numerology"]
    o = []
    o.append("%s — %s · %s · %s" % (c["birth"]["name"], L["date_long"], L["time_label"], L["place"]))
    o.append("prepared %s · age %d · JD(UT) %.6f" % (L["prepared_long"], L["age_at_prepared"], c["jd_ut"]))
    if c["meta"]["note"]:
        o.append("NOTE " + c["meta"]["note"])
    for nm, why in c["meta"]["unavailable"].items():
        o.append("NOTE %s unavailable: %s" % (nm, why.split("(")[0].strip()))
    o.append("\n── BODIES ──")
    for nm, p in c["bodies"].items():
        o.append("  %-11s%22s  %s%s" % (nm, p["fmt"], "R" if p["retrograde"] else " ",
                                       ("  H%d" % p["house"]) if p.get("house") else ""))
    if c["has_time"]:
        A = c["angles"]
        o.append("\n── ANGLES ──")
        o.append("  ASC %s   MC %s   DSC %s   IC %s" % (A["Ascendant"]["fmt"], A["Midheaven"]["fmt"],
                                                      A["Descendant"]["fmt"], A["Imum Coeli"]["fmt"]))
        o.append("  Chart ruler: %s" % c["chart_ruler"])
        o.append("\n── WHOLE-SIGN HOUSES ──")
        for h in c["houses"]:
            o.append("  H%-2d %-12s %s" % (h["n"], h["sign"], ", ".join(h["occupants"]) or "—"))
        o.append("  whole-sign vs quadrant disagreements: " + (", ".join(
            "%s H%d/H%d" % (d["body"], d["whole_sign"], d["quadrant"]) for d in c["house_disagreements"]) or "none"))
        o.append("\n  Sect: %s   (Saturn %s sect → %s; Mars %s sect)" % (
            c["sect"].upper(), "IN" if c["saturn_in_sect"] else "OUT OF",
            "milder" if c["saturn_in_sect"] else "HARSHER", "in" if c["mars_in_sect"] else "out of"))
        o.append("  Part of Fortune %s (H%d)" % (c["part_of_fortune"]["fmt"], c["part_of_fortune"]["house"]))
        for nm, alt in c["altitudes"].items():
            o.append("  %s altitude %+.2f° (%s the horizon)" % (nm, alt, "above" if alt > 0 else "below"))
    mp = c["moon_phase"]
    o.append("  Moon phase: %s, %.1f%% lit" % (mp["name"], mp["illumination"]))
    if c["stellium_houses"]:
        o.append("  Stellium by house: " + "; ".join("H%d %s (%s)" % (s["n"], s["sign"], ", ".join(s["bodies"]))
                                                   for s in c["stellium_houses"]))
    if c["stellium_signs"]:
        o.append("  Stellium by sign: " + "; ".join("%s (%s)" % (s["sign"], ", ".join(s["bodies"]))
                                                  for s in c["stellium_signs"]))
    o.append("\n── ASPECTS ──")
    for a in c["aspects"]:
        o.append("  %-11s %-9s %-12s %5.2f°%s" % (a["a"], a["type"], a["b"], a["orb"], "   ← EXACT" if a["exact"] else ""))
    o.append("\n── BALANCE ──\n  Elements %s\n  Modalities %s" % (c["balance"]["elements"], c["balance"]["modalities"]))
    o.append("\n── NUMEROLOGY (%s) ──" % N["name_used"])
    for p in N["name_parts"]:
        o.append("  %-12s %3d → %d" % (p["part"], p["total"], p["reduced"]))
    o.append("  Life Path %d   (all-digit method: %d%s)" % (
        N["life_path"], N["life_path_all_digit"], "" if N["life_path_methods_agree"] else " — methods differ; use the component method"))
    o.append("  Expression %d · Soul Urge %d · Personality %d · Birthday %d · Maturity %d" % (
        N["expression"], N["soul_urge"], N["personality"], N["birthday"], N["maturity"]))
    o.append("  Masters: %s" % (", ".join("%d (%s)" % (m["number"], m["where"]) for m in N["masters"]) or "none"))
    o.append("  balance check %d+%d=%d %s" % (N["totals"]["vowels"], N["totals"]["consonants"], N["totals"]["expression"],
                                              "OK" if N["totals"]["balance_ok"] else "FAIL"))
    o.append("  tally {%s}" % ", ".join("%s:%d" % kv for kv in N["tally"].items()))
    o.append("  Karmic Lessons (absent): %s" % (N["karmic_lessons"] or "none"))
    o.append("  Hidden Passion: %s" % N["hidden_passion"])
    o.append("  Chaldean %d → %d · Kabbalistic path %d (%s · %s · %s) · Balance %s" % (
        N["chaldean"]["total"], N["chaldean"]["reduced"], N["kabbalistic"]["path"], N["kabbalistic"]["letter"],
        N["kabbalistic"]["card"], N["kabbalistic"]["attribution"], N["balance_number"]))
    V = N["vedic"]
    o.append("  Vedic: psychic %d (%s) · destiny %d (%s) · name %d (%s)" % (
        V["psychic"], V["psychic_planet"], V["destiny"], V["destiny_planet"], V["name"], V["name_planet"]))
    o.append("  Lo Shu grid %s · missing %s · strongest %s" % (
        N["lo_shu"]["grid"], N["lo_shu"]["missing"] or "none", N["lo_shu"]["strongest"]))
    o.append("  Pinnacles %s  switching at ages %s%s" % (
        "·".join(str(p["number"]) for p in N["pinnacles"]), ", ".join(str(a) for a in N["pinnacle_ages"]),
        ("   [Life Path %d reduced to %d for this formula]" % (N["life_path"], N["pinnacle_life_path_reduced"]))
        if N["life_path"] != N["pinnacle_life_path_reduced"] else ""))
    o.append("  Current pinnacle: #%d (%s)" % next((p["n"], p["number"]) for p in N["pinnacles"] if p["current"]))
    o.append("  Challenges %s" % "·".join(str(x) for x in N["challenges"]))
    o.append("  Personal years: " + " · ".join("%d PY%d%s" % (p["year"], p["number"], "*" if p["current"] else "")
                                               for p in N["personal_years"]))
    T = c["timing"]
    o.append("\n── RETURNS & TRANSITS ──")
    for key, lab in [("saturn_returns", "Saturn returns"), ("jupiter_returns", "Jupiter returns"),
                     ("nodal_returns", "Nodal returns"), ("chiron_return", "Chiron return"),
                     ("uranus_opposition", "Uranus opposition"), ("neptune_square", "Neptune square"),
                     ("pluto_square", "Pluto square")]:
        v = T.get(key)
        o.append("  %-20s %s" % (lab, " · ".join("%s (%d)" % (h["date"], h["age"]) for h in v) if v else "—"))
    o.append("\n  Progressed Sun (1 day = 1 year):")
    for p in T["progressed_sun"]:
        o.append("    age %2d: %s" % (p["age"], p["fmt"]))
    o.append("  Progressed Moon now: %s" % T["progressed_moon_now"]["fmt"])
    return "\n".join(o)


# ── main ────────────────────────────────────────────────────────────────────
def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("birth", nargs="?", help="path to birth.json")
    ap.add_argument("-o", "--out", help="where to write chart.json (default: beside birth.json)")
    ap.add_argument("--example", action="store_true", help="print a birth.json skeleton and exit")
    ap.add_argument("-q", "--quiet", action="store_true", help="no summary on stdout")
    args = ap.parse_args()
    if args.example:
        print(json.dumps(EXAMPLE, indent=2, ensure_ascii=False))
        return
    if not args.birth:
        ap.error("birth.json is required (or use --example)")
    b, ymd, has_time = load_birth(args.birth)
    chart = compute(b, ymd, has_time)
    out = args.out or os.path.join(os.path.dirname(os.path.abspath(args.birth)), "chart.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(chart, f, indent=2, ensure_ascii=False)
    if not args.quiet:
        print(summary(chart))
        print("\nwrote %s" % out)


if __name__ == "__main__":
    main()
