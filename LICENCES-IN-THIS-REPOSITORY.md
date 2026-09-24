# What is licensed how

This repository holds four different kinds of thing, and one licence would be
wrong for at least two of them. Each is stated here rather than left to a
single file at the root, because a blanket licence would quietly give away the
identity, and silence gives away nothing at all: with no statement, default
copyright applies and nobody may reuse any of it.

None of this covers **the corpus itself**, which is CC BY 4.0 and is described
in `docs/guide/licence.md`. The corpus is not in this repository.

| What | Licence |
|---|---|
| Code: `tools/`, `scripts/`, the site's configuration and theme | AGPL-3.0-or-later, text in `LICENSE` |
| Documentation prose: `docs/**/*.md`, `README.md` | CC BY 4.0 |
| Identity: `brand/**` | All rights reserved, with the narrow permission below |
| Webfonts: `docs/public/fonts/` | SIL Open Font License 1.1, text in `docs/public/fonts/OFL.txt` |

## Why the identity is not under the code licence

The obvious thing to do here is drop one AGPL file at the root and move on.
That would put the Pentimento mark and wordmark under a licence that permits
modification and redistribution, and the mark would then be free to brand a
modified corpus, a degraded fork, or a mirror whose provenance nobody has
checked.

For a dataset whose entire argument is that its provenance is traceable, a
freely relicensable identity is not a theoretical problem. It is the one asset
whose value is that it cannot be applied to something else.

So `brand/` is reserved, with one permission that covers every honest use:

> You may reproduce the Pentimento mark, wordmark and lockups **unmodified**
> to refer to this project: in a paper, a slide, an article, a link preview or
> a list of datasets. You may scale them. You may not alter, recolour or
> recombine them, use them to identify anything that is not this project, or
> imply endorsement.

If you want to do something this does not cover, ask.

## Why the prose is CC BY 4.0 rather than AGPL

The documentation is copied around by design. It is reproduced on the Internet
Archive item, the HuggingFace dataset card and the Kaggle page, and a reader
quoting the splitting guidance into their own methods section is doing the
thing it exists for. AGPL makes that awkward and does nothing useful for
prose. CC BY 4.0 matches the corpus, so the same attribution habit covers
both.

## Attribution

For the code and the prose, credit **Daniel Iwugo** and link to
<https://github.com/elementmerc/pentimento>.
