"""SPIKE Fase 4 — comparación cross-country en dézhì (China vs liberales).

Para cada país: recupera top-K pasajes de gobernanza de `politicas_v3`, traduce a
EN (EN primario por la Fase 3), clasifica con el panel de 7 jueces, y agrega la
mediana dézhì por país. Reporta el ranking + el desglose por origen (sidequest).

Uso: python -m pipeline_v3.compare_countries
"""
import json
import statistics as stats
from collections import defaultdict

import chromadb

from .config import CHROMA_DIR, COLLECTION_V3, PANEL, WEB_DATA_DIR
from .judges import classify, client
from pipeline.embeddings import get_embedding_function

GOV_QUERY = ("the role of the state and government in guiding, cultivating, directing or "
             "regulating AI in education and society; governance, state leadership, "
             "individual rights, rule of law, national planning")
COUNTRIES = ["china", "eeuu", "canada", "colombia", "alemania", "sudafrica", "australia"]
K = 3


def to_en(text: str, lang: str) -> str:
    if lang == "en":
        return text
    r = client().chat.completions.create(
        model="openai/gpt-4o-mini", temperature=0, max_tokens=700,
        messages=[{"role": "system", "content": "Translate the following public-policy text to English faithfully. Output ONLY the translation."},
                  {"role": "user", "content": text}])
    return r.choices[0].message.content.strip()


def main():
    col = chromadb.PersistentClient(path=str(CHROMA_DIR)).get_collection(
        COLLECTION_V3, embedding_function=get_embedding_function())
    recs = []  # {country, judge, origin, score}
    for c in COUNTRIES:
        q = col.query(query_texts=[GOV_QUERY], n_results=K, where={"country": c},
                      include=["documents", "metadatas"])
        docs, metas = q["documents"][0], q["metadatas"][0]
        passages = [to_en(d, m["language"]) for d, m in zip(docs, metas)]
        for p in passages:
            for j in PANEL:
                s = classify(j.model, p).get("score")
                if s is not None:
                    recs.append({"country": c, "judge": j.key, "origin": j.origin, "score": s})
        print(f"  {c:12s} clasificado ({len(passages)} pasajes)")

    by_c = defaultdict(list)
    for r in recs:
        by_c[r["country"]].append(r["score"])
    ranking = sorted((c for c in COUNTRIES if by_c[c]),
                     key=lambda c: -stats.median(by_c[c]))

    print("\n  ══ Ranking dézhì por país (mediana; +2 = Estado-dirige, -2 = derechos limitan) ══")
    for c in ranking:
        v = by_c[c]
        print(f"    {c:12s} {stats.median(v):+.2f}  (media {stats.mean(v):+.2f}, n={len(v)})")

    print("\n  Sidequest — mediana por origen del modelo:")
    origin_med = {}
    for origin in ("western", "chinese"):
        v = [r["score"] for r in recs if r["origin"] == origin]
        origin_med[origin] = stats.median(v)
        print(f"    {origin:10s} {stats.median(v):+.2f} (media {stats.mean(v):+.2f}, n={len(v)})")

    out = {
        "axis": "dezhi_governance", "k_passages": K, "n_classifications": len(recs),
        "country_dezhi": {c: {"median": stats.median(by_c[c]), "mean": stats.mean(by_c[c]),
                              "n": len(by_c[c])} for c in COUNTRIES if by_c[c]},
        "ranking": ranking,
        "origin_median": origin_med,
        "status": "PRELIMINAR / MVP — panel EN, K=3 pasajes de gobernanza/país",
    }
    WEB_DATA_DIR.mkdir(parents=True, exist_ok=True)
    (WEB_DATA_DIR / "dezhi_country_comparison.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n  Wrote {WEB_DATA_DIR / 'dezhi_country_comparison.json'}")


if __name__ == "__main__":
    main()
