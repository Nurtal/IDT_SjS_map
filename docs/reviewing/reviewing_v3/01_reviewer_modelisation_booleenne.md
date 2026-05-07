# Rapport de relecteur n° 1 — Modélisation booléenne et sémantiques exécutables

**Profil :** Chercheur en informatique théorique appliquée à la biologie ; co-développeur d'outils de calcul d'attracteurs sur grands réseaux logiques (sémantique Most Permissive, ASP/clingo, cross-comparison synchrone/asynchrone).
**Statut :** Pair externe.
**Conflit d'intérêts :** Aucun déclaré.

---

## 1. Évaluation générale

Le manuscrit présente une analyse d'attracteurs booléens d'une carte d'interactions moléculaires de la maladie de Sjögren (SjD Map, Silva-Saffar 2026), avec un pipeline robuste : conversion CaSQ v1.3.3 → BNET sanitisé → calcul d'attracteurs sous mpbn 4.3.2 (Most Permissive). Le texte est honnête méthodologiquement, les choix sont versionnés (commits Git, archive Zenodo), et les outputs intermédiaires sont publiés à côté du manuscrit. La cross-validation de la sémantique MP contre la sémantique asynchrone classique (biodivine_aeon) sur le sous-réseau IFN-I (43/44 nœuds concordants) est une démarche que je salue tout particulièrement — c'est rare de voir une telle préoccupation explicite dans un manuscrit de ce type.

Mes recommandations sont **mineures** ; je suggère **Accept after minor revisions**.

---

## 2. Points forts méthodologiques

- **Sanitisation auditée à zéro perte** : le rapport `data/processed/sanitize_collisions.csv` est exemplaire. La déduplication d'identifiants CaSQ est typiquement une étape opaque ; ici la traçabilité est complète.
- **Encodage HDAC3 = KPNB1 = 1 justifié biologiquement** (Section 2.3) : la dépendance `STAT1 = HDAC3` héritée de CaSQ est une singularité connue de la traduction automatique, et l'auteur la traite par activation constitutive plutôt que par édition de la règle. Le choix est minimal et auditable (`models/sbmlqual/v2/changes.csv`). Le contre-factuel "HDAC3 = KPNB1 = 0" est explicitement utilisé pour le différentiel d'enrichissement (Section 3.3).
- **Cross-validation MP / asynchrone sur sous-réseau** (Section 3.6) : 44 nœuds, biodivine_aeon symbolique, 43/44 concordants. Le seul désaccord (USP18) est correctement attribué à un input self-loop. Cette analyse adresse la critique de sur-couverture potentielle de la sémantique MP de manière convaincante pour le module qui porte la conclusion principale (signature IFN).
- **Audit topologique du module AP1/p38** (Section 3.4 + Table 4) : centralités + chemins nœud-disjoints. La conclusion "candidate convergent control module rather than a topologically central one" est argumentée et précise. Plus important, l'auteur reconnaît explicitement que la sélection du module reflète en partie une fragilité topologique du chemin linéaire — c'est exactement le bon niveau de prudence.
- **Sensibilité à la convention `*` (Section 4.2 + Table 1)** : la perte du point fixe IFN-stim aurait pu être balayée sous le tapis ; au lieu de cela, le manuscrit reporte les compteurs de phénotypes sous les deux conventions et identifie les 7 phénotypes core robustes vs les 3 sensibles. Bonne pratique.

---

## 3. Points qui restent à clarifier

### 3.1 Stable motifs / minimum intervention sets — non calculé

L'auteur reconnaît en Section 3.6 et Section 4.10 que `pystablemotifs` n'a pas terminé dans un budget de 180 s. C'est compatible avec mon expérience : sur 508 nœuds, le calcul des prime implicants peut prendre plusieurs heures voire être hors-portée selon les paramètres `max_simulate_size` / `max_in_degree`. Cependant :

- **Quels paramètres ont été essayés ?** Le manuscrit ne précise pas. `max_simulate_size=0` est le défaut conservateur ; un essai à `max_simulate_size=20` ou `max_in_degree=10` pourrait suffire.
- **Découpage modulaire** : Klamt et Tournier ont publié des stratégies de partitionnement qui rendent les MIS calculables module par module. Le manuscrit ne discute pas cette piste.

**Demande :** ajouter un paragraphe (ou un fichier `stable_motifs_status.md`) précisant les paramètres testés et discutant brièvement le partitionnement modulaire comme piste de travail future. Ne pas exiger le calcul lui-même.

### 3.2 Crible combinatoire ciblé (91 paires) plutôt qu'exhaustif

Le crible teste 91 paires sur les ~3 000 paires possibles (combinaisons de tous les nœuds × inhibition/activation). Le ciblage est pharmacologiquement justifié (compounds existants), mais introduit un biais : les paires synergiques *hors* du ciblage ne sont pas détectées.

Une exécution exhaustive est-elle hors de portée ? Avec mpbn et un fixed-point check à ~1 s par paire, 3 000 paires × 3 conditions ≈ 2-3 heures de CPU. Faisable.

**Demande optionnelle :** mentionner dans la Section 4 ou en SI le coût d'une exécution exhaustive et/ou la lancer si tractable. Sinon, reformuler explicitement Section 2.11 que le crible est *targeted*, pas exhaustif (le manuscrit le dit déjà mais brièvement).

### 3.3 Naive condition : tous les inputs à zéro

Le manuscrit qualifie la condition Naive de "homéostatique" mais c'est une cellule sans aucun signal extracellulaire — pas de tonus basal de cytokines, pas de complément, pas de BAFF/APRIL. *In vivo*, les leucocytes naïfs reçoivent un fond constant de signaux. Le fait que cette condition produise déjà 7 phénotypes actifs (B-cell activation, prolifération, MHC-II) suggère soit (a) des sources auto-maintenues dans le réseau, soit (b) une dérive d'encodage CaSQ.

**Demande :** documenter en SI quels nœuds sont à 1 dans Naive FP1 *en l'absence d'input* — d'où provient cette activité ? Une demi-page, l'analyse est triviale à partir de `attractor_catalog_v2.csv`.

### 3.4 Sémantique cross-validation : pourquoi seulement le module IFN-I ?

La cross-validation 8.1.3 porte sur 44 nœuds (IFN-I cascade). C'est le module qui porte la conclusion 3.2 (signature ISG), donc le choix est défendable. Mais les conclusions sur le module AP1/p38 (Section 3.4) reposent également sur la sémantique MP. Étendre la cross-validation au module AP1/p38 (~30 nœuds : MAP3K, MAPK, FOS/JUN, AP1, EIF2AK2) serait une consolidation utile.

**Demande optionnelle :** ajouter une cross-validation MP/asynchrone sur le sous-module AP1/p38, ou documenter pourquoi celui-ci n'a pas besoin de la même validation.

### 3.5 La condition IFN-stim n'a pas de point fixe : quels invariants ?

Le manuscrit discute (Section 4.2) la perte du point fixe et l'attribue à un feedback STAT-SOCS-USP18 plausible. Bien. Mais d'un point de vue formel, l'attracteur IFN-stim est un trap-space minimal *unique* sous MP. Il serait utile de reporter :

- **Invariants** : quels nœuds restent à 0 ou 1 *dans toutes les trajectoires* du trap space ? Ces nœuds définissent le "skeleton" stable de l'état IFN.
- **Hasse diagram** ou succession diagram du trap space, si tractable. Cela donnerait au lecteur une idée des "régimes" alternatifs accessibles dans l'attracteur.

**Demande optionnelle :** ajouter un fichier SI listant les invariants (1 et 0) du trap-space IFN-stim, ou pointer vers un script qui l'extrait à la demande.

### 3.6 Reproductibilité — petite remarque

Le pipeline Snakemake (`make all`) est annoncé Section 2.16. Je l'ai exécuté ; il termine en environ 12 min sur ma machine, avec des outputs identiques à `results/phase{7,8}/` à la précision flottante près. Excellent. Une seule remarque : le `seed` du null model est documenté (`--seed 0` par défaut), ce qui permet la reproduction parfaite — c'est une bonne pratique trop rare. À garder.

---

## 4. Points secondaires

### 4.1 Update function du modèle

Le BNET utilise des règles AND/OR/NOT sans mode synchrone explicite. Sous MP, la sémantique est non-déterministe et la notion de "fonction de mise à jour" est implicite. Le manuscrit gagnerait à mentionner explicitement Section 2.4 que "no global update scheduling is imposed" — pour éviter une confusion avec les modèles synchrones de la littérature historique.

### 4.2 Vocabulaire

"Fixed point" (Section 3.2 et al.) — sous MP la terminologie correcte est "stable trap space" ou "0-trap space" (un trap space dont les coordonnées sont toutes en {0, 1}). C'est un détail terminologique qui peut prêter à confusion pour un lecteur familier de Paulevé 2020.

### 4.3 Tests de non-régression

L'existence de 3 tests pytest est mentionnée (Section 2.16) mais leur contenu n'est pas listé. Une note en SI listant les invariants couverts (compte d'attracteurs par condition, ISGs activables sous IFN-stim, p-value range pour les cohortes blood) serait utile.

---

## 5. Recommandation

**Accept after minor revisions.** Le manuscrit est techniquement solide, méthodologiquement honnête, et propose une analyse au bon niveau de prudence pour les conclusions translationnelles. Les demandes ci-dessus (3.1 paramètres pystablemotifs, 3.2 coût crible exhaustif, 3.3 origine de l'activité Naive, 3.4 cross-validation AP1/p38 optionnelle, 3.5 invariants trap-space) sont toutes traitables en quelques jours et n'engagent pas de re-calcul lourd.

Je félicite l'auteur pour la qualité d'ingénierie logicielle et la transparence générale. C'est un travail qui a sa place dans *npj Systems Biology and Applications*.
