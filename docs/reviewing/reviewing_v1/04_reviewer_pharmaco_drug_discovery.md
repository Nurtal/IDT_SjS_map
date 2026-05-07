# Rapport de relecteur n° 4 — Pharmacologie des réseaux et drug discovery

**Profil :** Pharmacologue-bioinformaticien ; expertise en simulation in silico de perturbations thérapeutiques, druggabilité, ADMET, et translation des modèles de réseau vers la priorisation de cibles.
**Statut :** Pair externe.
**Conflit d'intérêts :** Aucun déclaré.

---

## 1. Évaluation générale

Ce manuscrit propose des prédictions thérapeutiques (p38, AP1, PKR) à partir d'un crible de perturbations dans un réseau booléen. C'est un usage légitime des modèles de réseau, mais l'évaluation de la solidité d'une prédiction thérapeutique demande une chaîne de validations spécifiques que ce manuscrit n'a pas encore parcourue. Mon évaluation porte sur deux axes :
1. **Robustesse de la simulation in silico** (Phase 5.1)
2. **Druggabilité et plausibilité translationnelle** des cibles prédites

---

## 2. Simulation in silico des médicaments

### 2.1 Encodage des cibles : trop simpliste

Chaque médicament est encodé comme une inhibition booléenne d'un seul nœud (ou d'un petit ensemble), comme listé dans `therapeutic_validation.py:61-76`. Trois problèmes :

#### (a) Sélectivité ignorée

Tofacitinib est encodé comme `JAK1/2/3/TYK2 = 0` simultanément. Or *in vivo*, la sélectivité du tofacitinib est documentée : IC50 ratio JAK3/JAK2/JAK1/TYK2 ≈ 1 / 5 / 8 / >100. Le forçage simultané à 0 surestime l'effet. Inversement, baricitinib (JAK1/2 préférentiel) est encodé `JAK1=0, JAK2=0` — ce qui le rend identique à tofacitinib en pratique sur le BNET. Le modèle ne peut donc pas discriminer baricitinib vs tofacitinib alors que leurs profils cliniques différent.

#### (b) Pharmacocinétique absente

Aucun encodage de la pharmacodynamique : pas de notion de durée d'effet, de saturation, de seuil d'inhibition. Or l'effet de p38i en clinique se caractérise précisément par une perte d'efficacité après 8–12 semaines (échappement). Un modèle booléen statique ne peut pas le capturer, mais le manuscrit doit reconnaître cette limite.

#### (c) Médicaments « non modélisables »

Cinq des neuf médicaments cliniques sont déclarés non-modélisables (cibles input non dynamiques) :

| Médicament | Cible | Statut clinique |
|---|---|---|
| Iscalimab | CD40 | Phase 2 actif |
| Ianalumab | TNFRSF13C (BAFF-R) | Phase 3, efficace |
| Belimumab | TNFSF13B (BAFF) | Approuvé SLE, modeste SjD |
| Anifrolumab | IFNAR | Approuvé SLE |
| (autres : pilocarpine, etc.) | divers | divers |

Que cinq des médicaments centraux du champ SjD ne soient pas modélisables est *l'observation la plus importante* du manuscrit en termes de drug discovery — et elle n'est ni mise en avant ni discutée. La raison : ces cibles sont des récepteurs de surface ou des ligands extracellulaires, encodés comme inputs dans la SjD Map. Le manuscrit hérite donc la limite structurelle de la carte.

**Le manuscrit doit reconnaître que la portée des prédictions est limitée à la signalisation intracellulaire en aval des inputs.** Ce n'est pas un défaut intrinsèque, mais une contrainte qui doit être annoncée à l'abstract et au début de la discussion.

### 2.2 Pas de simulation de combinaisons

L'auteur affirme dans la discussion que « la combinaison JAK + p38 pourrait être synergique » (§4.2 et §4.5 du manuscrit ; §5.4 du `validation_report.md`). Cette affirmation est *non testée* dans le crible : seuls les inhibiteurs en monothérapie sont simulés.

Ajouter la simulation des combinaisons est trivial techniquement (le crible est déjà mono-nœud, il suffit d'itérer sur les paires) et serait l'un des arguments les plus translationnels du papier. **Demande critique.**

### 2.3 Définition de l'« élimination de l'attracteur »

Le critère est : *« n'importe lequel des FP restants ne contient pas ≥ 6 phénotypes du DISEASE_SET »* (`control_analysis.py:113`). Plusieurs failles :

- Si une perturbation transforme FP1 (7 phénotypes) en un nouveau attracteur à 5 phénotypes (encore très inflammatoire), le crible la déclare « efficace ». Mais cliniquement, passer de 7 à 5 phénotypes inflammatoires n'est pas synonyme de rémission.
- Le seuil 6/7 est arbitraire (si on prenait 5/7, davantage de perturbations « élimineraient » l'attracteur ; si on prenait 7/7, peut-être aucune).
- Aucune analyse de sensibilité au seuil.

**Demande :** rapporter les hits du crible pour plusieurs seuils (5, 6, 7) et discuter la stabilité du module AP1/p38 à travers ces seuils.

### 2.4 Pas de comparaison à un null model de perturbation

Sur 158 perturbations testées, 7 « éliminent l'attracteur ». 7/158 ≈ 4.4 %. Sans null model (perturbations sur des nœuds aléatoires d'un réseau random équivalent), on ne peut pas dire si ce taux est élevé ou faible. Une analyse simple par bootstrap des étiquettes des nœuds donnerait une référence.

---

## 3. Druggabilité des cibles prédites

### 3.1 p38 MAPK (MAPK11/12/13/14)

| Critère | Évaluation |
|---|---|
| Druggabilité | ✓ Très étudiée. Inhibiteurs ATP-compétitifs disponibles (losmapimod, doramapimod, BIRB-796). |
| Sécurité | ⚠ Hépatotoxicité documentée pour la classe. |
| Échecs cliniques | ⚠ Multiples : RA (failed Ph2 doramapimod), psoriasis, BPCO, infarctus (LATITUDE-TIMI 60). |
| Mécanisme d'échec | Tachyphylaxie (8–12 sem), redondance avec ERK et JNK, effets paradoxaux. |
| Cohérence avec le modèle | ✓ Le modèle ne capture pas la redondance ERK/JNK car ces voies ne sont peut-être pas modélisées. |

**Verdict :** prédiction biologiquement cohérente *en intracellulaire*, mais avec une histoire pharmacologique très défavorable. Le manuscrit doit citer les études d'échec (Damjanov 2018 est citée mais c'en est *un* exemple positif sur fait). Le repurposing d'un p38i pour la SjD aurait probablement les mêmes effets de classe.

### 3.2 AP1 (FOS/JUN/AP1_complex)

| Critère | Évaluation |
|---|---|
| Druggabilité | ✗ Mauvaise. Facteur de transcription pléiotrope, sans poche druggable identifiée. |
| Inhibiteurs disponibles | T-5224, SR11302 — outils précliniques, pas de phase I à ma connaissance. |
| Spécificité | Très faible — AP1 contrôle la prolifération, l'apoptose, la différenciation tissulaire. |
| Cohérence translationnelle | Faible. |

**Verdict :** prédiction de niveau « cible mécanistique » mais pas « cible thérapeutique ». Le manuscrit doit reformuler : AP1 est un *output régulatoire intéressant*, pas un *médicament potentiel*.

### 3.3 PKR / EIF2AK2

| Critère | Évaluation |
|---|---|
| Druggabilité | Variable. Quelques outils (C16, imoxin, PKR pseudosubstrate peptides) mais pas en phase clinique. |
| Sécurité | Inconnue chez l'humain. Modèles murins : déficits hématopoïétiques, sensibilité accrue aux infections virales. |
| Cohérence biologique avec SjD | ✓ Plausible (ERV / dsRNA → PKR → ISG-like response, Arleevskaya 2021). |
| Spécificité | PKR a aussi des fonctions homéostatiques (apoptose, traduction protéique) — risque on-target. |

**Verdict :** l'angle PKR est intéressant *en recherche fondamentale*. Pour le translationnel, il faudrait :
1. Démontrer la dépendance ERV/dsRNA chez les patients SjD (existe partiellement, mais pas démontrée comme driver causal).
2. Disposer d'inhibiteurs PKR sélectifs et tolérés — pas le cas aujourd'hui.

Le manuscrit présente PKR comme « unexplored mechanistic entry point ». La formulation est correcte, mais la suite *« strong computational prediction of efficacy »* (cover letter) est trop forte.

### 3.4 Combinaison JAK + p38

C'est la prédiction la plus intéressante translationnellement, mais comme noté plus haut, elle n'est pas réellement testée par le modèle. Si elle l'était, et si la simulation montrait que la double perturbation élimine FP1 alors que ni l'un ni l'autre seuls ne le font, ce serait un résultat fort. À tester avant publication.

---

## 4. Comparaison aux essais cliniques en cours

Le tableau de concordance (§3.5) traite tous les médicaments sur le même plan, mais ils ne sont pas comparables :

- **Filgotinib** : Phase 2 MOSAIC, Bowman 2023 — résultats décevants confirmés.
- **Baricitinib** : essais français de petite taille (N<50), résultats hétérogènes — il est trompeur de dire « mitigé » sans nuance.
- **Tofacitinib** : Phase 2 prématurément arrêtée — pas de réponse majeure mais étude sous-puissante.
- **Tirabrutinib** : essai *encore en cours* — la « concordance ○ à confirmer » donnée par l'auteur est honnête mais n'a pas sa place dans un score de validation.
- **Iscalimab** : non modélisé.

**Demande :** retirer la métrique « 8/10 concordance » du résumé. Présenter un tableau analytique reconnaissant les essais en cours, les non-modélisés, et les vraies prédictions positives/négatives — distinction qualitative plus qu'un score.

---

## 5. La cohorte ASSESS et l'angle lymphome

L'angle « prévention du lymphome SjD » (cover letter, §5.4 validation_report) est attractif mais sous-soutenu :

- BTK est forcé à 1 par l'auteur en condition BCR — donc le modèle ne *prédit* pas l'activation BTK, il l'impose.
- TNFSF13B (APRIL) reste à 0 dans tous les attracteurs — alors que l'upregulation APRIL/BTK *cooperative* est précisément la signature distinctive du lymphome SjD-associé.
- Le manuscrit attribue cette absence à un mécanisme « paracrine non capturé » — c'est-à-dire que le modèle reconnaît son incapacité à modéliser le mécanisme central du lymphome SjD.

**L'argument « le modèle distingue correctement le contexte BCR-dependent » est tautologique** : il distingue parce que l'auteur a explicitement encodé deux conditions distinctes. Cela n'apporte pas de validation prédictive.

---

## 6. Analyse des « cibles thérapeutiques connues »

Le tableau 4 du `control_report.md` confronte 39 gènes-cibles d'essais SjD aux résultats du crible. Le résultat est éclairant : **la plupart des cibles cliniques (TNFRSF13C, IFNAR1, MIF, NR3C1, MS4A1 = CD20, etc.) sont absentes du BNET** — colonne « — (absent BNET) ».

Ceci est en réalité **un des résultats les plus instructifs du papier**, mais il n'est pas mis en avant : le BNET CaSQ-derivé d'une SjD Map manque une fraction importante des cibles thérapeutiques actuelles. Ceci devrait être présenté comme :

> *« 25/39 SjD drug targets cannot be evaluated in the current Boolean network, highlighting the need for SjD Map enrichment with currently absent extracellular signalling components and surface receptors. »*

C'est une recommandation pour la communauté SjD Map qui mérite un §dédié.

---

## 7. Recommandations

| Priorité | Action |
|---|---|
| **R4.1** | Simuler effectivement les paires { JAK1, MAPK11-14 }, { JAK1, AP1 }, { BTK, AP1 } avant de revendiquer la synergie. |
| **R4.2** | Discuter la sélectivité réelle des JAK inhibiteurs (filgotinib, baricitinib, tofacitinib) ; encoder différemment les inhibiteurs non-équivalents. |
| **R4.3** | Reformuler les prédictions p38/AP1/PKR pour distinguer (i) cibles mécanistiquement intéressantes, (ii) cibles druggables, (iii) candidats de phase préclinique réaliste. |
| **R4.4** | Ajouter une section « Limitations of the current SjD Map for drug repurposing » mettant en avant les cibles non-modélisables (≥ 50 % des cibles cliniques). |
| **R4.5** | Tester le robustesse du module AP1/p38 à différents seuils de définition du « disease attractor ». |
| **R4.6** | Citer les échecs historiques de la classe p38 inhibiteurs (RA, BPCO, cardiologie) plutôt qu'un seul exemple. |
| **R4.7** | Retirer ou nuancer la métrique « 8/10 concordance » dans l'abstract. |
| **R4.8** | Section dédiée discutant les implications du résultat « 25/39 cibles absentes » pour la communauté SjD Map. |

---

## 8. Verdict du relecteur

**Recommandation : Major Revision.**

Le manuscrit a le mérite d'être l'un des premiers à confronter un réseau booléen issu d'une carte MIM aux données d'essais cliniques en SjD. C'est précieux pour la communauté.

Mais en tant que pharmacologue, je ne peux pas accepter en l'état les revendications de prédictions thérapeutiques. Les corrections demandées (notamment R4.1 sur les combinaisons et R4.4 sur les cibles non modélisables) sont essentielles pour donner au lecteur une image juste de la portée du modèle.

Une fois ces corrections faites, je pense que le papier sera un *meilleur* papier sur le rôle des cartes MIM en drug discovery, même si les prédictions individuelles deviennent plus modestes.
