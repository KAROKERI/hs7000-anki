# Licensing / attribution notice

**English** | [繁體中文](https://github.com/KAROKERI/hs7000-anki/blob/main/NOTICE.zh-TW.md)

This repository has three layers with different licensing, kept
deliberately separate so the copyrighted layer never has to leave your
own machine.

## Scripts (`scripts/`) -- MIT

`parse_ceec_pdf.py` and `build_apkg.py` are original code, MIT licensed
(see `LICENSE`). They contain no vocabulary content -- they are tools
you run yourself against a PDF you download yourself.

## Card template (`template/`) -- MIT

The CSS in `template/card.css` is original, written from scratch for a plain word/POS/level index deck. It does not reuse or derive from any third-party Anki deck template, and carries the same MIT license as the scripts.

The deck currently shared on AnkiWeb is different from what these scripts produce. It is built directly from the author's separate, personal `高中7000單字` study deck -- the one with full Chinese definitions and two example sentences per card -- rather than from `build_apkg.py`. That personal deck's card styling is adapted from [egg rolls' JLPT10k deck](https://github.com/5mdld/anki-jlpt-decks) under CC BY-NC 4.0 (non-commercial use, attribution required), and that attribution is given on the AnkiWeb listing itself. If you build your own deck from this repo's scripts instead, you get the plain MIT-licensed template above, not the egg-rolls-derived one.

## Vocabulary content -- NOT included, copyright 大學入學考試中心 (CEEC)

This repo does not ship the official *高中英文參考詞彙表* (the Taiwanese
CEEC high-school reference vocabulary list), nor any word list extracted
from it, nor a pre-built `.apkg`. The list's own copyright notice reads:
> 著作權屬財團法人大學入學考試中心基金會所有，僅供非營利目的使用，轉載請
> 註明出處。若作為營利目的使用，應事前經由財團法人大學入學考試中心基金會
> 書面同意授權。

("Copyright held by the CEEC Foundation. For non-commercial use only;
cite the source when reproducing it. Commercial use requires prior
written permission from the CEEC Foundation.")

To build the deck yourself, download your own copy of the official PDF
from the CEEC website (search "高中英文參考詞彙表" on ceec.edu.tw, or use
the direct link in `README.md`), run `scripts/parse_ceec_pdf.py` against
your copy to produce `words_by_level.json` locally, then run `scripts/build_apkg.py` against that JSON to produce your own `.apkg` for your own non-commercial study use.

Neither the PDF, the JSON it produces, nor a built `.apkg` should be
committed to this repo or redistributed from it.
