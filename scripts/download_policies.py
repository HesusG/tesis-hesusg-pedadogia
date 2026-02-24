#!/usr/bin/env python3
"""
Download policy documents for the thesis corpus.
Run: python3 scripts/download_policies.py

Documents are saved to policies/raw/{country}/
A status report is printed at the end.
"""

import os
import sys
import json
import urllib.request
import urllib.error
import ssl
import time
from pathlib import Path

# Base directory
BASE = Path(__file__).resolve().parent.parent / "policies" / "raw"

# SSL context that doesn't verify (some government sites have cert issues)
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Each entry: (country_dir, filename, url, bib_key, notes)
DOCUMENTS = [
    # ── UNESCO (use alternate mirrors since unesdoc blocks direct download) ──
    ("unesco", "beijing_consensus_2019.pdf",
     "https://unesdoc.unesco.org/ark:/48223/pf0000368303/PDF/368303qaa.pdf.multi",
     "unesco2019beijing", "Beijing Consensus on AI and Education"),

    ("unesco", "ethics_recommendation_2021.pdf",
     "https://unesdoc.unesco.org/ark:/48223/pf0000381137/PDF/381137eng.pdf.multi",
     "unesco2021ai", "Recommendation on the Ethics of AI"),

    ("unesco", "ai_education_guidance_2021.pdf",
     "https://discovery.ucl.ac.uk/id/eprint/10130180/1/Miao%20and%20Holmes%20-%202021%20-%20AI%20and%20education%20guidance%20for%20policy-makers.pdf",
     "miao2021guidance", "AI and Education: Guidance for Policy-Makers"),

    ("unesco", "genai_guidance_2023.pdf",
     "https://cdn.table.media/assets/wp-content/uploads/2023/09/386693eng.pdf",
     "unesco2023genai", "Guidance for Generative AI in Education"),

    ("unesco", "gem_report_2023.pdf",
     "https://unesdoc.unesco.org/ark:/48223/pf0000385723/PDF/385723eng.pdf.multi",
     "unesco2023gem", "GEM Report 2023: Technology in Education"),

    ("unesco", "ai_education_challenges_2019.pdf",
     "https://unesdoc.unesco.org/ark:/48223/pf0000366994/PDF/366994eng.pdf.multi",
     "pedro2019aieducation", "AI in Education: Challenges and Opportunities"),

    # ── OECD ──
    ("oecd", "ai_principles_2019.pdf",
     "MANUAL",
     "oecd2019ai", "MANUAL: Visit https://legalinstruments.oecd.org/en/instruments/OECD-LEGAL-0449"),

    ("oecd", "digital_education_outlook_2021.pdf",
     "MANUAL",
     "oecd2021digitaloutlook", "MANUAL: OECD publication, requires purchase or library access"),

    # ── WEF ──
    ("wef", "future_of_jobs_2020.pdf",
     "https://www3.weforum.org/docs/WEF_Future_of_Jobs_2020.pdf",
     "wef2020future", "Future of Jobs Report 2020"),

    # ── World Bank ──
    ("worldbank", "reimagining_human_connections_2020.pdf",
     "MANUAL",
     "worldbank2020reimagining", "MANUAL: Search World Bank Open Knowledge Repository"),

    # ── EU ──
    ("eu", "ai_act_2024.pdf",
     "https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=OJ:L_202401689",
     "eu2024aiact", "EU AI Act - Regulation 2024/1689"),

    ("eu", "digital_education_action_plan_2020.pdf",
     "MANUAL",
     "eu2020deap", "MANUAL: Search EUR-Lex for COM(2020) 624 final"),

    # ── Spain ──
    ("spain", "enia_2020.pdf",
     "https://portal.mineco.gob.es/RecursosArticulo/mineco/ministerio/ficheros/201202_ENIA_V1_0.pdf",
     "spain2020enia", "Estrategia Nacional de Inteligencia Artificial"),

    # ── France ──
    ("france", "villani_report_2018.pdf",
     "https://www.jaist.ac.jp/~bao/AI/OtherAIstrategies/MissionVillani_Report_ENG-VF.pdf",
     "villani2018ai", "For a Meaningful AI (Villani Report)"),

    # ── Germany ──
    ("germany", "ai_strategy_2018.pdf",
     "https://www.ki-strategie-deutschland.de/home.html?file=files/downloads/Nationale_KI-Strategie_engl.pdf",
     "germany2018aistrategy", "KI-Strategie der Bundesregierung"),

    ("germany", "ai_strategy_update_2020.pdf",
     "MANUAL",
     "germany2020aiupdate", "MANUAL: Search bundesregierung.de for Fortschreibung 2020"),

    # ── Finland ──
    ("finland", "ai_strategy_2017.pdf",
     "MANUAL",
     "finland2017ai", "MANUAL: Search tem.fi for Finland's Age of AI report"),

    # ── Estonia ──
    ("estonia", "krattai_2019.pdf",
     "MANUAL",
     "estonia2019krattai", "MANUAL: Search kratid.ee or riigikantselei.ee for AI taskforce report"),

    # ── USA ──
    ("usa", "executive_order_ai_2023.pdf",
     "MANUAL",
     "whitehouse2023aeo", "MANUAL: Visit federalregister.gov and search for EO 14110 (Oct 30, 2023). Save PDF."),

    # ── Canada ──
    ("canada", "pan_canadian_ai_strategy_2017.pdf",
     "https://www.jaist.ac.jp/~bao/AI/OtherAIstrategies/Pan-Canadian%20Artificial%20Intelligence%20Strategy.pdf",
     "canada2017ai", "Pan-Canadian AI Strategy"),

    # ── Mexico ──
    ("mexico", "ia_mexico_2018.pdf",
     "MANUAL",
     "cminds2018iamexico", "MANUAL: Search cminds.co for Hacia una Estrategia de IA en Mexico"),

    ("mexico", "programa_sectorial_educacion_2020.pdf",
     "MANUAL",
     "sep2020sectorial", "MANUAL: Search DOF or sep.gob.mx for PSE 2020-2024"),

    ("mexico", "nem_plan_estudios_2022.pdf",
     "MANUAL",
     "sep2022nem", "MANUAL: Search sep.gob.mx for Plan de Estudios NEM 2022"),

    # ── Brazil ──
    ("brazil", "ebia_2021.pdf",
     "https://lapin.org.br/wp-content/uploads/2021/04/Estrategia-Brasileira-de-Inteligencia-Artificial.pdf",
     "brasil2021ebia", "Estrategia Brasileira de Inteligencia Artificial"),

    # ── Chile ──
    ("chile", "politica_ia_2021.pdf",
     "MANUAL",
     "chile2021ia", "MANUAL: Search minciencia.gob.cl for Politica Nacional de IA"),

    # ── Colombia ──
    ("colombia", "conpes_3975_2019.pdf",
     "https://colaboracion.dnp.gov.co/CDT/Conpes/Econ%C3%B3micos/3975.pdf",
     "colombia2019conpes", "CONPES 3975"),

    # ── China ──
    ("china", "ngaidp_2017.pdf",
     "MANUAL",
     "china2017ai", "MANUAL: Visit https://digichina.stanford.edu/work/full-translation-chinas-new-generation-artificial-intelligence-development-plan-2017/ and save as PDF"),

    # ── Japan ──
    ("japan", "ai_strategy_2019.pdf",
     "https://www8.cao.go.jp/cstp/ai/aistratagy2019en.pdf",
     "japan2019ai", "AI Strategy 2019: AI for Everyone"),

    # ── Korea ──
    ("korea", "ai_strategy_2019.pdf",
     "https://wp.oecd.ai/app/uploads/2021/12/Korea_National_Strategy_for_Artificial_Intelligence_2019.pdf",
     "korea2019ai", "National Strategy for Artificial Intelligence"),

    # ── Singapore ──
    ("singapore", "nais_2019.pdf",
     "https://file.go.gov.sg/nais2019.pdf",
     "singapore2019nais", "National AI Strategy"),

    # ── India ──
    ("india", "aiforall_2018.pdf",
     "https://www.niti.gov.in/sites/default/files/2023-03/National-Strategy-for-Artificial-Intelligence.pdf",
     "india2018niti", "National Strategy for AI: #AIForAll"),

    ("india", "nep_2020.pdf",
     "https://www.education.gov.in/sites/upload_files/mhrd/files/NEP_Final_English_0.pdf",
     "india2020nep", "National Education Policy 2020"),

    # ── Australia ──
    ("australia", "ai_action_plan_2021.pdf",
     "https://wp.oecd.ai/app/uploads/2021/12/Australia_AI_Action_Plan_2021.pdf",
     "australia2021aiaction", "Australia's AI Action Plan"),
]


def download_file(url, dest_path):
    """Download a file from URL to dest_path. Returns (success, message)."""
    if url == "MANUAL":
        return False, "Manual download required"

    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Thesis-Research/1.0"
        })
        with urllib.request.urlopen(req, timeout=30, context=ctx) as response:
            content = response.read()

            # Check if we got a reasonable file (>1KB)
            if len(content) < 1024:
                return False, f"File too small ({len(content)} bytes), likely error page"

            with open(dest_path, "wb") as f:
                f.write(content)

            size_mb = len(content) / (1024 * 1024)
            return True, f"Downloaded ({size_mb:.1f} MB)"

    except urllib.error.HTTPError as e:
        return False, f"HTTP {e.code}: {e.reason}"
    except urllib.error.URLError as e:
        return False, f"URL Error: {e.reason}"
    except Exception as e:
        return False, f"Error: {str(e)}"


def main():
    print("=" * 60)
    print("POLICY DOCUMENT DOWNLOADER")
    print("=" * 60)
    print()

    results = {"downloaded": [], "manual": [], "failed": []}

    for country_dir, filename, url, bib_key, notes in DOCUMENTS:
        dest_dir = BASE / country_dir
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest_path = dest_dir / filename

        # Skip if already downloaded
        if dest_path.exists() and dest_path.stat().st_size > 1024:
            print(f"  SKIP  {country_dir}/{filename} (already exists)")
            results["downloaded"].append((country_dir, filename, bib_key, "Already existed"))
            continue

        if url == "MANUAL":
            print(f"  MANUAL {country_dir}/{filename}")
            print(f"         -> {notes}")
            results["manual"].append((country_dir, filename, bib_key, notes))
            continue

        print(f"  GET   {country_dir}/{filename}...", end=" ", flush=True)
        success, msg = download_file(url, dest_path)

        if success:
            print(f"OK - {msg}")
            results["downloaded"].append((country_dir, filename, bib_key, msg))
        else:
            print(f"FAIL - {msg}")
            results["failed"].append((country_dir, filename, bib_key, f"{msg} | URL: {url}"))

        time.sleep(0.5)  # Be polite

    # Summary
    print()
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"  Downloaded:     {len(results['downloaded'])}")
    print(f"  Manual needed:  {len(results['manual'])}")
    print(f"  Failed:         {len(results['failed'])}")
    print()

    if results["manual"]:
        print("MANUAL DOWNLOADS NEEDED:")
        print("-" * 40)
        for country, fname, key, notes in results["manual"]:
            print(f"  [{key}] {country}/{fname}")
            print(f"    {notes}")
        print()

    if results["failed"]:
        print("FAILED DOWNLOADS (retry or download manually):")
        print("-" * 40)
        for country, fname, key, msg in results["failed"]:
            print(f"  [{key}] {country}/{fname}")
            print(f"    {msg}")
        print()

    # Save status to JSON
    status_path = BASE.parent / "download_status.json"
    status = {
        "downloaded": [{"country": c, "file": f, "bib_key": k, "status": s}
                       for c, f, k, s in results["downloaded"]],
        "manual": [{"country": c, "file": f, "bib_key": k, "instructions": s}
                   for c, f, k, s in results["manual"]],
        "failed": [{"country": c, "file": f, "bib_key": k, "error": s}
                   for c, f, k, s in results["failed"]],
    }
    with open(status_path, "w", encoding="utf-8") as f:
        json.dump(status, f, indent=2, ensure_ascii=False)
    print(f"Status saved to: {status_path}")

    # Zotero import instructions
    print()
    print("=" * 60)
    print("ZOTERO IMPORT")
    print("=" * 60)
    print("  1. Open Zotero")
    print("  2. File → Import → select document/referencias.bib")
    print("  3. This imports all citation metadata")
    print("  4. Then drag-and-drop downloaded PDFs to their entries")
    print("  5. Or use Zotero's 'Find Available PDF' for academic papers")


if __name__ == "__main__":
    main()
