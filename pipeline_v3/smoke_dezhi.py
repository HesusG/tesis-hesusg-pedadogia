"""SPIKE Fase 2 (pre) — smoke test del edge case fǎ / Legalismo (法家).

Pregunta: ¿el panel clasifica una LEY DE CONTROL china (GenAI Interim Measures 2023,
legalista/estatista) como POSITIVO (Estado-dirige) — y NO como negativo (liberal),
que sería el error de confundir "ley" con "derechos que limitan al Estado"?

También verifica que cada modelo de OpenRouter responde (definido != funcionando).
"""
import statistics as stats

from .config import PANEL, PROJECT_ROOT
from .judges import classify

RAW = PROJECT_ROOT / "policies" / "raw" / "china"
PROC = PROJECT_ROOT / "policies" / "processed"


def chunks(text, size=500, overlap=50):
    out, i = [], 0
    while i < len(text):
        c = text[i:i + size].strip()
        if len(c) > 120:
            out.append(c)
        i += size - overlap
    return out


def pick(path, keywords, n=2):
    text = " ".join(path.read_text(encoding="utf-8").split())
    cand = [c for c in chunks(text) if any(k in c.lower() for k in keywords)]
    return cand[:n]


def main():
    passages = []
    # EDGE CASE: ley de control china (legalista) -> DEBE ser positivo (Estado-dirige)
    for c in pick(RAW / "2_generative_ai_interim_measures_2023_en.txt",
                  ["shall", "provider", "supervis", "management", "security", "measures"], n=3):
        passages.append({"doc": "China GenAI Measures (LEY control)", "expect": ">0", "text": c})
    # Contraste estatista: plan nacional china -> positivo
    for c in pick(RAW / "3_new_gen_ai_development_plan_2017_en.txt",
                  ["national", "strategic", "state", "nation"], n=1):
        passages.append({"doc": "China NGAIDP (plan estatal)", "expect": ">0", "text": c})
    # Contraste liberal: estrategia canadiense -> <=0
    for c in pick(PROC / "canada_pan_canadian_ai_strategy_2017.txt",
                  ["government", "invest", "lead", "fund"], n=1):
        passages.append({"doc": "Canadá (estrategia liberal)", "expect": "<=0", "text": c})

    print(f"Pasajes: {len(passages)} | Jueces: {len(PANEL)}\n")
    header = "  " + " " * 34 + "".join(f"{j.key[:8]:>9}" for j in PANEL) + f"{'MEDIANA':>9}"
    print(header)

    rows = []
    for p in passages:
        scores, cells = {}, ""
        for j in PANEL:
            r = classify(j.model, p["text"])
            s = r.get("score")
            scores[j.key] = s
            cells += f"{(str(s) if s is not None else 'ERR'):>9}"
        vals = [v for v in scores.values() if v is not None]
        med = stats.median(vals) if vals else None
        rows.append({**p, "scores": scores, "median": med})
        cells += f"{(f'{med:+.1f}' if med is not None else 'NA'):>9}"
        print(f"  {p['doc'][:34]:34s}{cells}")

    # ── Veredicto del edge case ──
    law = [r for r in rows if "GenAI" in r["doc"] and r["median"] is not None]
    law_ok = all(r["median"] > 0 for r in law)
    print("\n  EDGE CASE fǎ/Legalismo:")
    print(f"    Ley de control china clasificada como POSITIVO (Estado-dirige, no liberal): "
          f"{'✅ PASA' if law_ok else '❌ FALLA — algunos jueces la leen como liberal'}")
    # errores de modelo
    errs = {j.key: sum(1 for r in rows if r["scores"].get(j.key) is None) for j in PANEL}
    broken = [k for k, v in errs.items() if v == len(rows)]
    print(f"    Modelos que respondieron: {[j.key for j in PANEL if j.key not in broken]}")
    if broken:
        print(f"    Modelos caídos (revisar ID): {broken}")
    # acuerdo origen chino vs occidental (sidequest, preliminar)
    west = [s for r in rows for j in PANEL if j.origin == "western" and (s := r["scores"].get(j.key)) is not None]
    chi = [s for r in rows for j in PANEL if j.origin == "chinese" and (s := r["scores"].get(j.key)) is not None]
    if west and chi:
        print(f"    Sidequest (preliminar): media occidental={stats.mean(west):+.2f} vs china={stats.mean(chi):+.2f}")


if __name__ == "__main__":
    main()
