"""Independent letters-and-digits check of the Lei Orgânica against the PDF, read with a second PDF reader (PyMuPDF,
not the builder's pdftotext) and none of the builder's code.

    python -X utf8 check_letters.py [part.json ...]

The PDF text from the page that starts "TÍTULO I" (after the table of contents) to the end, with each page's number (first on the page in this reader),
the amendment notes ("(16) Emenda à LOM nº 16") and the amendment markers ("(16)") removed, reduced to letters and
digits, must equal the version's unit files reduced the same way, each unit found at its place in document order.
"""
import hashlib, json, re, sys
from pathlib import Path

import pymupdf

HERE = Path(__file__).resolve().parent


def ld(s):
    return ''.join(ch for ch in s if ch.isalnum())


def pdf_text(raw):
    doc = pymupdf.open(stream=raw, filetype='pdf')
    # PyMuPDF gives each page's number first (pdftotext gives it last)
    pages = [re.sub(r'^\s*\d{1,3}\s', '', p.get_text()) for p in doc]
    start = next(i for i, t in enumerate(pages) if t.lstrip().startswith('TÍTULO I') and '.....' not in t)
    out = []
    for t in pages[start:]:
        t = re.sub(r'\(\s*\d{1,2}\s*\)\s*Emenda(?:\s+[àa]\s+LOM)?\s*(?:n[º°o.]\s*)?\d{1,2}', ' ', t, flags=re.I)
        t = re.sub(r'\(\s*\d{1,2}\s*\)\s*\)?', ' ', t)
        out.append(t)
    return '\n'.join(out)


def main(paths):
    bad = total = 0
    for p in paths:
        c = json.load(open(p, encoding='utf-8'))
        for a in c['acts']:
            for v in a['versions']:
                raw = (HERE / '.cache' / 'lom.pdf').read_bytes()
                assert hashlib.sha256(raw).hexdigest() == v['sha256'], (a['slug'], 'sha256')
                src = ld(pdf_text(raw))
                rest = {k: ld(re.sub(r'(?m)^#+ ', '', u['text'])) for k, u in v['units'].items()}
                pos = 0
                while rest:
                    hit = None
                    for k, t in rest.items():
                        if t and src.startswith(t, pos) and (hit is None or len(t) > len(rest[hit])):
                            hit = k
                    if hit is None:
                        break
                    pos += len(rest.pop(hit))
                total += 1
                if rest or pos != len(src):
                    bad += 1
                    print(f'MISMATCH {a["slug"]} {v["from"]}: matched {pos}/{len(src)}; next source: '
                          f'{src[pos:pos + 80]!r}; unplaced: {list(rest)[:5]}')
    print(f'{total} versions checked, {bad} mismatches')
    return bad


if __name__ == '__main__':
    sys.exit(1 if main(sys.argv[1:] or sorted(str(p) for p in (HERE / 'corpus.d').glob('*.json'))) else 0)
