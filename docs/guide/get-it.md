# Get it

The Core tier is 10,000 covers and 344,357 stego pairs, about 48 GB in total.
Covers and arms are packaged separately, so you can take one without the other.

## Where it is

| Host | Good for | Link |
|---|---|---|
| Internet Archive | The canonical copy. No account, no approval, permanent | [pentimento-core-v1](https://archive.org/details/pentimento-core-v1) |
| HuggingFace | Loading straight into a training pipeline | [the-malware-files/pentimento-core](https://huggingface.co/datasets/the-malware-files/pentimento-core) |
| Kaggle | Notebooks. Covers only, and the shards arrive unpacked (see below) | [elementmerc/pentimento-core](https://www.kaggle.com/datasets/elementmerc/pentimento-core) |

## Take only what you need

Shards are grouped one set per arm, so evaluating against WOW at 0.2 bits per
pixel does not mean downloading MiPOD to get it.

| Part | Size | What it is |
|---|---|---|
| Covers | 3.3 GB | The 10,000 clean photographs |
| One stego arm | ~1.3 GB | 10,000 images from one tool at one payload |
| Clean arms | 4.1 GB | The other half of every pair, all four of them |
| Everything | 48 GB | The covers plus all 39 arms |

## One arm, start to finish

This is the whole thing: fetch one shard of an arm and the matching shard of
its clean half, check them, read a sample. About 130 MB.

```bash
BASE=https://archive.org/download/pentimento-core-v1

# The paperwork first: it is small and it tells you what the rest is.
# -L matters: the Archive answers with a 302 to whichever storage node holds
# the item, and curl without it writes an empty file and reports success.
# -f matters for the same reason, the other way round: without it a 404 is
# saved as a file containing the error page.
curl -fLsO $BASE/README.md -O $BASE/SHA256SUMS-covers -O $BASE/SHA256SUMS-arms -O $BASE/load_pentimento.py

# One arm, and the clean half it is measured against.
curl -fLO $BASE/pentimento-core-wow-0200-00000.tar
curl -fLO $BASE/pentimento-core-clean-grey-00000.tar

# Check what arrived. A shard that fails here changed in transit.
grep -E 'wow-0200-00000|clean-grey-00000' SHA256SUMS-arms | sha256sum -c

# Read it. Nothing to install.
python3 load_pentimento.py pentimento-core-wow-0200-00000.tar
```

```
first sample: 000000
  bytes      63,550
  licence    {'artist': 'Aleksandrs Timofejevs', 'attribution': '"File:Asare8.JPG", by Aleksandrs Timofejevs, CC0 (https://creativecommons.org/publicdomain/zero/1.0/), via Wikimedia Commons, https://commons.wikimedia.org/wiki/File:Asare8.JPG, cropped, then modified to carry a hidden payload', 'credit': 'Own work', 'descriptionurl': 'https://commons.wikimedia.org/wiki/File:Asare8.JPG', 'licence': 'CC0', 'title': 'File:Asare8.JPG', 'usage_terms': 'Creative Commons Zero, Public Domain Dedication'}
  cover      08848.png
500 samples in pentimento-core-wow-0200-00000.tar
```

Note what the `attribution` string carries: the licence, **the licence URI**,
the source, and what was done to the image. CC BY requires the URI and
requires you to say the work was modified, so reproduce that line as it
stands. Rebuilding one from the other fields drops both and leaves you
crediting a photograph as though it were untouched.

Two things in that output surprise people. The licence prints as a whole record
rather than a name, because a stego sample carries its cover's full credit line
and not only the licence label. And sample `000000` is not cover `00000.png`:
sample keys count the arm from zero in the order it was packed, while cover
filenames were fixed when the covers were fetched. They're two separate
numberings and they only agree by accident. The `cover` line is the one to
read.

## If you just want to look at one

```bash
tar -xf pentimento-core-wow-0200-00000.tar 000000.png
tar -xf pentimento-core-clean-grey-00000.tar 000000.png --transform 's/^/clean-/'
```

You now have the same photograph twice: one carrying a hidden payload, one not.
They are 512x512 greyscale PNGs, and **they will look identical to you**, at
any zoom. That is the whole point of the field: if you could see the difference
there would be nothing to detect. The two files differ in about 3% of pixels,
each by one in the last bit of its brightness value, which no eye resolves.

Finding that difference without being told which is which is the problem this
corpus is for.

Then see [Loading and splitting](using-it) before you train on it, because a
random split will quietly flatter your results.

## Everything

```bash
# The Archive's own client handles resume and integrity.
pip install internetarchive
ia download pentimento-core-v1 --checksum
```

On HuggingFace:

```bash
pip install huggingface_hub
hf download the-malware-files/pentimento-core --repo-type dataset --local-dir pentimento
```

That pulls all 48 GB. To take one arm and the clean half it is measured
against, the same way the Archive example does:

```bash
hf download the-malware-files/pentimento-core --repo-type dataset \
  --local-dir pentimento \
  --include 'pentimento-core-wow-0200-*.tar' 'pentimento-core-clean-grey-*.tar'
```

## Smaller tiers

A tier is the first *n* covers of one fixed ordering, so a smaller tier is
always a prefix of a larger one. You can develop against Nano and evaluate on
Core without the two overlapping in a way that flatters your results.

| Tier | Covers | Covers only | With every arm |
|---|---|---|---|
| Nano | 200 | 66 MB | 1.0 GB |
| Lite | 1,000 | 327 MB | 4.8 GB |
| **Core** | **10,000** | **3.3 GB** | **48 GB** |

The nesting is exact rather than approximate: Lite's cover shard is the same
file, byte for byte, as Core's first cover shard.

**Core is the tier published on the Internet Archive today.** Nano and Lite are
built and packed; they are not up yet, and this page will link them when they
are.

## Check what you downloaded

Each part ships its own checksum file, `SHA256SUMS-covers` for the cover
shards and `SHA256SUMS-arms` for the arms. They are named per part because
every destination is flat: two files both called `SHA256SUMS` would land on
one name and the second would silently replace the first.

```bash
sha256sum -c SHA256SUMS-covers
```

Verify before use. A shard that does not match is a shard that changed in
transit, and it will read as a smaller corpus rather than as an error.

### On Kaggle, use the records instead

Kaggle extracts archives when they are uploaded and gives no way to refuse it,
so there `pentimento-core-00000.tar` is a folder called
`pentimento-core-00000/` holding the same members under the same names. The
bytes are identical. The container is gone, and `SHA256SUMS-covers` names
containers, so on that copy the command above reports every shard as missing.

Check it against each record's own checksum, which ships beside every image:

```bash
python load_pentimento.py --verify pentimento-core-00000/
```

That is the finer check of the two, because it names the image that is wrong
rather than the shard holding it. `load_pentimento.py` reads a folder and a
tar alike, so the reading examples elsewhere in this guide work either way.
The one thing that does not is WebDataset, which needs real shards; see the
note beside it on the [using it](./using-it) page.
