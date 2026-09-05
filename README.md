# hs7000-anki

**English** | [繁體中文](README.zh-TW.md)

Scripts to build an Anki deck of Taiwan's official high-school reference
vocabulary list (大學入學考試中心《高中英文參考詞彙表》), organized into
Level 1-6 subdecks inside a single `.apkg` -- the same "one package,
levels as subdecks" structure used by
[egg rolls' JLPT10k deck](https://github.com/5mdld/anki-jlpt-decks) for
its N1-N5 levels.

This repo ships **no vocabulary content** -- only the parsing and build
tooling. See `NOTICE.md` for why, and for the full licensing breakdown.

Don't want to run the scripts yourself? The ready-built deck is shared
publicly on AnkiWeb: [高中英文參考詞彙表 Level 1-6（111學年度起適用｜大考中心）](https://ankiweb.net/shared/info/1109013663).
Import it straight into the Anki desktop app -- no PDF or Python required.
This repository itself stays scripts-only; see `NOTICE.md` for why.

## What you get

Each card: front = English word, back = part of speech plus official
level (`Level 1` through `Level 6`). This is a plain vocabulary index,
not a full study deck -- no Chinese definitions or example sentences,
since those aren't part of the official list itself.

## Usage

Install the dependencies:

```bash
pip install pdfplumber genanki
```

Download your own copy of the official PDF from CEEC (search
`高中英文參考詞彙表` on ceec.edu.tw), then parse it into a word/POS/level
JSON and build the `.apkg`:

```bash
python3 scripts/parse_ceec_pdf.py your-copy.pdf -o words_by_level.json
python3 scripts/build_apkg.py words_by_level.json -o hs7000-level1-6.apkg
```

Import `hs7000-level1-6.apkg` into Anki afterward. You'll get one parent
deck with six subdecks, `Level 1` through `Level 6`.

## Validation

Parsed against the 111學年度起適用 edition: 6,012 entries, exactly 1,002
per level, 0 duplicate headwords, 0 unparsed leftovers after column-aware
PDF text reconstruction (the alphabetical-order section in the PDF is a
3-column table that a naive `pdftotext`-style extraction scrambles --
see the parser's docstring for how it recovers correct reading order).
This matches the PDF's own stated design ("每一級收錄約1,000詞條，六個
級別共計約6,000詞條"). If you parse a different edition and get a very
different total, re-run with `--debug-columns` to check whether the
column x-ranges still match that edition's layout before trusting the
output.

## License

`scripts/` and `template/` are MIT (see `LICENSE`). Vocabulary content
is not included -- copyright CEEC, see `NOTICE.md`.
