"""SPIKE Fase 5/7 — Vía A (embeddings): los 6 ejes confucianos sobre los 7 países.

El MVP confuciano (`pipeline/confucian_axes.py`) proyectó los 6 ejes sobre solo
3 documentos de la colección v1. Aquí se proyectan los **6 ejes completos sobre
`politicas_v3`** (7 países), que es lo que hace falta para:

  - el **radar** de perfil confuciano por país (6 ejes = 6 vértices), y
  - el contraste **Vía A vs Vía B** en dézhì, país por país.

Reusa el eje GANADOR del A/B previo (anchor_mode=hybrid, axis_set=tuned6) sin
reconstruirlo: mismo `build_axis`, mismas anclas de las Analectas. Lo único nuevo
es el corpus proyectado y el fondo del z-score (todo `politicas_v3`), de modo que
la comparación entre países no dependa de qué país se mire.

Uso: python -m pipeline_v3.via_a
"""
import json

import numpy as np
import chromadb

from .config import CHROMA_DIR, COLLECTION_V3, CACHE_DIR, WEB_DATA_DIR, DEEP_DIVE_DOCS
from pipeline.config import ANALECTS_COLLECTION_NAME, CONFUCIAN_AXES, AXIS_SETS
from pipeline.confucian_axes import build_axis, l2norm, bg_stats, axis_stats
from pipeline.embeddings import get_embedding_function

COUNTRIES = ["china", "eeuu", "canada", "colombia", "alemania", "sudafrica", "australia"]
ANCHOR_MODE = "hybrid"          # ganador del A/B 3×3 (spike previo)
AXIS_SET = "tuned6"             # ren, li, yi, xiushen, dezhi_fa, he
PRIMARY_AXIS = "dezhi_fa"       # el que va también por Vía B (panel LLM)
OUT_FILE = CACHE_DIR / "via_a_dezhi.json"          # lo consume agreement.py
AXES_FILE = CACHE_DIR / "via_a_axes.json"
RADAR_FILE = WEB_DATA_DIR / "confucian_radar_v3.json"
SEED, N_BOOT = 42, 5000


def boot_ci_median(zs: np.ndarray, seed: int = SEED, n_boot: int = N_BOOT) -> list[float]:
    """IC95 bootstrap de la mediana, vectorizado.

    Sin intervalo, los puntos engañan: Canadá aporta 15 fragmentos y Sudáfrica
    1303, así que sus medianas no merecen la misma confianza.
    """
    rng = np.random.default_rng(seed)
    n = len(zs)
    idx = rng.integers(0, n, size=(n_boot, n))
    meds = np.sort(np.median(zs[idx], axis=1))
    return [float(meds[int(0.025 * n_boot)]), float(meds[int(0.975 * n_boot)])]


def main():
    ef = get_embedding_function()
    cl = chromadb.PersistentClient(path=str(CHROMA_DIR))
    pol = cl.get_collection(COLLECTION_V3, embedding_function=ef)
    analects = cl.get_collection(ANALECTS_COLLECTION_NAME, embedding_function=ef)

    allv = pol.get(include=["embeddings", "metadatas"])
    # Fuera los documentos de análisis-en-profundidad: no son comparables entre países,
    # ni deben contaminar el fondo del z-score (ver config.DEEP_DIVE_DOCS).
    keep = [i for i, m in enumerate(allv["metadatas"])
            if m.get("policy_id") not in DEEP_DIVE_DOCS]
    dropped = len(allv["metadatas"]) - len(keep)
    vecs = l2norm(np.array(allv["embeddings"]))[keep]
    countries = [allv["metadatas"][i].get("country") for i in keep]
    print(f"  Corpus: {len(vecs)} chunks, {len(set(countries))} países "
          f"({dropped} excluidos por DEEP_DIVE_DOCS)")

    axis_keys = AXIS_SETS[AXIS_SET]
    by_axis, background = {}, {}
    for ax_key in axis_keys:
        axis = build_axis(ANCHOR_MODE, ef, analects, CONFUCIAN_AXES[ax_key])
        mu, sigma = bg_stats(vecs, axis)
        background[ax_key] = {"mu": mu, "sigma": sigma}
        scores = {}
        for c in COUNTRIES:
            idx = [i for i, x in enumerate(countries) if x == c]
            if not idx:
                print(f"  ⚠ {c}: sin chunks")
                continue
            st = axis_stats(vecs[idx], axis, mu, sigma)
            st["ci95_median"] = boot_ci_median((vecs[idx] @ axis - mu) / sigma)
            scores[c] = st
        by_axis[ax_key] = scores
        print(f"  eje {ax_key:10s} listo (mu={mu:+.4f} sigma={sigma:.4f})")

    # ── Tabla país × eje (la materia prima del radar) ──
    print(f"\n  ══ Vía A — perfil confuciano por país (mediana z, fondo = corpus v3) ══")
    head = "    " + f"{'país':12s}" + "".join(f"{k:>11s}" for k in axis_keys)
    print(head)
    for c in COUNTRIES:
        if c not in by_axis[axis_keys[0]]:
            continue
        row = "".join(f"{by_axis[k][c]['median_z']:>+11.3f}" for k in axis_keys)
        print(f"    {c:12s}{row}")

    prim = by_axis[PRIMARY_AXIS]
    print(f"\n  ══ Eje primario ({PRIMARY_AXIS}) con IC95 ══")
    for c, v in sorted(prim.items(), key=lambda kv: -kv[1]["median_z"]):
        lo, hi = v["ci95_median"]
        print(f"    {c:12s} {v['median_z']:+.3f}  IC95 [{lo:+.2f}, {hi:+.2f}]  n={v['n_chunks']}")
    if "china" in prim and "canada" in prim:
        ch, ca = prim["china"]["ci95_median"], prim["canada"]["ci95_median"]
        overlap = ch[0] <= ca[1] and ca[0] <= ch[1]
        print(f"\n    China vs Canadá: brecha "
              f"{prim['china']['median_z'] - prim['canada']['median_z']:+.3f} z; IC95 "
              f"{'SE SOLAPAN → empate estadístico' if overlap else 'NO se solapan → hay separación'}")

    # ── ¿En qué ejes SÍ discrimina la Vía A? (rango entre países) ──
    print(f"\n  ══ Poder de discriminación por eje (rango entre países) ══")
    spread = {}
    for k in axis_keys:
        vals = [by_axis[k][c]["median_z"] for c in by_axis[k]]
        spread[k] = max(vals) - min(vals)
    for k, v in sorted(spread.items(), key=lambda kv: -kv[1]):
        top = max(by_axis[k], key=lambda c: by_axis[k][c]["median_z"])
        bot = min(by_axis[k], key=lambda c: by_axis[k][c]["median_z"])
        print(f"    {k:10s} rango {v:.3f}   (alto: {top}, bajo: {bot})")

    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    WEB_DATA_DIR.mkdir(parents=True, exist_ok=True)

    # Compatibilidad: agreement.py consume este archivo con solo el eje primario.
    OUT_FILE.write_text(json.dumps(
        {"axis": PRIMARY_AXIS, "anchor_mode": ANCHOR_MODE, "collection": COLLECTION_V3,
         "background_n": len(vecs), "background_mu": background[PRIMARY_AXIS]["mu"],
         "background_sigma": background[PRIMARY_AXIS]["sigma"],
         "country_scores": prim}, ensure_ascii=False, indent=2), encoding="utf-8")

    payload = {"anchor_mode": ANCHOR_MODE, "axis_set": AXIS_SET, "axes": axis_keys,
               "collection": COLLECTION_V3, "background_n": len(vecs),
               "background": background, "discrimination_range": spread,
               "labels": {k: {kk: CONFUCIAN_AXES[k].get(kk) for kk in ("zh", "pinyin", "label")}
                          for k in axis_keys},
               "country_axes": {c: {k: by_axis[k][c] for k in axis_keys}
                                for c in COUNTRIES if c in prim}}
    AXES_FILE.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    RADAR_FILE.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n  Wrote {OUT_FILE}\n  Wrote {AXES_FILE}\n  Wrote {RADAR_FILE}")


if __name__ == "__main__":
    main()
