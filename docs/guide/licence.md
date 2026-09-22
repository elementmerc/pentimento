# Licence and attribution

**The collection is published under CC BY 4.0.** That is the strictest
obligation present in it, not the loosest, so complying with it is sufficient
for every file. Where a file's own record names something looser, you may rely
on that instead.

## What is actually in there

| Licence | Covers |
|---|---|
| CC0 | 2,597 |
| CC BY 2.0 | 2,596 |
| Public domain | 1,974 |
| CC BY 4.0 | 1,808 |
| CC BY 3.0 | 838 |
| CC BY 2.5 | 185 |
| CC BY 1.0 | 2 |

**5,453 of 10,000 covers require attribution**, which is 54.5%.

## The credit line is already written

Every cover record carries an `attribution` field with a ready-made line, in
the order Creative Commons itself recommends: title, creator, licence with its
URL, source, and a statement of what was changed. Every cover in this corpus
is a crop, so that's part of the line, not an afterthought:

```
"File:Downtown Hagerstown on Franklin Street.jpg", by Charlotte Jackson,
CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/), via Wikimedia
Commons, https://commons.wikimedia.org/wiki/..., cropped
```

A stego image's own record carries a longer version of the same line, ending
in what was done beyond the crop ("cropped, then modified to carry a hidden
payload" for the stego half, "cropped, and re-encoded as the control half of a
pair" for its clean twin), because a reader holding only that file has no
other way to learn what happened to it. Stego images also inherit their
cover's licence under `cover_licence`, so a reader who downloads one arm and
never opens the cover tier still has everything the licence asks of them.

## Citing it

`CITATION.cff` ships beside the shards. It's [Citation File
Format](https://citation-file-format.github.io/), which is plain YAML, so you
can read it as it stands or hand it to a reference manager that speaks CFF.

None of the four places the corpus is published renders it into a formatted
citation for you, so copy the fields out yourself.

## If something looks wrong

The manifest is authoritative, not this page. If a file's record disagrees with
anything written here, the record is right and the page is stale; please say so.
