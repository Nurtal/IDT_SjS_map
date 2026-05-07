# Rapport de relecteur n° 2 — Immuno-rhumatologie / Sjögren clinique

**Profil :** Clinicien-chercheur, expert de la maladie de Sjögren (essais cliniques, biomarqueurs, classification ESSDAI, sous-groupes moléculaires de Soret 2021, lymphomagenèse SjD-associée).
**Statut :** Pair externe.
**Conflit d'intérêts :** Aucun déclaré (mais a été investigateur sur des essais JAK et anti-BAFF en SjD).

---

## 1. Évaluation générale

L'auteur convertit la SjD Map (Silva-Saffar 2026) en réseau booléen exécutable et utilise cette dynamique pour identifier des cibles thérapeutiques candidates. C'est une démarche pertinente dans la continuité directe d'un papier *npj Syst Biol Appl* récent, et le manuscrit est rédigé avec un niveau de prudence translationnelle exemplaire. La signature IFN-de type I — *la* signature transcriptomique la plus reconnue de la SjD — est correctement reproduite (17 ISGs activables, enrichissement Reactome IFN à p_adj = 3 × 10⁻⁸⁶), ce qui distingue ce travail de ses prédécesseurs sur d'autres MIM auto-immunes.

Plus important pour un clinicien : l'auteur ne sur-revendique pas. La Section 4.6 *Limitations of the SjD Map for SjD drug repurposing* fait honnêtement le constat que 25 des 39 cibles cliniques (BAFF/APRIL, CD40, IFNAR comme récepteur, TLR7/9) sont structurellement non-modélisables dans le BNET dérivé, et la Section 4.4 *Translational feasibility* discute explicitement les modèles précliniques pertinents pour la prédiction principale. Ce sont les sections qui rendent le manuscrit utilisable pour la communauté clinique.

Mes recommandations sont **mineures**. **Accept after minor revisions.**

---

## 2. Points forts cliniques

- **Signature IFN reproduite** : 17 ISGs canoniques activables sous IFN-stim, plus quatre voies KEGG/Reactome canoniques significativement enrichies. Cette signature est *le* point d'ancrage clinique pour valider qu'un modèle SjD a un sens biologique. Sans elle, aucune prédiction n'est défendable. Avec elle, le reste du manuscrit gagne en crédibilité.
- **Concordance statistique avec trois cohortes blood indépendantes** (PRECISESADS, UKPSSR, GSE51092) : Hamming significativement inférieure au null à p ≤ 0.014. Trois cohortes indépendantes, c'est plus que la majorité des études comparables.
- **Re-cadrage AP1/p38** : la formulation "candidate convergent control module rather than a topologically central one" (Section 3.4) est précisément le bon niveau de claim. Le module est interprétable mécaniquement (convergence PRR/BCR/IFN sur AP1) sans sur-revendication d'un rôle hub.
- **Prédiction SYK + p38 / PKR en BCR-stim** : l'orientation vers le SjD-DLBCL (Section 4.4) est intelligente — la lymphomagenèse SjD est l'une des questions cliniques où une cible nouvelle ferait *vraiment* avancer le champ. La discussion de la compatibilité ABC vs GCB DLBCL (Section 4.4, paragraphe 3) cite Davis 2010 à bon escient.
- **Section 4.6 sur les cibles non-modélisables** : honnêteté clinique remarquable. Le clinicien sait dès la première lecture ce que le modèle peut et ne peut pas dire.
- **Reconnaissance explicite de HCQ** (Section 3.7) : "the model cannot speak to its efficacy because TLR7 and TLR9 are encoded as input nodes" — exactement le caveat qu'il fallait poser.
- **Références cliniques 2024-2026** : ianalumab Phase 3 (Bowman 2024), telitacicept (approbation Chine 2025), MOSAIC. À jour.

---

## 3. Points qui restent à clarifier

### 3.1 La prédiction "SYK + p38 / PKR" en SjD-DLBCL — une étape de plus avant la testabilité

La Section 4.4 (Translational feasibility) discute fostamatinib, entospletinib (SYK) et losmapimod, doramapimod (p38). C'est utile. Mais pour rendre la prédiction réellement testable, il manque deux éléments :

- **Données pré-existantes sur la combinaison.** Y a-t-il une publication précédente qui ait testé fostamatinib + p38 inhibitor (ou entospletinib + losmapimod) en *xénogreffe DLBCL* ou *lignée TMD8/OCI-Ly10* ? Si oui, citer ; si non, dire explicitement que la prédiction est *de novo* sans précédent. La phrase actuelle "We have no comparable model evidence for GCB-DLBCL" couvre la GCB mais pas l'absence de précédent général.
- **Quel endpoint préclinique ?** Réduction de la viabilité cellulaire à concentration physiologique, ou taille de tumeur en xénogreffe ? Le manuscrit dit "evaluated in BCR-driven xenograft models" sans préciser. Une phrase plus opérationnelle ("a 7-day proliferation assay on TMD8 cells with fostamatinib + losmapimod at IC₅₀ of each compound serait un design plausible") rendrait la prédiction directement appropriable par un drug developer.

### 3.2 Le rôle de TNFSF13B (APRIL) reste un trou

L'auteur mentionne en Section 3.8 (ASSESS) que TNFSF13B reste à 0 dans tous les attracteurs et l'attribue à une source paracrine non-modélisée. C'est correct mais BAFF/APRIL est le *driver lymphomagénique le plus consensuellement reconnu* en SjD (Quartuccio 2014, et cohorte ASSESS elle-même). La prédiction SYK + p38 / PKR aborde la branche BCR-driven du modèle ; elle n'aborde pas la branche BAFF/APRIL → TACI/BCMA → NFkB → AP1, qui pourrait être indépendamment lymphomagénique.

**Demande :** Section 4.4 doit explicitement reconnaître que la prédiction couvre *une* dimension du driver lymphomagénique (BCR-AP1) mais laisse intacte la dimension BAFF/APRIL — non par choix mais par contrainte structurelle du modèle. Une phrase suffit.

### 3.3 Disparité entre les trois JAK inhibiteurs — distinction clinique

La Table 5 traite filgotinib, baricitinib et tofacitinib comme équivalents ("Insufficient (Naive)"). Cliniquement, les trois molécules ont des profils différents :

- **Filgotinib** (JAK1 préférentiel) : MOSAIC Phase 2 négatif (Bowman 2023).
- **Baricitinib** (JAK1/2) : pas d'essai randomisé en SjD ; quelques cas-séries off-label avec amélioration ESSDAI.
- **Tofacitinib** (pan-JAK) : essai BReakThrough cancellé pour raisons opérationnelles ; études observationnelles mitigées.

Le manuscrit pourrait distinguer dans Table 5 ou Section 3.7 le statut clinique réel de chaque molécule plutôt que de les regrouper. C'est mineur mais évite une simplification trompeuse.

### 3.4 Trap-space cyclique sous IFN-stim — interprétation clinique

La Section 4.2 attribue la perte de point fixe à un feedback STAT-SOCS-USP18 plausible. C'est défendable computationnellement. Cliniquement, néanmoins :

- Les patients SjD avec signature IFN-high atteignent un état de chronicité (mois à années) qui ressemble plus à un point fixe stable qu'à une oscillation au sens strict. Les ARNm STAT1 / SOCS3 / USP18 sont effectivement variables d'un échantillon à l'autre, mais le *pattern populationnel* est stable.
- L'oscillation `*` du modèle pourrait donc refléter la *variabilité inter-temporelle* (et inter-cellulaire) plutôt qu'une oscillation au sens dynamique. Cette distinction mérite d'être faite.

**Demande :** une demi-phrase Section 4.2 distinguant "oscillation au sens dynamique" (single cell, real time) vs "envelope de variabilité" (population, snapshots). Le clinicien lecteur ne lit pas de la même façon ces deux interprétations.

### 3.5 Sous-groupes moléculaires de Soret 2021

Les patients SjD ne sont pas homogènes : Soret et al. (2021) ont identifié 4 clusters moléculaires (C1 inactif, C2 IFN-high, C3 inflammatoire B-cell, C4 lymphoid). Le manuscrit ne mentionne pas cette stratification, alors que les cohortes PRECISESADS et UKPSSR utilisées sont précisément celles sur lesquelles ces clusters ont été établis. Le modèle pourrait potentiellement matcher *préférentiellement* certains clusters et pas d'autres.

**Demande optionnelle :** mentionner Soret 2021 en Section 3.3 ou 4.7 et discuter (sans nécessairement re-analyser) si le model match avec PRECISESADS reflète davantage le cluster IFN-high (C2) que les autres. Une phrase suffit.

### 3.6 Glandes salivaires et la limite tissulaire

GSE23117 est correctement classé comme "insufficiently powered" (Section 3.9), et la Section 4.7 reconnaît la cell-type agnosticité. Pour le clinicien, néanmoins, la glande salivaire est *l'organe* atteint en SjD ; un modèle qui ne s'y applique pas a une portée limitée.

**Demande :** Section 4.7 ou 4.9 (What the model can and cannot predict) doit dire explicitement : "the model is calibrated on the blood-derived transcriptomic signal of SjD; it does not, in its current form, predict salivary-gland-specific therapeutic responses". Cette phrase clarifie ce que le clinicien peut attendre du framework.

---

## 4. Points secondaires

### 4.1 Anifrolumab — interprétation

La Section 3.7 reporte que l'anifrolumab simulé réduit les ISGs (8 → 3) mais n'affecte pas les phénotypes maladie. Cliniquement c'est cohérent avec l'efficacité Phase 2 modérée. Mais attention : le résultat "phenotypes unchanged" est une conséquence du fait que les phénotypes en IFN-stim sont alimentés par d'autres voies (BCR, NFkB, MAPK) qui restent intactes. Le modèle suggère donc que **l'anti-IFNAR seul ne peut pas suffire en SjD multifactorielle**, ce qui est une prédiction utile et concordante. Mettre cette phrase explicitement plutôt que laisser le lecteur l'inférer.

### 4.2 ESSDAI et endpoint SjD

Le manuscrit cite ESSDAI à plusieurs reprises sans définir ce qu'est l'EULAR Sjögren's Syndrome Disease Activity Index. Pour un lecteur de *npj Syst Biol Appl* ce n'est pas évident. Une note en bas de page lors de la première mention (Bowman 2023, MOSAIC) suffirait.

### 4.3 Risk lymphomateux

Le manuscrit aborde la lymphomagenèse SjD via la Section 4.4 (SYK + p38 en BCR-stim) mais ne mentionne jamais le risque relatif (× 15-20 pour DLBCL, × 1000 pour MALT) qui motive cette piste. Une phrase en introduction (Section 1) renforcerait la pertinence clinique du focus DLBCL.

---

## 5. Recommandation

**Accept after minor revisions.** Les points 3.1 (testabilité concrète SYK + p38), 3.2 (BAFF/APRIL non-couvert), 3.3 (différentier les JAK inhibiteurs), 3.4 (oscillation vs envelope), 3.5 (clusters Soret), 3.6 (limite tissulaire) sont tous des ajustements éditoriaux de quelques heures à une demi-journée chacun.

Le manuscrit est, dans sa version actuelle, à un niveau de prudence et de transparence rarement atteint en biologie computationnelle appliquée à la rhumatologie. Je le recommande à *npj Systems Biology and Applications*.
