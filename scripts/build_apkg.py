#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_apkg.py

Takes the words_by_level.json produced by parse_ceec_pdf.py and builds a
single Anki .apkg containing one deck per level (Level 1 .. Level 6) as
subdecks under one parent deck -- the same "one package, level subdecks
inside it" structure egg rolls' JLPT10k deck uses for N1-N5
(https://github.com/5mdld/anki-jlpt-decks), rather than separate files or
git branches per level.

Each note has 3 fields: Word, POS, Level. This is a pure vocabulary index
(word + part of speech + official level) -- it intentionally does NOT
include Chinese definitions or example sentences, since those aren't part
of the official CEEC list itself.

Usage:
    pip install genanki
    python3 build_apkg.py words_by_level.json -o output.apkg \
        --deck-name "高中英文參考詞彙表(111學年度)"
"""

import argparse
import hashlib
import json

try:
    import genanki
except ImportError:
    raise SystemExit("This script needs genanki: pip install genanki")


def stable_id(seed, salt=0):
    """Deterministic id derived from a seed string, so re-running the build
    against unchanged input reproduces the same deck/model/note ids
    (important for Anki to treat re-imports as updates, not duplicates)."""
    h = int(hashlib.sha1(f'{salt}:{seed}'.encode('utf-8')).hexdigest(), 16)
    return 1 << 30 | (h % ((1 << 30) - 1))


CSS = '''
.card { font-family: -apple-system, "Noto Sans TC", sans-serif; text-align: center; color: #222; background: #fff; }
.word { font-size: 34px; font-weight: 600; }
.pos { font-size: 20px; color: #555; margin-top: 10px; }
.level { font-size: 16px; color: #888; margin-top: 6px; }
'''


def build(words_by_level, deck_name, model_name):
    model = genanki.Model(
        stable_id(model_name, salt=1),
        model_name,
        fields=[{'name': 'Word'}, {'name': 'POS'}, {'name': 'Level'}],
        templates=[{
            'name': 'Card 1',
            'qfmt': '<div class="word">{{Word}}</div>',
            'afmt': '{{FrontSide}}<hr id="answer">'
                    '<div class="pos">{{POS}}</div>'
                    '<div class="level">Level {{Level}}</div>',
        }],
        css=CSS,
    )

    decks = {}
    for level in range(1, 7):
        name = f'{deck_name}::Level {level}'
        decks[level] = genanki.Deck(stable_id(name, salt=2), name)

    for level_str, entries in words_by_level.items():
        level = int(level_str)
        if level not in decks:
            continue
        for word, pos in entries.items():
            note = genanki.Note(
                model=model,
                fields=[word, pos, str(level)],
                tags=[f'Level{level}'],
            )
            decks[level].add_note(note)

    return list(decks.values())


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('words_json', help='words_by_level.json from parse_ceec_pdf.py')
    ap.add_argument('-o', '--output', default='output.apkg')
    ap.add_argument('--deck-name', default='高中英文參考詞彙表(111學年度)')
    ap.add_argument('--model-name', default='高中英文參考詞彙表 111學年度')
    args = ap.parse_args()

    with open(args.words_json, encoding='utf-8') as f:
        words_by_level = json.load(f)

    decks = build(words_by_level, args.deck_name, args.model_name)
    genanki.Package(decks).write_to_file(args.output)

    total = sum(len(v) for v in words_by_level.values())
    print(f'Wrote {args.output}: {total} notes across {len(decks)} level subdecks')


if __name__ == '__main__':
    main()
