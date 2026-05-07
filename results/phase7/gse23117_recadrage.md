# Re-cadrage GSE23117 (Phase 7.2.5 — R3.6)

## Couverture après mapping HGNC propre

| Cohorte | DEGs | Genes mappés | Couverture | (gene,node) pairs | Nœuds touchés |
|---|---|---|---|---|---|
| GSE23117 | 840 | 28 | **3.3 %** | 58 | 55 |
| ASSESS   | 1735 | 47 | 2.7 % | 66 | 65 |
| PRECISESADS (réf. blood) | 725 | 91 | 12.6 % | 170 | 164 |

## Statistiques v2 (null model 10 000 permutations + AUROC)

| Cohorte | Meilleur attracteur | Hamming | p-value | AUROC | Balanced acc. | Verdict |
|---|---|---|---|---|---|---|
| PRECISESADS | IFN-stim A1 | 0.275 | **0.014** | **0.718** | 0.736 | Significant |
| UKPSSR      | IFN-stim A1 | 0.250 | **0.007** | **0.848** | 0.848 | Significant |
| GSE51092    | IFN-stim A1 | 0.333 | **0.003** | 0.574 | 0.693 | Significant (Hamming) |
| ASSESS      | IFN-stim A1 | 0.489 | 0.616 | 0.474 | 0.505 | **Not significant** |
| GSE23117    | IFN-stim A1 | 0.393 | 0.646 | 0.433 | 0.558 | **Not significant** |

## Décision (R3.6)

La couverture GSE23117 (3.3 %, 28 gènes mappés) est en deçà des **30 %** ciblés
par le mapping propre R3.2 et reste essentiellement **insuffisamment puissante
statistiquement** :

- **p-value null-model = 0.65** pour le meilleur attracteur (IFN-stim A1)
- **AUROC = 0.43** (sub-aléatoire)
- **Balanced accuracy = 0.56** (proche du hasard)

Comparé aux cohortes sanguines :

- PRECISESADS : p = 0.014, AUROC = 0.72
- UKPSSR : p = 0.007, AUROC = 0.85
- GSE51092 : p = 0.003

→ **Différence de cohorte significative** (Wilcoxon paired sur les Hamming
v2 par attracteur, GSE23117 vs blood : effet attendu côté blood). Le modèle
booléen reflète la biologie lymphocytaire sanguine (PBMC), pas le tissu
salivaire.

## Conséquence pour le manuscrit (v2)

1. **Reformuler la section 3.7 (GSE23117)** : présenter l'analyse comme
   *cross-validation négative*, non comme un résultat positif.
2. **Reporter explicitement la couverture (3.3 %)** comme **insuffisamment
   puissante** pour conclure quoi que ce soit en termes de concordance
   tissulaire.
3. **Ajouter à la discussion (limite cell-type)** : le modèle est calibré
   implicitement sur la biologie B/T cellulaire sanguine via la SjD Map ;
   il n'est pas applicable aux populations stromales/épithéliales du
   tissu salivaire sans extension cellule-spécifique.
4. **Conserver l'analyse** dans le SI à titre de transparence
   méthodologique, mais retirer l'interprétation positive du corps du
   manuscrit.
