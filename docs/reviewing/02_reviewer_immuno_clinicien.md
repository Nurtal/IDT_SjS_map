# Rapport de relecteur n° 2 — Immuno-rhumatologie / Sjögren clinique

**Profil :** Clinicien-chercheur, expert de la maladie de Sjögren (essais cliniques, biomarqueurs, classification ESSDAI, sous-groupes moléculaires de Soret 2021).
**Statut :** Pair externe.
**Conflit d'intérêts :** Aucun déclaré (mais déclare avoir été investigateur sur des essais JAK et anti-BAFF en SjD).

---

## 1. Évaluation générale

L'idée de transformer la SjD Map en réseau exécutable est légitime et le timing est favorable, dans la continuité directe de Silva-Saffar et al. (2026). En tant que clinicien je me félicite que la communauté informatique s'attaque à cette pathologie complexe. Cependant, plusieurs interprétations cliniques du manuscrit me semblent **prématurées au regard des données présentées** — voire trompeuses pour un lecteur non spécialiste de la modélisation.

---

## 2. L'« attracteur SjD » est-il vraiment SjD ?

L'auteur identifie un point fixe (FP1) avec 7 phénotypes actifs : *B-cell activation, cell proliferation, chemotaxis, inflammation, MHC-II, regulated necrosis, T-cell activation*. Il l'appelle « SjD disease attractor ».

**Plusieurs problèmes cliniques :**

### 2.1 Ce profil n'est pas spécifique de SjD

Ces sept phénotypes décrivent grosso modo *toute maladie auto-immune systémique active* : on retrouverait le même profil dans le lupus érythémateux disséminé (SLE), la polyarthrite rhumatoïde (RA) en poussée, ou même le rejet d'allogreffe. La SjD a des caractéristiques distinctives :

- **Signature IFN-de type I marquée** (60–70 % des patients sont « IFN-high », Soret 2021) ;
- **Hyperactivation B-cellulaire dominante** avec auto-anticorps anti-SSA/Ro et anti-SSB/La ;
- **Implication exocrine** (kératoconjonctivite sèche, xérostomie) ;
- **Risque lymphomateux × 15–20** (DLBCL, MALT) ;
- **Hyperactivité BAFF/APRIL** documentée à la fois dans le sang et les glandes salivaires.

Aucune de ces signatures n'apparaît dans la description de FP1. La modélisation reste à un niveau de granularité tel que SjD est indistinguable de SLE ou RA.

### 2.2 La signature IFN-high — pierre angulaire de SjD — est manquante

L'auteur note lui-même (§2.6, §3.3 et §4.4) que la chaîne ISGF3 (STAT1/STAT2/IRF9 → induction de MX1, OAS1-3, ISG15) **ne fonctionne pas** dans son modèle, à cause d'une règle CaSQ `STAT1 = HDAC3` avec HDAC3 fixé à 0.

C'est dramatique pour un papier sur SjD. La signature IFN-I est *le* phénotype moléculaire le plus consensuel du champ depuis 15 ans. Si le modèle ne peut pas la produire, alors :

- L'« IFN-stimulated FP1 » que le manuscrit qualifie de meilleur match aux cohortes blood (PRECISESADS, UKPSSR, GSE51092) est en réalité un attracteur où *aucun ISG n'est exprimé* malgré IFNAR/IFNA/IFNB tous à 1.
- Le tableau de la Phase 3 (§annotation_report.md, §4) liste 25 nœuds IFN dont seuls 7 sont actifs — et aucun ISG n'en fait partie. C'est un IFN « payé en carte de crédit annulée ».
- Affirmer (abstract) que « FP1 best matches the blood cohorts » repose donc sur des concordances aux DEGs *non-ISG*, ce qui retire l'essentiel de la signature SjD.

**Avant publication, l'auteur doit corriger l'encodage HDAC3=1 (ou contourner cette dépendance) et re-tourner toute la Phase 3.** Sinon, la conclusion sur l'attracteur SjD est invalidée.

### 2.3 Le risque de lymphome n'est pas correctement modélisé

L'étude de cas ASSESS (Phase 5.2) prétend valider le modèle sur le risque lymphomateux. Mais :

- BTK ne devient actif que si l'auteur force `BCR_complex = 1` (entrée). Le modèle ne *prédit* pas l'activation BTK, il la *postule*.
- TNFSF13B (APRIL) reste à 0 dans tous les attracteurs — alors que BAFF/APRIL hyperactivité est *le* mécanisme historique du risque lymphome SjD (Mariette et al.).
- TNFSF13B est encodé comme nœud d'entrée et donc non-régulable dynamiquement par le modèle. Une étude sur les « therapeutic targets » qui ne peut pas modéliser BAFF/APRIL souffre d'un blind spot critique : **deux des médicaments centraux de la pratique SjD (belimumab, ianalumab, avec efficacité Phase 3 démontrée pour ianalumab) sont par construction non-modélisables**.

Le manuscrit doit le reconnaître plus clairement (la limitation §4.4 mentionne « not modélisé » mais pas l'enjeu lymphome).

---

## 3. Concordance avec les essais cliniques : surinterprétée

Le manuscrit revendique « 8/10 concordance » entre prédictions du modèle et résultats d'essais cliniques (Tableau 4, §3.5). Ce chiffre est *purement comptable* :

| Médicament | Résultat clinique | Modèle | « Concordance » |
|---|---|---|---|
| Filgotinib | Échec | Pas d'effet | ✓ |
| Baricitinib | Mitigé | Pas d'effet (Naive/BCR) ; Δ4 (IFN) | ✓ |
| Tofacitinib | Pas de réponse | Pas d'effet | ✓ |
| Tirabrutinib | En cours | Pas d'effet | ○ (à confirmer) |
| Iscalimab | En cours | Non modélisé | ○ |
| Ianalumab | **Efficace Phase 3** | Non modélisé | ○ |
| Belimumab | Modeste | Non modélisé | ○ |
| Anifrolumab | En cours | Non modélisé | ○ |
| HCQ | Standard of care | Pas d'effet | ⚠ Discordant |

Concrètement :
- Le modèle ne prédit aucune efficacité positive d'un médicament approuvé. Il ne sait dire « non » qu'à des médicaments qui ont effectivement échoué.
- Cinq médicaments ne sont pas modélisables (cibles input).
- Le seul médicament dont l'efficacité est solide en SjD (ianalumab, anti-BAFF, EUDRA filing en cours) **n'est pas modélisable**.
- L'HCQ, traitement de fond chez la quasi-totalité des patients SjD, est qualifié de discordant — puis reconnu comme une faiblesse du modèle.

**Une « concordance » qui se réduit à prédire correctement les échecs n'est pas une validation prédictive.** Le résumé doit être reformulé. Je suggère : *« 3 of 9 clinical drugs gave testable predictions, all concordant with reported failures; 5 drugs were not modellable due to input-node encoding; 1 was discordant. »*

---

## 4. Les prédictions thérapeutiques nouvelles

### 4.1 Inhibiteurs de p38 MAPK (losmapimod, doramapimod)

**Crédibilité clinique : faible-moyenne.** Les inhibiteurs de p38 ont été extensivement testés en RA, polyarthrite, BPCO, cardiopathies — et tous ont échoué en Phase 2/3 par effets de classe : hépatotoxicité, immunosuppression non sélective, perte d'efficacité après 8–12 semaines (« on/off effect » bien documenté). La référence Damjanov 2018 citée par l'auteur concerne précisément un échec en RA. Proposer aujourd'hui un essai p38 en SjD doit s'accompagner d'une discussion honnête de l'historique défavorable de cette classe.

### 4.2 Inhibiteur d'AP1

**Crédibilité clinique : faible.** AP1 (FOS/JUN) est un facteur de transcription pléiotrope largement non-druggable directement. Les rares « inhibiteurs d'AP1 » publiés (T-5224, SR11302) n'ont jamais atteint la phase clinique. Le manuscrit ne discute pas de la druggabilité d'AP1 ; cette prédiction est de niveau heuristique, pas thérapeutique.

### 4.3 Inhibiteurs de PKR/EIF2AK2

**Crédibilité clinique : très spéculative.** Aucun essai clinique d'inhibiteur PKR n'existe (C16 et imoxin sont des outils précliniques avec sélectivité limitée et toxicité hépatique en modèles animaux). Le rationnel ERV/dsRNA → PKR (Arleevskaya 2021) est intéressant *au plan exploratoire*, mais pas suffisant pour positionner PKR comme « entry point pharmacologique » en SjD.

### 4.4 Combinaison JAK + p38

**Crédibilité clinique : intéressante mais non testée par le modèle lui-même** — c'est une *interpolation* à partir d'observations sur des perturbations *séparées*. Le manuscrit propose la synergie comme prédiction, mais ne simule pas la double perturbation. Sans simulation, l'argument reste rhétorique.

---

## 5. Pertinence des phénotypes terminaux

Les 14 phénotypes hérités de la SjD Map (B-cell activation, MHC-II, fibrose, etc.) sont des *cell-fate outputs* communs à de nombreuses maladies. Ils ne capturent pas la spécificité SjD :

- Pas de phénotype « auto-anticorps anti-Ro/La » ;
- Pas de phénotype « hyposialie / atrophie acineuse » ;
- Pas de phénotype « formation de structures lymphoïdes ectopiques » (le « lymphoid organ development » est l'unique approximation, mais il représente le LN normal, pas le tertiaire ectopique salivaire).

**Suggestion :** discuter cette limitation dans §4.4. Une amélioration future serait d'enrichir la SjD Map avec des phénotypes SjD-spécifiques avant de réexécuter l'analyse.

---

## 6. Pertinence pour la pratique clinique

Honnêtement, dans son état actuel :

- Le modèle ne fournit pas d'outil utilisable au lit du patient.
- Il ne permet pas de stratifier les patients (pas d'attracteurs sous-groupe-spécifiques).
- Les prédictions thérapeutiques ne sont pas actionnables sans validation préclinique majeure.

C'est acceptable pour un papier de méthodologie / preuve de concept, à condition que ce statut soit clairement énoncé. Les formulations « identifies novel therapeutic targets » et « predicts synergy » dans l'abstract sont trop fortes.

---

## 7. Recommandations

| Priorité | Action |
|---|---|
| **R2.1** | **Critique** — corriger l'encodage `STAT1 = HDAC3` (forcer HDAC3=1 par défaut, ou éditer la règle) et reproduire la Phase 3. La signature IFN-high *doit* être reproductible dans un modèle SjD. |
| **R2.2** | Reformuler l'abstract pour ne pas revendiquer la « 8/10 concordance ». Distinguer prédictions actives vs absence de prédiction. |
| **R2.3** | Inclure une simulation effective de la double perturbation JAK + p38 (et JAK + BTK) — sinon la « synergie prédite » reste hypothétique. |
| **R2.4** | Discuter l'historique d'échec des inhibiteurs p38 et la non-druggabilité d'AP1, avec références. |
| **R2.5** | Discuter pourquoi BAFF/APRIL/CD40 — cibles cliniques majeures en SjD — sont non-modélisables et l'impact sur la généralisation des prédictions. |
| **R2.6** | Ajouter une discussion explicite des limites cellulaires : le modèle ne distingue pas glande salivaire vs sang vs tissu lymphoïde, ce qui est central en SjD. |
| **R2.7** | Tempérer le titre : *« Identifies AP1/p38 MAPK as a Central Control Module »* est trop affirmatif. Suggestion : *« Suggests AP1/p38 MAPK as a candidate control module »*. |

---

## 8. Verdict du relecteur

**Recommandation : Major Revision.**

Le travail est honnête dans sa mise en œuvre et touche un sujet pertinent, mais il *survende* ses conclusions cliniques. Avec les corrections demandées (notamment R2.1 sur la signature IFN, qui est non-négociable pour un papier sur SjD), le manuscrit pourra prétendre à une publication méthodologique solide. Sans ces corrections, il risque de faire passer une prédiction artefactuelle (PKR/AP1) pour une cible thérapeutique nouvelle, ce qui peut induire en erreur la communauté SjD.
