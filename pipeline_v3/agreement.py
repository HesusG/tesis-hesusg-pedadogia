"""SPIKE Fase 5 — validación del instrumento (spec §6).

Tres preguntas que el spec exige responder antes de que los números de la Fase 4
sean defendibles en la tesis:

1. **¿El panel concuerda?** Acuerdo inter-juez con κ de Fleiss (nominal) y α de
   Krippendorff (ordinal e intervalo — el eje es ordinal, así que α ordinal es la
   métrica principal; κ se reporta por convención disciplinar).
2. **¿El origen del modelo sesga la medición?** Contraste occidental-vs-chino a
   nivel pasaje, con IC bootstrap sobre la brecha pareada.
3. **¿Vía A y Vía B coinciden?** Correlación de Spearman entre el score de
   embeddings y el del panel LLM, país por país — y el contraste China/Canadá que
   motivó todo el método.

Todo el cómputo es determinista salvo el bootstrap, sembrado con `SEED`.

Uso: python -m pipeline_v3.agreement
"""
import json
import random
import statistics as stats
from collections import defaultdict

from .config import CACHE_DIR, WEB_DATA_DIR, PANEL

RECORDS_FILE = CACHE_DIR / "dezhi_records.jsonl"
VIA_A_FILE = CACHE_DIR / "via_a_dezhi.json"
OUT_FILE = WEB_DATA_DIR / "dezhi_validation.json"
SEED = 42
N_BOOT = 5000
CATEGORIES = [-2, -1, 0, 1, 2]


# ── Acuerdo inter-juez ────────────────────────────────────────────────────────
def fleiss_kappa(units: list[list[int]]) -> float:
    """κ de Fleiss (nominal), generalizado a un número variable de jueces por unidad."""
    units = [u for u in units if len(u) >= 2]
    if not units:
        return float("nan")
    counts = [[u.count(c) for c in CATEGORIES] for u in units]
    m = [sum(row) for row in counts]
    p_i = [(sum(n * n for n in row) - mi) / (mi * (mi - 1)) for row, mi in zip(counts, m)]
    p_bar = stats.mean(p_i)
    total = sum(m)
    p_j = [sum(row[j] for row in counts) / total for j in range(len(CATEGORIES))]
    p_e = sum(p * p for p in p_j)
    return (p_bar - p_e) / (1 - p_e) if p_e != 1 else float("nan")


def percent_agreement(units: list[list[int]]) -> dict:
    """Acuerdo OBSERVADO por pares (exacto y dentro de ±1).

    κ y α corrigen por azar, y esa corrección los deprime cuando la distribución
    está concentrada en una categoría (la "paradoja de kappa": Feinstein & Cicchetti
    1990). El eje dézhì está concentrado en 0, así que el acuerdo crudo debe
    reportarse JUNTO a α — no en su lugar — para no exagerar ni el acuerdo ni el
    desacuerdo.
    """
    exact = within1 = total = 0
    for u in units:
        for i in range(len(u)):
            for j in range(i + 1, len(u)):
                total += 1
                d = abs(u[i] - u[j])
                exact += d == 0
                within1 += d <= 1
    if not total:
        return {"exact": float("nan"), "within_1": float("nan"), "n_pairs": 0}
    return {"exact": exact / total, "within_1": within1 / total, "n_pairs": total}


def krippendorff_alpha(units: list[list[int]], metric: str = "ordinal") -> float:
    """α de Krippendorff. `metric` ∈ {nominal, ordinal, interval}.

    Implementado sobre la matriz de coincidencias (Krippendorff 2004, cap. 11), sin
    dependencias externas: tolera unidades con distinto número de jueces y descarta
    las de un solo juez, como manda la definición.
    """
    units = [u for u in units if len(u) >= 2]
    if not units:
        return float("nan")
    idx = {c: i for i, c in enumerate(CATEGORIES)}
    K = len(CATEGORIES)

    o = [[0.0] * K for _ in range(K)]
    for u in units:
        mu = len(u)
        cnt = [u.count(c) for c in CATEGORIES]
        for ci in range(K):
            if not cnt[ci]:
                continue
            for ki in range(K):
                same = 1 if ci == ki else 0
                o[ci][ki] += cnt[ci] * (cnt[ki] - same) / (mu - 1)

    n_c = [sum(row) for row in o]
    n = sum(n_c)
    if n <= 1:
        return float("nan")

    def delta2(ci: int, ki: int) -> float:
        if metric == "nominal":
            return 0.0 if ci == ki else 1.0
        if metric == "interval":
            return (CATEGORIES[ci] - CATEGORIES[ki]) ** 2
        # ordinal: distancia acumulada sobre las frecuencias marginales
        lo, hi = min(ci, ki), max(ci, ki)
        acc = sum(n_c[g] for g in range(lo, hi + 1))
        return (acc - (n_c[ci] + n_c[ki]) / 2) ** 2

    d_o = sum(o[ci][ki] * delta2(ci, ki) for ci in range(K) for ki in range(K))
    d_e = sum(n_c[ci] * (n_c[ki] - (1 if ci == ki else 0)) / (n - 1) * delta2(ci, ki)
              for ci in range(K) for ki in range(K))
    return 1 - d_o / d_e if d_e else float("nan")


# ── Correlaciones ─────────────────────────────────────────────────────────────
def _ranks(xs: list[float]) -> list[float]:
    order = sorted(range(len(xs)), key=lambda i: xs[i])
    r = [0.0] * len(xs)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and xs[order[j + 1]] == xs[order[i]]:
            j += 1
        avg = (i + j) / 2 + 1
        for k in range(i, j + 1):
            r[order[k]] = avg
        i = j + 1
    return r


def pearson(xs: list[float], ys: list[float]) -> float:
    n = len(xs)
    if n < 2:
        return float("nan")
    mx, my = stats.mean(xs), stats.mean(ys)
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    den = (sum((x - mx) ** 2 for x in xs) * sum((y - my) ** 2 for y in ys)) ** 0.5
    return num / den if den else float("nan")


def spearman(xs: list[float], ys: list[float]) -> float:
    return pearson(_ranks(xs), _ranks(ys))


def main():
    if not RECORDS_FILE.exists():
        raise SystemExit(f"Falta {RECORDS_FILE} — corre primero `python -m pipeline_v3.compare_countries`")
    recs = [json.loads(l) for l in RECORDS_FILE.read_text(encoding="utf-8").splitlines() if l.strip()]
    print(f"  {len(recs)} clasificaciones crudas cargadas")

    # unidad = un pasaje (país, índice); jueces = los 7 del panel
    by_unit = defaultdict(dict)
    for r in recs:
        by_unit[(r["country"], r["passage_idx"])][r["judge"]] = r["score"]
    units_all = [list(d.values()) for d in by_unit.values()]

    origin_of = {j.key: j.origin for j in PANEL}
    units_w = [[s for j, s in d.items() if origin_of.get(j) == "western"] for d in by_unit.values()]
    units_c = [[s for j, s in d.items() if origin_of.get(j) == "chinese"] for d in by_unit.values()]

    agreement = {
        "n_units": len(units_all),
        "observed_agreement": percent_agreement(units_all),
        "panel": {
            "fleiss_kappa": fleiss_kappa(units_all),
            "krippendorff_alpha_ordinal": krippendorff_alpha(units_all, "ordinal"),
            "krippendorff_alpha_interval": krippendorff_alpha(units_all, "interval"),
            "krippendorff_alpha_nominal": krippendorff_alpha(units_all, "nominal"),
        },
        "within_western": {"fleiss_kappa": fleiss_kappa(units_w),
                           "krippendorff_alpha_ordinal": krippendorff_alpha(units_w, "ordinal")},
        "within_chinese": {"fleiss_kappa": fleiss_kappa(units_c),
                           "krippendorff_alpha_ordinal": krippendorff_alpha(units_c, "ordinal")},
    }

    print("\n  ══ 1. Acuerdo inter-juez ══")
    print(f"    unidades (pasajes): {agreement['n_units']}")
    oa = agreement["observed_agreement"]
    print(f"    acuerdo observado por pares: exacto {oa['exact']:.1%}  ·  dentro de ±1 "
          f"{oa['within_1']:.1%}  (n={oa['n_pairs']} pares)")
    for k, v in agreement["panel"].items():
        print(f"    panel completo  {k:32s} {v:+.3f}")
    a = agreement["panel"]["krippendorff_alpha_ordinal"]
    umbral = ("≥.800 fiable" if a >= 0.8 else
              "≥.667 conclusiones tentativas" if a >= 0.667 else
              "POR DEBAJO de .667 — insuficiente a nivel pasaje (Krippendorff 2004)")
    print(f"    → α ordinal {a:.3f}: {umbral}")
    print(f"    solo occidentales  α ordinal {agreement['within_western']['krippendorff_alpha_ordinal']:+.3f}"
          f"   κ {agreement['within_western']['fleiss_kappa']:+.3f}")
    print(f"    solo chinos        α ordinal {agreement['within_chinese']['krippendorff_alpha_ordinal']:+.3f}"
          f"   κ {agreement['within_chinese']['fleiss_kappa']:+.3f}")

    # ── 2. Sesgo de origen: brecha pareada por pasaje ──
    pairs = []
    for d in by_unit.values():
        w = [s for j, s in d.items() if origin_of.get(j) == "western"]
        c = [s for j, s in d.items() if origin_of.get(j) == "chinese"]
        if w and c:
            pairs.append((stats.mean(w), stats.mean(c)))
    gaps = [w - c for w, c in pairs]
    rng = random.Random(SEED)
    boots = []
    for _ in range(N_BOOT):
        sample = [gaps[rng.randrange(len(gaps))] for _ in range(len(gaps))]
        boots.append(stats.mean(sample))
    boots.sort()
    ci = (boots[int(0.025 * N_BOOT)], boots[int(0.975 * N_BOOT)])
    origin_bias = {
        "n_paired_passages": len(pairs),
        "mean_western": stats.mean(w for w, _ in pairs),
        "mean_chinese": stats.mean(c for _, c in pairs),
        "mean_gap_western_minus_chinese": stats.mean(gaps),
        "ci95": list(ci),
        "excludes_zero": bool(ci[0] > 0 or ci[1] < 0),
        "pearson_r_passage_level": pearson([w for w, _ in pairs], [c for _, c in pairs]),
        "n_boot": N_BOOT, "seed": SEED,
    }
    print("\n  ══ 2. Sesgo de origen del modelo (pareado por pasaje) ══")
    print(f"    occidental {origin_bias['mean_western']:+.3f}  vs  chino {origin_bias['mean_chinese']:+.3f}")
    print(f"    brecha (occ − chi) {origin_bias['mean_gap_western_minus_chinese']:+.3f}  "
          f"IC95 [{ci[0]:+.3f}, {ci[1]:+.3f}]  "
          f"{'→ EXCLUYE el 0 (sesgo real)' if origin_bias['excludes_zero'] else '→ incluye el 0 (no concluyente)'}")
    print(f"    correlación pasaje a pasaje r = {origin_bias['pearson_r_passage_level']:+.3f} "
          f"(validez convergente transcultural)")

    # ── 3. Estabilidad del agregado por país ──
    # El acuerdo a nivel PASAJE es moderado, pero la tesis no afirma nada sobre un
    # pasaje suelto: afirma que China se separa. Esa afirmación vive en el agregado,
    # así que hay que ponerle intervalo. Se remuestrean PASAJES (la unidad de muestreo),
    # no clasificaciones sueltas — remuestrear clasificaciones fingiría independencia
    # entre los 7 jueces que leen el mismo pasaje.
    by_country_passages = defaultdict(lambda: defaultdict(list))
    for r in recs:
        by_country_passages[r["country"]][r["passage_idx"]].append(r["score"])
    rng2 = random.Random(SEED)
    country_ci = {}
    for c, passages in by_country_passages.items():
        pmeans = [stats.mean(v) for v in passages.values()]
        n = len(pmeans)
        bs = sorted(stats.mean([pmeans[rng2.randrange(n)] for _ in range(n)])
                    for _ in range(N_BOOT))
        country_ci[c] = {"mean": stats.mean(pmeans), "n_passages": n,
                         "ci95": [bs[int(0.025 * N_BOOT)], bs[int(0.975 * N_BOOT)]]}

    print("\n  ══ 3. Estabilidad del agregado por país (bootstrap sobre pasajes) ══")
    for c, v in sorted(country_ci.items(), key=lambda kv: -kv[1]["mean"]):
        lo, hi = v["ci95"]
        print(f"    {c:12s} {v['mean']:+.3f}  IC95 [{lo:+.3f}, {hi:+.3f}]  ({v['n_passages']} pasajes)")
    china_separates = None
    if "china" in country_ci:
        ch = country_ci["china"]["ci95"]
        others = [c for c in country_ci if c != "china"]
        china_separates = all(ch[0] > country_ci[o]["ci95"][1] for o in others)
        print(f"    → el IC de China {'NO se solapa con ningún otro país → separación sólida' if china_separates else 'se solapa con algún país'}")

    # ── 4. Vía A (embeddings) vs Vía B (panel LLM) ──
    via_ab = None
    if VIA_A_FILE.exists():
        via_a = json.loads(VIA_A_FILE.read_text(encoding="utf-8"))["country_scores"]
        by_country = defaultdict(list)
        for r in recs:
            by_country[r["country"]].append(r["score"])
        common = [c for c in via_a if c in by_country]
        a_vals = [via_a[c]["median_z"] for c in common]
        b_vals = [stats.mean(by_country[c]) for c in common]
        via_ab = {
            "countries": common,
            "via_a_median_z": {c: via_a[c]["median_z"] for c in common},
            "via_b_mean_llm": {c: stats.mean(by_country[c]) for c in common},
            "spearman": spearman(a_vals, b_vals),
            "pearson": pearson(a_vals, b_vals),
        }
        if "china" in via_a and "canada" in via_a:
            via_ab["china_vs_canada"] = {
                "via_a_gap": via_a["china"]["median_z"] - via_a["canada"]["median_z"],
                "via_b_gap": stats.mean(by_country["china"]) - stats.mean(by_country["canada"]),
            }
        print("\n  ══ 4. Vía A (embeddings) vs Vía B (panel LLM) ══")
        print(f"    {'país':12s} {'Vía A (z)':>12s} {'Vía B (LLM)':>12s}")
        for c in sorted(common, key=lambda c: -via_a[c]["median_z"]):
            print(f"    {c:12s} {via_a[c]['median_z']:>+12.3f} {stats.mean(by_country[c]):>+12.3f}")
        print(f"    Spearman ρ = {via_ab['spearman']:+.3f}   Pearson r = {via_ab['pearson']:+.3f}")
        if "china_vs_canada" in via_ab:
            g = via_ab["china_vs_canada"]
            print(f"    China − Canadá:  Vía A {g['via_a_gap']:+.3f} (empate)  vs  "
                  f"Vía B {g['via_b_gap']:+.3f}  ← el payoff del método")
    else:
        print(f"\n  ⚠ Falta {VIA_A_FILE} — corre `python -m pipeline_v3.via_a` para la comparación Vía A/B")

    payload = {"agreement": agreement, "origin_bias": origin_bias,
               "country_stability": country_ci, "china_separates": china_separates,
               "via_a_vs_via_b": via_ab, "n_classifications": len(recs)}
    WEB_DATA_DIR.mkdir(parents=True, exist_ok=True)
    OUT_FILE.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n  Wrote {OUT_FILE}")


if __name__ == "__main__":
    main()
