"""
Phase 7.1.4 — Re-compute attractors on v2 BNET (IFN-I cascade fix).

Same pipeline as src/analysis/compute_attractors.py but on the v2 model
(HDAC3=1, KPNB1=1 by construction). Outputs a v2 catalog and a v2 ISG
audit table to verify that ISGF3 / ISGs become activatable under IFN-stim.

Outputs:
  results/phase7/attractor_catalog_v2.csv
  results/phase7/isg_audit_v2.csv
  results/phase7/attractor_report_v2.md

Usage:
    python3 src/analysis/compute_attractors_v2.py
"""

from __future__ import annotations

import csv
import pathlib

import mpbn

BNET    = pathlib.Path("models/sbmlqual/v2/sjd_map_v2.bnet")
OUT_DIR = pathlib.Path("results/phase7")

PHENOTYPES = [
    "Angiogenesis_phenotype",
    "Apoptosis_phenotype",
    "B_Cell_Activation_Survival_phenotype",
    "Cell_Proliferation_Survival_phenotype",
    "Chemotaxis_Infiltration_phenotype",
    "Fibrosis_phenotype",
    "Inflammation_phenotype",
    "Lymphoid_organ_development_phenotype",
    "MHC_Class_1_Activation_phenotype",
    "MHC_Class_2_Activation_phenotype",
    "Matrix_degradation_phenotype",
    "Phagocytosis_phenotype",
    "Regulated_Necrosis_phenotype",
    "T_Cell_Activation_Differentiation_phenotype",
]

CONDITIONS: dict[str, dict[str, int]] = {
    "Naive (homeostatic)": {},
    "IFN-stimulated": {
        "IFNA_Extracellular_ligands":  1,
        "IFNB1_Extracellular_ligands": 1,
        "IFNG_IFNGR_complex":          1,
        "IFNAR_complex":               1,
    },
    "BCR-stimulated": {"BCR_complex": 1},
}

ISG_NODES = [
    "MX1", "MX2", "OAS1", "OAS2", "OAS3", "OASL",
    "ISG15_Cell", "ISG20",
    "IFIT1_rna", "IFIT2_rna", "IFIT3_rna", "IFIT5_rna",
    "IFITM1_rna", "IFITM2_rna", "IFITM3_rna",
    "IRF7_Cell", "IRF9",
    "STAT1", "STAT1_phosphorylated", "STAT1_homodimer_phosphorylated",
    "STAT1_STAT2_IRF9_complex_Cell", "STAT1_STAT2_IRF9_complex_nucleus",
]


def compute(bnet_path: pathlib.Path = BNET) -> tuple[list[dict], list[dict]]:
    bn_base = mpbn.MPBooleanNetwork(str(bnet_path))
    inputs  = [n for n, r in bn_base.items() if str(r) == n]
    print(f"Inputs (self-loops): {len(inputs)}")

    rows: list[dict] = []
    isg_rows: list[dict] = []

    for cond_name, overrides in CONDITIONS.items():
        bn = mpbn.MPBooleanNetwork(str(bnet_path))
        # Fix every input node: those listed in overrides keep the override
        # value, the rest go to 0. Without this the 102 self-loops of v2 leave
        # a 2^102 search space that mpbn cannot enumerate fixed points over.
        for n in inputs:
            bn[n] = overrides.get(n, 0)
        bn.propagate_constants()
        non_triv = sum(1 for n, r in bn.items() if str(r) not in ("0", "1"))

        fps = list(bn.fixedpoints())
        attrs = list(bn.attractors())
        print(f"  {cond_name}: {non_triv} dynamic nodes, "
              f"{len(fps)} fixed points, {len(attrs)} trap spaces")

        # Treat fixed points as a special case of trap space ('0'/'1' only).
        # Trap spaces with at least one '*' are cyclic attractors under MP
        # semantics — we still report them but mark them as such.
        for i, attr in enumerate(attrs, 1):
            kind = "fixed_point" if all(
                str(attr.get(k, 0)) in ("0", "1") for k in attr
            ) else "trap_space"

            def _v(n: str) -> int:
                """Coerce trap-space coord to 0/1 for phenotype counting:
                '*' (oscillating) is treated as 1 because the phenotype is
                reachable (= activable in some trajectory)."""
                v = str(attr.get(n, 0))
                return 1 if v in ("1", "*") else 0

            active = [p.replace("_phenotype", "").replace("_", " ")
                      for p in PHENOTYPES if _v(p) == 1]
            row: dict = {
                "condition":         cond_name,
                "attractor":         f"A{i}",
                "kind":              kind,
                "n_dynamic":         non_triv,
                "active_phenotypes": "|".join(active),
                "n_active":          len(active),
            }
            for p in PHENOTYPES:
                row[p] = _v(p)
            rows.append(row)

            isg_row: dict = {"condition": cond_name, "attractor": f"A{i}",
                             "kind": kind}
            for n in ISG_NODES:
                isg_row[n] = str(attr.get(n, 0))
            # Count ISGs that are activable (= 1 or '*') and exclude the STAT1
            # protein/complex nodes from the ISG tally to keep the metric on
            # downstream effectors only.
            isg_row["n_active_isgs"] = sum(
                1 for n in ISG_NODES
                if str(attr.get(n, 0)) in ("1", "*") and "STAT" not in n
            )
            isg_rows.append(isg_row)

    return rows, isg_rows


def render_report(rows: list[dict], isg_rows: list[dict]) -> str:
    lines = [
        "# Rapport attracteurs v2 — Phase 7.1.4",
        "",
        "**Modèle :** `models/sbmlqual/v2/sjd_map_v2.bnet` (HDAC3=1, KPNB1=1)",
        "",
        "Sous semantique MP, les trap-spaces minimaux sont les attracteurs ;",
        "une coordonnée à `*` indique un nœud oscillant dans l'attracteur.",
        "Pour le décompte des phénotypes et des ISGs, `*` est traité comme",
        "*activable* (= 1 dans au moins une trajectoire de l'attracteur).",
        "",
        "## Phénotypes actifs / activables par attracteur",
        "",
        "| Condition | Attracteur | Type | n_dyn | n_actifs | Phénotypes actifs |",
        "|---|---|---|---|---|---|",
    ]
    for r in rows:
        lines.append(
            f"| {r['condition']} | {r['attractor']} | {r['kind']} "
            f"| {r['n_dynamic']} | {r['n_active']} | {r['active_phenotypes']} |"
        )

    lines += [
        "",
        "## Audit ISG (validation correction IFN-I)",
        "",
        "| Condition | Attracteur | n_ISGs activables | STAT1 | STAT1_p | "
        "ISGF3_nucleus | MX1 | OAS1 | ISG15 | IRF7_Cell |",
        "|---|---|---|---|---|---|---|---|---|---|",
    ]
    for r in isg_rows:
        lines.append(
            f"| {r['condition']} | {r['attractor']} | {r['n_active_isgs']} "
            f"| {r.get('STAT1','?')} | {r.get('STAT1_phosphorylated','?')} "
            f"| {r.get('STAT1_STAT2_IRF9_complex_nucleus','?')} "
            f"| {r.get('MX1','?')} | {r.get('OAS1','?')} | "
            f"{r.get('ISG15_Cell','?')} | {r.get('IRF7_Cell','?')} |"
        )

    ifn_max = max(
        (r["n_active_isgs"] for r in isg_rows if r["condition"] == "IFN-stimulated"),
        default=0,
    )
    lines += [
        "",
        f"### Critère 7.1.1 : ≥ 3 ISGs canoniques activables sous IFN-stim → "
        f"**{'✅ ATTEINT' if ifn_max >= 3 else '❌ NON ATTEINT'}** "
        f"(max observé : {ifn_max} ISGs)",
        "",
        "*Le critère utilise les coordonnées de trap-space MP : `1` ou `*` = activable.*",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    rows, isg_rows = compute()

    cat_path = OUT_DIR / "attractor_catalog_v2.csv"
    fieldnames = ["condition", "attractor", "kind", "n_dynamic",
                  "active_phenotypes", "n_active"] + PHENOTYPES
    with open(cat_path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)
    print(f"Saved: {cat_path}")

    isg_path = OUT_DIR / "isg_audit_v2.csv"
    isg_fields = ["condition", "attractor", "kind", "n_active_isgs"] + ISG_NODES
    with open(isg_path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=isg_fields)
        w.writeheader()
        w.writerows(isg_rows)
    print(f"Saved: {isg_path}")

    report = render_report(rows, isg_rows)
    rep_path = OUT_DIR / "attractor_report_v2.md"
    rep_path.write_text(report)
    print(f"Saved: {rep_path}")


if __name__ == "__main__":
    main()
