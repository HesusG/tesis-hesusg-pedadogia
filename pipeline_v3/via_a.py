"""SPIKE Fase 5 — Vía A (embeddings) sobre los 7 países de `politicas_v3`.

El MVP confuciano (`pipeline/confucian_axes.py`) proyectó el eje dézhì solo sobre
3 documentos de la colección v1. Para poder contrastar **Vía A vs Vía B** país por
país hace falta la misma proyección sobre el corpus v3 completo.

Reusa el eje GANADOR del A/B previo (anchor_mode=hybrid, axis_set=tuned6) sin
reconstruirlo: mismo `build_axis`, mismas anclas de las Analectas. Lo único nuevo
es el corpus proyectado y el fondo del z-score (todo `politicas_v3`).

Uso: python -m pipeline_v3.via_a
"""
import json
import random

import numpy as np
import chromadb

from .config import CHROMA_DIR, COLLECTION_V3, CACHE_DIR
from pipeline.config import ANALECTS_COLLECTION_NAME, CONFUCIAN_AXES
from pipeline.confucian_axes import build_axis, l2norm, bg_stats, axis_stats
from pipeline.embeddings import get_embedding_function

COUNTRIES = ["china", "eeuu", "canada", "colombia", "alemania", "sudafrica", "australia"]
ANCHOR_MODE = "hybrid"       # ganador del A/B 3×3 (spike previo)
AXIS_KEY = "dezhi_fa"
OUT_FILE = CACHE_DIR / "via_a_dezhi.json"
SEED, N_BOOT = 42, 5000


def boot_ci_median(zs: np.ndarray, seed: int = SEED, n_boot: int = N_BOOT) -> list[float]:
    """IC95 bootstrap de la mediana. Canadá tiene 15 chunks: sin IC, su punto engaña."""
    rng = random.Random(seed)
    n = len(zs)
    meds = sorted(float(np.median([zs[rng.randrange(n)] for _ in range(n)])) for _ in range(n_boot))
    return [meds[int(0.025 * n_boot)], meds[int(0.975 * n_boot)]]


def main():
    ef = get_embedding_function()
    cl = chromadb.PersistentClient(path=str(CHROMA_DIR))
    pol = cl.get_collection(COLLECTION_V3, embedding_function=ef)
    analects = cl.get_collection(ANALECTS_COLLECTION_NAME, embedding_function=ef)

    axis = build_axis(ANCHOR_MODE, ef, analects, CONFUCIAN_AXES[AXIS_KEY])

    # Fondo del z-score = TODO el corpus v3 (mismo fondo para todos los países →
    # la comparación entre países no depende de qué país se mire).
    allv = pol.get(include=["embeddings", "metadatas"])
    vecs = l2norm(np.array(allv["embeddings"]))
    countries = [m.get("country") for m in allv["metadatas"]]
    mu, sigma = bg_stats(vecs, axis)
    print(f"  Fondo: {len(vecs)} chunks  mu={mu:+.4f}  sigma={sigma:.4f}")

    out = {}
    for c in COUNTRIES:
        idx = [i for i, x in enumerate(countries) if x == c]
        if not idx:
            print(f"  ⚠ {c}: sin chunks en {COLLECTION_V3}")
            continue
        out[c] = axis_stats(vecs[idx], axis, mu, sigma)
        out[c]["ci95_median"] = boot_ci_median((vecs[idx] @ axis - mu) / sigma)

    print(f"\n  ══ Vía A — dézhì por embeddings (mediana z, fondo = corpus v3) ══")
    for c, v in sorted(out.items(), key=lambda kv: -kv[1]["median_z"]):
        lo, hi = v["ci95_median"]
        print(f"    {c:12s} {v['median_z']:+.3f}  IC95 [{lo:+.2f}, {hi:+.2f}]  n={v['n_chunks']}")

    # ¿Los IC de China y Canadá se solapan? Si sí, el "empate" es sólido, no un artefacto.
    if "china" in out and "canada" in out:
        ch, ca = out["china"]["ci95_median"], out["canada"]["ci95_median"]
        overlap = ch[0] <= ca[1] and ca[0] <= ch[1]
        print(f"\n    China vs Canadá: brecha {out['china']['median_z'] - out['canada']['median_z']:+.3f} z; "
              f"IC95 {'SE SOLAPAN → empate estadístico' if overlap else 'NO se solapan → hay separación'}")

    payload = {"axis": AXIS_KEY, "anchor_mode": ANCHOR_MODE, "collection": COLLECTION_V3,
               "background_n": len(vecs), "background_mu": mu, "background_sigma": sigma,
               "country_scores": out}
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    OUT_FILE.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n  Wrote {OUT_FILE}")


if __name__ == "__main__":
    main()
