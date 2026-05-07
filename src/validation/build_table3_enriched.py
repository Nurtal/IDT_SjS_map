"""
Phase 9.1.2 — Build the enriched TP/TN/FP/FN decomposition table.

Combines the per-attractor TP/TN/FP/FN from Phase 7.2.3 with the trivial
all-1 / all-0 baselines from Phase 8.1.5, adding the n_down column (from
the baselines file) so each cohort row makes the class imbalance visible.

Output:
    results/phase9/table3_extended.csv
"""

from __future__ import annotations

import csv
import pathlib

SENS = pathlib.Path("results/phase7/sensitivity_specificity_auroc.csv")
BASELINES = pathlib.Path("results/phase8/baselines_trivial.csv")
OUT_CSV = pathlib.Path("results/phase9/table3_extended.csv")


def main() -> None:
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)

    # Load per-attractor decomposition (IFN-stim A1 only for the headline table)
    sens_rows: list[dict] = []
    with open(SENS) as f:
        for r in csv.DictReader(f):
            sens_rows.append(r)

    # Load class composition from baselines
    composition: dict[str, dict] = {}
    baseline_rows: list[dict] = []
    with open(BASELINES) as f:
        for r in csv.DictReader(f):
            baseline_rows.append(r)
            if r["baseline"] == "all-1":
                composition[r["cohort"]] = {
                    "n_pairs": int(r["n_pairs"]),
                    "n_up":    int(r["n_up"]),
                    "n_down":  int(r["n_down"]),
                }

    # Build output: for each cohort, one IFN-stim A1 row + 2 baseline rows.
    out_rows: list[dict] = []
    for cohort, comp in composition.items():
        # IFN-stim A1
        ifn = next((r for r in sens_rows
                    if r["cohort"] == cohort
                    and r["condition"] == "IFN-stimulated"
                    and r["attractor"] == "A1"), None)
        if ifn:
            out_rows.append({
                "cohort":   cohort,
                "method":   "IFN-stim A1",
                "n_pairs":  comp["n_pairs"],
                "n_up":     comp["n_up"],
                "n_down":   comp["n_down"],
                "tp":       ifn["tp"],
                "tn":       ifn["tn"],
                "fp":       ifn["fp"],
                "fn":       ifn["fn"],
                "sensitivity":  ifn["sensitivity"],
                "specificity":  ifn["specificity"],
                "ppv":          ifn["ppv"],
                "npv":          ifn["npv"],
                "balanced_acc": ifn["balanced_acc"],
                "auroc":        ifn["auroc"],
            })
        for label in ("all-1", "all-0"):
            br = next((b for b in baseline_rows
                       if b["cohort"] == cohort and b["baseline"] == label),
                      None)
            if br:
                out_rows.append({
                    "cohort":   cohort,
                    "method":   label,
                    "n_pairs":  comp["n_pairs"],
                    "n_up":     comp["n_up"],
                    "n_down":   comp["n_down"],
                    "tp":       br["tp"],
                    "tn":       br["tn"],
                    "fp":       br["fp"],
                    "fn":       br["fn"],
                    "sensitivity":  br["sensitivity"],
                    "specificity":  br["specificity"],
                    "ppv":          br["ppv"],
                    "npv":          br["npv"],
                    "balanced_acc": br["balanced_acc"],
                    "auroc":        "—",
                })

    fieldnames = list(out_rows[0].keys())
    with open(OUT_CSV, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(out_rows)
    print(f"Saved: {OUT_CSV}  ({len(out_rows)} rows)")


if __name__ == "__main__":
    main()
