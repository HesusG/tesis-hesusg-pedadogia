"""SPIKE Fase 3 — experimento de idioma: ZH vs EN × origen (chino vs occidental).

Convierte el edge case de idioma en un hallazgo medible: ¿cuánto mueve el score
del clasificador el IDIOMA del texto (chino vs inglés traducido) frente al ORIGEN
del modelo (chino vs occidental)? Diseño 2×2 sobre pasajes de gobernanza del corpus
China v3.

Uso: python -m pipeline_v3.lang_experiment
"""
import statistics as stats
import chromadb

from .config import CHROMA_DIR, COLLECTION_V3, PANEL
from .judges import classify, client
from pipeline.embeddings import get_embedding_function

GOV_QUERY = ("el papel del Estado en dirigir, cultivar, guiar o regular la educación "
             "en IA y la sociedad; gobernanza, liderazgo estatal, derechos, ley")
N_PASSAGES = 6


def translate_to_en(text: str) -> str:
    r = client().chat.completions.create(
        model="openai/gpt-4o-mini", temperature=0, max_tokens=700,
        messages=[
            {"role": "system", "content": "Translate the following Chinese public-policy text to English, faithfully and completely. Output ONLY the English translation, no notes."},
            {"role": "user", "content": text},
        ])
    return r.choices[0].message.content.strip()


def main():
    col = chromadb.PersistentClient(path=str(CHROMA_DIR)).get_collection(
        COLLECTION_V3, embedding_function=get_embedding_function())
    q = col.query(query_texts=[GOV_QUERY], n_results=N_PASSAGES,
                  include=["documents", "metadatas"])
    passages = [{"zh": d, "pid": m["policy_id"]}
                for d, m in zip(q["documents"][0], q["metadatas"][0])]
    print(f"{len(passages)} pasajes de gobernanza (China v3):")
    for p in passages:
        print(f"  - {p['pid']}")
    print("\nTraduciendo ZH→EN (gpt-4o-mini, cacheado en memoria)...")
    for p in passages:
        p["en"] = translate_to_en(p["zh"])

    # clasificar: pasaje × idioma × juez
    recs = []
    for p in passages:
        for lang in ("zh", "en"):
            for j in PANEL:
                s = classify(j.model, p[lang]).get("score")
                if s is not None:
                    recs.append({"pid": p["pid"], "lang": lang, "judge": j.key,
                                 "origin": j.origin, "score": s})
    print(f"\n  Clasificaciones válidas: {len(recs)} / {len(passages)*2*len(PANEL)}")

    def mean(f):
        v = [r["score"] for r in recs if f(r)]
        return stats.mean(v) if v else float("nan")

    print("\n  Media de score (idioma × origen):")
    print(f"  {'':8s}{'occidental':>12}{'chino':>9}{'  |  fila':>9}")
    for lang in ("zh", "en"):
        w = mean(lambda r: r["lang"] == lang and r["origin"] == "western")
        c = mean(lambda r: r["lang"] == lang and r["origin"] == "chinese")
        row = mean(lambda r: r["lang"] == lang)
        print(f"  {lang.upper():8s}{w:>12.2f}{c:>9.2f}{row:>12.2f}")

    lang_eff = mean(lambda r: r["lang"] == "zh") - mean(lambda r: r["lang"] == "en")
    orig_eff = mean(lambda r: r["origin"] == "chinese") - mean(lambda r: r["origin"] == "western")
    print(f"\n  ▸ Efecto IDIOMA  (ZH − EN):     {lang_eff:+.2f}")
    print(f"  ▸ Efecto ORIGEN  (chino − occ): {orig_eff:+.2f}")
    print("  Interpretación: si |idioma| >> |origen|, el idioma domina (traducir importa);")
    print("  si son comparables, el origen del modelo es un factor real (tu sidequest).")


if __name__ == "__main__":
    main()
