# Rapport de relecture — Modélisation booléenne (round 2)

**Manuscrit :** *Boolean Attractor Analysis of the Sjögren's Disease Map Identifies AP1/p38 MAPK as a Candidate Convergent Control Module Under IFN Stimulation* (Foulquier, v2)
**Relecteur :** Pr. L. — Modélisation booléenne, sémantique MP, contrôle de réseaux
**Date :** 2026-05-07
**Recommandation :** **Minor revision** (sur les 7 recommandations R1.x du round 1, 5 sont entièrement traitées, 1 partiellement, 1 reste documentée comme limite — l'auteur a choisi la transparence plutôt que le contournement, ce qui est défendable)

---

## 1. Avis global

Le manuscrit v2 répond de manière substantielle aux critiques méthodologiques formulées au round 1. La correction du modèle (HDAC3 = 1, KPNB1 = 1) est minimale, auditée (`models/sbmlqual/v2/changes.csv`), et biologiquement défendue ; la conséquence — réactivation de la cascade ISGF3 → ISGs canoniques sous stimulation IFN — est un résultat concret et vérifiable. Le crible combinatoire ciblé adresse directement R1.3, et l'audit topologique (R1.7) re-cadre honnêtement le module AP1/p38 comme un *bottleneck convergent* plutôt qu'un hub. La déduplication de sanitisation est désormais auditée à zéro perte (R1.5), ce qui clôt cette interrogation.

L'auteur conserve cependant **deux limites méthodologiques importantes**, l'une documentée (R1.1, stable motifs intractables sur 508 nœuds) et l'autre non traitée (R1.4, comparaison MP vs asynchrone). Ces deux trous laissent ouverte la question : la sémantique MP sous-approxime-t-elle ou sur-approxime-t-elle des comportements pertinents pour la conclusion thérapeutique ? Sur un manuscrit qui propose des cibles de combinaison (SYK + p38 / PKR), cette question n'est pas anodine.

L'introduction d'une condition IFN-stim qui ne possède **aucun point fixe** — uniquement un trap space cyclique — pose un problème conceptuel qui n'est pas suffisamment discuté (voir §3.5).

---

## 2. Points traités au round 2 — évaluation détaillée

| Reco | Statut | Évaluation |
|---|---|---|
| R1.1 — Stable motifs / MIS | Documenté comme intractable (Section 4.7, `stable_motifs_status.md`) | Acceptable mais perfectible — voir §4 |
| R1.2 — Inputs biologiquement plausibles | HDAC3 = 1, KPNB1 = 1 (Section 2.3) | ✅ Correct, justifié, auditable |
| R1.3 — Crible combinatoire | 91 paires × 3 conditions (Section 3.5) | ✅ Excellent — falsification explicite du JAK + p38 |
| R1.4 — Comparaison MP vs asynchrone | **Non traité** (Section 4.7 mentionne "future work") | ❌ Reste ouvert — voir §3 |
| R1.5 — Audit déduplication sanitisation | 0 collisions, 0 règles perdues (`sanitize_collisions.csv`) | ✅ Définitif |
| R1.6 — Tests de non-régression | 3 tests pytest (`tests/`) | ✅ Couvre les invariants critiques |
| R1.7 — Audit topologique AP1/p38 | Centralités + chemins disjoints (Section 3.4, `audit_ap1_p38.md`) | ✅ Excellent ; conclusion honnête |

---

## 3. Points qui restent insuffisamment traités

### 3.1 Comparaison de sémantiques (R1.4 non traité)

L'auteur reconnaît en Section 4.7 que la comparaison MP vs asynchrone classique (BoolNet, GINsim) n'a pas été menée. **Ce point est important pour la conclusion centrale** parce que :

- La sémantique MP (Paulevé 2020) sous-approxime certains attracteurs cycliques *ne pouvant pas* être atteints sous asynchrone classique.
- Les six hits monogéniques d'AP1/p38 reposent sur la disparition de l'attracteur sous MP — il faudrait vérifier qu'ils restent éliminateurs sous asynchrone (où le bassin de l'attracteur peut être plus restreint).
- Le manuscrit présente un argument élégant : "MP donne une borne supérieure des MIS, donc nos hits sont nécessairement candidats". Mais cette borne supérieure peut contenir des faux positifs (hits MP qui ne sont pas hits asynchrones).

**Demande minimale acceptable :** au moins une exécution BoolNet ou GINsim sur un sous-réseau (B-cell ou IFN module), reportant la concordance des attracteurs et des hits. Ne pas demander l'exécution sur le réseau entier (compatibilité Java/R, charge de mise en place).

### 3.2 IFN-stim sans point fixe : conséquence inquiétante de la correction v2

C'est mon point le plus important pour cette révision. Sous v1, la condition IFN-stim avait 2 FPs ; sous v2, elle a **0 FP et un trap space cyclique unique** avec 17 ISGs à `*` (oscillants). Le manuscrit traite cette transformation comme un succès (Section 3.2, "17 canonical ISGs are activable"), mais :

1. **Biologiquement**, les cellules immunitaires stimulées par IFN atteignent un *état stable d'expression ISG*, pas une oscillation. La perte de point fixe sous v2 est donc *contre-intuitive*.
2. **Méthodologiquement**, la perte de point fixe complique tous les seuils : la définition "≥ 6 phénotypes pathologiques actifs" ne peut plus être appliquée sans la convention `* → activable`. Cette convention est défendable mais introduit une asymétrie inflationniste : tout phénotype atteignable dans une trajectoire compte comme actif, ce qui sur-estime potentiellement la concordance avec les DEGs up.
3. **Il faut investiguer** la cause : l'oscillation provient probablement d'un feedback négatif (NFKBIA, TNFAIP3, SOCS, PPP2R1A) qui, libéré par STAT1 = 1 constant, crée une boucle. L'identification du sous-réseau oscillant est faisable en regardant les nœuds à `*` dans le trap space.

**Demande :** Section 3.2 doit (a) mentionner la disparition du point fixe IFN-stim comme un changement de structure dynamique non-trivial, (b) lister les nœuds à `*` du trap space (au moins par classe : feedback inhibitors, ISG, MAPK), (c) discuter si l'oscillation est biologiquement plausible (par exemple : oscillation des SOCS feedback) ou méthodologiquement artefactuelle.

Sans cette discussion, le résultat "v2 déverrouille les ISGs" cache un changement de régime dynamique qui pourrait fragiliser les conclusions ultérieures (Sections 3.3, 3.5).

### 3.3 Significativité statistique du null model — détails techniques

Le null model permute la *direction* des DEG en gardant la cardinalité. C'est le bon test, mais deux raffinements seraient utiles :

- **Bootstrap des paires (gene, node)** : la permutation actuelle suppose que les n_pairs paires forment l'univers fixe. Or le mapping HGNC peut être perfectible — un bootstrap où on rééchantillonne les paires (avec remplacement) donnerait un intervalle de confiance sur la *Hamming observée*, ce qui complète bien le test sur la *null distribution*.
- **Correction multiple** : le manuscrit reporte 5 cohortes × 5 attracteurs = 25 tests. Avec α = 0.05, 1.25 tests devraient passer par chance pure. Les 3 cohortes blood significatives (p ≤ 0.014) survivent confortablement à un Bonferroni 25-tests (seuil 0.002 — UKPSSR p = 0.007 et GSE51092 p = 0.003 passent ; PRECISESADS p = 0.014 ne passe pas strictement). À expliciter en limitations ou via FDR Benjamini-Hochberg.

---

## 4. Points qui demeurent ambigus

### 4.1 Stable motifs intractables — quelle vraie blocking constraint ?

Le rapport `stable_motifs_status.md` indique un timeout > 180 s lors de l'étape *prime implicants*. Mais 180 s est bref ; dans la littérature (Klamt, Tournier), des réseaux de 500-1000 nœuds ont été traités avec quelques heures de calcul moyennant des paramètres de coupure (`max_simulate_size`, `max_in_degree`). L'auteur a-t-il essayé d'ajuster ces paramètres ? Le passage du paramètre `max_simulate_size=0` (cf. mon test rapide sur le code) coupe explicitement la simulation locale — ce qui peut être trop conservateur.

**Demande :** mentionner dans `stable_motifs_status.md` les paramètres exacts utilisés et discuter brièvement (1 paragraphe) pourquoi le découpage modulaire n'a pas été tenté. Ne pas exiger le calcul lui-même.

### 4.2 Le crible combinatoire est *targeted* (91 paires sur ~3000 possibles)

L'auteur justifie le ciblage par des critères pharmacologiques. C'est correct mais introduit un biais de sélection : on ne sait pas si parmi les ~2900 paires non testées, certaines seraient également synergiques en BCR (et certaines pourraient impliquer des nœuds non-cibles). Une version *exhaustive* du crible serait l'idéal mais peut-être tractable (chaque paire prend ~5 s mpbn ; 3000 × 5 s = 4 h).

**Demande :** soit (a) compléter avec un crible exhaustif paires (~4 h CPU), soit (b) justifier explicitement qu'une exploration exhaustive a été simulée et qu'aucune paire hors-ciblage n'aurait été manquée. (b) est difficile à défendre. (a) est faisable.

### 4.3 Convention `*` ↦ 1 pour le décompte de phénotypes

Le manuscrit utilise la convention "trap space coordinate `*` est traité comme activable (= 1)" pour le décompte de phénotypes (Section 2.4). C'est défendable pour la *discussion biologique* ("le phénotype est atteignable") mais c'est une *convention* qui peut sur-compter les phénotypes actifs. La convention symétrique (`*` = 0, "non garanti actif") donnerait potentiellement moins de phénotypes par attracteur.

**Demande :** ajouter une analyse de sensibilité dans le SI : refaire le décompte de phénotypes avec la convention `*` = 0 et reporter les différences. Si la conclusion (IFN-stim A1 a 9 phénotypes actifs) est insensible au choix, la robustesse est démontrée. Sinon, c'est un autre paramètre à discuter.

---

## 5. Points positifs à conserver

- **Audit topologique (Section 3.4 + Table 4)** : exemplaire. L'argument "betweenness 3× plus faible que le contrôle" couplé aux chemins nœud-disjoints donne une lecture nuancée correcte.
- **Falsification explicite du JAK + p38** : c'est rare et précieux qu'un manuscrit retracte explicitement une de ses propres prédictions. Garder cet esprit.
- **Tests de non-régression** : couvrent les invariants pertinents (compte d'attracteurs, ISGs activables, p-value cohortes blood). Bonne pratique d'ingénierie.
- **Tag Git `model-v2.0`** + `changes.csv` : reproductibilité parfaite.
- **Réorientation BCR/lymphome (SYK + p38/PKR)** : émergence d'une prédiction *nouvelle* qui n'était pas dans v1 — la révision majeure a produit un résultat scientifique additionnel, pas seulement une réponse aux relecteurs.

---

## 6. Recommandation

**Minor revision.** Le manuscrit v2 est nettement au niveau de publication ; les trois points demandés (3.1 BoolNet sub-réseau, 3.2 discussion oscillation IFN-stim, 3.3 correction multiple, 4.1 paramètres stable_motifs, 4.3 sensibilité convention `*`) sont tous traitables en quelques jours sans re-exécuter la totalité de la Phase 7.

Le point 4.2 (crible exhaustif) est de niveau "amélioration souhaitable", non bloquant.

**Estimation délai révision :** 1–2 semaines.
