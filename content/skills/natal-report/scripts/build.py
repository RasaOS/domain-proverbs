#!/usr/bin/env python3
"""
build.py — assemble a report draft from the house template + chart.json; export the PDF.

    python3 build.py chart.json                         # → report.html beside chart.json
    python3 build.py chart.json -o out/report.html [--template PATH]
    python3 build.py --pdf report.html [-o "Name — Natal Chart & Numerology.pdf"]

Draft: fills every machine-owned token ({{NAME}}, {{WHEEL_SCRIPT}}, {{POSITIONS_ROWS}}, …)
and resolves the conditional blocks (<!-- @if has_time -->, @if no_time, @if masters).
Writer-owned slots — {{WRITE: guidance}} — are left in place; check-report.py refuses
a report while any remain. The writer never edits what build.py filled.

PDF: wraps the finished report with data-theme="light" + scripts/print.css and prints
it with headless Chrome (env CHROME overrides the binary; see REPORT-SPEC.md §10).
"""
import argparse
import html
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = os.path.normpath(os.path.join(HERE, "..", "templates", "report.html"))
PRINT_CSS = os.path.join(HERE, "print.css")
WHEEL_JS = os.path.join(HERE, "wheel.js")
SUFFIX = " — Natal Chart & Numerology"

# U+FE0E after each sign glyph forces TEXT presentation — without it Chrome prints a colour emoji.
SIGN_GLYPH = dict(zip(["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio",
                       "Sagittarius", "Capricorn", "Aquarius", "Pisces"], [g + "\ufe0e" for g in "♈♉♊♋♌♍♎♏♐♑♒♓"]))
ORDINAL = ["First", "Second", "Third", "Fourth", "Fifth", "Sixth", "Seventh", "Eighth",
           "Ninth", "Tenth", "Eleventh", "Twelfth"]
CHROME_CANDIDATES = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/usr/bin/google-chrome", "/usr/bin/google-chrome-stable", "/usr/bin/chromium", "/usr/bin/chromium-browser",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
]


def esc(s):
    return html.escape(str(s), quote=False)


def tokens(c):
    b, L, N, bodies = c["birth"], c["labels"], c["numerology"], c["bodies"]
    t = {}
    t["NAME"] = esc(b["name"])
    t["TITLE"] = esc(b["name"] + SUFFIX)
    t["DATE_LONG"], t["TIME_LABEL"], t["PLACE"] = esc(L["date_long"]), esc(L["time_label"]), esc(L["place"])
    t["PREPARED_LONG"] = esc(L["prepared_long"])
    t["PREPARED_YEAR"] = b["prepared"][:4]
    t["NEXT_YEAR"] = str(int(b["prepared"][:4]) + 1)
    t["AGE_NOW"] = str(L["age_at_prepared"])
    t["DAY_MONTH"] = esc(L["day_month"])
    t["FOR"] = esc(b.get("for") or b["name"])
    t["FROM_LINE"] = (" · with affection, from %s." % esc(b["from"])) if b.get("from") else "."

    def house_label(p):
        return (", %s House" % ORDINAL[p["house"] - 1]) if p.get("house") else ""

    sun, moon = bodies["Sun"], bodies["Moon"]
    t["SUN_SIGN"], t["SUN_GLYPH"], t["SUN_HOUSE_LABEL"] = sun["sign"], SIGN_GLYPH[sun["sign"]], house_label(sun)
    t["MOON_SIGN"], t["MOON_GLYPH"], t["MOON_HOUSE_LABEL"] = moon["sign"], SIGN_GLYPH[moon["sign"]], house_label(moon)
    if c["has_time"]:
        asc = c["angles"]["Ascendant"]
        t["RISING_SIGN"], t["RISING_GLYPH"] = asc["sign"], SIGN_GLYPH[asc["sign"]]
    else:
        t["RISING_SIGN"], t["RISING_GLYPH"] = "Not known", "—"

    for key in ("life_path", "expression", "soul_urge", "personality", "birthday", "maturity"):
        K, v = key.upper(), N[key]
        master = v in (11, 22, 33)
        t["N_" + K] = str(v)
        t["MASTER_CLASS_" + K] = " master" if master else ""
        t["MASTER_CHIP_" + K] = '<span class="chip">Master</span>' if master else ""
    for p in N["pinnacles"]:
        n = p["n"]
        t["PIN_%d_NUM" % n] = str(p["number"])
        t["PIN_%d_RANGE" % n] = p["range_label"]
        t["PIN_%d_CLASS" % n] = " now" if p["current"] else ""
        t["PIN_%d_CHIP" % n] = '<span class="now-chip">Now</span>' if p["current"] else ""

    rows = []
    for nm in ["Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune",
               "Pluto", "Chiron", "True Node", "Lilith"]:
        p = bodies.get(nm)
        if not p:
            continue
        label = {"True Node": "North Node", "Lilith": "Black Moon Lilith"}.get(nm, nm)
        label += " ℞" if p["retrograde"] else ""
        rows.append('      <tr><td class="g">%s</td><td>%s</td><td class="pos">%s</td><td>%s</td></tr>'
                    % (p["glyph"] + "\ufe0e", label, esc(p["fmt"]), p.get("house") or "—"))
    if c["has_time"]:
        for nm in ("Ascendant", "Midheaven"):
            rows.append('      <tr><td class="g">·</td><td>%s</td><td class="pos">%s</td><td>—</td></tr>'
                        % (nm, esc(c["angles"][nm]["fmt"])))
    t["POSITIONS_ROWS"] = "\n".join(rows)

    if c["has_time"]:
        t["FOOTER_DATA"] = esc(
            "Computed with the Swiss Ephemeris for %s, %s, %s — tropical zodiac, whole-sign houses. "
            "The numerology is Pythagorean, from the full birth name, with four other traditions read "
            "alongside it." % (L["date_long"], L["time_label"], L["place"]))
    else:
        t["FOOTER_DATA"] = esc(
            "Computed with the Swiss Ephemeris for %s at noon Universal Time, the time of birth not being "
            "known — tropical zodiac, no houses or angles. The numerology is Pythagorean, from the full birth "
            "name, with four other traditions read alongside it." % L["date_long"])

    with open(WHEEL_JS, encoding="utf-8") as f:
        wheel_js = f.read()
    t["WHEEL_SCRIPT"] = ("<script>window.NATAL_WHEEL=%s;</script>\n<script>\n%s\n</script>"
                         % (json.dumps(c["wheel"], ensure_ascii=False), wheel_js))
    return t


def render(template, c):
    flags = {"has_time": bool(c["has_time"]), "no_time": not c["has_time"],
             "masters": bool(c["numerology"]["masters"])}

    def cond(m):
        name = m.group(1)
        if name not in flags:
            sys.exit("build.py: unknown condition <!-- @if %s -->" % name)
        return m.group(2) if flags[name] else ""
    out = re.sub(r"<!-- @if (\w+) -->(.*?)<!-- @endif -->", cond, template, flags=re.S)
    t = tokens(c)

    def tok(m):
        key = m.group(1)
        if key not in t:
            sys.exit("build.py: token {{%s}} has no value — add it to tokens() or make it a {{WRITE: …}} slot" % key)
        return t[key]
    return re.sub(r"\{\{([A-Z][A-Z0-9_]*)\}\}", tok, out)


def build(args):
    with open(args.chart, encoding="utf-8") as f:
        c = json.load(f)
    if c.get("schema") != "natal-report/chart.v1":
        sys.exit("build.py: %s is not a natal-report/chart.v1 file" % args.chart)
    with open(args.template or TEMPLATE, encoding="utf-8") as f:
        template = f.read()
    out = args.out or os.path.join(os.path.dirname(os.path.abspath(args.chart)), "report.html")
    if os.path.exists(out) and not args.force:
        sys.exit("build.py: %s exists — it may hold written prose. Pass --force to overwrite." % out)
    html_out = render(template, c)
    with open(out, "w", encoding="utf-8") as f:
        f.write(html_out)
    slots = len(re.findall(r"\{\{WRITE:", html_out))
    print("wrote %s — %d writer slots to fill ({{WRITE: …}}); run check-report.py when done" % (out, slots))


def find_chrome():
    env = os.environ.get("CHROME")
    for cand in ([env] if env else []) + CHROME_CANDIDATES:
        if cand and os.path.isfile(cand):
            return cand
    sys.exit("build.py: no Chrome/Chromium found — set CHROME=/path/to/binary")


def pdf(args):
    with open(args.report, encoding="utf-8") as f:
        h = f.read()
    if "{{" in h:
        sys.exit("build.py: %s still has unfilled {{ slots — finish the draft and run check-report.py first" % args.report)
    with open(PRINT_CSS, encoding="utf-8") as f:
        css = f.read()
    head = h.split("<head", 1)[0]
    if "data-theme=" in head:
        h = re.sub(r'(<html[^>]*?)data-theme="[^"]*"', r'\1data-theme="light"', h, count=1)
    else:
        h = h.replace("<html", '<html data-theme="light"', 1)
    h = h.replace("</body>", css + "\n</body>", 1)
    m = re.search(r"<h1>(.*?)</h1>", h, re.S)
    name = html.unescape(re.sub(r"<[^>]+>", "", m.group(1))).strip() if m else "report"
    out = args.out or os.path.join(os.path.dirname(os.path.abspath(args.report)), name + SUFFIX + ".pdf")
    pre = os.path.splitext(os.path.abspath(args.report))[0] + "-print.html"
    with open(pre, "w", encoding="utf-8") as f:
        f.write(h)
    cmd = [find_chrome(), "--headless=new", "--disable-gpu", "--virtual-time-budget=25000",
           "--run-all-compositor-stages-before-draw", "--no-pdf-header-footer",
           "--print-to-pdf=" + os.path.abspath(out), "file://" + pre]
    r = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True)
    if r.returncode != 0 or not os.path.isfile(out):
        sys.exit("build.py: Chrome failed (%d): %s" % (r.returncode, r.stderr.strip()[-800:]))
    print("wrote %s\n(print wrapper kept at %s)\nNow open the PDF and look: the cover, one card-heavy spread, the last page."
          % (out, pre))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("chart", nargs="?", help="chart.json (draft mode)")
    ap.add_argument("--pdf", metavar="REPORT_HTML", help="export this finished report to PDF")
    ap.add_argument("-o", "--out", help="output path (report.html, or the .pdf)")
    ap.add_argument("--template", help="override the house template path")
    ap.add_argument("--force", action="store_true", help="overwrite an existing report.html")
    args = ap.parse_args()
    if args.pdf:
        args.report = args.pdf
        pdf(args)
    elif args.chart:
        build(args)
    else:
        ap.error("give chart.json to draft, or --pdf report.html to export")


if __name__ == "__main__":
    main()
