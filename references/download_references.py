"""Download bibliography references locally.

Usage: python download_references.py
Creates PDFs in references/ with naming: bibkey_short-title.pdf
"""
import os
import time
import json
import urllib.request
import urllib.error
import ssl

REFS_DIR = os.path.dirname(os.path.abspath(__file__))

# SSL context that doesn't verify (some gov sites have cert issues)
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def download(url, filename, headers=None):
    """Download URL to filename, return True on success."""
    path = os.path.join(REFS_DIR, filename)
    if os.path.exists(path) and os.path.getsize(path) > 1000:
        print(f"  SKIP (exists): {filename}")
        return True
    try:
        req = urllib.request.Request(url, headers=headers or {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Academic-Research/1.0"
        })
        with urllib.request.urlopen(req, timeout=30, context=ctx) as resp:
            data = resp.read()
            if len(data) < 500:
                print(f"  WARN: {filename} too small ({len(data)} bytes), skipping")
                return False
            with open(path, "wb") as f:
                f.write(data)
            print(f"  OK: {filename} ({len(data):,} bytes)")
            return True
    except Exception as e:
        print(f"  FAIL: {filename} — {e}")
        return False


# ============================================================
# DIRECT URLs (PDFs from UNESCO, OECD, etc.)
# ============================================================
DIRECT_DOWNLOADS = {
    # UNESCO documents
    "unesco2019beijing_beijing-consensus-ai-education.pdf":
        "https://unesdoc.unesco.org/ark:/48223/pf0000368303/PDF/368303eng.pdf.multi",
    "miao2021guidance_ai-education-guidance-policymakers.pdf":
        "https://unesdoc.unesco.org/ark:/48223/pf0000376709/PDF/376709eng.pdf.multi",
    "unesco2023genai_guidance-generative-ai-education.pdf":
        "https://unesdoc.unesco.org/ark:/48223/pf0000386693/PDF/386693eng.pdf.multi",
    "pedro2019aieducation_ai-challenges-opportunities.pdf":
        "https://unesdoc.unesco.org/ark:/48223/pf0000366994/PDF/366994eng.pdf.multi",
    "unesco2021ai_ethics-recommendation.pdf":
        "https://unesdoc.unesco.org/ark:/48223/pf0000381137/PDF/381137eng.pdf.multi",
    "unesco2023gem_global-education-monitoring-technology.pdf":
        "https://unesdoc.unesco.org/ark:/48223/pf0000385723/PDF/385723eng.pdf.multi",

    # JRC / European Commission
    "tuomi2018impact_ai-learning-teaching-education.pdf":
        "https://publications.jrc.ec.europa.eu/repository/bitstream/JRC113226/jrc113226_jrcb4_the_impact_of_ai_on_learning_final_2.pdf",

    # Open Access articles
    "zawacki2019systematic_ai-higher-education-review.pdf":
        "https://educationaltechnologyjournal.springeropen.com/counter/pdf/10.1186/s41239-019-0171-0",
    "ng2021ailiteracy_conceptualizing-ai-literacy.pdf":
        "https://www.sciencedirect.com/science/article/pii/S2666920X21000357/pdfft?isDTMRedir=true&download=true",
    "nguyen2020words_text-social-cultural-data.pdf":
        "https://www.frontiersin.org/articles/10.3389/frai.2020.00062/pdf",
    "roberts2019stm_structural-topic-models.pdf":
        "https://www.jstatsoft.org/index.php/jss/article/view/v091i02/3011",

    # Stanford AI Index
    "maslej2024aiindex_ai-index-2024.pdf":
        "https://aiindex.stanford.edu/wp-content/uploads/2024/04/HAI_AI-Index-Report-2024.pdf",

    # AAAI open proceedings
    "touretzky2019k12ai_ai-k12-every-child.pdf":
        "https://ojs.aaai.org/index.php/AAAI/article/view/5053/4926",

    # WEF
    "wef2020future_future-of-jobs-2020.pdf":
        "https://www3.weforum.org/docs/WEF_Future_of_Jobs_2020.pdf",

    # World Bank
    "worldbank2020reimagining_technology-innovation-education.pdf":
        "https://documents1.worldbank.org/curated/en/829491606860379513/pdf/Reimagining-Human-Connections-Technology-and-Innovation-in-Education-at-the-World-Bank.pdf",

    # OECD AI Principles
    "oecd2019ai_recommendation-ai.pdf":
        "https://legalinstruments.oecd.org/api/download/?uri=/public/c80444de-fc33-4f6f-87ff-dd9844421cf2.pdf&name=OECD-LEGAL-0449-en.pdf",

    # EU AI Act (EUR-Lex)
    "eu2024aiact_regulation-2024-1689.pdf":
        "https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=OJ:L_202401689",

    # India NEP 2020
    "india2020nep_national-education-policy.pdf":
        "https://www.education.gov.in/sites/upload_files/mhrd/files/NEP_Final_English_0.pdf",

    # India NITI Aayog AI for All
    "india2018niti_ai-for-all-strategy.pdf":
        "https://niti.gov.in/sites/default/files/2023-03/National-Strategy-for-Artificial-Intelligence.pdf",

    # Australia AI Action Plan
    "australia2021aiaction_ai-action-plan.pdf":
        "https://storage.googleapis.com/converlens-au-industry/industry/p/prj2452c8e24d7a400c72429/public_assets/Australias-AI-Action-Plan.pdf",

    # Singapore NAIS
    "singapore2019nais_national-ai-strategy.pdf":
        "https://www.smartnation.gov.sg/files/publications/national-ai-strategy.pdf",

    # Canada Pan-Canadian AI Strategy
    "canada2017ai_pan-canadian-ai-strategy.pdf":
        "https://ised-isde.canada.ca/site/ai-strategy/sites/default/files/attachments/2022/Pan-Canadian_AI_Strategy_2022_e.pdf",

    # Colombia CONPES 3975
    "colombia2019conpes_conpes-3975-transformacion-digital.pdf":
        "https://colaboracion.dnp.gov.co/CDT/Conpes/Econ%C3%B3micos/3975.pdf",

    # Brasil EBIA
    "brasil2021ebia_estrategia-brasileira-ia.pdf":
        "https://www.gov.br/mcti/pt-br/acompanhe-o-mcti/transformacaodigital/arquivosinteligenciaartificial/ebia-diagramacao_4-979_2021.pdf",

    # Spain ENIA
    "spain2020enia_estrategia-nacional-ia.pdf":
        "https://portal.mineco.gob.es/RecursosArticulo/mineco/ministerio/ficheros/201202_ENIA_V1_0.pdf",

    # France Villani Report
    "villani2018ai_meaningful-ai-france.pdf":
        "https://www.aiforhumanity.fr/pdfs/MissionVillani_Report_ENG-VF.pdf",

    # Korea AI Strategy
    "korea2019ai_national-strategy-ai.pdf":
        "https://wp.oecd.ai/app/uploads/2021/12/Korea_National_Strategy_for_Artificial_Intelligence_2019.pdf",

    # Japan AI Strategy
    "japan2019ai_ai-strategy-everyone.pdf":
        "https://www.cas.go.jp/jp/seisaku/jinkouchinou/pdf/aistratagy2019en.pdf",

    # Open Access: Long & Magerko AI Literacy (ACM OA)
    "long2020ailiteracy_what-is-ai-literacy.pdf":
        "https://dl.acm.org/doi/pdf/10.1145/3313831.3376727",

    # Bowen - Document Analysis (preprint-style)
    "bowen2009document_document-analysis-qualitative.pdf":
        "https://www.researchgate.net/profile/Glenn-Bowen/publication/240807798_Document_Analysis_as_a_Qualitative_Research_Method/links/59d807d0a6fdcc2aad065377/Document-Analysis-as-a-Qualitative-Research-Method.pdf",

    # Thierer - Pacing Problem
    "thierer2018pacing_pacing-problem-tech-regulation.pdf":
        "https://www.mercatus.org/system/files/thierer-pacing-problem-mercatus-v1.pdf",

    # EU Digital Education Action Plan
    "eu2020deap_digital-education-action-plan.pdf":
        "https://education.ec.europa.eu/sites/default/files/document-library-docs/deap-communication-sept2020_en.pdf",

    # Oxford Insights AI Readiness
    "oxfordinsights2023_ai-readiness-index.pdf":
        "https://oxfordinsights.com/wp-content/uploads/2023/12/2023-Government-AI-Readiness-Index-3.pdf",

    # White House Executive Order on AI
    "whitehouse2023aeo_executive-order-ai.pdf":
        "https://www.whitehouse.gov/wp-content/uploads/2023/10/M-24-10-Advancing-Governance-Innovation-and-Risk-Management-for-Agency-Use-of-Artificial-Intelligence.pdf",

    # Chile Política Nacional IA
    "chile2021ia_politica-nacional-ia.pdf":
        "https://minciencia.gob.cl/uploads/filer_public/bc/38/bc389daf-4514-4306-867c-760ae7686e2c/politica-nacional-ia.pdf",
}

# ============================================================
# DOI-based downloads (try Unpaywall / direct publisher)
# ============================================================
DOI_REFS = {
    "oecd2021digitaloutlook_digital-education-outlook.pdf": "10.1787/589b283f-en",
    "holmes2022ethics_ethics-ai-education-framework.pdf": "10.1007/s40593-021-00239-1",
    "holmes2022state_state-art-ai-education.pdf": "10.1111/ejed.12533",
    "grimmer2013text_text-as-data.pdf": "10.1093/pan/mps028",
    "rodriguez2022embeddings_word-embeddings-applied.pdf": "10.1086/715162",
    "fatima2020aipolicy_national-ai-policy-comparative.pdf": "10.1002/asi.24365",
    "jobin2019landscape_global-ai-ethics-guidelines.pdf": "10.1038/s42256-019-0088-2",
    "ball1998big_big-policies-small-world.pdf": "10.1080/03050069828225",
    "dolowitz2000learning_policy-transfer.pdf": "10.1111/0952-1895.00121",
    "nelson2020computational_computational-grounded-theory.pdf": "10.1177/0049124117729703",
    "kozlowski2019geometry_geometry-culture-embeddings.pdf": "10.1177/0003122419877135",
    "bareis2022talking_talking-ai-into-being.pdf": "10.1177/01622439211030007",
    "gulson2019digitizing_data-infrastructures-education.pdf": "10.1177/0263775818813144",
}

# ============================================================
# BOOKS & ITEMS REQUIRING MANUAL DOWNLOAD
# ============================================================
MANUAL = [
    ("holmes2019aied", "Holmes et al. (2019) AI in Education: Promises and Implications — BOOK, need library/purchase"),
    ("collingridge1980social", "Collingridge (1980) Social Control of Technology — BOOK, classic text"),
    ("bray2014comparative", "Bray et al. (2014) Comparative Education Research — BOOK"),
    ("rizvi2010globalizing", "Rizvi & Lingard (2010) Globalizing Education Policy — BOOK"),
    ("steiner2004global", "Steiner-Khamsi (2004) Global Politics Educational Borrowing — BOOK"),
    ("bereday1964comparative", "Bereday (1964) Comparative Method in Education — BOOK, classic"),
    ("noah1969toward", "Noah & Eckstein (1969) Toward a Science of Comparative Education — BOOK"),
    ("creswell2018mixed", "Creswell & Plano Clark (2018) Mixed Methods Research — BOOK"),
    ("moretti2013distant", "Moretti (2013) Distant Reading — BOOK"),
    ("krippendorff2018content", "Krippendorff (2018) Content Analysis — BOOK"),
    ("williamson2017big", "Williamson (2017) Big Data in Education — BOOK"),
    ("lasswell1951policy", "Lasswell (1951) The Policy Orientation — BOOK CHAPTER"),
    ("steinerkhamsi2014cross", "Steiner-Khamsi (2014) Cross-National Policy Borrowing — BOOK CHAPTER"),
    ("bray1995levels", "Bray & Thomas (1995) Levels of Comparison — JOURNAL (Harvard Educational Review, paywalled)"),
    ("southgate2020aiethics", "Southgate (2020) AI Ethics Equity Education — AUSTRALIAN GOV REPORT, search manually"),
    ("cminds2018iamexico", "C Minds (2018) Hacia una Estrategia IA México — search cminds.co"),
    ("sep2020sectorial", "SEP (2020) Programa Sectorial Educación 2020-2024 — DOF México"),
    ("sep2022nem", "SEP (2022) Plan de Estudios NEM — search gob.mx"),
    ("inegi2024endutih", "INEGI (2024) ENDUTIH 2023 — search inegi.org.mx"),
    ("germany2018aistrategy", "Bundesregierung (2018) AI Strategy Germany — search bmbf.de"),
    ("germany2020aiupdate", "Bundesregierung (2020) AI Strategy Update — search bmbf.de"),
    ("finland2017ai", "Finland (2017) Age of AI — search tem.fi"),
    ("estonia2019krattai", "Estonia (2019) AI Taskforce Report — search kratid.ee"),
    ("china2017ai", "China (2017) New Gen AI Development Plan — search English translation"),
    ("sevilla2022compute", "Sevilla et al. (2022) Compute Trends — conference paper, search ArXiv"),
    ("mikolov2013efficient", "Mikolov et al. (2013) Word2Vec — search ArXiv: 1301.3781"),
    ("devlin2019bert", "Devlin et al. (2019) BERT — search ArXiv: 1810.04805"),
]


def try_unpaywall(doi, filename):
    """Try Unpaywall API for open access PDF."""
    try:
        url = f"https://api.unpaywall.org/v2/{doi}?email=thesis@upaep.mx"
        req = urllib.request.Request(url, headers={"User-Agent": "Academic-Research/1.0"})
        with urllib.request.urlopen(req, timeout=15, context=ctx) as resp:
            data = json.loads(resp.read())
            if data.get("best_oa_location") and data["best_oa_location"].get("url_for_pdf"):
                pdf_url = data["best_oa_location"]["url_for_pdf"]
                print(f"  Unpaywall found OA PDF for {doi}")
                return download(pdf_url, filename)
            elif data.get("best_oa_location") and data["best_oa_location"].get("url"):
                print(f"  Unpaywall: OA page (no direct PDF) for {doi}: {data['best_oa_location']['url']}")
    except Exception as e:
        print(f"  Unpaywall failed for {doi}: {e}")
    return False


if __name__ == "__main__":
    results = {"downloaded": [], "failed": [], "manual": []}

    print("=" * 60)
    print("  DOWNLOADING DIRECT URLs")
    print("=" * 60)
    for filename, url in DIRECT_DOWNLOADS.items():
        ok = download(url, filename)
        if ok:
            results["downloaded"].append(filename)
        else:
            results["failed"].append((filename, url))
        time.sleep(0.5)

    print("\n" + "=" * 60)
    print("  TRYING DOI-BASED DOWNLOADS (Unpaywall)")
    print("=" * 60)
    for filename, doi in DOI_REFS.items():
        ok = try_unpaywall(doi, filename)
        if ok:
            results["downloaded"].append(filename)
        else:
            results["failed"].append((filename, f"doi:{doi}"))
        time.sleep(1)

    print("\n" + "=" * 60)
    print("  MANUAL DOWNLOAD REQUIRED")
    print("=" * 60)
    for bibkey, note in MANUAL:
        print(f"  [{bibkey}] {note}")
        results["manual"].append(bibkey)

    # Save manifest
    manifest_path = os.path.join(REFS_DIR, "MANIFEST.md")
    with open(manifest_path, "w", encoding="utf-8") as f:
        f.write("# Referencias — Manifest\n\n")
        f.write(f"Total en .bib: 75 referencias\n\n")
        f.write(f"## Descargadas ({len(results['downloaded'])})\n\n")
        for fn in sorted(results["downloaded"]):
            f.write(f"- `{fn}`\n")
        f.write(f"\n## Fallidas ({len(results['failed'])})\n\n")
        for fn, url in results["failed"]:
            f.write(f"- `{fn}` — {url}\n")
        f.write(f"\n## Descarga manual requerida ({len(results['manual'])})\n\n")
        for bibkey in results["manual"]:
            note = next(n for k, n in MANUAL if k == bibkey)
            f.write(f"- **{bibkey}**: {note}\n")

    print(f"\n{'=' * 60}")
    print(f"  SUMMARY")
    print(f"{'=' * 60}")
    print(f"  Downloaded: {len(results['downloaded'])}")
    print(f"  Failed:     {len(results['failed'])}")
    print(f"  Manual:     {len(results['manual'])}")
    print(f"\n  Manifest saved to: {manifest_path}")
