# Couverture du mapping HGNC → BNET (Phase 7.2.1)

- Vocabulaire HGNC : 3825 symboles (union de 120 graines + DEGs des cohortes)
- Nœuds BNET (hors phénotypes) : 494
- Nœuds mappés à ≥ 1 HGNC : **483** (97.8 %)
- Nœuds non mappés       : 11
- Lignes mappings (1 HGNC × 1 nœud) : 593

## Couverture par cohorte (DEGs ↦ nœuds BNET)

| Cohorte | DEGs | Genes mappés | Couverture genes | (gene,node) pairs | Nœuds touchés |
|---|---|---|---|---|---|
| PRECISESADS | 725 | 91 | 12.6 % | 170 | 164 |
| UKPSSR | 196 | 28 | 14.3 % | 54 | 54 |
| GSE51092 | 1040 | 93 | 8.9 % | 172 | 165 |
| ASSESS | 1735 | 47 | 2.7 % | 66 | 65 |
| GSE23117 | 840 | 28 | 3.3 % | 58 | 55 |

*Note R3.2 :* la couverture cohorte ↦ nœuds est plafonnée par la **portée curée du SjD Map** (pathways signalisation, pas tous les ISGs/ARNm transcriptomiques). Le gain attendu de R3.2 (> 30 %) n'est pas atteignable à modèle inchangé — la couverture reflète une limite structurelle de la carte, à reporter en limitation discutée.

## Distribution des `kind`

- complex_member: 214
- protein: 192
- rna: 101
- phosphorylated: 35
- secreted_ligand: 13
- secreted: 13
- cell_localised: 10
- nucleus: 5
- active: 4
- small_molecule: 3
- homodimer: 2
- empty: 1
