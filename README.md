# Salvador (city): law history in git

Part of [lexifina/global-law](https://github.com/lexifina/global-law), one git history for every country's law: this is the law of Salvador, Bahia, Brazil, which global-law reads at `brazil/bahia/salvador/acts/`.

The municipal law of the Município de Salvador, the city of Salvador (Bahia) (Brazil) as a git history: one file per Artigo, one paragraph per line, so `git blame`, `git log` and `git diff` work line by line. The text is Portuguese, the only official language.

It follows the shared design of [lexifina/global-law](https://github.com/lexifina/global-law).

## What this repository holds

| Folder | Act | Versions |
| --- | --- | ---: |
| `lei-organica/` | Lei Orgânica do Município de Salvador (1990), consolidated up to Emenda nº 41 | 1 |

**Lei Orgânica only.** The Câmara publishes the Lei Orgânica as a consolidated edition; for the municipal Leis its site links only to a private aggregator, which this record does not use, so no ordinary or complementary law is in yet. The text is given **only as the edition's text in force**, credited to the Câmara as the oldest version available. State law is in [brazil-bahia-law](https://github.com/lexifina/brazil-bahia-law); federal law in [brazil-law](https://github.com/lexifina/brazil-law).

## Source

[Câmara Municipal de Salvador, Lei Orgânica do Município](https://www.cms.ba.gov.br/lei-organica), published by the Câmara Municipal de Salvador. Each version names the page it was taken from and that page's sha256, in `data/versions.json`.

## Dates

The one version is dated by the edition itself: the PDF "Edição consolidada até a Emenda nº 41" was created on 22 February 2024. Commits are at noon in Salvador.

## How it is built

Lexifina reads the sources listed here and records each act's dated versions, and the laws that made each change, in one corpus file. `tools/build.py` writes this repository from that file, and the same corpus always gives the same commit hashes; `REPRODUCE.md` gives the details and the checks. A model (Claude) wrote Lexifina's code; it wrote no legal text, and no model runs when the history is built.

The PDF's text layer is read with pdftotext; the cover, the lists of members, the table of contents, page numbers, the amendment markers in front of a provision ("(16)") and the amendment notes under it ("(16) Emenda à LOM nº 16") are left out, and a paragraph broken across two pages is joined again. One file per Art.; headings stand above the first article under them; the Ato das Disposições Transitórias, numbered from 1 again, is `adt-*`.

## How it is checked

Every version is read back from git on the day it took effect (`tools/check_repo.py`) and must match the corpus; an independent letters-and-digits comparison of every version against the source page must show no difference. Results are in `REPRODUCE.md`.

## What "author" means

The author of each commit is the law that made the text, or, for a consolidated text, the publisher, with an e-mail address that cannot exist; the committer is always Lexifina.

## Limits

Not a history: the Lei Orgânica as promulgated in 1990 and the wordings its 41 amendments replaced are not in the edition. The amendment markers are left out, so the record does not say which amendment changed which provision. The text is not the official version: only the Diário Oficial do Município is authoritative.

## Licence

See [LICENSE](LICENSE): Brazilian law texts are not protected by copyright (Lei 9.610/1998, art. 8, IV). Fonte: Câmara Municipal de Salvador, Lei Orgânica do Município, Câmara Municipal de Salvador.
