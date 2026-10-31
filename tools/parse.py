"""Builds corpus.d/10-lei-organica.json for the Município de Salvador from the Câmara Municipal's consolidated edition
of the Lei Orgânica (PDF with a text layer; no network).

    python -X utf8 parse.py --today YYYY-MM-DD

The edition ("Edição consolidada até a Emenda nº 41", Câmara Municipal de Salvador, 2024) is read with pdftotext
(poppler) page by page. Left out: the cover and the lists of members (pages before the table of contents), the table
of contents, each page's number, the amendment markers in front of a provision ("(16) (21) (26) Art. 14. ...") and the
amendment notes under it ("(16) Emenda à LOM nº 16"). A paragraph broken across two pages is joined again.
"""
import argparse, re, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from br_lib import units_of, write_part, sha, norm  # noqa: E402

PDF_URL = 'https://www.cms.ba.gov.br/uploads/3bdae368d1a3e255c81b7f262ba1bbf6_1709038424.pdf'
PDF = HERE / '.cache' / 'lom.pdf'
MARK = re.compile(r'^(?:\(\s*\d{1,2}\s*\)\s*\)?\s*)+')
INMARK = re.compile(r'^([IVXLC]{1,6}) \(\s*\d{1,2}\s*\)(?=\s*[-–])')  # "I (36) - por incapacidade ..." 
ENDNOTE = re.compile(r'^(?:\(\s*\d{1,2}\s*\)\s*Emenda(?:\s+[àa]\s+LOM)?\s*(?:n[º°o.]\s*)?\d{1,2}\s*)+$', re.I)
STARTS = re.compile(r'^(?:Art\.|§|Par[áa]grafo|[IVXLC]+\s*[-–]|[a-z]\)|T[ÍI]TULO|CAP[ÍI]TULO|Se[çc][ãa]o|SE[ÇC][ÃA]O|ATO\b)')


def pages():
    out = subprocess.run(['pdftotext', '-enc', 'UTF-8', str(PDF), '-'], capture_output=True, check=True).stdout
    return out.decode('utf-8').split('\f')


def lines_of_pdf():
    """The law's paragraphs: from the first page after the table of contents (the one starting "TÍTULO I")."""
    ps = pages()
    start = next(i for i, p in enumerate(ps) if p.lstrip().startswith('TÍTULO I') and '.....' not in p)
    out = []
    for n, p in enumerate(ps[start:], start + 1):
        ls = [norm(l) for l in p.split('\n')]
        ls = [l for l in ls if l]
        # the page number: a line of its own at the end, or glued to the end of the last paragraph
        if ls and re.fullmatch(r'\d{1,3}', ls[-1]):
            ls.pop()
        elif ls and re.search(r'\s\d{1,3}$', ls[-1]) and not re.search(r'\bArt\.\s*\d+$', ls[-1]):
            ls[-1] = re.sub(r'\s\d{1,3}$', '', ls[-1])
        page = []
        for l in ls:
            if ENDNOTE.match(l):
                continue
            l = INMARK.sub(lambda m: m.group(1), MARK.sub('', l)).strip()
            if l:
                page.append(l)
        if page and out and not re.search(r'[.;:!?)"”]$', out[-1]) and not STARTS.match(page[0]):
            out[-1] = out[-1] + ' ' + page.pop(0)
        out += page
    return out


COUNTRY = {
    'code': 'BR-BA-SALVADOR', 'name': 'Salvador', 'slug': 'brazil-salvador-city', 'lang': 'pt',
    'tz': 'America/Bahia', 'future_branch': 'futuro',
    'publisher': {'name': 'Câmara Municipal de Salvador', 'email': 'cms@cms.ba.gov.br.invalid'},
    'default_in_force_rule': {
        'text': 'Decreto-Lei 4.657/1942 (LINDB) art. 1: unless it says otherwise, a law takes effect 45 days after its '
                'official publication. The Lei Orgânica and its amendments are promulgated by the Mesa da Câmara and '
                'take effect on promulgation; this record holds only the consolidated text, dated by the edition.',
        'source': 'https://www.planalto.gov.br/ccivil_03/decreto-lei/del4657compilado.htm'},
    'licence_note': 'Text: Câmara Municipal de Salvador, Lei Orgânica do Município de Salvador, edição consolidada até '
                    'a Emenda nº 41 (2024), www.cms.ba.gov.br. Lei 9.610/1998 art. 8 IV: the texts of laws and other '
                    'official acts are not protected by copyright. Non-official text: only the Diário Oficial do '
                    'Município is authoritative.',
}
DECISIONS = [
    'The Lei Orgânica is given only as the Câmara\'s consolidated edition ("Edição consolidada até a Emenda nº 41", '
    '2024), credited to the Câmara as the oldest version available and dated by the edition\'s own date (the PDF\'s '
    'creation date, 22 February 2024; the Câmara put it online on 27 February 2024). The text as promulgated in 1990 '
    'and the wordings each amendment replaced are not in the edition, so no earlier version is given.',
    'Left out: the cover, the lists of members of the Câmara and of the Prefeitura, the table of contents, page numbers, '
    'the amendment markers in front of a provision ("(16) (21) (26)") and the amendment notes under it ("(16) Emenda à '
    'LOM nº 16"). A paragraph broken across two pages is joined again.',
    'One file per Art.; headings stand above the first article under them; the articles of the Ato das Disposições '
    'Transitórias, numbered from 1 again, are adt-*.',
]
AI = ["Claude Code (claude-opus-5-5) wrote Lexifina's code and chose the sources. No model output is used as legal "
      "text or dates: every word comes from the Câmara's PDF."]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--today', required=True)
    a = ap.parse_args()
    lines = [('p', l) for l in lines_of_pdf()]
    units = units_of(lines, adt=True)
    b = PDF.read_bytes()
    key = 'lei-organica-1990'
    laws = {key: {'label': 'Lei Orgânica do Município de Salvador, de 5 de abril de 1990',
                  'title': 'Lei Orgânica do Município de Salvador', 'kind': 'law', 'enacted': '1990-04-05',
                  'published': None, 'url': 'https://www.cms.ba.gov.br/lei-organica', 'temporary_until': None,
                  'restores': None, 'note': None}}
    v = {'from': '2024-02-22', 'source_url': PDF_URL, 'sha256': sha(b), 'units': units,
         'note': 'Text in force as consolidated by the Câmara Municipal de Salvador up to Emenda nº 41 (edition of 2024).'}
    act = {'slug': 'lei-organica', 'short': 'LOM-Salvador', 'title': 'Lei Orgânica do Município de Salvador',
           'url': 'https://www.cms.ba.gov.br/lei-organica', 'first_law': None, 'earlier_laws': [key], 'versions': [v]}
    c = {'country': COUNTRY,
         'sources': [{'name': 'Câmara Municipal de Salvador: Lei Orgânica do Município, edição consolidada até a '
                              'Emenda nº 41 (PDF)', 'url': 'https://www.cms.ba.gov.br/lei-organica', 'retrieved': a.today,
                      'licence': COUNTRY['licence_note'], 'notes': '1 act.'}],
         'laws': laws, 'acts': [act], 'applies': [], 'decisions': DECISIONS, 'ai_use': AI}
    print(write_part(HERE / 'corpus.d', '10-lei-organica', c), len(units))


if __name__ == '__main__':
    main()
