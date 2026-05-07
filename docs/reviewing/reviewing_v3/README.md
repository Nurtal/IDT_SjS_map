# Dossier de relecture par les pairs

Ce dossier contient une simulation de l'évaluation par les pairs du manuscrit `docs/manuscript_v3.md`, par quatre relecteurs aux profils complémentaires, accompagnée d'une synthèse éditoriale.

Les relecteurs ont évalué le manuscrit *en aveugle* : aucun n'a eu accès à des versions antérieures éventuelles ni à des échanges éditoriaux préalables. Chaque rapport est rédigé comme une première lecture du manuscrit.

## Sommaire

| Fichier | Auteur (profil simulé) | Verdict |
|---|---|---|
| [`00_synthese_editoriale.md`](00_synthese_editoriale.md) | Éditeur en chef (synthèse) | **Accept after minor revisions** |
| [`01_reviewer_modelisation_booleenne.md`](01_reviewer_modelisation_booleenne.md) | Modélisation booléenne (sémantique MP, ASP) | **Accept after minor revisions** |
| [`02_reviewer_immuno_clinicien.md`](02_reviewer_immuno_clinicien.md) | Immuno-rhumatologue, expert SjD | **Accept after minor revisions** |
| [`03_reviewer_bioinfo_transcriptomique.md`](03_reviewer_bioinfo_transcriptomique.md) | Bioinformaticien transcriptomique | **Accept after minor revisions** |
| [`04_reviewer_pharmaco_drug_discovery.md`](04_reviewer_pharmaco_drug_discovery.md) | Pharmacologue / drug discovery | **Accept after minor revisions** |

## Convergences inter-relecteurs

Sept points convergents, tous éditoriaux ou tabulaires (aucun ne demande de re-calcul) :

1. **C1** — Statistique : ratios up:down par cohorte, p_BH explicites, IC bootstrap pour 5 cohortes (R3).
2. **C2** — Stable motifs : préciser les paramètres pystablemotifs testés et discuter le partitionnement modulaire (R1).
3. **C3** — SYK + p38 : préciser la sélectivité modérée des SYK inhibiteurs cliniques (R4).
4. **C4** — PKR : reconnaître plus explicitement la non-disponibilité de compounds cliniquement avancés (R2, R4).
5. **C5** — BAFF/APRIL non-couvert dans la prédiction lymphomagénique : expliciter (R2).
6. **C6** — Naive condition : documenter quels nœuds restent à 1 dans Naive FP1 (R1).
7. **C7** — Trap-space cyclique IFN-stim : distinguer "oscillation au sens dynamique" vs "envelope de variabilité populationnelle" (R2).

## Articulation avec le manuscrit

Les recommandations sont numérotées `Rx.y` où *x* est le numéro du relecteur. Pour la lettre de réponse aux relecteurs, ces identifiants peuvent être réutilisés.

## Estimation de charge de la révision

Total estimé : **3-5 jours** (additions tabulaires, précisions textuelles, paragraphes ciblés ; aucune ré-exécution lourde de pipeline ni de nouveau calcul).
