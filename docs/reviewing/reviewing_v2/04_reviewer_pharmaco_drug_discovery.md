# Rapport de relecture — Pharmacologie / drug discovery (round 2)

**Manuscrit :** v2 (Foulquier, 2026)
**Relecteur :** Dr. K. — Pharmacologie des réseaux, drug repositioning, ADMET
**Date :** 2026-05-07
**Recommandation :** **Accept after minor revisions**

---

## 1. Avis global

Le retour aux corrections que j'avais demandées est satisfaisant à un degré rare : le manuscrit retire la métrique "8/10 concordance" (R4.7), assume la non-modélisabilité de 25/39 cibles cliniques (R4.4 / R4.8), tempère les prédictions (R4.3) et ajoute le contexte historique d'échec des inhibiteurs p38 (R4.6). En outre, la version révisée fait apparaître une prédiction nouvelle et plus précise — SYK + p38 / PKR en condition BCR-stim (Section 3.5) — qui adresse directement R4.1 et donne au manuscrit une thèse translationnelle plus défendable que la simple "p38 inhibitor en monothérapie pour SjD".

L'angle "what the model can and cannot predict" (Sections 3.6, 4.4) est le bon angle. C'est ce qui distingue une étude de modélisation utile en pharmacologie d'une étude qui sur-promet — la communauté drug-discovery a appris à se méfier des deuxièmes ; l'auteur a pris le bon virage.

Trois axes de révision restent à mes yeux : (i) la prédiction SYK + p38 / PKR a besoin d'un *paragraphe dédié à la faisabilité translationnelle* ; (ii) PKR (EIF2AK2) est étayé par moins de données cliniques que p38 et l'asymétrie devrait être reconnue ; (iii) la table de drug simulation gagnerait en lisibilité avec une colonne explicite "next preclinical step".

---

## 2. Points traités au round 2 — évaluation détaillée

| Reco | Statut | Évaluation |
|---|---|---|
| R4.1 — Simulation combinaisons | 91 paires, 3 conditions (Section 3.5) | ✅ Excellent |
| R4.2 — Sélectivité JAK inhibiteurs | Distinction filgotinib / baricitinib / tofacitinib | ✅ Adressé |
| R4.3 — Reformulation prédictions p38/AP1/PKR | "Candidate", *combination*, pas monothérapie | ✅ Approprié |
| R4.4 — Section cibles non modélisables | Section 4.4 (25/39) | ✅ Direct et utile |
| R4.5 — Sensibilité au seuil disease attractor | `threshold_sensitivity.csv` (θ ∈ {5,6,7}) | ✅ Robuste |
| R4.6 — Échecs p38 (3+ refs) | Damjanov + Watz + Newby + Hammaker | ✅ Solide |
| R4.7 — Retirer "8/10 concordance" | Retiré, recasté en 3 modellable / 9 not modellable | ✅ Rare et bien fait |
| R4.8 — Section 25/39 cibles absentes | Section 4.4 explicite | ✅ Honnête |

---

## 3. Points qui restent à clarifier

### 3.1 La prédiction SYK + p38 / PKR — quelle prochaine étape concrète ?

C'est la prédiction-phare de la révision et elle mérite d'être armée pour le lecteur drug-discovery. Actuellement la Section 3.5 dit :

> "These three pairs define a candidate combinatorial axis for SjD-associated DLBCL, where chronic BCR signalling is hypothesised to bypass mono-kinase inhibition."

C'est le bon claim mais il faut **rendre la prédiction testable**. Les questions naturelles que se pose un drug developer :

1. **Quel modèle préclinique** ? Souris NOD.B10.H2b développe une SS-like puis B-cell lymphoma. Modèle Aire⁻/⁻ ? Lignée DLBCL avec activation BCR (TMD8, OCI-Ly10) traitée par fostamatinib + losmapimod ?
2. **Compound availability** : fostamatinib (AAFOST) est approuvé en ITP ; entospletinib en Phase 2 DLBCL. Losmapimod, doramapimod sont en compléments d'études Phase 2 disponibles. C16 (PKR inhibitor) reste précliniquement disponible mais n'a aucune Phase 1 humaine. **Cette asymétrie de maturité clinique mérite d'être explicite dans la Section 4 ou dans un tableau additif.**
3. **Mécanisme moléculaire** : la combinaison SYK + p38 a-t-elle été testée dans d'autres pathologies BCR-driven (CLL, MCL, ABC-DLBCL) ? Si oui, citer ces données ; si non, reconnaître que la prédiction est *de novo* et n'a aucun précédent.

**Demande :** ajouter une sous-section de Discussion ("4.x Translational feasibility of SYK + p38 / PKR predictions") couvrant ces trois points en ~1 page.

### 3.2 PKR (EIF2AK2) — base translationnelle plus mince que p38

Le manuscrit mentionne C16 et imoxin comme inhibiteurs PKR existants. Mais à ma connaissance (vérifier dans clinicaltrials.gov), aucun inhibiteur PKR n'a atteint la Phase 1 humaine pour quelque indication que ce soit. C16 est outil de recherche ; imoxin est un peptide. Cette différence avec p38 (où des compounds ont franchi la Phase 2 en RA et COPD) doit être reconnue. Sinon le lecteur pourrait conclure "trois prédictions équivalentes" alors qu'elles diffèrent radicalement en maturité translationnelle.

**Demande :** dans Section 4.5 (predictions translationnelles) ou dans Table 5, ajouter une colonne "Compound availability" avec :
- p38 inhibitors : losmapimod, doramapimod (Phase 2 completed in RA / COPD ; safety profile published)
- PKR inhibitors : C16 (research tool only), imoxin (peptide ; preclinical only ; no Phase 1)
- AP1 inhibitors : pas de compound clinique direct ; T-5224 est en preclinical (cancer)
- SYK inhibitors : fostamatinib (approved ITP), entospletinib (Phase 2 DLBCL)

### 3.3 Tirabrutinib row de Table 5 — ambigu

Le tableau dit : "Insufficient (Naive/IFN); — (BCR baseline = AP1 active)". Cela me prend trois lectures pour comprendre que sous BCR, AP1 est *déjà* actif au baseline et que tirabrutinib n'élimine pas l'attracteur. Le lecteur clinicien risquerait d'interpréter "—" comme "non testé" alors que le résultat est en fait "testé et inefficace".

**Demande :** simplifier la cellule en "Insufficient (3 conditions)" ou "No effect on attractor (3 conditions)".

### 3.4 Drugs in Phase 3 récent — actualiser

Quelques mises à jour bibliographiques utiles (round 2 tient compte de la fenêtre temporelle 2024-2026) :

- **Ianalumab** : Phase 3 NCT05349214 (Bowman 2024) — résultats positifs, 13.8 vs 10.0 ESSDAI à S52. Le manuscrit dit "Moderate" — c'est plutôt "Significant in Phase 3".
- **Dazukibart** (anti-IFN-β monoclonal) : entré en Phase 2 SjD en 2024. Si pertinent, mentionner comme candidat anti-IFNAR alternatif.
- **Telitacicept** (TACI-Fc, Chine) : approuvé en SjD en Chine en 2025 — premier traitement ciblé BAFF/APRIL approuvé pour SjD. Cela renforce la pertinence du module BAFF que le SjD Map ne capture pas dynamiquement (R4.4).

**Demande :** revoir Table 5 et Section 4 avec ces mises à jour.

### 3.5 Drug repurposing — vue d'ensemble manquante

Une chose qui manque pour le lecteur drug-discovery : un tableau "drugs by mechanism of action" qui croise (rangée = mécanisme : JAK, BTK, BAFF, p38, …) × (colonne = compound, statut clinique, prédiction du modèle). C'est aujourd'hui éclaté entre Table 5, Section 4.3 et Section 4.4. Une consolidation en un tableau récapitulatif (peut-être en Discussion 4.7 ou en SI) aiderait grandement.

C'est de la suggestion éditoriale, pas une exigence.

---

## 4. Points secondaires

### 4.1 Anifrolumab — opportunité de simulation directe

Comme suggéré par le reviewer 2 (clinicien), simuler anifrolumab en forçant IFNAR_complex à 0 sous IFN-stim est un test direct et tractable. Il pourrait apparaître dans Table 5 avec une prédiction explicite plutôt que "Not modellable (input)". Cela renforcerait l'utilité du modèle pour anti-IFNAR.

### 4.2 Hydroxychloroquine — encore une fois

Le manuscrit retire la discordance HCQ en disant "TLR7/9 sont des inputs". C'est correct mais cliniquement frustrant. Une note explicite que **toute extension future** du framework devra prioritariser l'encodage dynamique de TLR7/9 (et BAFF/APRIL) serait utile pour orienter les développements ultérieurs.

### 4.3 Section 5 (Conclusions) — un peu dense

La conclusion actuelle (un long paragraphe) gagnerait à être restructurée en 3-4 alinéas distincts : (i) résultat principal v2 (concordance IFN-stim attestée stat), (ii) re-cadrage AP1/p38, (iii) prédictions actionnables avec next steps, (iv) limites.

---

## 5. Points positifs à conserver

- **Section 4.4 (25/39 cibles absentes)** : c'est exactement le type d'auto-critique que les pharmacologues attendent. À ne pas atténuer.
- **Re-cast Table 5 en 3 catégories (Modellable / Not modellable / Predicted novel)** : grande lisibilité. Bonne décision éditoriale.
- **La rétraction explicite du JAK + p38 synergy** : aligne l'auteur avec les pratiques de pré-enregistrement / falsifiabilité. Rare et précieux.
- **Threshold sensitivity (R4.5)** : démontre que le hit AP1/p38 est robuste, ce qui répond à mes inquiétudes initiales sur l'arbitraire du seuil θ = 6.
- **Le crible combinatoire est *targeted* (drug-target nodes)** : le bon ciblage pour drug discovery, plutôt qu'un crible exhaustif noise-prone.

---

## 6. Recommandation

**Accept after minor revisions.** Les demandes principales (3.1 paragraphe faisabilité translationnelle SYK + p38, 3.2 colonne "compound availability", 3.4 actualisation références cliniques 2024-2026) sont des additions ciblées de prose et de références. L'analyse anifrolumab (4.1) est optionnelle mais ajoutée elle renforcerait significativement le manuscrit.

Estimation délai révision : 1 semaine.

Le manuscrit v2 est, à mon avis, prêt pour acceptation après ces ajustements éditoriaux. La science est solide ; il s'agit maintenant de soigner la communication translationnelle.
