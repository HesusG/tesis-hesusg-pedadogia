"""Verificación de las métricas de acuerdo contra implementaciones de referencia.

`agreement.py` implementa κ de Fleiss y α de Krippendorff sin dependencias externas
(el pipeline debe correr sin scipy/statsmodels). Este test cruza esas implementaciones
contra `krippendorff` y `statsmodels` para que la métrica que sostiene el capítulo de
validación no dependa de mi aritmética.

Uso: python -m pipeline_v3.test_agreement    (requiere: pip install krippendorff statsmodels)
"""
import numpy as np

from .agreement import krippendorff_alpha, fleiss_kappa

TOL = 1e-6

# Ejemplo canónico de Krippendorff: 3 observadores, 12 unidades, con faltantes.
CANONICAL = np.array([
    [1, 2, 3, 3, 2, 1, 4, 1, 2, np.nan, np.nan, np.nan],
    [1, 2, 3, 3, 2, 2, 4, 1, 2, 5, np.nan, 3],
    [np.nan, 3, 3, 3, 2, 3, 4, 2, 2, 5, 1, np.nan],
])


def _to_units(mat: np.ndarray, shift: int = 3) -> list[list[int]]:
    """Matriz jueces×unidades → lista de unidades; mapea 1..5 a -2..+2 (monótono)."""
    return [[int(v) - shift for v in mat[:, u] if not np.isnan(v)] for u in range(mat.shape[1])]


def main():
    import krippendorff as kd
    from statsmodels.stats.inter_rater import fleiss_kappa as sm_fleiss, aggregate_raters

    failures = []

    def check(name, got, ref):
        ok = abs(got - ref) < TOL
        print(f"  {name:46s} {got:+.6f}  ref {ref:+.6f}  {'OK' if ok else 'MISMATCH'}")
        if not ok:
            failures.append(name)

    print("Caso 1 — ejemplo canónico (nº de jueces variable, con faltantes):")
    units = _to_units(CANONICAL)
    for m in ("nominal", "ordinal", "interval"):
        check(f"alpha {m}", krippendorff_alpha(units, m),
              kd.alpha(reliability_data=CANONICAL, level_of_measurement=m))

    print("Caso 2 — 7 jueces × 40 unidades, sin faltantes (la forma real del panel):")
    data = np.random.default_rng(7).integers(-2, 3, size=(7, 40))
    units2 = [list(data[:, u]) for u in range(data.shape[1])]
    for m in ("nominal", "ordinal", "interval"):
        check(f"alpha {m}", krippendorff_alpha(units2, m),
              kd.alpha(reliability_data=data.astype(float), level_of_measurement=m))
    table, _ = aggregate_raters(data.T)
    check("fleiss kappa", fleiss_kappa(units2), sm_fleiss(table))

    print(f"\n{'✓ todas las métricas coinciden con la referencia' if not failures else '✗ FALLAS: ' + ', '.join(failures)}")
    raise SystemExit(1 if failures else 0)


if __name__ == "__main__":
    main()
