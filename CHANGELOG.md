# Changelog

All notable changes to this project are documented here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project uses [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-09-24 - Pilot

First public release of the Pentimento corpus.

### Corpus

- 10,000 cover photographs from Wikimedia Commons, 512x512 greyscale PNG, every
  one under CC0, a CC BY licence, or public domain. No licence-encumbered
  images, and nothing whose terms could not be established.
- 344,357 matched stego pairs across 35 labelled stego arms and 4 clean arms.
  Arms are kept separate rather than blended, so you can measure one tool at one
  payload rate without the others in the way.
- Every file carries its own SHA-256 and its own credit line. 5,453 of the
  10,000 covers require attribution, and each ships a ready-made line including
  the licence URI and a statement that the image was modified.
- Three nested tiers: Nano (200 covers), Lite (1,000) and Core (10,000). A tier
  is the first *n* covers of one fixed ordering, so a smaller tier is exactly a
  prefix of a larger one, byte for byte.

### Distribution

- Published to the Internet Archive as `pentimento-core-v1`, which needs no
  account and no approval.
- Published to HuggingFace as `the-malware-files/pentimento-core`, with a
  config declared per arm so a single arm loads by name.
- Published to Kaggle as `elementmerc/pentimento-core`, covers only: Kaggle
  extracts archives on upload and offers no way to refuse, and unpacking the
  full corpus would produce 784,952 loose files.
- A loader, `load_pentimento.py`, that reads a tar shard or an unpacked folder
  with nothing to install, and verifies each record against its own digest.

### Documentation

- A seven-page guide covering what is in the corpus, how to get it, how to load
  and split it, how the licensing works, what the corpus cannot tell you, and
  how to rebuild it.
- A datasheet following Gebru et al., including the composition, collection and
  withdrawal questions a reviewer asks.
- Splitting guidance that partitions by cover, because a random split puts a
  photograph's clean and stego halves on both sides of the line and flatters
  every result that follows.
- A limitations page stating plainly what the corpus does not establish:
  covers are JPEG-decompressed, embedding is simulated rather than a real STC,
  and detector rankings can invert with cover source.

### Licence

- The corpus is CC BY 4.0. The tooling in this repository is AGPL-3.0-or-later,
  the documentation prose is CC BY 4.0, and the identity in `brand/` is reserved
  with a narrow permission for unmodified use.
