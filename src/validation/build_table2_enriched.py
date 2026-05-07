"""
Phase 9.1.1 — Build the enriched cohort × attractor table:

  - existing columns (cohort, condition, attractor, n_pairs, hamming, null_mean,
    null_std, z_score, p_value)
  - hamming_lo / hamming_hi (95 % bootstrap CI for every cohort × attractor)
  - n_up / n_down / up_down_ratio per cohort
  - coverage_% (n_pairs / n_DEGs_total per cohort)
  - p_BH (Benjamini-Hochberg adjusted p-value across the 25 tests)

Output:
    results/phase9/table2_extended.csv
"""

from __future__ import annotations

import csv
import pathlib
from collections import defaultdict

DIST_V3 = pathlib.Path("results/phase8/attractor_cohort_distance_v3.csv")
BASELINES = pathlib.Path("results/phase8/baselines_trivial.csv")
OVERLAY_DIR = pathlib.Path(
    "data/raw/zenodo_17585308/TheSjDMap/TheSjDMap/Statistics_Overlays"
)
OVERLAYS = {
    "PRECISESADS": OVERLAY_DIR / "Blood_datasets/overlay_PRECISESADS.txt",
    "UKPSSR":      OVERLAY_DIR / "Blood_datasets/overlay_UKPSSR.txt",
    "GSE51092":    OVERLAY_DIR / "Blood_datasets/overlay_GSE51092.txt",
    "ASSESS":      OVERLAY_DIR / "ASSESS/ASSESS_lymphoma.txt",
    "GSE23117":    OVERLAY_DIR / "GSE23117/overlay_GSE23117.txt",
}
OUT_CSV = pathlib.Path("results/phase9/table2_extended.csv")


def count_overlay_degs(path: pathlib.Path) -> int:
    """Count rows with a +/- direction (red/blue colour)."""
    n = 0
    with open(path) as f:
        next(f, None)
        for line in f:
            parts = line.strip().split("\t")
            if len(parts) < 2 or not parts[0] or parts[0] == "NA":
                continue
            color = parts[1].upper()
            if "FF0000" in color or "0000FF" in color:
                n += 1
    return n


def benjamini_hochberg(p_values: list[float]) -> list[float]:
    """Standard BH FDR on a list of p-values; preserves input order."""
    n = len(p_values)
    indexed = sorted(enumerate(p_values), key=lambda kv: kv[1])
    adj = [0.0] * n
    prev = 1.0
    for rank, (orig_idx, p) in enumerate(reversed(indexed), 1):
        # Rank from largest to smallest
        k = n - rank + 1
        adj_p = min(prev, p * n / k)
        prev = adj_p
        adj[orig_idx] = adj_p
    return adj


def main() -> None:
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)

    # Load distances + bootstrap CI
    rows: list[dict] = []
    with open(DIST_V3) as f:
        for r in csv.DictReader(f):
            rows.append(r)

    # Compute coverage_% per cohort
    coverage: dict[str, tuple[int, float]] = {}
    for cohort, path in OVERLAYS.items():
        n_total = count_overlay_degs(path)
        # n_pairs is the same for every attractor of a cohort; pull from first row
        n_pairs = next((int(r["n_pairs"]) for r in rows
                        if r["cohort"] == cohort), 0)
        cov = 100.0 * n_pairs / max(1, n_total)
        coverage[cohort] = (n_total, cov)

    # Load up/down ratios from baselines
    ratios: dict[str, tuple[int, int, float]] = {}
    with open(BASELINES) as f:
        for r in csv.DictReader(f):
            if r["baseline"] == "all-1":
                ratios[r["cohort"]] = (
                    int(r["n_up"]), int(r["n_down"]),
                    float(r["up_down_ratio"]),
                )

    # BH correction over the 25 tests (or however many)
    p_raw = [float(r["p_value"]) if r["p_value"] not in ("", "nan") else 1.0
             for r in rows]
    p_bh = benjamini_hochberg(p_raw)

    # Build output rows
    out_rows: list[dict] = []
    for r, p_adj in zip(rows, p_bh):
        cohort = r["cohort"]
        n_up, n_down, ud = ratios.get(cohort, (0, 0, 0.0))
        n_total, cov = coverage.get(cohort, (0, 0.0))
        out_rows.append({
            "cohort":      cohort,
            "condition":   r["condition"],
            "attractor":   r["attractor"],
            "n_pairs":     r["n_pairs"],
            "n_total_DEGs": n_total,
            "coverage_pct": round(cov, 1),
            "n_up":        n_up,
            "n_down":      n_down,
            "up_down_ratio": ud,
            "hamming":     r["hamming"],
            "hamming_lo":  r["hamming_lo"],
            "hamming_hi":  r["hamming_hi"],
            "null_mean":   r["null_mean"],
            "null_std":    r["null_std"],
            "z_score":     r["z_score"],
            "p_value":     r["p_value"],
            "p_BH":        round(p_adj, 4),
        })

    fieldnames = list(out_rows[0].keys())
    with open(OUT_CSV, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(out_rows)
    print(f"Saved: {OUT_CSV}  ({len(out_rows)} rows)")

    # Print headline rows (IFN-stim per cohort) for the manuscript
    print("\nHeadline IFN-stim rows:")
    for r in out_rows:
        if r["condition"] == "IFN-stimulated" and r["attractor"] == "A1":
            print(f"  {r['cohort']:12s} n={r['n_pairs']:>3} cov={r['coverage_pct']:.1f}% "
                  f"up:down={r['up_down_ratio']} H={r['hamming']} "
                  f"[{r['hamming_lo']},{r['hamming_hi']}]  p={r['p_value']} "
                  f"p_BH={r['p_BH']}")


if __name__ == "__main__":
    main()
