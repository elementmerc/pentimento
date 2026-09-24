#!/usr/bin/env python3
# Author:  Daniel Iwugo
# Comment: Christ is King
# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 Daniel Iwugo
"""Draw the README figures from the corpus's own numbers.

THIS FILE IS THE GENERATOR, NOT A SKETCH
----------------------------------------
Every figure is built by a function from the arrays in FIGURES below, so the
numbers in the drawing are the measured numbers and changing one changes the
picture. The last set of figures on this project was hand-drawn, and the
consequence is still visible: the README banner shipped "344,348 pairs" and
"29 arms" long after the corpus held 341,997 pairs across 39.

HOUSE STYLE
-----------
Flat vector, real `<text>` elements and no rasterised labels, so a figure stays
hand editable after export. One ink, one faint, and semantic colour spent only
where it carries the argument. Blue is the mark's own accent and reads as "this
corpus"; rust reads as "closed to you"; flat grey reads as "no signal".

WEBFONTS DO NOT LOAD ON GITHUB
------------------------------
An SVG embedded in a README renders in the reader's fallback fonts, so every
stack here ends in a generic family and nothing depends on Fraunces arriving.
The brand faces are named first so the same files look right on the docs site,
where they do load.

Usage::

    python3 tools/make_figures.py            # writes docs/media/*.svg
    python3 tools/make_figures.py --check    # fails if a file would change
"""
from __future__ import annotations

import argparse
import pathlib
import re
import sys

# ── The measured corpus ──────────────────────────────────────────────────
# Verified against the packed index on 2026-09-22 by
# `stegobench/generators/check_docs_figures.py`, which derives these from the
# release rather than restating them. If you change one here, run that.

COVERS = 10_000
PAIRS = 344_357
STEGO_ARMS = 35
CLEAN_ARMS = 4

#: family, label, rates, samples per arm, domain
ARMS = [
    ("hugo", "HUGO", ["0.05", "0.1", "0.2", "0.4"], 10_000, "spatial"),
    ("wow", "WOW", ["0.05", "0.1", "0.2", "0.4"], 10_000, "spatial"),
    ("suniward", "S-UNIWARD", ["0.05", "0.1", "0.2", "0.4"], 10_000, "spatial"),
    ("hill", "HILL", ["0.05", "0.1", "0.2", "0.4"], 10_000, "spatial"),
    ("mipod", "MiPOD", ["0.05", "0.1", "0.2", "0.4"], 10_000, "spatial"),
    ("juniward", "J-UNIWARD", ["0.05", "0.1", "0.2", "0.4"], 10_000, "dct"),
    ("uerd", "UERD", ["0.05", "0.1", "0.2", "0.4"], 10_000, "dct"),
    ("steghide", "steghide", ["5%", "20%", "50%"], 10_000, "tool"),
    ("outguess", "outguess", ["5%", "20%", "50%"], 8_119, "tool"),
    ("append", "appended data", ["one fixed payload"], 10_000, "control"),
]

#: The licence spread, from the cover manifest.
LICENCES = [
    ("CC0", 2_625),
    ("CC BY 2.0", 2_624),
    ("Public domain", 1_922),
    ("CC BY 4.0", 1_794),
    ("CC BY 3.0", 850),
    ("CC BY 2.5", 183),
    ("CC BY 1.0", 2),
]
ATTRIBUTION_REQUIRED = 5_453

#: The three corpora a reader is choosing between, and what each permits.
#: Sources: stegobench/docs/design/cover-source-licensing.md
CORPORA = [
    ("BOSSbase", "10,000", "No licence survives. The organisers claimed rights "
     "and the terms died with their host", True, False),
    ("ALASKA2", "80,000", "CC BY-NC-ND. The no-derivatives term forbids "
     "publishing a stego image made from a cover", True, False),
    ("Pentimento", "10,000", "CC0, public domain and CC BY only. Every file "
     "carries its own terms and its own credit line", True, True),
]

#: The three measurements lost to a pairing confound, which is why the rule is
#: enforced structurally rather than restated. No longer drawn: the operator
#: took the block off F3 on 2026-09-22, and the README carries it as prose
#: beneath the figure. Kept here because it is the reason the rule exists.
CONFOUNDS = [
    ("outguess re-encoded at quality 75 whatever it was given",
     "the halves came from different quality settings"),
    ("two different encoders wrote the two halves",
     "the detector could read the encoder, not the payload"),
    ("same encoder, different number of writes",
     "jpeglib prepends a JFIF APP0 every time, so one half carried two and "
     "the other three"),
]

# ── Palette ──────────────────────────────────────────────────────────────
LIGHT = {
    "ground": "#F5F5F7", "card": "#FFFFFF", "ink": "#1D1D1F",
    "mid": "#6E6E73", "faint": "#86868B", "line": "#D2D2D7",
    "grid": "#E8E8EA", "accent": "#0071E3", "accent_soft": "#D6E9FC",
    "closed": "#A8341F", "closed_soft": "#F2DED8", "flat": "#C7C7CC",
}
DARK = {
    "ground": "#1D1D1F", "card": "#262628", "ink": "#FFFFFF",
    "mid": "#A1A1A6", "faint": "#86868B", "line": "#3A3A3C",
    "grid": "#2F2F31", "accent": "#409CFF", "accent_soft": "#16324D",
    "closed": "#E0705A", "closed_soft": "#3A211B", "flat": "#48484A",
}

DISPLAY = "Fraunces, Georgia, 'Times New Roman', serif"
BODY = "'Hanken Grotesk', system-ui, -apple-system, 'Segoe UI', sans-serif"
MONO = "'IBM Plex Mono', ui-monospace, 'SF Mono', Menlo, monospace"


def wrap(s: str, width: int) -> list[str]:
    """Break text on spaces, never mid-word.

    The first draft sliced at a fixed column and rendered "its own te / rms" in
    a published figure. SVG has no line box, so every wrap here is explicit.
    """
    lines, line = [], ""
    for word in s.split():
        trial = f"{line} {word}".strip()
        if len(trial) > width and line:
            lines.append(line)
            line = word
        else:
            line = trial
    if line:
        lines.append(line)
    return lines


def esc(s: str) -> str:
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def text(x, y, s, *, size=13, fill="ink", weight=400, anchor="start",
         font=BODY, track=None, opacity=None, P=None):
    bits = [f'x="{x}"', f'y="{y}"', f'fill="{P[fill] if fill in P else fill}"',
            f'font-family="{font}"', f'font-size="{size}"']
    if weight != 400:
        bits.append(f'font-weight="{weight}"')
    if anchor != "start":
        bits.append(f'text-anchor="{anchor}"')
    if track:
        bits.append(f'letter-spacing="{track}"')
    if opacity:
        bits.append(f'opacity="{opacity}"')
    return f'<text {" ".join(bits)}>{esc(s)}</text>'


def rect(x, y, w, h, *, fill=None, stroke=None, sw=1, rx=0, opacity=None, P=None):
    bits = [f'x="{x}"', f'y="{y}"', f'width="{max(0, w)}"', f'height="{max(0, h)}"']
    bits.append(f'fill="{(P[fill] if fill in P else fill) if fill else "none"}"')
    if stroke:
        bits.append(f'stroke="{P[stroke] if stroke in P else stroke}"')
        bits.append(f'stroke-width="{sw}"')
    if rx:
        bits.append(f'rx="{rx}"')
    if opacity:
        bits.append(f'opacity="{opacity}"')
    return f'<rect {" ".join(bits)}/>'


def line(x1, y1, x2, y2, *, stroke="line", sw=1, dash=None, P=None):
    bits = [f'x1="{x1}"', f'y1="{y1}"', f'x2="{x2}"', f'y2="{y2}"',
            f'stroke="{P[stroke] if stroke in P else stroke}"',
            f'stroke-width="{sw}"', 'stroke-linecap="round"']
    if dash:
        bits.append(f'stroke-dasharray="{dash}"')
    return f'<line {" ".join(bits)}/>'


def svg(w, h, body, label, P):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
            f'width="{w}" height="{h}" role="img" aria-label="{esc(label)}">\n'
            f'{rect(0, 0, w, h, fill="ground", P=P)}\n{body}\n</svg>\n')


# ── F1 · what is in it ───────────────────────────────────────────────────
def fig_arms(P):
    rows = len(ARMS)
    top, rowh, lx, cx, cw = 130, 34, 48, 300, 108
    table_end = top + rows * rowh
    summary = table_end + 34
    W, H = 1200, summary + 96
    g = []
    g.append(text(48, 60, "What is in it", size=32, weight=600, font=DISPLAY, P=P))
    g.append(text(48, 88, f"{PAIRS:,} matched pairs across {STEGO_ARMS} stego arms, "
                          f"plus {CLEAN_ARMS} clean arms that are the other half "
                          f"of every pair.", size=15, fill="mid", P=P))

    g.append(text(lx, top - 14, "FAMILY", size=10, fill="faint", weight=600,
                  track="0.1em", P=P))
    g.append(text(cx, top - 14, "PAYLOAD RATE, AND SAMPLES AT EACH", size=10,
                  fill="faint", weight=600, track="0.1em", P=P))

    colour = {"spatial": "accent", "dct": "accent", "tool": "ink", "control": "flat"}
    for i, (_key, label, rates, n, domain) in enumerate(ARMS):
        y = top + i * rowh
        g.append(line(lx, y + 26, W - 48, y + 26, stroke="grid", P=P))
        g.append(text(lx, y + 15, label, size=14, weight=600, P=P))
        dom = {"spatial": "spatial", "dct": "JPEG DCT", "tool": "end-user tool",
               "control": "control"}[domain]
        g.append(text(lx + 150, y + 15, dom, size=11, fill="faint", P=P))
        for j, r in enumerate(rates):
            x = cx + j * cw
            full = n >= 10_000
            # "control" is a word rather than a rate, so it needs a wider pill
            # than "0.05" does; at one column it sat on top of its own count.
            pw = (2 * cw - 12) if domain == "control" else (cw - 12)
            g.append(rect(x, y, pw, 22, fill=colour[domain],
                          opacity=0.14 if full else 0.09, rx=3, P=P))
            g.append(text(x + 10, y + 15, r, size=12, weight=600,
                          fill=colour[domain] if domain != "control" else "mid", P=P))
            g.append(text(x + pw - 10, y + 15, f"{n:,}", size=11, fill="faint",
                          anchor="end", font=MONO, P=P))

    g.append(line(48, summary - 16, W - 48, summary - 16, stroke="line", P=P))
    for i, (n, cap) in enumerate([
            (f"{COVERS:,}", "cover photographs"),
            (f"{PAIRS:,}", "matched stego pairs"),
            (f"{STEGO_ARMS + CLEAN_ARMS}", "arms in total"),
            ("48 GB", "everything, or one arm at 1.3 GB")]):
        x = 48 + i * 290
        g.append(text(x, summary + 26, n, size=30, weight=600, font=MONO,
                      fill="accent", P=P))
        g.append(text(x, summary + 50, cap, size=12, fill="mid", P=P))
    return svg(W, H, "\n".join(g),
               f"The Pentimento corpus: {PAIRS:,} matched pairs across "
               f"{STEGO_ARMS} stego arms and {CLEAN_ARMS} clean arms", P)


# ── F2 · why it exists ───────────────────────────────────────────────────
def fig_licences(P):
    top, rowh = 140, 112
    lic_y = top + len(CORPORA) * rowh + 24
    W, H = 1200, lic_y + 150
    g = []
    g.append(text(48, 60, "Why it exists", size=32, weight=600, font=DISPLAY, P=P))
    for i, ln in enumerate(wrap(
            "The standard corpora in this field can be used and cannot be "
            "republished. A stego image is a derivative work, so the arms built "
            "from them cannot be shared either.", 96)):
        g.append(text(48, 88 + i * 21, ln, size=15, fill="mid", P=P))

    for i, (name, n, why, use, publish) in enumerate(CORPORA):
        y = top + i * rowh
        mine = name == "Pentimento"
        g.append(rect(48, y, W - 96, rowh - 18, fill="card",
                      stroke="accent" if mine else "line",
                      sw=1.6 if mine else 1, rx=4, P=P))
        g.append(text(72, y + 34, name, size=20, weight=600, font=DISPLAY,
                      fill="accent" if mine else "ink", P=P))
        g.append(text(72, y + 58, f"{n} covers", size=12, fill="faint",
                      font=MONO, P=P))
        for j, ln in enumerate(wrap(why, 58)):
            g.append(text(240, y + 32 + j * 20, ln, size=13, fill="mid", P=P))

        for j, (label, ok) in enumerate((("use it", use), ("republish it", publish))):
            x = W - 340 + j * 150
            tone = "accent" if ok else "closed"
            g.append(rect(x, y + 20, 132, 48, fill=f"{tone}_soft", rx=4, P=P))
            g.append(text(x + 66, y + 42, "yes" if ok else "no", size=17,
                          weight=600, anchor="middle", fill=tone, P=P))
            g.append(text(x + 66, y + 60, label, size=11, anchor="middle",
                          fill="mid", P=P))

    g.append(text(48, lic_y, "Every Pentimento cover, by licence", size=14,
                  weight=600, P=P))
    bx, bw, bh = 48, W - 96, 36
    run = 0
    for i, (lic, n) in enumerate(LICENCES):
        w = bw * n / COVERS
        g.append(rect(bx + run, lic_y + 16, max(2, w - 2), bh, fill="accent",
                      opacity=round(0.9 - i * 0.11, 2), rx=2, P=P))
        if w > 150:
            g.append(text(bx + run + 12, lic_y + 33, lic, size=12, weight=600,
                          fill="#FFFFFF", P=P))
            g.append(text(bx + run + 12, lic_y + 49, f"{n:,}", size=11,
                          fill="#FFFFFF", font=MONO, opacity=0.85, P=P))
    # The four small slices cannot carry a label inside them, so they get a
    # line of their own rather than a silent gap.
        run += w
    small = ", ".join(f"{lic} {n:,}" for lic, n in LICENCES if bw * n / COVERS <= 150)
    g.append(text(48, lic_y + bh + 38, f"and {small}", size=11.5, fill="faint", P=P))
    for i, ln in enumerate(wrap(
            f"{ATTRIBUTION_REQUIRED:,} of {COVERS:,} covers require a credit "
            f"line, and every stego image made from one inherits it. The line "
            f"is already written into each record.", 96)):
        g.append(text(48, lic_y + bh + 68 + i * 20, ln, size=13, fill="mid", P=P))
    return svg(W, H, "\n".join(g),
               "Licence comparison: BOSSbase and ALASKA2 may be used but not "
               "republished; Pentimento may be both", P)


# ── F3 · the rule that makes it worth anything ───────────────────────────
def fig_pairs(P):
    W, H = 1200, 324
    g = []
    g.append(text(48, 60, "Pairs that differ only in the payload", size=32,
                  weight=600, font=DISPLAY, P=P))
    g.append(text(48, 88, "Both halves come off the same encoder, through the same "
                          "code path, in the same number of writes.", size=15,
                  fill="mid", P=P))

    y = 130
    g.append(rect(48, y, 250, 76, fill="card", stroke="line", rx=4, P=P))
    g.append(text(70, y + 32, "One photograph", size=15, weight=600, P=P))
    g.append(text(70, y + 54, "from Wikimedia Commons", size=11, fill="faint", P=P))

    g.append(line(298, y + 38, 350, y + 38, stroke="faint", P=P))
    g.append(line(350, y + 38, 350, y - 6, stroke="faint", P=P))
    g.append(line(350, y + 38, 350, y + 120, stroke="faint", P=P))
    g.append(line(350, y - 6, 396, y - 6, stroke="faint", P=P))
    g.append(line(350, y + 120, 396, y + 120, stroke="faint", P=P))

    g.append(rect(400, y - 34, 300, 64, fill="card", stroke="line", rx=4, P=P))
    g.append(text(422, y - 8, "Nothing written", size=15, weight=600, P=P))
    g.append(text(422, y + 14, "the clean half", size=11, fill="faint", P=P))

    g.append(rect(400, y + 90, 300, 64, fill="card", stroke="accent", sw=1.6,
                  rx=4, P=P))
    g.append(text(422, y + 116, "Payload written", size=15, weight=600,
                  fill="accent", P=P))
    g.append(text(422, y + 138, "the only difference", size=11, fill="faint", P=P))

    g.append(line(700, y - 2, 752, y + 30, stroke="faint", P=P))
    g.append(line(700, y + 122, 752, y + 90, stroke="faint", P=P))
    g.append(rect(756, y + 22, 396, 76, fill="accent_soft", rx=4, P=P))
    g.append(text(780, y + 50, f"{PAIRS:,} pairs", size=22, weight=600, font=MONO,
                  fill="accent", P=P))
    g.append(text(780, y + 74, "containers verified byte-identical at pack time",
                  size=12, fill="mid", P=P))
    return svg(W, H, "\n".join(g),
               "How a matched pair is made: both halves from one photograph "
               "through one encoder, differing only in the payload", P)


FIGURES = [
    ("01-what-is-in-it", fig_arms),
    ("02-why-it-exists", fig_licences),
    ("03-matched-pairs", fig_pairs),
]


def brand_figure_drift(brand: pathlib.Path) -> list[str]:
    """Figures quoted in the identity kit that this file does not recognise.

    The kit is drawn by hand from a design board, so nothing generated it and
    nothing checked it. Three of its cards carried "341,997 pairs" for days
    after the corpus grew to 344,357, and one of those cards is this project's
    GitHub social preview: the first image anybody sees.

    A thousands separator is the giveaway. SVG coordinates never carry one, so
    any number written `12,345` inside one of these files is a FIGURE about the
    corpus, and it has to be one of the figures above.

    Comments are stripped first, because a comment recording that an old value
    was once wrong is the opposite of drift.
    """
    allowed = {f"{n:,}" for n in (COVERS, PAIRS, ATTRIBUTION_REQUIRED,
                                  STEGO_ARMS + CLEAN_ARMS)}
    allowed |= {f"{count:,}" for _, count in LICENCES}
    allowed |= {f"{samples:,}" for *_, samples, _ in ARMS}

    problems = []
    for svg in sorted(brand.glob("*.svg")):
        body = re.sub(r"<!--.*?-->", "", svg.read_text(encoding="utf-8"),
                      flags=re.DOTALL)
        for figure in sorted(set(re.findall(r"\d{1,3}(?:,\d{3})+", body))):
            if figure not in allowed:
                problems.append(f"{svg}: {figure}")
    return problems


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out", default="docs/media")
    ap.add_argument("--brand", default="brand/social",
                    help="identity-kit cards, which quote figures by hand")
    ap.add_argument("--check", action="store_true",
                    help="fail if any file would change, rather than writing")
    args = ap.parse_args(argv)

    out = pathlib.Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    changed = []
    for name, fn in FIGURES:
        for suffix, palette in (("", LIGHT), ("-dark", DARK)):
            path = out / f"{name}{suffix}.svg"
            body = fn(palette)
            if args.check:
                if not path.is_file() or path.read_text() != body:
                    changed.append(str(path))
            else:
                path.write_text(body)
                print(f"  {path}  {len(body):,} bytes")

    if args.check:
        if changed:
            print("these figures are out of date with the data in this file:",
                  file=sys.stderr)
            for c in changed:
                print(f"  {c}", file=sys.stderr)
            print("run `python3 tools/make_figures.py`", file=sys.stderr)
            return 1

        brand = pathlib.Path(args.brand)
        drift = brand_figure_drift(brand) if brand.is_dir() else []
        if drift:
            print("the identity kit quotes figures this file does not know:",
                  file=sys.stderr)
            for d in drift:
                print(f"  {d}", file=sys.stderr)
            print("These cards are drawn by hand and nothing else checks them. "
                  "Either the card is stale, or a figure changed here and the "
                  "card was not redrawn.", file=sys.stderr)
            return 1

        print(f"{len(FIGURES) * 2} figure(s) match the data they are drawn from")
        if brand.is_dir():
            cards = len(list(brand.glob('*.svg')))
            print(f"{cards} identity card(s) quote only figures this file knows")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
