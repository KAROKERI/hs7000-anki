#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
parse_ceec_pdf.py

Parses the official Taiwanese CEEC (大學入學考試中心) high-school reference
vocabulary list PDF ("高中英文參考詞彙表 -111學年度起適用-") into a
word -> {pos, level} JSON mapping.

This script does NOT ship the PDF or any extracted vocabulary content
(the list is copyrighted by CEEC, non-commercial use only -- see NOTICE.md).
Download your own copy of the official PDF from the CEEC website and pass
its path to this script.

Source PDF layout used by this parser:
  - Pages ~65-115 ("依字母排序" / alphabetical order section): a 3-column
    table where every entry is printed as "word POS LEVEL", e.g.
    "quote v./n. 3". This is the single section that carries word, part
    of speech, AND level together, so it's the only section this script
    parses -- no need to reconcile it against the separate "依級別排序"
    (grouped-by-level) section earlier in the document.

Parsing approach:
  - pdfplumber's default extract_text() interleaves the 3 columns in a
    way that scrambles reading order (rows from different columns land on
    the same visual line). Instead, this script buckets words by x0 into
    3 column ranges, sorts each column's words by vertical position, and
    reconstructs each column's rows independently -- which recovers the
    true top-to-bottom reading order within each column.
  - Entries that wrap across two physical rows (long POS chains, or a
    level digit alone on the next row) are re-joined by buffering rows
    until a full "word POS level" match is found.
  - Page footer numbers (which happen to fall inside the middle column's
    x-range) are dropped by their vertical position near the page bottom,
    not by "looks like a digit" -- a lone digit that is a genuine wrapped
    level number is kept.

Validated against the 111學年度 PDF: 6,012 entries, exactly 1,002 per
level (Level 1-6), 0 duplicate headwords, 0 unparsed leftovers, spot
checked against ~30 known entries with 100% match. This total matches
the PDF's own stated design ("每一級收錄約1,000詞條，六個級別共計約
6,000詞條" -- p.6; "共計收錄約6,000個英文詞條" -- p.8). Treat any other
total (e.g. "6,172") you may see cited elsewhere for this same PDF with
suspicion unless it's independently re-verified the same way.

Usage:
    python3 parse_ceec_pdf.py path/to/official_vocab.pdf -o words_by_level.json
"""

import argparse
import collections
import json
import re
import sys

try:
    import pdfplumber
except ImportError:
    sys.exit("This script needs pdfplumber: pip install pdfplumber")

POS = r'\(?(?:n|v|adj|adv|prep|conj|pron|art|aux)\.?\)?'
POS_BLOCK = POS + r'(?:/' + POS + r')*'
ENTRY_RE = re.compile(r'^(?P<word>.+?)\s+(?P<pos>' + POS_BLOCK + r')\s+(?P<level>[1-6])$')

# 3-column x0 ranges for the "依字母排序" section, in PDF points.
# Re-check these against a histogram of word x0 values if you run this
# against a different edition of the PDF -- see `--debug-columns`.
COLUMN_BOUNDS = [(0, 200), (200, 370), (370, 600)]

SKIP_LINES = {'依字母排序', '高中英文參考詞彙表'}
FOOTER_TOP_THRESHOLD = 790  # page is ~842pt tall; footer page numbers sit below this


def is_letter_header(line):
    """A lone capital letter is a section sub-header (e.g. 'A', 'B', ...)."""
    return re.fullmatch(r'[A-Z]', line.strip()) is not None


def get_columns(page, bounds):
    words = page.extract_words()
    cols = [[] for _ in bounds]
    for w in words:
        x0 = w['x0']
        for i, (lo, hi) in enumerate(bounds):
            if lo <= x0 < hi:
                cols[i].append(w)
                break
    return cols


def rows_from_words(ws, tol=2.5):
    """Group words into physical rows by y-position, return (text, top) per row."""
    ws = sorted(ws, key=lambda w: w['top'])
    rows, cur, cur_top = [], [], None
    for w in ws:
        if cur_top is None or abs(w['top'] - cur_top) <= tol:
            cur.append(w)
            cur_top = w['top'] if cur_top is None else cur_top
        else:
            rows.append(cur)
            cur = [w]
            cur_top = w['top']
    if cur:
        rows.append(cur)
    out = []
    for row in rows:
        row_sorted = sorted(row, key=lambda w: w['x0'])
        text = ' '.join(w['text'] for w in row_sorted)
        top = min(w['top'] for w in row_sorted)
        out.append((text, top))
    return out


def append_buf(buf, s):
    """Join a new line onto the buffer. A trailing '/' means the POS chain
    was split across a line-wrap -- glue directly with no space so the
    POS regex still recognizes it as one unbroken chain."""
    if not buf:
        return s
    if buf.endswith('/'):
        return buf + s
    return buf + ' ' + s


def parse_pdf(pdf_path, alpha_page_range=(65, 115), debug_columns=False):
    entries = []
    leftover = []

    with pdfplumber.open(pdf_path) as pdf:
        if debug_columns:
            page = pdf.pages[alpha_page_range[0] - 1]
            xs = collections.Counter(round(w['x0'] / 10) * 10 for w in page.extract_words())
            for k in sorted(xs):
                print(k, xs[k], file=sys.stderr)
            return []

        for pno in range(alpha_page_range[0] - 1, alpha_page_range[1]):
            page = pdf.pages[pno]
            cols = get_columns(page, COLUMN_BOUNDS)
            for ci, col in enumerate(cols):
                lines = rows_from_words(col)
                buf = ''
                for s, top in lines:
                    s = s.strip()
                    if s in SKIP_LINES or is_letter_header(s):
                        continue
                    if re.fullmatch(r'\d+', s) and top > FOOTER_TOP_THRESHOLD:
                        continue  # page footer number, not a wrapped level digit
                    buf = append_buf(buf, s)
                    m = ENTRY_RE.match(buf)
                    if m:
                        word = re.sub(r'/\s+', '/', m.group('word').strip())
                        pos = m.group('pos').strip()
                        entries.append((word, pos, int(m.group('level')), pno + 1))
                        buf = ''
                if buf.strip():
                    leftover.append((pno + 1, ci + 1, buf))

    if leftover:
        print(f'WARNING: {len(leftover)} unparsed leftover buffer(s):', file=sys.stderr)
        for e in leftover:
            print(' ', e, file=sys.stderr)

    return entries


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('pdf_path', help='Path to your own copy of the official CEEC vocabulary PDF')
    ap.add_argument('-o', '--output', default='words_by_level.json',
                     help='Output JSON path (default: words_by_level.json)')
    ap.add_argument('--debug-columns', action='store_true',
                     help='Print an x0 histogram for the first alphabetical-section page and exit '
                          '(use this to re-derive COLUMN_BOUNDS if parsing a different PDF edition)')
    args = ap.parse_args()

    entries = parse_pdf(args.pdf_path, debug_columns=args.debug_columns)
    if args.debug_columns:
        return

    dupes = collections.Counter(e[0] for e in entries)
    dupes = {k: v for k, v in dupes.items() if v > 1}
    if dupes:
        print(f'WARNING: {len(dupes)} duplicate headword(s) -- keeping first occurrence', file=sys.stderr)

    by_level = collections.defaultdict(dict)
    for word, pos, level, page in entries:
        by_level[str(level)].setdefault(word, pos)

    counts = {k: len(v) for k, v in sorted(by_level.items())}
    total = sum(counts.values())
    print(f'Parsed {total} entries: {counts}', file=sys.stderr)

    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(by_level, f, ensure_ascii=False, indent=1)
    print(f'Wrote {args.output}', file=sys.stderr)


if __name__ == '__main__':
    main()
