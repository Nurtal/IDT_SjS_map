# Round 2 — Évaluation par les pairs du manuscrit v2

Ce dossier rassemble la simulation du **second tour de relecture** du manuscrit
*Boolean Attractor Analysis of the Sjögren's Disease Map…* (Foulquier, v2,
2026-05-07). Le round 1 (verdict *Major revision*) est archivé dans
`../reviewing_v1/`.

## Fichiers

| Fichier | Contenu |
|---|---|
| `00_synthese_editoriale.md` | Synthèse éditoriale, verdict consensuel, points convergents |
| `01_reviewer_modelisation_booleenne.md` | Pr. L. — sémantique MP, contrôle, scalabilité |
| `02_reviewer_immuno_clinicien.md` | Pr. M. — pertinence clinique SjD, prédictions translationnelles |
| `03_reviewer_bioinfo_transcriptomique.md` | Dr. T. — null model, AUROC, enrichissement |
| `04_reviewer_pharmaco_drug_discovery.md` | Dr. K. — drug repositioning, ADMET, cibles |

## Verdict consensuel

**Accept after minor revisions.** Les quatre relecteurs convergent vers une
acceptation conditionnée à des révisions principalement éditoriales (1–2
semaines de travail, pas de ré-exécution de Phase 7).

## Convergences round 2

| # | Point critique | Soulevé par |
|---|---|---|
| C1' | IFN-stim n'a plus de point fixe sous v2 — discuter biologiquement la perte | R1, R2 |
| C2' | Enrichissement KEGG/Reactome — reporter le différentiel v1 vs v2 pour distinguer le tautologique du génuin | R3 |
| C3' | Translational feasibility de la prédiction SYK + p38 / PKR — paragraphe dédié + compound availability | R2, R4 |
| C4' | Asymétrie maturité clinique p38 (Phase 2) vs PKR (preclinical only) | R4 |
| C5' | Comparaison MP vs asynchrone — au moins sur un sous-réseau (R1.4) | R1 |

## Évolution round 1 → round 2

| Relecteur | Round 1 | Round 2 |
|---|---|---|
| R1 (Modélisation) | Major revision | **Minor revision** |
| R2 (Clinicien) | Major revision | **Accept after minor** |
| R3 (Bioinfo) | Major revision | **Accept after minor** |
| R4 (Pharmaco) | Major revision | **Accept after minor** |

Tous les relecteurs ont *upgradé* leur verdict. La transparence avec laquelle
le round 1 a été adressé (rétraction explicite du JAK + p38, recasting 3/9
modellable, ajout du null model, audit topologique) est unanimement saluée.

## Prochaines étapes

1. Implémenter les ajustements éditoriaux (≈ 1 semaine).
2. Re-soumettre à *npj Systems Biology and Applications* avec la lettre de
   réponse round 2 (à rédiger dans `docs/response_to_reviewers_v2.md`).
3. Pré-publier sur Zenodo (DOI v2.1 après ces minor revisions).

---

*Round 2 généré le 2026-05-07. Round 1 archivé dans `../reviewing_v1/`.*
