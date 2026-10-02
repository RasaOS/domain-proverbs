#!/usr/bin/env python3
"""
check-report.py — the conformance gate for a drafted natal report (REPORT-SPEC.md §9).

    python3 check-report.py report.html [--chart chart.json] [--strict]

Exit 0 = clean (warnings allowed unless --strict); exit 1 = at least one error.

It checks shape and every writing rule that a machine can check: unfilled slots, title,
section order, the Portrait's length, banned phrases, leaked arithmetic and technique,
exclamation marks and emoji, gendering, stray exact figures, the footer, the theme tokens,
the wheel, the machine-owned numbers (with --chart), and kindred chips carrying a year.
It does NOT grade prose, verify doctrine, or recheck arithmetic — that is the human
adversarial pass in SKILL.md, and it still has to happen.
"""
import argparse
import html
import json
import re
import sys

SUFFIX = " — Natal Chart & Numerology"

# (id, required) — required True, or the chart.json flag that decides it
SECTIONS = [("portrait", True), ("big-three", True), ("gravity", True), ("sun", True),
            ("world", "has_time"), ("numbers", True), ("masters", "masters"), ("nodes", True),
            ("work", True), ("wounds", True), ("traditions", True), ("arc", True),
            ("road", True), ("love", True), ("kindred", True), ("chart", True)]

BANNED = [r"cosmic blueprint", r"the universe is telling you", r"divine timing", r"your soul chose",
          r"\bold soul\b", r"on a deep level", r"\bjourney\b", r"\benerg(y|ies)\b",
          r"\bvibrations?\b", r"\bvibes?\b", r"\bmanifest(ing|ation|s)?\b", r"\bsoulmate\b",
          r"\bthe stars (say|have|want)\b", r"\bwritten in the stars\b"]

# tier 1 — arithmetic and method on the page: always an error
LEAK_ERR = [(r"\d\s*[+×*]\s*\d", "arithmetic"), (r"=\s*\d", "equation"), (r"[→➔⇒]", "arrow reduction"),
            (r"\breduc(e|es|ed|ing|tion)\s+(to|down)\b", "'reduces to'"), (r"\bmod(ulo)?\s*22\b", "mod 22"),
            (r"\bdigit(al)?[- ]?(sum|root)s?\b", "digit sum"), (r"\bletter[- ]?(sum|value|by[- ]letter)s?\b", "letter sums"),
            (r"\b(Pythagorean|Chaldean|Vedic|Kabbalistic)\s+(method|system|calculation)\b", "a method named"),
            (r"\b(two|both) (schools|methods|systems) (differ|disagree)\b", "method dispute on the page"),
            (r"\bcomponent method\b|\ball-digit method\b", "method dispute on the page")]
# tier 2 — technique vocabulary: a warning, because occasionally one honest sentence earns it
LEAK_WARN = [(r"\bstellium\b", "stellium"), (r"\bdecan\b", "decan"), (r"\borbs?\b", "orb"),
             (r"\bwhole[- ]sign\b|\bplacidus\b|\bquadrant\b", "house system"), (r"\bpinnacles?\b", "pinnacle"),
             (r"\bpersonal years?\b", "personal year"), (r"\b(north|south) node\b", "node"),
             (r"\bmidheaven\b|\bascendant\b|\bdescendant\b|\bimum coeli\b", "an angle named by technique"),
             (r"\bsect\b", "sect"), (r"\bkarmic (lesson|debt)\b", "karmic lesson"),
             (r"\bhidden passion\b", "hidden passion"), (r"\bexpression number\b|\bsoul urge number\b", "number named by technique"),
             (r"\bconjunct(ion)?\b|\bsextile\b|\btrine\b|\bsquares?\b(?= (the|your|to))|\bopposition\b", "aspect named by technique"),
             (r"\bretrograde\b", "retrograde"), (r"\bprogress(ed|ion)\b", "progression"), (r"\btransit(s|ing)?\b", "transit")]
BRITISH = [r"\bcolou?rs?\b(?<!color)(?<!colors)", r"\bcentre\b", r"\brealis(e|ed|ing)\b", r"\bbehaviour\b",
           r"\bfavou?rite\b(?<!favorite)", r"\bfavour\b", r"\bhonour\b", r"\borganis(e|ed|ing)\b",
           r"\brecognis(e|ed|ing)\b", r"\bapologis(e|ed|ing)\b", r"\bgrey\b", r"\btheatre\b",
           r"\bdefence\b", r"\btravelling\b", r"\bcancelled\b", r"\bprogramme\b", r"\bpractise\b"]
PRONOUN = r"\b(he|she|his|hers|him|himself|herself)\b"
EMOJI = re.compile("[\U0001F000-\U0001FAFF\U0001F900-\U0001F9FF]")

errors, warnings = [], []


def err(rule, msg):
    errors.append("ERR  %-4s %s" % (rule, msg))


def warn(rule, msg):
    warnings.append("WARN %-4s %s" % (rule, msg))


def strip(fragment):
    """HTML → plain text, dropping script/style/table entirely."""
    s = re.sub(r"(?is)<(script|style|table)\b.*?</\1>", " ", fragment)
    s = re.sub(r"(?is)<br\s*/?>", "\n", s)
    s = re.sub(r"(?s)<[^>]+>", " ", s)
    return re.sub(r"[ \t]+", " ", html.unescape(s)).strip()


def words(text):
    return len(re.findall(r"[A-Za-z’'\-]+", text))


def snippet(text, m, width=40):
    a, b = max(0, m.start() - width), min(len(text), m.end() + width)
    return "…" + re.sub(r"\s+", " ", text[a:b]) + "…"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("report")
    ap.add_argument("--chart", help="chart.json — enables the machine-number and conditional-section checks")
    ap.add_argument("--strict", action="store_true", help="warnings also fail")
    args = ap.parse_args()
    with open(args.report, encoding="utf-8") as f:
        doc = f.read()
    chart = None
    if args.chart:
        with open(args.chart, encoding="utf-8") as f:
            chart = json.load(f)

    # R1 unfilled slots
    slots = re.findall(r"\{\{WRITE:\s*([^{}]*)\}\}", doc)
    other = re.findall(r"\{\{(?!WRITE:)[^{}]*\}\}", doc)
    if slots:
        err("R1", "%d writer slot(s) still unfilled — first: %s" % (len(slots), "; ".join(s[:60] for s in slots[:3])))
    if other:
        err("R1", "%d machine token(s) unfilled — run build.py: %s" % (len(other), ", ".join(other[:5])))

    # split: head, body-without-footer, footer
    title_m = re.search(r"(?is)<title>(.*?)</title>", doc)
    title = html.unescape(title_m.group(1)).strip() if title_m else ""
    h1_m = re.search(r"(?is)<h1>(.*?)</h1>", doc)
    name = strip(h1_m.group(1)) if h1_m else ""
    footer_m = re.search(r"(?is)<footer>(.*?)</footer>", doc)
    footer = strip(footer_m.group(1)) if footer_m else ""
    body_m = re.search(r"(?is)<body[^>]*>(.*)</body>", doc)
    body = body_m.group(1) if body_m else doc
    body_nofooter = re.sub(r"(?is)<footer>.*?</footer>", " ", body)
    sections = [(m.group(1), m.group(2)) for m in
                re.finditer(r'(?is)<section[^>]*data-sec="([^"]+)"[^>]*>(.*?)</section>', body)]
    sec = dict(sections)
    prose_html = re.sub(r'(?is)<section[^>]*data-sec="(chart|kindred)".*?</section>', " ", body_nofooter)
    prose = strip(prose_html)
    prose_no_kindred = prose
    all_prose = strip(body_nofooter)

    # R2 title + name
    if not title:
        err("R2", "no <title>")
    elif not name:
        err("R2", "no <h1>")
    elif title != name + SUFFIX:
        err("R2", "title must be exactly '<h1> — Natal Chart & Numerology'; got %r vs h1 %r" % (title, name))
    if chart and name and name != chart["birth"]["name"]:
        err("R2", "h1 %r != birth name %r in chart.json" % (name, chart["birth"]["name"]))

    # R3 sections, order, conditionals
    seen = [s for s, _ in sections]
    if len(seen) != len(set(seen)):
        err("R3", "duplicate data-sec: %s" % sorted({s for s in seen if seen.count(s) > 1}))
    for sid, req in SECTIONS:
        need = req if req is True else (None if chart is None else
                                        (chart["has_time"] if req == "has_time" else bool(chart["numerology"]["masters"])))
        if need is True and sid not in sec:
            err("R3", "missing section data-sec=\"%s\"" % sid)
        if need is False and sid in sec:
            err("R3", "section \"%s\" present but chart.json says it does not apply (%s)" % (sid, req))
    order = [s for s, _ in SECTIONS if s in sec]
    if [s for s in seen if s in dict(SECTIONS)] != order:
        err("R3", "sections out of order: %s" % " › ".join(seen))
    unknown = [s for s in seen if s not in dict(SECTIONS)]
    if unknown:
        warn("R3", "unlisted section id(s) %s — fine if deliberate, but the spec does not know them" % unknown)

    # R4 Portrait length, lede length
    if "portrait" in sec:
        body_m2 = re.search(r'(?is)<div class="prose p-body">(.*?)</div>', sec["portrait"])
        n = words(strip(body_m2.group(1))) if body_m2 else words(strip(sec["portrait"]))
        if n < 1000 or n > 1450:
            err("R4", "Portrait is %d words; the budget is 1100–1300" % n)
        elif n < 1100 or n > 1300:
            warn("R4", "Portrait is %d words; the budget is 1100–1300" % n)
        if not re.search(r'class="p-close"', sec["portrait"]):
            warn("R4", "Portrait has no closing italic lines (p.p-close)")
    lede_m = re.search(r'(?is)<div class="lede">(.*?)</div>', body)
    if lede_m:
        n = words(strip(lede_m.group(1)))
        if n < 40 or n > 110:
            warn("R4", "lede is %d words; aim for 60–90" % n)

    # R5 banned phrases
    for pat in BANNED:
        for m in re.finditer(pat, all_prose, re.I):
            err("R5", "banned phrase %r: %s" % (m.group(0), snippet(all_prose, m)))

    # R6 leaked method
    for pat, what in LEAK_ERR:
        for m in re.finditer(pat, prose, re.I):
            err("R6", "leaked method (%s): %s" % (what, snippet(prose, m)))
    hits = {}
    for pat, what in LEAK_WARN:
        ms = list(re.finditer(pat, prose, re.I))
        if ms:
            hits[what] = (len(ms), snippet(prose, ms[0]))
    for what, (n, snip) in hits.items():
        warn("R6", "technique word %s ×%d — does the sentence go on to its meaning? %s" % (what, n, snip))

    # R7 exclamation marks, emoji
    for m in re.finditer(r"!", all_prose):
        err("R7", "exclamation mark: %s" % snippet(all_prose, m))
    for m in EMOJI.finditer(all_prose):
        err("R7", "emoji %r in the body" % m.group(0))

    # R8 gendering
    if not (chart and chart["birth"].get("pronouns")):
        ms = list(re.finditer(PRONOUN, prose_no_kindred, re.I))
        if ms:
            warn("R8", "gendered pronoun ×%d outside Kindred — the subject stated no pronouns; is this about someone else? %s"
                 % (len(ms), snippet(prose_no_kindred, ms[0])))

    # R9 exact figures in prose
    figs = list(re.finditer(r"\d+°|\b\d+\.\d+\b|\b\d+′", prose))
    if len(figs) > 4:
        err("R9", "%d exact figures in the prose (degrees/decimals); at most one or two survive a whole report" % len(figs))
    elif len(figs) > 2:
        warn("R9", "%d exact figures in the prose; the budget is one or two, and only where precision is the point" % len(figs))

    # R10 footer
    if not footer:
        err("R10", "no <footer>")
    else:
        for need in ("Swiss Ephemeris", "symbolic", "portrait, not a forecast", "Prepared "):
            if need not in footer:
                err("R10", "footer is missing %r" % need)
        if footer.count(". ") > 14:
            warn("R10", "footer runs long — one short paragraph each, not three essays")

    # R11 theme tokens
    style = " ".join(re.findall(r"(?is)<style[^>]*>(.*?)</style>", doc))
    for need in (":root{", ":root[data-theme=\"dark\"]", "prefers-color-scheme:dark", "--ground", "--panel",
                 "--ink", "--brass", "--star", "Iowan Old Style"):
        if need.replace(" ", "") not in style.replace(" ", ""):
            err("R11", "stylesheet is missing %s" % need)

    # R12 wheel
    if 'id="wheel"' not in body:
        err("R12", "no <canvas id=\"wheel\">")
    if "NATAL_WHEEL" not in doc:
        err("R12", "no window.NATAL_WHEEL data — run build.py")
    elif chart:
        m = re.search(r"window\.NATAL_WHEEL=(\{.*?\});</script>", doc, re.S)
        try:
            w = json.loads(m.group(1)) if m else None
        except ValueError:
            w = None
        if w is None or w.get("asc") != chart["wheel"]["asc"] or len(w.get("bodies", [])) != len(chart["wheel"]["bodies"]):
            err("R12", "wheel data in the report does not match chart.json#wheel")

    # R13 section openers restating their own title
    for sid, frag in sections:
        h2 = re.search(r"(?is)<h2>(.*?)</h2>", frag)
        p = re.search(r"(?is)<p[^>]*>(.*?)</p>", frag)
        if h2 and p:
            t = strip(h2.group(1)).lower()
            opener = " ".join(strip(p.group(1)).lower().split()[:8])
            if t and t in opener:
                warn("R13", "section %r opens by restating its own title" % sid)

    # R14 British spellings
    for pat in BRITISH:
        try:
            ms = list(re.finditer(pat, all_prose, re.I))
        except re.error:
            ms = []
        if ms:
            warn("R14", "spelling %r — American spelling throughout: %s" % (ms[0].group(0), snippet(all_prose, ms[0])))

    # R15 kindred chips
    if "kindred" in sec:
        chips = re.findall(r'(?is)<div class="kin(?: hi)?">(.*?)</div>', sec["kindred"])
        if len(chips) < 12:
            warn("R15", "only %d kindred chips; the house format carries four groups of them" % len(chips))
        for ch in chips:
            if not re.search(r"\b1[0-9]{3}\b|\b20[0-9]{2}\b", ch):
                err("R15", "kindred chip without a birth year: %s" % strip(ch)[:50])
        groups = re.findall(r'(?is)<div class="kin-group">(.*?)</div>\s*(?:<p class="kin-note">|</div>)', sec["kindred"])
        if "kin-note" in sec["kindred"] and re.search(r'<p class="kin-note">\s*</p>', sec["kindred"]):
            warn("R15", "empty kin-note paragraph — delete it")

    # R16 machine-owned numbers untouched (needs chart)
    if chart:
        N = chart["numerology"]
        want = [str(N[k]) for k in ("life_path", "expression", "soul_urge", "personality", "birthday", "maturity")]
        got = re.findall(r'(?is)<div class="plate[^"]*"><div class="num">(\d+)</div>', body)
        if got != want:
            err("R16", "the six plate numbers %s do not match chart.json %s — they are machine-owned" % (got, want))
        wantp = [str(p["number"]) for p in N["pinnacles"]]
        gotp = re.findall(r'(?is)<div class="pin[^"]*">(?:<span class="now-chip">Now</span>)?<div class="num">(\d+)</div>', body)
        if gotp != wantp:
            err("R16", "the four chapter numbers %s do not match chart.json %s" % (gotp, wantp))
        now = [i for i, p in enumerate(N["pinnacles"]) if p["current"]]
        if now and body.count('class="now-chip"') != 1:
            err("R16", "exactly one chapter should carry the Now chip")
        rows = len(re.findall(r"(?is)<tr>", sec.get("chart", "")))
        if rows < len(chart["bodies"]):
            err("R16", "positions table has %d rows but chart.json has %d bodies" % (rows, len(chart["bodies"])))

    # R17 second person
    you = len(re.findall(r"\byou(r|rs|rself)?\b", prose, re.I))
    if you < 80:
        warn("R17", "only %d second-person references — the reading is written TO the subject" % you)

    # report
    print("check-report — %s\n" % args.report)
    for w in warnings:
        print(w)
    for e in errors:
        print(e)
    n_err, n_warn = len(errors), len(warnings)
    if n_err or (args.strict and n_warn):
        print("\nFAIL %d error(s), %d warning(s)" % (n_err, n_warn))
        sys.exit(1)
    print("\nOK   shape conforms. %d warning(s). The human pass (doctrine, arithmetic, overclaimed convergence) still has to happen." % n_warn)


if __name__ == "__main__":
    main()
