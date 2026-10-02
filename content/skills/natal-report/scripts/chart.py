#!/usr/bin/env python3
"""
Natal chart engine for the natal-report skill.
    pip3 install pyswisseph
    curl -sL -o ephe/seas_18.se1 \
      https://raw.githubusercontent.com/aloistr/swisseph/master/ephe/seas_18.se1   # Chiron only

Edit the BIRTH block, then: python3 chart.py
Tropical zodiac, whole-sign houses (quadrant cusps also reported).
"""
import swisseph as swe, math, os
from collections import Counter

# ─────────────── BIRTH ───────────────
NAME     = "Carey Page Forbes"     # full name AS ON THE BIRTH CERTIFICATE
Y, M, D  = 1988, 12, 31
LOCAL_H, LOCAL_MIN = 0, 28         # 24h local clock time
UTC_OFFSET = -6                    # hours; CHECK DST FOR THAT DATE + JURISDICTION + YEAR
LAT, LON = 33.5207, -86.8025       # +N, +E
PLACE    = "Birmingham, Alabama"
TODAY_Y  = 2026                    # year the reading is prepared
# ─────────────────────────────────────

swe.set_ephe_path('ephe' if os.path.isdir('ephe') else None)
UT = LOCAL_H + LOCAL_MIN/60 - UTC_OFFSET
jd = swe.julday(Y, M, D + int(UT//24), UT % 24, swe.GREG_CAL)
FL = swe.FLG_SWIEPH | swe.FLG_SPEED

SIGNS = ["Aries","Taurus","Gemini","Cancer","Leo","Virgo","Libra","Scorpio",
         "Sagittarius","Capricorn","Aquarius","Pisces"]
RULER = dict(zip(SIGNS,["Mars","Venus","Mercury","Moon","Sun","Mercury","Venus","Pluto",
                        "Jupiter","Saturn","Uranus","Neptune"]))
ELEM  = {s:e for s,e in zip(SIGNS,["Fire","Earth","Air","Water"]*3)}
MODE  = {s:m for s,m in zip(SIGNS,["Cardinal","Fixed","Mutable"]*4)}
def sign_of(l): return SIGNS[int(l//30) % 12]
def fmt(l):
    d = l % 30; dd = int(d); mm = int(round((d-dd)*60))
    if mm == 60: dd, mm = dd+1, 0
    return f"{dd}°{mm:02d}' {sign_of(l)}"

BODIES = [("Sun",swe.SUN),("Moon",swe.MOON),("Mercury",swe.MERCURY),("Venus",swe.VENUS),
          ("Mars",swe.MARS),("Jupiter",swe.JUPITER),("Saturn",swe.SATURN),("Uranus",swe.URANUS),
          ("Neptune",swe.NEPTUNE),("Pluto",swe.PLUTO),("Chiron",swe.CHIRON),
          ("True Node",swe.TRUE_NODE),("Lilith",swe.MEAN_APOG)]

print(f"{NAME} — {D:02d}/{M:02d}/{Y} {LOCAL_H:02d}:{LOCAL_MIN:02d} (UTC{UTC_OFFSET:+d}) — {PLACE}")
print(f"JD(UT) {jd:.6f}\n")

pos = {}
print("── BODIES ──")
for nm, pl in BODIES:
    try: xx, _ = swe.calc_ut(jd, pl, FL)
    except Exception as e: print(f"  {nm:11} unavailable ({e})"); continue
    pos[nm] = xx[0]
    print(f"  {nm:11}{fmt(xx[0]):>20}  {'R' if xx[3] < 0 else ' '}")

cusps_w, ascmc = swe.houses(jd, LAT, LON, b'W')
cusps_q, _     = swe.houses(jd, LAT, LON, b'P')
ASC, MC = ascmc[0], ascmc[1]
asc_i = int(ASC // 30)
def whole_house(l): return ((int(l//30) - asc_i) % 12) + 1
print(f"\n── ANGLES ──\n  ASC {fmt(ASC)}   MC {fmt(MC)}   DSC {fmt((ASC+180)%360)}   IC {fmt((MC+180)%360)}")
print(f"  Chart ruler: {RULER[sign_of(ASC)]} (ruler of {sign_of(ASC)})")

print(f"\n── WHOLE-SIGN HOUSES ──")
for i in range(12):
    occ = [n for n in pos if whole_house(pos[n]) == i+1]
    print(f"  H{i+1:<2} {SIGNS[(asc_i+i)%12]:12} {', '.join(occ) or '—'}")
diff = [(n, whole_house(pos[n]), next(h for h in range(12,0,-1)
        if ((pos[n]-cusps_q[h-1]) % 360) < ((cusps_q[h%12]-cusps_q[h-1]) % 360 or 360)))
        for n in pos]
mism = [(n,w,q) for n,w,q in diff if w != q]
print("  whole-sign vs quadrant disagreements: " +
      (", ".join(f"{n} H{w}/H{q}" for n,w,q in mism) or "none"))

sun, moon = pos['Sun'], pos['Moon']
is_day = whole_house(sun) in range(7,13)
POF = (ASC + moon - sun) % 360 if is_day else (ASC + sun - moon) % 360
print(f"\n  Sect: {'DAY' if is_day else 'NIGHT'}   "
      f"(Saturn is {'IN' if is_day else 'OUT OF'} sect → {'milder' if is_day else 'HARSHER'})")
print(f"  Part of Fortune {fmt(POF)} (H{whole_house(POF)})")
elong = (moon - sun) % 360
ph = ["New","Waxing Crescent","First Quarter","Waxing Gibbous","Full",
      "Waning Gibbous","Last Quarter","Waning Crescent"][int(((elong+22.5)%360)//45)]
print(f"  Moon phase: {ph}, {(1-math.cos(math.radians(elong)))/2*100:.1f}% lit")
# true altitude of each light — settles 'above or below the horizon' arguments
for nm, pl in [("Moon",swe.MOON),("Sun",swe.SUN)]:
    xx,_ = swe.calc_ut(jd, pl, swe.FLG_SWIEPH|swe.FLG_EQUATORIAL)
    H = math.radians((swe.sidtime(jd)*15 + LON - xx[0]) % 360)
    dec, phi = math.radians(xx[1]), math.radians(LAT)
    alt = math.degrees(math.asin(math.sin(phi)*math.sin(dec)+math.cos(phi)*math.cos(dec)*math.cos(H)))
    print(f"  {nm} altitude {alt:+.2f}° ({'above' if alt>0 else 'below'} the horizon)")

print("\n── ASPECTS ──")
ASPECTS = [("conjunct",0),("sextile",60),("square",90),("trine",120),("opposite",180),("quincunx",150)]
pts = dict(pos); pts["Ascendant"] = ASC; pts["Midheaven"] = MC
order = [n for n in ["Sun","Moon","Mercury","Venus","Mars","Jupiter","Saturn","Uranus","Neptune",
                     "Pluto","Chiron","True Node","Ascendant","Midheaven"] if n in pts]
found = []
for i, a in enumerate(order):
    for b in order[i+1:]:
        d = abs(pts[a]-pts[b]) % 360
        if d > 180: d = 360 - d
        for rel, ang in ASPECTS:
            lim = 8 if {a,b} & {"Sun","Moon"} else 6
            if rel == "quincunx": lim = 3
            if {a,b} & {"Ascendant","Midheaven"}: lim = 6
            if abs(d-ang) <= lim:
                found.append((abs(d-ang), a, rel, b)); break
for orb, a, rel, b in sorted(found):
    print(f"  {a:11} {rel:9} {b:12} {orb:5.2f}°" + ("   ← EXACT" if orb < 1 else ""))

w = {"Sun":3,"Moon":3,"Ascendant":3,"Mercury":2,"Venus":2,"Mars":2,"Midheaven":2}
eb, mb = Counter(), Counter()
for k in order:
    wt = w.get(k,1); eb[ELEM[sign_of(pts[k])]] += wt; mb[MODE[sign_of(pts[k])]] += wt
print(f"\n── BALANCE ──\n  Elements {dict(eb)}\n  Modalities {dict(mb)}")

# ── NUMEROLOGY ──
def red(n, keep=(11,22,33)):
    while n > 9 and n not in keep: n = sum(int(c) for c in str(n))
    return n
PY = {c:(i%9)+1 for i,c in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ")}
CH = {c:v for v,ls in {1:"AIJQY",2:"BKR",3:"CGLS",4:"DMT",5:"EHNX",6:"UVW",7:"OZ",8:"FP"}.items() for c in ls}
up = NAME.upper(); parts = up.split(); letters = up.replace(" ","")
VOW = set("AEIOU")
tot   = sum(PY[c] for c in letters)
vowel = sum(PY[c] for c in letters if c in VOW)
cons  = tot - vowel
rm, rd, ry = red(M), red(D), red(Y)
lp = red(rm+rd+ry)
print(f"\n── NUMEROLOGY ({NAME}) ──")
for p in parts: print(f"  {p:12} {sum(PY[c] for c in p):>3} → {red(sum(PY[c] for c in p))}")
print(f"  Life Path {lp}   (all-digit method: {red(sum(int(c) for c in f'{D:02d}{M:02d}{Y}'))})")
print(f"  Expression {red(tot)} · Soul Urge {red(vowel)} · Personality {red(cons)} "
      f"· Birthday {red(D)} · Maturity {red(lp+red(tot))}")
print(f"  balance check {vowel}+{cons}={tot} {'OK' if vowel+cons==tot else 'FAIL'}")
c = Counter(PY[x] for x in letters)
print(f"  tally {{{', '.join(f'{k}:{c.get(k,0)}' for k in range(1,10))}}}")
print(f"  Karmic Lessons (absent): {[k for k in range(1,10) if not c.get(k)] or 'none'}")
mx = max(c.values()); print(f"  Hidden Passion: {sorted(k for k in c if c[k]==mx)}")
print(f"  Chaldean {sum(CH[x] for x in letters)} → {red(sum(CH[x] for x in letters))}"
      f" · Kabbalistic path {tot % 22} · Balance {red(sum(PY[p[0]] for p in parts))}")
P1,P2 = rm+rd, rd+ry; P3,P4 = P1+P2, rm+ry
lp_r = red(lp, keep=())          # master Life Paths reduce for the pinnacle-age formula (11→2, 22→4, 33→6)
print(f"  Pinnacles {red(P1)}·{red(P2)}·{red(P3)}·{red(P4)}  switching at ages "
      f"{36-lp_r}, {36-lp_r+9}, {36-lp_r+18}"
      + (f"   [Life Path {lp} reduced to {lp_r} for this formula]" if lp!=lp_r else ""))
print(f"  Challenges {abs(rm-rd)}·{abs(rd-ry)}·{abs(abs(rm-rd)-abs(rd-ry))}·{abs(rm-ry)}")
print("  Personal years: " + " · ".join(
    f"{y} PY{red(rm+rd+red(y), keep=())}" for y in range(TODAY_Y-2, TODAY_Y+9)))

# ── TIMING ──
print("\n── RETURNS & TRANSITS ──")
def hits(pl, target, a, b, step=2.0):
    out=[]; jd0=a; prev=None
    while jd0 < b:
        d = ((swe.calc_ut(jd0,pl,swe.FLG_SWIEPH)[0][0]-target+180)%360)-180
        if prev is not None and prev*d < 0 and abs(d-prev) < 180:
            lo,hi = jd0-step, jd0
            for _ in range(50):
                mid=(lo+hi)/2
                dm=((swe.calc_ut(mid,pl,swe.FLG_SWIEPH)[0][0]-target+180)%360)-180
                if dm*prev < 0: hi=mid
                else: lo=mid
            out.append((lo+hi)/2)
        prev=d; jd0+=step
    return out
end = swe.julday(Y+75,1,1,0)
for lab, pl, tgt in [("Saturn returns",swe.SATURN,pos.get('Saturn')),
                     ("Jupiter returns",swe.JUPITER,pos.get('Jupiter')),
                     ("Nodal returns",swe.TRUE_NODE,pos.get('True Node')),
                     ("Chiron return",swe.CHIRON,pos.get('Chiron')),
                     ("Uranus opposition",swe.URANUS,(pos.get('Uranus',0)+180)%360)]:
    if tgt is None: continue
    hh = hits(pl,tgt,jd,end)
    dates = [f"{swe.revjul(h)[0]}-{swe.revjul(h)[1]:02d}-{swe.revjul(h)[2]:02d}" for h in hh[:6]]
    print(f"  {lab:20} " + (" · ".join(dates) or "—"))
print("\n  Progressed Sun (1 day = 1 year):")
for age in (0,20,30,40,50,60):
    print(f"    age {age:>2}: {fmt(swe.calc_ut(jd+age, swe.SUN, FL)[0][0])}")
