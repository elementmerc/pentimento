# What is in it

| | |
|---|---|
| Covers | 10,000 photographs from Wikimedia Commons |
| Stego pairs | 344,357 |
| Arms | 35 stego, plus 4 clean |
| Format | WebDataset tar shards |
| Licence | CC BY 4.0 for the collection; each file's own terms in its record |

## The arms

| Family | Tools | Payloads | Domain |
|---|---|---|---|
| Adaptive, spatial | HUGO, WOW, S-UNIWARD, HILL, MiPOD | 0.05, 0.1, 0.2, 0.4 bpp | Pixels |
| Adaptive, DCT | J-UNIWARD, UERD | 0.05, 0.1, 0.2, 0.4 bpnzac | JPEG coefficients |
| End-user tools | steghide, outguess | 5%, 20%, 50% of capacity | JPEG |
| Control | Appended data after the end marker | n/a | JPEG |

### The four digits in an arm name are not always the same thing

An arm is named for its tool and a four digit number, and that number is always
the payload rate times a thousand. The **unit** of the rate is set by the
family, so the same digits mean three different quantities.

| Arm name | Reads as | Which is |
|---|---|---|
| `hugo-0050` | 0.05 bits per pixel | An absolute rate: bits hidden per pixel of the image |
| `juniward-0050` | 0.05 bits per non-zero AC coefficient | An absolute rate, over JPEG coefficients rather than pixels |
| `steghide-0050` | 5% of capacity | A relative rate: a share of what that tool said that picture could hold |
| `append_after_eoi-0000` | n/a | A fixed payload, the same on every image |

`hugo-0400` and `steghide-0500` are not "more payload" versions of each other,
and the relative rates are not comparable between pictures either, because
steghide's capacity depends on the content of the photograph.

### Every JPEG arm is quality 95

The JPEG arms and their clean halves are written at quality 95: one setting,
everywhere, both halves, with identical quantisation tables. Steganalysis
performance on JPEG moves sharply with the quality factor, so a number measured
here is a number at quality 95 and should be reported as one.

### The appended-data arm

This is the sanity check. Anything claiming to detect steganography should find
it trivially; a tool that misses it is not reading the file. No detector result
is published here, so this is a statement about what the arm is for rather than
a measurement: if you want a number, measure it and say how.

The payload is a fixed 4,122 byte literal, identical in all 10,000 images, sat
after the end-of-image marker. That makes it a clean control and a useless
training target: a classifier trained on this arm learns one byte string and
reports a perfect score that means nothing.

### The tool arms carry no passphrase

steghide and outguess were run without one, so all 54,357 samples in those six
arms can be extracted by anybody who has them. That's deliberate, because a
corpus whose payloads nobody can recover cannot be checked, but it does mean
these arms are readable rather than merely detectable.

## The clean arms

Every pair needs both halves, and the clean half is not always the cover.

| Arm | What it is | Pairs with |
|---|---|---|
| `clean-grey` | The cover in greyscale | The spatial arms |
| `clean-jpeg` | Written back through the DCT library, coefficients untouched | The DCT arms |
| `clean-jpeg-tools` | The cover as a JPEG, as the tools were handed it | steghide, appended data |
| `clean-outguess` | Through outguess's own writer, carrying the least it accepts | outguess |

They are separate because they are different encodings of the same photograph.
A tool that rewrites the whole file leaves its encoder's signature on
everything it writes, so pairing it against anything else measures the encoder
rather than the hiding.

## The format

A sample's parts share a basename, which is the WebDataset convention:

```
pentimento-core-wow-0200-00000.tar
  000000.png     the image
  000000.json    its record, licence included
```

Shards stream without unpacking and every major dataset loader reads them.

## What a record holds

| Field | What it is |
|---|---|
| `source_png` | The cover this descends from. Group by it to split |
| `cover_licence` | The cover's licence, artist, credit line and source URL |
| `sha256` | The image's digest, checked when it was packed |
| `arm`, `tool` | Which arm this came from, and what made it |
| `rate` | The nominal payload, `null` on the clean arms |
| `rate_unit` | What the rate counts, including `unstated` on the clean arms |
| `pairing` | `container-verified`, or `no-clean-half` on the clean arms |
| `licence_join` | How this file's licence was traced back to its cover |

Every one of the 39 arms carries those nine. Nothing else is universal,
and a loader that assumes otherwise falls over on the first arm it has not seen
before. Reach for anything in the next table with `record.get(...)` rather than
`record[...]`.

| Field | Arms that have it | Arms that don't |
|---|---|---|
| `clean`, `clean_sha256`, `stego`, `stego_sha256` | The 35 stego arms | The 4 clean arms, which are one half rather than a pair |
| `file`, `role` | The 4 clean arms | The 35 stego arms |
| `coding` | The 28 adaptive arms | The 6 tool arms, the appended-data arm, the 4 clean arms |
| `domain` | All 39, but `null` on `clean-jpeg-tools` and `clean-outguess` | Nobody, though two carry it empty |
| `samples_changed`, `change_rate` | The 20 spatial adaptive arms | Everything else, the DCT arms included |
| `coefficients_changed` | The 8 DCT adaptive arms | Everything else |
| `jpeg_quality`, `payload_bytes`, `detail` | The 6 tool arms and the appended-data arm | Everything else. The DCT arms are quality 95 too, they just don't record it |
| `capacity_bytes` | The 6 tool arms, whose rates are relative to it | Everything else |
| `source_sha256` | The 35 stego arms, proving which cover bytes they came from | The 4 clean arms |
| `source_png` | All 39 arm shards | The cover shards, which call the same value `file` |
| `source_jpeg` | The 8 DCT adaptive arms and the 4 clean arms, 12 in total | The 20 spatial adaptive arms, the 6 tool arms, the appended-data arm |
