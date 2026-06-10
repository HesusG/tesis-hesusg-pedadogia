"""Consolidate rubric scores and compute inter-coder agreement.

Merges policies/eval/scores_draft/<pid>.json (primary coder) into
policies/eval/scores.json, computes per-document and per-block totals, and
reports inter-coder agreement against *.RELIABILITY.json files (exact agreement
% and within-one-point %; weighted kappa if scipy available).

Run: python3 -m pipeline.eval_merge
Output: policies/eval/scores.json (consolidated) + web/data/eval_matrix.json
"""
import json
from collections import defaultdict
from pathlib import Path

from .config import POLICIES_DIR, WEB_DATA_DIR

EVAL_DIR = POLICIES_DIR / "eval"
DRAFT_DIR = EVAL_DIR / "sheets" / ".." / "scores_draft"
DRAFT_DIR = (EVAL_DIR / "scores_draft").resolve()
RUBRIC_FILE = EVAL_DIR / "rubrica.json"
SCORES_FILE = EVAL_DIR / "scores.json"


def load_rubric():
    with open(RUBRIC_FILE, encoding="utf-8") as f:
        return json.load(f)


def merge_scores(rubric) -> dict:
    """Merge primary-coder draft files into one scores dict."""
    crit_ids = [c["id"] for c in rubric]
    merged = {}
    for path in sorted(DRAFT_DIR.glob("*.json")):
        if ".RELIABILITY" in path.name:
            continue
        pid = path.stem
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        missing = [c for c in crit_ids if c not in data]
        if missing:
            print(f"  ⚠ {pid}: faltan criterios {missing}")
        merged[pid] = data
    return merged


def agreement_report(merged) -> dict:
    """Exact and within-1 agreement vs RELIABILITY files."""
    report = {}
    for path in sorted(DRAFT_DIR.glob("*.RELIABILITY.json")):
        pid = path.name.replace(".RELIABILITY.json", "")
        if pid not in merged:
            continue
        with open(path, encoding="utf-8") as f:
            second = json.load(f)
        pairs = [
            (merged[pid][cid]["score"], second[cid]["score"])
            for cid in second
            if cid in merged[pid]
            and merged[pid][cid]["score"] is not None
            and second[cid]["score"] is not None
        ]
        n = len(pairs)
        exact = sum(1 for a, b in pairs if a == b)
        within1 = sum(1 for a, b in pairs if abs(a - b) <= 1)
        entry = {
            "n": n,
            "exact_pct": round(100 * exact / n, 1),
            "within1_pct": round(100 * within1 / n, 1),
            "disagreements": [
                {"criterio": cid, "primario": merged[pid][cid]["score"], "fiabilidad": second[cid]["score"]}
                for cid in second
                if cid in merged[pid] and merged[pid][cid]["score"] != second[cid]["score"]
            ],
        }
        try:
            import numpy as np

            a = np.array([p[0] for p in pairs])
            b = np.array([p[1] for p in pairs])
            # quadratic weighted kappa
            categories = [0, 1, 2, 3]
            O = np.zeros((4, 4))
            for x, y in zip(a, b):
                O[x][y] += 1
            W = np.array([[(i - j) ** 2 / 9 for j in categories] for i in categories])
            E = np.outer(O.sum(1), O.sum(0)) / O.sum()
            kappa = 1 - (W * O).sum() / (W * E).sum()
            entry["weighted_kappa"] = round(float(kappa), 3)
        except Exception:
            pass
        report[pid] = entry
    return report


def totals(merged, rubric) -> dict:
    """Per-document totals and per-block subtotals."""
    block_of = {c["id"]: c["bloque"] for c in rubric}
    out = {}
    for pid, data in merged.items():
        total = sum(v["score"] for v in data.values() if v["score"] is not None)
        blocks = defaultdict(lambda: [0, 0])
        instruments = defaultdict(int)
        for cid, v in data.items():
            if v["score"] is None:
                continue
            b = blocks[block_of.get(cid, "?")]
            b[0] += v["score"]
            b[1] += 3
            if v.get("instrumento"):
                instruments[v["instrumento"]] += 1
        out[pid] = {
            "total": total,
            "max": 3 * len(data),
            "pct": round(100 * total / (3 * len(data)), 1),
            "bloques": {k: {"puntos": v[0], "max": v[1], "pct": round(100 * v[0] / v[1], 1)}
                        for k, v in sorted(blocks.items())},
            "instrumentos": dict(instruments),
        }
    return out


def main():
    rubric = load_rubric()
    merged = merge_scores(rubric)
    if not merged:
        raise SystemExit("No hay borradores de puntuación en scores_draft/")

    SCORES_FILE.write_text(json.dumps(merged, indent=2, ensure_ascii=False), encoding="utf-8")
    summary = totals(merged, rubric)
    agreement = agreement_report(merged)

    WEB_DATA_DIR.mkdir(parents=True, exist_ok=True)
    out = WEB_DATA_DIR / "eval_matrix.json"
    out.write_text(json.dumps(
        {"totales": summary, "fiabilidad": agreement, "criterios": [c["id"] for c in rubric]},
        indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"✓ {len(merged)} documentos consolidados → {SCORES_FILE}")
    print(f"✓ Matriz de evaluación → {out}\n")
    print(f"{'documento':<36} {'total':>7} {'%':>6}")
    for pid, s in sorted(summary.items(), key=lambda kv: -kv[1]["total"]):
        print(f"{pid:<36} {s['total']:>3}/{s['max']:<3} {s['pct']:>5}%")
    print()
    for pid, rep in agreement.items():
        kappa = rep.get("weighted_kappa", "n/a")
        print(f"FIABILIDAD {pid}: exacto {rep['exact_pct']}% | ±1 {rep['within1_pct']}% | kappa_pond {kappa} | desacuerdos {len(rep['disagreements'])}")


if __name__ == "__main__":
    main()
