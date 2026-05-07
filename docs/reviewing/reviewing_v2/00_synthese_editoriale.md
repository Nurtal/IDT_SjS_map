# Synthèse éditoriale — Évaluation par les pairs (round 2)

**Manuscrit :** *Boolean Attractor Analysis of the Sjögren's Disease Map Identifies AP1/p38 MAPK as a Candidate Convergent Control Module Under IFN Stimulation* (Foulquier, v2)
**Journal cible :** *npj Systems Biology and Applications*
**Date de synthèse :** 2026-05-07
**Statut suggéré :** **Accept after minor revisions** (consensus convergent)

---

## 1. Contexte du round 2

Cette synthèse rassemble les retours des quatre relecteurs ayant déjà évalué le round 1 (verdict : *Major revision* unanime) et qui ont reçu pour ce round :

- le manuscrit révisé (`docs/manuscript_v2.md`)
- la lettre de réponse aux relecteurs (`docs/response_to_reviewers.md`)
- les outputs nouvelle Phase 7 (`results/phase7/`, `data/processed/hgnc_to_bnet.csv`, etc.)
- le tag Git `model-v2.0` du modèle Boolean corrigé

| # | Relecteur | Profil | Recommandation round 1 | Recommandation round 2 |
|---|---|---|---|---|
| 1 | Pr. L. — Modélisation booléenne | Sémantique MP, contrôle | Major revision | **Minor revision** |
| 2 | Pr. M. — Immuno-rhumatologue SjD | Pertinence biologique, essais | Major revision | **Accept after minor** |
| 3 | Dr. T. — Bioinfo transcriptomique | Statistique, validation externe | Major revision | **Accept after minor** |
| 4 | Dr. K. — Pharmacologie / drug discovery | Cibles, prédiction, ADMET | Major revision | **Accept after minor** |

**Verdict consensuel : Accept after minor revisions.**

---

## 2. Avis global

Le manuscrit v2 répond de manière substantielle, traçable et honnête aux 30 recommandations R1.1–R4.8 du round 1. Les corrections principales — modèle v2 corrigé pour la cascade IFN-I (HDAC3 = 1, KPNB1 = 1), null model statistique 10 000 permutations, AUROC, KEGG/Reactome enrichment, crible combinatoire ciblé, audit topologique du module AP1/p38, et tempérance générale du langage — adressent toutes les critiques majeures du round 1. La rétraction explicite de la prédiction "JAK + p38 synergique", remplacée par la prédiction nouvelle "SYK + p38 / PKR en BCR-stim", est un acte de transparence rare qui renforce la crédibilité du travail.

Quatre points cependant **demeurent à clarifier** avant l'acceptation finale (tous traitables en 1–2 semaines de révision, sans nouvelle exécution lourde) :

1. **L'IFN-stim de v2 n'a plus aucun point fixe** — uniquement un trap space cyclique. Cette transformation dynamique majeure n'est pas suffisamment discutée. Identifier les nœuds oscillants (probable feedback STAT-SOCS, NFkB-NFKBIA) et discuter la plausibilité biologique. (R1+R2 convergents)
2. **L'enrichissement KEGG/Reactome de IFN-stim A1 est peut-être tautologique** : il faudrait reporter le différentiel d'enrichissement v1 vs v2 pour distinguer ce que la correction "rend testable" de ce qui était déjà présent. (R3)
3. **Translational feasibility de SYK + p38 / PKR** : la prédiction-phare de v2 manque d'un paragraphe dédié à la faisabilité concrète (modèle préclinique, compound availability, précédents en autres pathologies BCR-driven comme ABC-DLBCL). (R4)
4. **Comparaison MP vs asynchrone classique** (R1.4) demeure non-traitée — au minimum, exécuter BoolNet/GINsim sur un sous-réseau (B-cell ou IFN module) pour valider la concordance des hits.

Aucun de ces points ne demande une re-exécution de Phase 7. Ce sont des ajouts éditoriaux et des analyses ciblées de quelques heures à quelques jours.

---

## 3. Convergences inter-relecteurs (round 2)

| # | Point | Soulevé par |
|---|---|---|
| C1' | Discussion biologique de la perte de point fixe sous IFN-stim v2 (oscillation = artefact ou réalité ?) | R1, R2 |
| C2' | Feedback statistique : reporter IC bootstrap + correction multiple + baselines triviaux | R1, R3 |
| C3' | Enrichissement KEGG/Reactome — différentiel v1 vs v2 attendu, sinon le résultat est tautologique | R3 |
| C4' | Translational feasibility de SYK + p38 / PKR — paragraphe dédié, compound availability | R2, R4 |
| C5' | Asymétrie maturité translationnelle p38 (Phase 2) vs PKR (preclinical only) | R4 |

Ces points convergent vers une demande de **révision principalement éditoriale**, sans nouveau calcul. Le verdict "Accept after minor revisions" reflète cet accord.

---

## 4. Forces qui justifient le passage en acceptation

Pour mémoire dans la décision éditoriale, les éléments qui sont salués transversalement :

- **Reproductibilité exemplaire** maintenue (Snakemake, MIT, tag Git `model-v2.0`, `changes.csv`).
- **Transparence méthodologique remarquable** : la rétraction du JAK + p38 et le re-cast 3/9 modellable sont des choix éditoriaux rares.
- **Statistique restaurée** : null model + AUROC + enrichissement avec p-values défendables (10 000 permutations, Benjamini-Hochberg, hypergeometric).
- **Audit topologique** (Section 3.4) qui re-cadre honnêtement la conclusion centrale — *candidate convergent control module* est défendable et précis.
- **Émergence d'une prédiction nouvelle** (SYK + p38 / PKR en BCR-stim) qui n'était pas dans v1 et qui adresse une question clinique concrète (lymphome SjD-associé).
- **Tests de non-régression** (3 tests pytest) : couverture des invariants critiques.
- **Réponse point-par-point** (`docs/response_to_reviewers.md`) à toutes les 30 recommandations — traçabilité exhaustive.

---

## 5. Décisions éditoriales en suspens

| # | Question | Recommandation |
|---|---|---|
| Q1' | La perte de point fixe IFN-stim sous v2 doit-elle déclencher une nouvelle correction du modèle ? | **Non** — discuter biologiquement, ne pas re-corriger ; la convention `*` = activable est défendable si analysée en sensibilité |
| Q2' | Les stable motifs (R1.1) doivent-ils être bloqueurs ? | **Non** — la documentation comme limite + le crible combinatoire constituent une mitigation acceptable |
| Q3' | Bootstrap CI sur Hamming + correction multiple suffisent-ils pour la robustesse stat ? | **Oui** — combinés au null model existant, ils stabilisent les conclusions |
| Q4' | Le manuscrit gagne-t-il en force translationnelle après révision (vs perte de "8/10" et de "JAK+p38") ? | **Oui si** la Section "translational feasibility SYK + p38" est ajoutée |

---

## 6. Recommandation éditoriale

**Accept after minor revisions.** Les délais nécessaires aux clarifications demandées (discussion oscillation IFN-stim, enrichissement différentiel v1/v2, paragraphe translationnel SYK + p38, BoolNet sub-réseau, IC bootstrap) sont estimés à **1–2 semaines** de révision. Aucune ré-exécution de Phase 7 n'est requise.

Le manuscrit a substantiellement progressé entre v1 et v2 ; la qualité atteinte justifie largement la publication dans *npj Systems Biology and Applications*. La transparence sur les limites (cell-type agnostique, 25/39 cibles non modélisables, JAK+p38 falsifié) et la démarche de falsification explicite distinguent ce travail des études de modélisation systématique de la littérature.

---

*Synthèse rédigée à partir des rapports individuels des relecteurs 1–4 (round 2). Voir `01_*.md` à `04_*.md` pour les détails par profil.*
