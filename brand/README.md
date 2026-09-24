# Pentimento, brand assets

Visual identity for **Pentimento**, a steganalysis corpus with its licences
attached. Iwugo Industries.

The name is the brief. In painting, a *pentimento* is the earlier image showing
through as the upper layer turns translucent, and conservators find them with
infrared reflectography and X-radiography. It is the same problem as
steganalysis and the same word, so the identity is literal rather than
decorative: **two squares, one behind the other, the front one just translucent
enough that the back one shows through the overlap.** That overlap is the mark.

## Palette

| Role | Hex | Use |
|---|---|---|
| Ink | `#1D1D1F` | The surface square, body text, dark ground |
| Blue | `#0071E3` | The layer underneath, links, accents |
| Ground | `#F5F5F7` | Light ground, the default page |
| Paper | `#FFFFFF` | Cards, the reversed mark |
| Muted | `#86868B` | Captions, secondary text on light |
| Muted dark | `#6E6E73` | Body text that is not a heading |
| Line | `#D2D2D7` | Rules, borders, dividers |

Contrast, measured, because a light palette is where this goes wrong. **Ground
and Paper are different grounds and they give different answers**, so both are
listed: an earlier version of this table named Ground and carried Paper's
numbers, which made Blue look like it passed on the page it is actually used
on.

| Pair | on Ground `#F5F5F7` | on Paper `#FFFFFF` | Verdict |
|---|---|---|---|
| Ink | 15.5:1 | 16.8:1 | body text, any size |
| Blue | 4.31:1 | 4.70:1 | **fails AA on Ground**, see below |
| Muted | 3.33:1 | 3.62:1 | 18px and above only, and only on Paper |
| Muted dark | 4.66:1 | 5.07:1 | body text |

Reversed, Paper on Ink is 16.8:1.

**Blue at `#0071E3` is below the 4.5:1 floor on Ground**, which is the default
page. Use it for the mark, for graphic accents and for large text. For links
and body-size text on Ground, use the darker `#0067CF`, which measures 5.02:1
and is what the documentation site ships.

Never put Blue on Ink as body text (3.58:1). On dark grounds use Paper for text
and keep Blue for the mark and for graphic accents.

## Typography

- **Display and wordmark:** Fraunces, 600. Old-style, warm, and doing the art
  half of the idea.
- **Body:** Hanken Grotesk. Shared with the sibling project on purpose, so Pentimento
  reads as a sibling rather than a stranger.
- **Data:** IBM Plex Mono. Counts, hashes, licence codes, arm names. Anything a
  reader might compare character by character.

| Level | Size / leading | Face |
|---|---|---|
| Display | 52 / 1.08 | Fraunces 600 |
| Title | 30 / 1.24 | Fraunces 600 |
| Lede | 21 / 1.5 | Hanken Grotesk 400 |
| Body | 17 / 1.6 | Hanken Grotesk 400 |
| Caption | 14 / 1.55 | Hanken Grotesk 400 |
| Data | 13 | IBM Plex Mono 400 |
| Eyebrow | 12, 0.16em, caps | IBM Plex Mono 500 |

The wordmark is set in Fraunces 600 at `-0.015em` tracking, sentence case. Never
uppercase it.

## Files

### logo/
- `mark.svg` — primary, Blue behind Ink. Use this by default
- `mark-reversed.svg` — for Ink and other dark grounds
- `mark-mono-ink.svg` / `mark-mono-white.svg` — one ink, for etching, embroidery
  and anywhere colour is not available. The back square drops to 45% of the same
  ink rather than changing hue
- `lockup-horizontal.svg` / `-dark.svg` — mark, wordmark and descriptor in a row
- `lockup-stacked.svg` / `-dark.svg` — mark above wordmark

### favicon/
- `favicon.svg` — modern browsers

### icon/
- `icon-512.svg` — PWA and app icon
- `maskable-512.svg` — Android maskable, mark inset into the safe zone on Ground

### social/
- `readme-banner-1280x320.svg` / `-dark.svg` — top of README
- `github-social-1280x640.svg` — GitHub repo social preview
- `kaggle-cover-1200x600.svg` / `.png` — the Kaggle dataset cover. Kaggle's
  minimum is 564x284; this is 2:1 like the GitHub card so one ratio serves
  both. **The PNG is the file Kaggle takes**, rendered from the SVG with
  `rsvg-convert -w 1200 -h 600`, and the three brand faces must be installed
  or the render silently substitutes generic fonts and looks like the brand
  without being it

**Figures on these cards are checked.** `tools/make_figures.py --check` reads
every SVG in `social/` and fails on any thousands-separated number it does not
recognise, because three of these cards carried "341,997 pairs" for days after
the corpus grew to 344,357, and one of them is the GitHub social preview: the
first image anybody sees. A comment is exempt, so recording an old value as
history is fine.

## Clear space and minimum size

Clear space on every side is **twice the front square's corner radius**, which
is 14 units in the 64-unit viewBox. Nothing enters that margin.

- Mark: minimum **16 px**. Below that use `mark-mono-*`, because the 8% opacity
  difference in the overlap stops resolving
- Horizontal lockup: minimum **120 px** wide. Below that, stack it
- Stacked lockup: minimum **96 px** wide

## Do not

- Do not separate the two squares. The overlap is the entire idea
- Do not square up the offset, or align the two squares on an axis
- Do not make the front square fully opaque. At 100% there is no pentimento
- Do not recolour the back square to anything but Blue, except in the mono marks
- Do not add a gradient, a shadow or a glow
- Do not set the wordmark in anything but Fraunces, and never in caps
- Do not put Blue text on Ink

## Rasterising

The sources are SVG. PNG exports, when a host demands one:

```sh
for s in 16 32 48 180 192 512; do
  rsvg-convert -w $s -h $s docs/brand/logo/mark.svg -o mark-$s.png
done
rsvg-convert -w 1280 -h 640 docs/brand/social/github-social-1280x640.svg \
  -o github-social-1280x640.png
```

`rsvg-convert` ships with librsvg. The SVGs reference Fraunces, Hanken Grotesk
and IBM Plex Mono by name, so install them before rasterising anything with text
in it or the fallback will be substituted silently.

## Where this came from

Chosen from a board of eight directions: the original concept in its own warm
palette, five alternatives each with a distinct mark, and the concept recoloured
into two other palettes. This is the third of those, the concept on Apple's
neutrals. It was picked because it is the only one that reads on paper, which
matters for a corpus whose readers are writing papers.

## Licence

**Reserved, not open.** Everything in this directory is all rights reserved,
with one permission: you may reproduce the mark, wordmark and lockups
UNMODIFIED to refer to this project, and you may scale them. You may not
alter, recolour or recombine them, use them for anything that is not this
project, or imply endorsement.

This is deliberately narrower than the AGPL that covers the code. A mark that
can be modified and reapplied is a mark that can brand a degraded fork of a
corpus whose whole argument is traceable provenance. See
`../LICENCES-IN-THIS-REPOSITORY.md`.

## Recorded exceptions

Deviations from the rules above that were made deliberately, with the reason,
so nobody removes one later believing it to be a mistake. A deviation that is
not written down here is a mistake.

- **`docs/public/favicon.svg` is not byte-identical to `favicon/favicon.svg`.**
  The site's copy carries a `prefers-color-scheme` block so the front square is
  Ink on a light browser chrome and Paper on a dark one. The kit ships one
  fixed mark per ground, and a favicon cannot know which ground it will be
  drawn on, so a fixed one disappears in one of the two. The marks and lockups
  in `docs/public/` ARE byte-identical; this is the only file that differs.

- **The documentation site's hero mark sits on a blurred glow**, against "Do not
  add a gradient, a shadow or a glow". Decided by the operator on 2026-09-24
  after seeing the home page with and without it. It is the mark's own two
  colours in the mark's own order, blurred well past any edge, so it reads as
  light rather than as a shape competing with the two squares. It applies to
  that one hero image and nowhere else: the rule still holds everywhere.
