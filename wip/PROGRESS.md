# brazil-salvador-city-law (gitlaw-scraper-dell, 2026-10-31)

Private. Municipal tier. Source: Câmara Municipal de Salvador (www.cms.ba.gov.br): robots `User-agent: * / Disallow:`
(empty); no reproduction terms found; no challenge. Its "Leis Municipais" link goes to leismunicipais.com.br (private
aggregator: not used). cmsalvador.sys.inf.br (robots `User-agent: *`) is financial transparency only; 45.4.247.157 is
plain-http by IP (legislative process, no law texts checked). So: Lei Orgânica only, from the consolidated PDF
(/uploads/3bdae368d1a3e255c81b7f262ba1bbf6_1709038424.pdf, "até a Emenda nº 41", created 2024-02-22).
- parse.py (pdftotext) -> corpus.d/10-lei-organica.json; check_letters.py (PyMuPDF) 0 mismatches.
- 2026-10-31T18:12:44Z: repo created (one API call, scaffold 2f7986b), 10-lei-organica PUBLISHed.
- Next if a source appears: the Diário Oficial do Município (dom) for laws; the Câmara's own Leis pages.
