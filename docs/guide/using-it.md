# Loading and splitting

## Loading

Shards are [WebDataset](https://github.com/webdataset/webdataset) tar files.
Each sample is an image and a JSON record sharing a basename:

```
pentimento-core-wow-0200-00000.tar
  000000.png     the image
  000000.json    its record, licence included
```

`load_pentimento.py` ships with the corpus and reads a shard with nothing
installed:

```bash
python3 load_pentimento.py pentimento-core-wow-0200-00000.tar
```

For training, any WebDataset loader reads the shards unchanged:

::: tip On the Kaggle copy, add the suffix
The Kaggle shards are named `pentimento-core-00000.tar.bin`, because Kaggle
unpacks anything ending in `.tar`. They are ordinary tars, so WebDataset reads
them; the brace pattern just needs the longer name:
`pentimento-core-{00000..00009}.tar.bin`
:::


`.decode("pil")` needs Pillow, and installing `webdataset` does not bring it.
Without it the traceback ends in `webdataset.autodecode.DecodingError` with no
message, and the real cause (`ModuleNotFoundError: No module named 'PIL'`) is
thirty lines further up:

```bash
pip install webdataset pillow
```

```python
import webdataset as wds

# One shard, which is what the Get it page has you download. The whole arm is
# `{00000..00019}`, and that pattern matches nothing until all twenty are here.
dataset = (
    wds.WebDataset("pentimento-core-wow-0200-00000.tar")
    .decode("pil")
    .to_tuple("png;jpg;jpeg", "json")
)
```

The image extension is not the same in every arm: the spatial arms are PNG and
the JPEG arms are JPEG, so ask for all three or the JPEG arms come back empty.

Split by cover before this, not after. The next section is why.

## Split by cover, never at random

This is the one thing that will quietly ruin a result.

A cover and its stego versions are near-identical: same scene, same camera,
same everything except a handful of changed bits. Split at random and a cover
lands in training while its own stego copy lands in test. The classifier
recognises the photograph, scores beautifully, and has learned nothing about
hiding.

```
    random split                     split by cover
    ────────────                     ──────────────
    train: 09710.png (clean)         train: every version of 09710
           09710.png (wow 0.2)  ✗
    test:  09710.png (hugo 0.1)      test:  every version of 05047
```

Group by the cover. Results in the literature differ by several accuracy points
on the choice of split alone.

### Which field names the cover

Arm shards and cover shards name it differently, so a fold function written
against one raises `KeyError` on the other.

| Shard | Field | Example |
|---|---|---|
| Any of the 39 arm shards, stego or clean | `source_png` | `"source_png": "09710.png"` |
| The cover shards, `pentimento-core-NNNNN.tar` | `file` | `"file": "09710.png"` |

The values are the same namespace, so `record.get("source_png") or
record["file"]` covers both.

### Two split rules ship with the corpus, and they disagree

Both partition by cover, so neither leaks. They're different partitions, so
mixing them puts the same photograph on both sides of the boundary and undoes
the point of either.

| | `split` field | `fold()` in `SPLITS.md` |
|---|---|---|
| What it is | A fixed `train` / `test` label, 8,029 and 1,971 covers | A recipe: `sha256(cover)[:8] % folds` |
| Where it lives | Cover records only, alongside `split_salt: "pentimento-v1"` | Nowhere; you write it |
| Works from an arm alone | No, you need the cover tier to join against | Yes, from `source_png` |
| Good for | One published holdout that two readers reproduce identically | k-fold cross validation |

Take `split` if you have the cover tier and you're reporting a headline number
against the corpus, because it's recorded in the data and can't be reimplemented
slightly differently by the next person. Take `fold()` if you only pulled a
couple of arms, or you want cross validation. Say in the paper which one you
used.

`split_salt` is the string the labels were derived under. It's there so that a
future version that reshuffles the split is visibly a different partition rather
than silently the same one.

## Pairing a stego sample with its clean half

Every stego record names its clean half in a `clean` field, and that name is a
path from the build tree (`clean_grey/00000.png`). No such file ships. The clean
halves ship as their own arms, `pentimento-core-clean-*.tar`, and you pair
against those.

Two ways in, and they agree:

- **By position.** A stego arm and **its own clean arm** are key aligned and
  shard aligned. Key `NNNNNN` in shard `K` of a stego arm is the same
  photograph as key `NNNNNN` in shard `K` of its clean arm. This holds for the
  outguess arms too, which are short of 10,000 samples.
- **By digest.** A stego record's `clean_sha256` is the `sha256` of its clean
  record. This is the join to use if you're streaming the two arms separately,
  or if you want the pairing checked rather than assumed.

[What is in it](/guide/whats-in-it#the-clean-arms) says which clean arm goes
with which stego arm. Use that one rather than the cover tier, or the pair will
differ in the encoder as well as in the payload.

::: danger Keys line up within a pair, never between two stego arms
Shard `K` of one stego arm and shard `K` of a different stego arm are not the
same photographs. Shard 0 of `wow-0200` and shard 0 of `outguess-0200` hold 500
covers each and share only 395 of them, because a short arm skips the covers
its tool refused and everything after the gap shifts up.

So comparing two arms by zipping them on key gives a wrong answer that looks
right: the counts match, every digest matches its own record, and
`sha256sum -c` passes on both. **Join across arms on `source_png`**, which
names the photograph, not on the key, which names a position.
:::

## Verify before you publish

Every part ships its own checksum file, `SHA256SUMS-covers` or
`SHA256SUMS-arms`, beside its shards. If a number is going into a
paper, check them first:

```bash
sha256sum -c SHA256SUMS-arms
```

It costs a minute, and a shard that arrived truncated reads as a smaller
corpus rather than as an error.

## Crediting the photographers

5,453 of the 10,000 covers are CC BY and require attribution, and stego images
inherit their cover's terms. `ATTRIBUTION.md` carries every credit line, and
`ATTRIBUTION.csv` the same list in a form you can join against. If you used one
arm rather than the whole corpus, each record names its cover under
`source_png`, so you need only the lines for the covers you actually used.
