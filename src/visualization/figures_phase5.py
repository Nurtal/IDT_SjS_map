"""Phase 5 figures — drug simulation results and validation."""
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

DRUG_SIM  = "results/phase5/drug_simulation.csv"
ASSESS    = "results/phase5/assess_validation.csv"
GSE       = "results/phase5/gse23117_validation.csv"
OUT       = "figures/phase5"

CONDITIONS = ["Naive", "IFN-stimulated", "BCR-stimulated"]
CMAP = {"Naive": "#4C72B0", "IFN-stimulated": "#DD8452", "BCR-stimulated": "#55A868"}

# ── Figure 5A : drug simulation heatmap ──────────────────────────────────────
def fig5a_drug_heatmap():
    df = pd.read_csv(DRUG_SIM)
    drugs = df["drug"].unique()
    cond_order = CONDITIONS

    # Build matrix: min phenotypes per (drug, condition) after perturbation
    mat_pheno = pd.pivot_table(df, values="pert_min_pheno",
                               index="drug", columns="condition", aggfunc="min")
    mat_elim  = pd.pivot_table(df, values="disease_eliminated",
                               index="drug", columns="condition", aggfunc="max")
    mat_elim  = mat_elim.astype(bool)

    # Order drugs by mechanism
    phase_order = df.drop_duplicates("drug").set_index("drug")["best_phase"]
    drug_order = df.drop_duplicates("drug").sort_values(
        ["best_phase", "drug"], ascending=[False, True])["drug"].tolist()

    mat_pheno = mat_pheno.reindex(drug_order)[cond_order]
    mat_elim  = mat_elim.reindex(drug_order)[cond_order]

    fig, ax = plt.subplots(figsize=(8, 6))
    cmap = plt.cm.RdYlGn_r
    im = ax.imshow(mat_pheno.values.astype(float), cmap=cmap, vmin=0, vmax=7,
                   aspect="auto")

    ax.set_xticks(range(len(cond_order)))
    ax.set_xticklabels(cond_order, rotation=15, ha="right", fontsize=9)
    ax.set_yticks(range(len(drug_order)))
    ax.set_yticklabels(drug_order, fontsize=8)

    # Mark eliminated cells with star
    for i, drug in enumerate(drug_order):
        for j, cond in enumerate(cond_order):
            if mat_elim.loc[drug, cond]:
                ax.text(j, i, "★", ha="center", va="center",
                        fontsize=12, color="gold", fontweight="bold")
            val = mat_pheno.loc[drug, cond]
            ax.text(j, i, f"{int(val) if not pd.isna(val) else '?'}",
                    ha="center", va="center", fontsize=7,
                    color="white" if val >= 5 else "black",
                    alpha=0.0 if mat_elim.loc[drug, cond] else 1.0)

    plt.colorbar(im, ax=ax, label="Min active phenotypes post-treatment")
    ax.set_title("Figure 5A — Drug simulation: phenotype count per condition\n★ = SjD attractor eliminated",
                 fontsize=10)
    plt.tight_layout()
    plt.savefig(f"{OUT}/fig5a_drug_heatmap.png", dpi=150, bbox_inches="tight")
    plt.close()
    print("  Saved fig5a_drug_heatmap.png")


# ── Figure 5B : concordance clinical vs. model ───────────────────────────────
def fig5b_concordance():
    concordance = [
        ("Filgotinib (JAK1)",    "✓ Concordant",  "#2ca02c"),
        ("Baricitinib (JAK1/2)", "✓ Concordant",  "#2ca02c"),
        ("Tofacitinib (JAK)",    "✓ Concordant",  "#2ca02c"),
        ("Tirabrutinib (BTK)",   "○ À confirmer", "#aec7e8"),
        ("Iscalimab (CD40)",     "○ Non modélisé","#aec7e8"),
        ("Ianalumab (BAFF)",     "○ Non modélisé","#aec7e8"),
        ("Hydroxychloroquine",   "⚠ Discordant",  "#d62728"),
        ("p38-inhibitor",        "✓ Prédiction",  "#9467bd"),
        ("AP1-inhibitor",        "✓ Prédiction",  "#9467bd"),
        ("PKR-inhibitor",        "✓ Prédiction",  "#9467bd"),
    ]
    drugs = [c[0] for c in concordance]
    colors = [c[2] for c in concordance]
    labels = [c[1] for c in concordance]

    fig, ax = plt.subplots(figsize=(9, 4))
    y = range(len(drugs))
    bars = ax.barh(list(y), [1]*len(drugs), color=colors, edgecolor="white", height=0.7)
    ax.set_yticks(list(y))
    ax.set_yticklabels(drugs, fontsize=9)
    ax.set_xlim(0, 1.6)
    ax.set_xticks([])
    for i, (bar, lbl) in enumerate(zip(bars, labels)):
        ax.text(1.05, i, lbl, va="center", fontsize=9)
    ax.set_title("Figure 5B — Model–clinical concordance", fontsize=10)

    patches = [
        mpatches.Patch(color="#2ca02c", label="Concordant (model = clinical outcome)"),
        mpatches.Patch(color="#9467bd", label="Novel prediction (no clinical data yet)"),
        mpatches.Patch(color="#aec7e8", label="Not modelled / pending trial"),
        mpatches.Patch(color="#d62728", label="Discordant"),
    ]
    ax.legend(handles=patches, loc="lower right", fontsize=8)
    plt.tight_layout()
    plt.savefig(f"{OUT}/fig5b_concordance.png", dpi=150, bbox_inches="tight")
    plt.close()
    print("  Saved fig5b_concordance.png")


# ── Figure 5C : Hamming distances across cohorts ─────────────────────────────
def fig5c_hamming():
    gse = pd.read_csv(GSE)
    ass = pd.read_csv(ASSESS)

    # PRECISESADS best values from Phase 3
    prec_vals = {
        "IFN-stimulated FP1": 0.849,
        "IFN-stimulated FP2": 0.887,
        "BCR-stimulated FP1": 0.874,
        "BCR-stimulated FP2": 0.912,
    }

    fig, ax = plt.subplots(figsize=(8, 5))

    # GSE23117 IFN conditions
    gse_ifn = gse[gse["condition"] == "IFN-stimulated"][["attractor", "gse23117_hamming"]]
    gse_bcr = gse[gse["condition"] == "BCR-stimulated"][["attractor", "gse23117_hamming"]]

    x = np.arange(4)
    w = 0.25

    prec = [prec_vals["IFN-stimulated FP1"], prec_vals["IFN-stimulated FP2"],
            prec_vals["BCR-stimulated FP1"], prec_vals["BCR-stimulated FP2"]]
    gse_v = list(gse_ifn["gse23117_hamming"]) + list(gse_bcr["gse23117_hamming"])

    # ASSESS best hamming per condition (FP1)
    ass_v = list(ass.groupby("condition")["assess_hamming"].min().reindex(
        ["IFN-stimulated", "BCR-stimulated"]))
    ass_all = [ass_v[0], None, ass_v[1], None]  # only 2 conditions available

    b1 = ax.bar(x - w, prec, w, label="PRECISESADS (blood)", color="#4C72B0")
    b2 = ax.bar(x,     gse_v, w, label="GSE23117 (salivary gland)", color="#DD8452")
    b3_x = [xi for xi, v in zip(x + w, ass_all) if v is not None]
    b3_v = [v for v in ass_all if v is not None]
    ax.bar(b3_x, b3_v, w, label="ASSESS (lymphoma)", color="#55A868")

    ax.axhline(0.5, ls="--", color="gray", lw=0.8, label="Random (0.5)")
    ax.set_xticks(x)
    ax.set_xticklabels(["IFN FP1", "IFN FP2", "BCR FP1", "BCR FP2"], fontsize=9)
    ax.set_ylabel("Hamming distance (lower = better match)")
    ax.set_ylim(0, 1.05)
    ax.set_title("Figure 5C — Cross-cohort Hamming distances", fontsize=10)
    ax.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(f"{OUT}/fig5c_hamming.png", dpi=150, bbox_inches="tight")
    plt.close()
    print("  Saved fig5c_hamming.png")


# ── Figure 5D : AP1/p38 control module ───────────────────────────────────────
def fig5d_control_module():
    fig, ax = plt.subplots(figsize=(9, 4))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 4)
    ax.axis("off")

    nodes = [
        (1.0, 2.0, "EIF2AK2\n(PKR)", "#9467bd"),
        (2.8, 2.0, "MAP2K6\n(phosph.)", "#ff7f0e"),
        (4.6, 2.0, "MAPK11-14\n(p38)", "#ff7f0e"),
        (6.4, 2.8, "FOS\n(phosph.)", "#d62728"),
        (6.4, 1.2, "JUN\n(phosph.)", "#d62728"),
        (8.2, 2.0, "AP1\ncomplex", "#d62728"),
        (9.5, 2.0, "Inflammation\npathway", "#c5b0d5"),
    ]

    for x, y, label, color in nodes:
        ax.add_patch(mpatches.FancyBboxPatch(
            (x-0.7, y-0.5), 1.4, 1.0, boxstyle="round,pad=0.1",
            facecolor=color, edgecolor="black", linewidth=1.5, alpha=0.85))
        ax.text(x, y, label, ha="center", va="center", fontsize=7.5,
                color="white", fontweight="bold")

    arrows = [
        (1.7, 2.0, 2.1, 2.0),
        (3.5, 2.0, 3.9, 2.0),
        (5.3, 2.2, 5.7, 2.7),
        (5.3, 1.8, 5.7, 1.3),
        (7.1, 2.7, 7.5, 2.2),
        (7.1, 1.3, 7.5, 1.8),
        (8.9, 2.0, 9.2, 2.0),
    ]
    for x1, y1, x2, y2 in arrows:
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="->", color="black", lw=1.5))

    # Drug inhibition markers
    for drug, node_x, node_y, offset in [
        ("PKR-inh.", 1.0, 2.0, -0.7),
        ("p38-inh.", 4.6, 2.0, -0.7),
        ("AP1-inh.", 8.2, 2.0, -0.7),
    ]:
        ax.add_patch(mpatches.FancyBboxPatch(
            (node_x-0.55, node_y+offset-0.2), 1.1, 0.4,
            boxstyle="round,pad=0.05", facecolor="#bcbd22",
            edgecolor="#8c564b", linewidth=1, alpha=0.9))
        ax.text(node_x, node_y+offset, drug, ha="center", va="center",
                fontsize=6.5, color="black")
        ax.annotate("", xy=(node_x, node_y-0.5), xytext=(node_x, node_y+offset+0.2),
                    arrowprops=dict(arrowstyle="-|>", color="#8c564b", lw=1.5,
                                   connectionstyle="arc3,rad=0"))

    ax.set_title("Figure 5D — AP1/p38 MAPK control module and predicted drug targets",
                 fontsize=10, pad=10)
    plt.tight_layout()
    plt.savefig(f"{OUT}/fig5d_control_module.png", dpi=150, bbox_inches="tight")
    plt.close()
    print("  Saved fig5d_control_module.png")


if __name__ == "__main__":
    print("Generating Phase 5 figures...")
    fig5a_drug_heatmap()
    fig5b_concordance()
    fig5c_hamming()
    fig5d_control_module()
    print("Done.")
