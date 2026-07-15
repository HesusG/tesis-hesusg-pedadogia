"""SPIKE Fase 2c — fetch corpus China 2025-2026 de IA-educación (curl + extracción).

Recupera texto VERBATIM de páginas gov/edu chinas con curl (WebFetch resume, no sirve),
extrae texto limpio (stdlib, sin deps), guarda el ZH crudo y registra la metadata Tier A.
Traducción ZH→EN e ingesta son pasos posteriores.

Uso: python -m pipeline_v3.fetch_china
"""
import re
import json
import html
import subprocess
from pathlib import Path

from .config import PROJECT_ROOT, GENRE_VOCAB

RAW_DIR = PROJECT_ROOT / "policies" / "raw" / "china_2026"
REGISTRY = Path(__file__).parent / "china_2026_registry.json"

# Registro pre-registrado (Tier A). url=None => pendiente de pinear (provinciales 2025).
DOCS = [
    # ── 2026 nacionales/provinciales con URL confirmada ──
    {"doc_id": "cn_ai_edu_action_2026", "year": 2026, "genre": "action_plan", "scope": "national",
     "adopting_body": "教育部+4部委", "doc_type_official": "行动计划",
     "title_en": "AI + Education Action Plan (人工智能+教育行动计划)",
     "url": "https://www.eol.cn/zhengce/wenjian/202604/t20260410_2727386.shtml"},
    {"doc_id": "cn_ai_edu_qa_2026", "year": 2026, "genre": "guidance", "scope": "national",
     "adopting_body": "教育部科信司", "doc_type_official": "答记者问",
     "title_en": "MoE Q&A on the AI+Education Plan",
     "url": "http://www.moe.gov.cn/jyb_xwfb/s271/202604/t20260410_1433232.html"},
    {"doc_id": "cn_edu_15fyp_2026", "year": 2026, "genre": "strategy", "scope": "national",
     "adopting_body": "国务院", "doc_type_official": "规划",
     "title_en": "Education Development 15th Five-Year Plan (教育发展十五五规划)",
     "url": "http://www.moe.gov.cn/jyb_xxgk/moe_1777/moe_1778/202606/t20260629_1442045.html"},
    {"doc_id": "cn_teachers_genai_report_2026", "year": 2026, "genre": "report", "scope": "national",
     "adopting_body": "教育部教育技术与资源发展中心", "doc_type_official": "报告",
     "title_en": "China Teachers' Generative-AI Usage Report 2026",
     "url": "https://www.ncet.edu.cn/zhuzhan/sjsyzyxw/20260514/6765.html"},
    {"doc_id": "cn_guangdong_ai_edu_2026", "year": 2026, "genre": "guidance", "scope": "provincial",
     "adopting_body": "广东省教育厅", "doc_type_official": "应用指南",
     "title_en": "Guangdong Basic-Education AI Full-Scenario Application Guide",
     "url": "https://www.szns.gov.cn/nsqjyj/gkmlpt/content/12/12794/post_12794118.html"},
    # ── provinciales/nacionales 2025 — URL exacta PENDIENTE de pinear ──
    {"doc_id": "cn_statecouncil_aiplus_2025", "year": 2025, "genre": "law", "scope": "national",
     "adopting_body": "国务院", "doc_type_official": "意见",
     "title_en": "State Council 'AI+' Opinion (education/AI-literacy section)", "url": None},
    {"doc_id": "cn_beijing_k12_ai_2025", "year": 2025, "genre": "action_plan", "scope": "municipal",
     "adopting_body": "北京市教委", "doc_type_official": "工作方案",
     "title_en": "Beijing K-12 AI Education Plan 2025-2027", "url": None},
    {"doc_id": "cn_zhejiang_ai_edu_2025", "year": 2025, "genre": "action_plan", "scope": "provincial",
     "adopting_body": "浙江省教育厅", "doc_type_official": "行动方案",
     "title_en": "Zhejiang 'AI+Education' Action Plan 2025-2029", "url": None},
    {"doc_id": "cn_henan_ai_edu_2025", "year": 2025, "genre": "action_plan", "scope": "provincial",
     "adopting_body": "河南省教育厅", "doc_type_official": "三年行动计划",
     "title_en": "Henan 'AI+Education' 3-Year Action Plan 2025-2027", "url": None},
    {"doc_id": "cn_jiangsu_ai_edu_2025", "year": 2025, "genre": "action_plan", "scope": "provincial",
     "adopting_body": "江苏省教育厅", "doc_type_official": "行动方案",
     "title_en": "Jiangsu AI-Enabled Education Development Plan 2025-2027", "url": None},
]


def fetch(url: str) -> str:
    r = subprocess.run(["curl", "-sL", "-A", "Mozilla/5.0", "-m", "30", url],
                       capture_output=True, timeout=70)
    raw = r.stdout
    for enc in ("utf-8", "gb18030"):
        try:
            return raw.decode(enc)
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8", "ignore")


def html_to_text(h: str) -> str:
    h = re.sub(r"(?is)<(script|style).*?</\1>", " ", h)
    h = re.sub(r"(?i)<br\s*/?>", "\n", h)
    h = re.sub(r"(?i)</(p|div|li|h[1-6]|tr|section)>", "\n", h)
    h = re.sub(r"(?s)<[^>]+>", " ", h)
    h = html.unescape(h)
    lines = []
    for ln in h.splitlines():
        ln = re.sub(r"[ \t ]+", " ", ln).strip()
        if len(ln) >= 8 and re.search(r"[一-鿿]", ln):   # línea con contenido chino
            lines.append(ln)
    return "\n".join(lines)


def main():
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    assert all(d["genre"] in GENRE_VOCAB for d in DOCS), "genre fuera del vocabulario controlado"
    reg = []
    for d in DOCS:
        rec = {**d, "language": "zh", "country": "china", "region": "asia", "ingest_version": "v3.0"}
        if not d["url"]:
            rec["status"] = "url_pendiente"
            print(f"  [PEND] {d['doc_id']:32s} (falta URL exacta — provincial 2025)")
            reg.append(rec)
            continue
        try:
            text = html_to_text(fetch(d["url"]))
            ai = text.count("人工智能")
            (RAW_DIR / f"{d['doc_id']}_zh.txt").write_text(text, encoding="utf-8")
            rec.update(status="ok", source_uri=d["url"], n_chars=len(text), ai_mentions=ai)
            flag = "" if ai >= 3 and len(text) > 800 else "  ⚠ revisar (poco contenido)"
            print(f"  [OK]   {d['doc_id']:32s} {len(text):>7} chars | 人工智能×{ai}{flag}")
        except Exception as e:  # noqa: BLE001
            rec.update(status=f"fail: {e}", source_uri=d["url"])
            print(f"  [FAIL] {d['doc_id']:32s} {e}")
        reg.append(rec)
    REGISTRY.write_text(json.dumps(reg, ensure_ascii=False, indent=2), encoding="utf-8")
    ok = sum(1 for r in reg if r.get("status") == "ok")
    pend = sum(1 for r in reg if r.get("status") == "url_pendiente")
    print(f"\n  Fetched OK: {ok} | URL pendiente: {pend} | total registrados: {len(reg)}")
    print(f"  ZH crudo -> {RAW_DIR}  |  registro -> {REGISTRY.name}")


if __name__ == "__main__":
    main()
