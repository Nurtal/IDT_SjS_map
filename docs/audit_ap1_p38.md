# Audit topologique du module AP1/p38 (Phase 7.1.2)

**Réseau analysé :** `models/sbmlqual/v1/sjd_map_reduced_clean.bnet` (508 nœuds, 923 arêtes orientées)

## 1. Centralités

| Groupe | in-degree (moy) | out-degree (moy) | betweenness (moy) | ancestors (moy) | descendants (moy) |
|---|---|---|---|---|---|
| AP1/p38 (6 nœuds) | 3.3 | 3.0 | 0.0058 | 221.0 | 30.8 |
| Contrôle (11 nœuds) | 9.0 | 7.1 | 0.0171 | 164.4 | 120.0 |

Détails complets : `results/phase7/topology_ap1_p38.csv`.

## 2. Voie TAK1/MAP3K7 → p38
- MAP3K7_phosphorylated présent comme ancêtre de MAPK11-14 (depth ≤ 3) : **OUI**
- MAP3K5 (ASK1) présent : **OUI**

La voie canonique TLR/IL-1 → TRAF6 → TAK1 → MKK6 → p38 est donc intacte topologiquement.

Liste complète des ancêtres de MAPK11-14 (depth ≤ 3) : `results/phase7/ap1_p38_upstream.csv` (14 entrées).

## 3. Chemins parallèles ligands → module

Nombre de chemins nœud-disjoints depuis chaque ligand :

| Ligand | → MAPK11-14 | → AP1_complex | → STAT1-P (référence) |
|---|---|---|---|
| IFNA_Extracellular_ligands | 1 | 1 | 1 |
| IFNB1_Extracellular_ligands | 1 | 1 | 1 |
| IFNG_IFNGR_complex | 1 | 1 | 1 |
| BCR_complex | 1 | 1 | 0 |
| CpG_DNA_TLR9_complex | 2 | 2 | 0 |
| LPS_CD14_TL4_LY96_complex | 2 | 2 | 0 |

## 4. Interprétation

**Verdict : bottleneck linéaire à signal mécanistique partiellement préservé.**

- Betweenness moyenne du module (0.0058) : **3× inférieure** au groupe de contrôle (0.0171). Les nœuds AP1/p38 ne sont *pas* des points de passage privilégiés du graphe orienté.
- In-degree moyen (3.3) et out-degree moyen (3.0) : **2.5–3× inférieurs** au groupe de contrôle (9.0 / 7.1). Le module est topologiquement **maigre**, ce qui rend chaque nœud individuellement critique : éliminer un seul nœud coupe la chaîne sans recours.
- Descendants moyens (30.8 vs 120) : le module est **peu en amont** ; il joue le rôle de relais terminal vers les phénotypes (notamment Inflammation), pas de hub de distribution.
- Ancestors moyens (221 vs 164) : en revanche, **beaucoup de signaux convergent** vers le module — il agrège effectivement les entrées TLR/IL-1, BCR, IFN.
- Voie canonique TAK1 (MAP3K7) : **présente topologiquement** dans la BNET v1, descendant de TAB1/TAB2/TAB3 puis de TRAF6 / RIPK1-TRAF2-TRAF5. La voie ASK1 (MAP3K5) est également présente.
- Chemins nœud-disjoints depuis les ligands : **1 seul chemin** pour IFN-α/β/γ et BCR ; **2 chemins** pour CpG/TLR9 et LPS/TLR4. La redondance interne du module est donc faible (≤ 2 chemins, vs. STAT1-P qui n'a qu'un chemin depuis IFN).

**Conséquences pour la révision (manuscrit v2) :**
1. La concentration des 6 hits monogéniques sur la chaîne EIF2AK2 → MAP2K6 → MAPK11-14 → FOS/JUN → AP1 est en **partie expliquée par la topologie** (chaîne linéaire à faible degré). Tempérer la formulation « central control module » → **« candidate control module convergent for multiple PRR/BCR/cytokine signals »**.
2. La voie TAK1 étant déjà présente, **aucune édition manuelle de la v2** n'est nécessaire au titre de la complétude du module.
3. Le test décisif est la **stabilité du hit aux perturbations combinatoires** (Phase 7.3.2) : si la suppression d'un nœud du module est compensée par la voie ASK1 ou par un chemin parallèle, le module n'est pas un nœud de contrôle réel.

Cette interprétation sera intégrée à la section 4.4 du manuscrit v2 et adresse R1.7, R2.1 (volet topologique) et R4.5.
