# Rapport de relecture — Immuno-rhumatologie / SjD (round 2)

**Manuscrit :** v2 (Foulquier, 2026)
**Relecteur :** Pr. M. — Immuno-rhumatologue, expert SjD, principal investigator de cohortes PRECISESADS et UKPSSR
**Date :** 2026-05-07
**Recommandation :** **Accept after minor revisions** — la révision a fait passer le manuscrit d'une étude méthodologiquement fragile (round 1) à une étude méthodologiquement solide qui propose une lecture honnête et nuancée des forces et limites du SjD Map en mode dynamique.

---

## 1. Avis global

C'est une révision sérieuse. Les trois points qui me retenaient au round 1 (R2.1 encodage IFN cassé, R2.2 sur-revendication "8/10", R2.3 combinaison non simulée) sont traités directement et sans détour. Plus important : l'auteur a accepté de **retracter** une prédiction (JAK + p38) plutôt que la défendre — c'est un choix éditorial fort qui rehausse la crédibilité du manuscrit. La nouvelle prédiction qui émerge (SYK + p38 / PKR en contexte BCR-stim) est mécaniquement plus défendable et ouvre une piste pertinente pour le lymphome SjD-associé.

Les sections discussion (4.3 historique p38, 4.4 cibles non modélisables, 4.5 cell-type) sont maintenant à la hauteur des attentes d'un reviewer clinicien — claires, sourcées, sans sur-revendication.

Les points qui me retiennent encore relèvent de l'interprétation clinique de résultats nouveaux (Section 3.5 SYK + p38 et 3.6 BTK / IFN-stim), pas de la méthodologie.

---

## 2. Points traités au round 2 — évaluation détaillée

| Reco | Statut | Évaluation |
|---|---|---|
| R2.1 — Correction HDAC3 / IFN-I | v2 livre 17 ISGs activables (Section 3.2) | ✅ Critique levée |
| R2.2 — Reformulation abstract | "8/10 concordance" retiré, langage tempéré | ✅ Excellent |
| R2.3 — Simulation JAK + p38 effective | Testé et **falsifié** explicitement (Section 3.5) | ✅ Modèle de transparence |
| R2.4 — Échecs historiques p38 | 4 références citées (Damjanov, Hammaker, Watz, Newby) | ✅ Solide |
| R2.5 — Discussion non-modélisabilité BAFF/CD40 | Section 4.4 (25/39 cibles absentes) | ✅ Honnête |
| R2.6 — Limitation cell-type agnostique | Section 4.5 référence AIR | ✅ Adéquat |
| R2.7 — Tempérer le titre | "Candidate Convergent Control Module Under IFN Stimulation" | ✅ Précis et défendable |

---

## 3. Points qui restent à clarifier ou à nuancer

### 3.1 La prédiction "SYK + p38 / PKR" en BCR-stim mérite des références supplémentaires

C'est la nouvelle prédiction principale du manuscrit v2. L'argument est élégant : SYK fournit l'activation BCR-driven du module AP1, donc bloquer p38 seul laisse SYK actif et inversement. Mais avant que cette prédiction soit utilisable cliniquement, je voudrais voir :

- **Y a-t-il des données précliniques** sur la combinaison SYK + p38 ou SYK + PKR dans des modèles de DLBCL ? Fostamatinib (SYK) a été testé en monothérapie en DLBCL (étude STELLAR-DLBCL, Friedberg 2010) avec efficacité limitée. La combinaison fostamatinib + losmapimod a-t-elle été testée ?
- **La logique BCR → SYK → AP1** dans le BNET passe-t-elle par les mêmes intermédiaires que la voie observée dans les ABC-DLBCL (chronic active BCR signaling, Davis 2010) ? Le manuscrit ne le précise pas. La carte SjD est-elle compatible avec la biologie ABC-DLBCL ou plutôt GCB-DLBCL ?
- **TNFSF13B (APRIL) reste à 0** dans tous les attracteurs (Section 3.7) — c'est un point clé pour le lymphome SjD car APRIL est un driver classique. L'auteur le reconnaît mais ne discute pas l'impact sur la prédiction SYK + p38 : si APRIL contribue au lymphome via TACI/BCMA, et que ces voies sont absentes du modèle, la prédiction SYK + p38 n'adresse qu'une partie du driver lymphomateux.

**Demande :** Section 4 (discussion) doit ajouter un paragraphe explicite sur la compatibilité (ou non) de la prédiction SYK + p38 avec la biologie connue du lymphome SjD-associé, citant Duret 2023 et Quartuccio 2014 (BAFF/APRIL en lymphomagenèse SjD).

### 3.2 IFN-stim sans point fixe — mon point de convergence avec le relecteur 1

Comme le relecteur 1 (modélisation), je trouve que la disparition du point fixe sous IFN-stim v2 mérite une discussion biologique explicite, pas uniquement méthodologique. Cliniquement :

- Les patients SjD avec signature IFN-high atteignent un état de chronicité (mois à années d'élévation des ISGs) qui ressemble à un point fixe stable, pas à une oscillation continue.
- Si le trap space cyclique de v2 reflète une oscillation transcriptionnelle réelle (par exemple SOCS3 ↔ STAT1 feedback), c'est intéressant. Si c'est un artefact d'encodage CaSQ (où une boucle négative est encodée trop strictement comme NOT), c'est une limite à reconnaître.

**Demande :** identifier au moins quelques nœuds oscillants du trap space (par exemple : si SOCS3 et STAT1 sont à `*`, on peut l'attribuer au feedback IFN-STAT-SOCS-IFN ; si c'est NFKBIA et RELA, c'est le feedback NFkB ; etc.). Une demi-page est suffisante.

### 3.3 Le manuscrit gagne en honnêteté mais perd en force translationnelle — équilibre à soigner

Avec la rétraction du JAK + p38 et le re-cadrage 3/9 modellable, le manuscrit fait moins de prédictions "translationnelles" qu'en v1. C'est honnête mais l'éditeur de *npj Syst Biol Appl* lit aussi la dimension impact. Je propose deux corrections de framing **sans inflation** des résultats :

- **Section 5 (Conclusions)** : structurer plus nettement les "trois actionnables" annoncés dans l'abstract en : (i) p38 inhibitors as a *combination partner*, pas en monothérapie ; (ii) PKR (EIF2AK2) comme *cible orpheline à valider précliniquement* ; (iii) SYK + p38 / PKR comme *combinaison candidate pour le SjD-DLBCL* — chacun avec une étape concrète suivante (modèle murin, lignée cellulaire, étude clinique pilote).
- **Discussion** : ajouter un court paragraphe sur "what the model is not" — explicitement, le modèle ne prédit pas l'efficacité absolue (réponse clinique en %), il prédit le *signe* de la réponse (élimination ou non d'un attracteur). C'est le bon niveau de claim mais le lecteur clinicien a besoin de cette précision.

### 3.4 Ianalumab — Phase 3 récente

Le manuscrit cite ianalumab comme "moderate efficacy" (Table 5) sans référence précise. Les résultats de la Phase 3 NCT05349214 (Bowman 2024) montrent en réalité une efficacité plus marquée que ce que le terme "moderate" suggère. À actualiser si les références bibliographiques sont mises à jour.

---

## 4. Points secondaires

### 4.1 Hydroxychloroquine (HCQ) — discordance retirée mais à préciser

Le manuscrit v1 reportait HCQ comme "discordant" ; le v2 le retire en disant que TLR7/9 sont des inputs non modélisables. C'est une explication formellement correcte mais cliniquement frustrante : HCQ est l'unique standard of care en SjD et l'une des questions les plus pratiques que le modèle pourrait éclairer. **Une note explicite** ("the model cannot predict HCQ effects because TLR7/9 are encoded as input nodes; this is a structural limitation of the SjD Map, not a falsification") serait utile pour le lecteur.

### 4.2 Anifrolumab (anti-IFNAR1) — un test indirect possible

Anifrolumab cible IFNAR1, qui est encodé comme input. Mais sous v2, la conséquence d'IFNAR_complex = 0 (au lieu de 1) sous IFN-stim peut être simulée. Cela testerait si bloquer la signalisation IFNAR transforme l'attracteur cyclique IFN-stim en un point fixe similaire à Naive. C'est un test biologiquement intéressant et facilement faisable.

**Demande optionnelle :** ajouter une simulation anifrolumab (IFNAR_complex forcé à 0) sous chaque condition et reporter le résultat dans Table 5.

---

## 5. Points positifs à conserver

- **La rétraction du JAK + p38** est un acte de transparence rare. À garder explicitement dans l'abstract et la conclusion.
- **Le 3/9 modellable** est honnête et instructif. C'est exactement le type d'auto-critique que la communauté demande aux études de modélisation.
- **Section 4.4 (25/39 cibles absentes)** : informe directement le lecteur sur ce qu'il peut et ne peut pas attendre du framework SjD-Map-as-BNET.
- **Audit topologique (Section 3.4)** : tempère élégamment le claim sans le démolir.
- **Annexes complètes** (`results/phase7/*.csv`) : chaque table du manuscrit est traçable à un fichier source.

---

## 6. Recommandation

**Accept after minor revisions.** Les demandes principales (3.1 références SYK+p38 lymphome, 3.2 nœuds oscillants IFN-stim, 3.3 framing translationnel, 3.4 référence ianalumab Phase 3) sont des ajustements éditoriaux et discussions, pas des analyses nouvelles à mener. Estimation : 1 semaine de révision.

Une fois ces clarifications apportées, le manuscrit est à mon sens prêt pour publication dans *npj Systems Biology and Applications*.
