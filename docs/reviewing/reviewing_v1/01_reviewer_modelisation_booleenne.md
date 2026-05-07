# Rapport de relecteur n° 1 — Modélisation booléenne et sémantiques exécutables

**Profil :** Chercheur en informatique théorique appliquée à la biologie ; co-développeur d'outils de calcul d'attracteurs sur grands réseaux logiques (sémantique Most Permissive, ASP/clingo).
**Statut :** Pair externe.
**Conflit d'intérêts :** Aucun déclaré.

---

## 1. Évaluation générale

Le manuscrit est techniquement correct dans le choix des outils. L'enchaînement *CellDesigner SBML L2v4 → CaSQ v1.3.3 → BNET → mpbn 4.3.2* est l'état de l'art pour la conversion de cartes MIM en réseaux booléens exécutables, et l'auteur a manifestement pris soin de figer les versions, le DOI Zenodo, et le commit. La sanitisation des noms (`sanitize_bnet.py`) avec remplacement par longueur décroissante et déduplication par formule est élégante et résout un piège classique de pyboolnet.

Cependant, **plusieurs choix méthodologiques limitent la portée des conclusions** et m'amènent à recommander des révisions majeures avant publication.

---

## 2. Points méthodologiques préoccupants

### 2.1 Définition des conditions « biologiques » et propagation des constantes

Le pipeline fixe les 104 nœuds-entrées à 0 dans la condition « Naive », puis applique `propagate_constants()`. Cela revient à une *cellule sans aucun signal extracellulaire*, hypothèse qui n'a aucune réalité biologique : *in vivo*, les cellules immunitaires reçoivent un tonus basal de cytokines, BAFF/APRIL, complément, etc. Le fait que des phénotypes inflammatoires (B/T-cell activation, MHC-II, prolifération) soient actifs dans cette condition « tout-éteint » suggère que :

- Soit le réseau possède des sources internes auto-maintenues (rules `node = node` ou cycles auto-amplificateurs en l'absence de signal) ;
- Soit la conversion CaSQ a propagé des activations par défaut dans les transitions logiques.

Avant d'interpréter FP1 comme « état pathologique SjD », il faudrait :
1. Documenter quels nœuds sont à 1 dans FP1 *en l'absence d'inputs* — quelles sont les sources de cette activité ?
2. Tester un encodage où les inputs ont leur valeur biologique attendue (ligands cytokiniques bas-mais-présents) et vérifier la robustesse.
3. Ne pas appeler « Naive » une configuration qui n'a aucun analogue *in vivo* — le terme « inputs-zéro » ou « ground state » serait plus honnête.

### 2.2 Sémantique Most Permissive : sur-couverture potentielle

La sémantique MP (Paulevé et al., *Nat Commun* 2020) est exacte pour les *fixed points* mais sur-approximée pour les *trap spaces* et les attracteurs cycliques. Le manuscrit annonce « no cyclic attractors » dans toutes les conditions, ce qui est cohérent avec MP, mais une sémantique plus stricte (asynchrone classique, par exemple via boolean networks de Naldi/bioLQM) pourrait révéler des attracteurs cycliques absents en MP. Or la roadmap initiale (`README.md` §5.2) annonçait précisément *« Schémas de mise à jour évalués : synchrone, asynchrone, et stochastique (MaBoSS) »* — promesse non tenue dans le manuscrit final.

**Demande :** ajouter une comparaison synchrone/asynchrone (au moins via bioLQM stable states + BoolNet attractor()) et reporter les divergences. Sinon, justifier explicitement pourquoi MP suffit pour la conclusion « pas d'attracteur cyclique ».

### 2.3 Crible de perturbations : trop superficiel

Le crible mono-nœud (158 perturbations, 79 nœuds × 2 valeurs) ne constitue pas une analyse de contrôle complète. Notamment :

- **Pas de stable motifs** alors que la roadmap mentionne `pystablemotifs` (Rozum et al.) — c'est précisément l'outil pertinent pour identifier les *minimum intervention sets* sans dépendre d'une définition arbitraire de « disease attractor ».
- **Pas de perturbations combinatoires** (paires, triplets) alors que le manuscrit lui-même (§4.5) propose la combinaison JAK + p38 comme prédiction. Or cette prédiction n'est *pas testée* dans le crible : seuls les inhibiteurs sont simulés isolément (Phase 5, Tableau 4).
- **Définition ad hoc du « disease attractor »** : `len(active ∩ DISEASE_PHENOS) ≥ 6` (cf. `control_analysis.py:113`). Cette définition est circulaire — elle force l'identification du « bon » attracteur en supposant le profil pathologique connu. Un crible plus rigoureux comparerait toutes les paires d'attracteurs avant/après perturbation.

### 2.4 Le « module AP1/p38 » est-il un signal ou un artefact topologique ?

Six des sept perturbations qui éliminent FP1 ciblent des nœuds adjacents d'une chaîne linéaire :

```
EIF2AK2 → MAP2K6 → MAPK11_12_13_14 → FOS/JUN → AP1_complex
```

Quand un nœud n'a qu'une seule voie d'entrée vers un *bottleneck* aval, couper *n'importe lequel* de ses parents le coupe — c'est de la trivialité graphique. Pour départager artefact et signal mécaniste, il faut :

1. Calculer le score de centralité de chaque nœud du module (betweenness, in-component) et le comparer au reste du réseau.
2. Vérifier la présence de redondances : si l'on ajoute un autre activateur de p38 (par exemple via TLR/TAK1, voie biologiquement réelle mais possiblement absente du modèle), le module reste-t-il un point de passage obligé ?
3. Si la voie TAK1/MAP3K7 → p38 est absente du BNET (à vérifier), le « signal AP1/p38 » disparaîtrait dès que cette voie est ajoutée — c'est probablement le cas.

**Le manuscrit doit auditer la complétude topologique de la voie p38 dans le BNET avant de revendiquer la non-redondance du module.**

### 2.5 Sanitisation des noms : ambiguïté biologique

Le script `sanitize_bnet.py` collapse `PI(3,4,5)P3` en `PI_3_4_5_P3` et `STAT1/STAT2/IRF9` en `STAT1_STAT2_IRF9`. C'est nécessaire pour les solveurs, mais cela introduit deux risques :

- **Mapping gènes→nœuds en aval** (Phase 3) : la regex `(?<![A-Za-z0-9])STAT1(?![A-Za-z0-9])` matchera `STAT1_STAT2_IRF9` comme contenant STAT1 — correct, mais si un autre nœud est nommé `STAT1_inhibitor`, il matchera aussi. Pas un bug *stricto sensu*, mais source de bruit non quantifiée.
- Le manuscrit affirme « 0 collision » (§2.2) — vrai à la sortie de la sanitisation, mais pas après la déduplication par target (`if san_target not in deduped or len(san_formula) > len(deduped[san_target])`, ligne 117). Cette stratégie écrase silencieusement des règles. Combien de règles ont été écartées ? À documenter.

### 2.6 Reproductibilité et environnement

- ✅ Snakemake fourni.
- ✅ `pyproject.toml` et `environment.yml` présents.
- ⚠️ Pas de lockfile (`environment-lock.yml` ou `poetry.lock`) — la commande `make all` reproduira-t-elle les résultats dans 18 mois ? mpbn et clingo évoluent.
- ⚠️ Pas de tests unitaires (`tests/` est vide, cf. `ls tests/`). Pour un pipeline annoncé comme « pipeline reproductible » dans l'abstract, un minimum de tests de non-régression sur les attracteurs de la Phase 2 serait attendu.

---

## 3. Points positifs à souligner

- Conversion CaSQ correctement versionnée (v1.3.3, identique à celle des auteurs originaux).
- Vérification de la cohérence structurelle (`structural_check.py`) avant analyse dynamique — bonne pratique souvent omise.
- Documentation exhaustive (`journal.md`) du processus de découverte, y compris les écueils (timeout BNetToPrime → bascule vers mpbn).
- Choix de mpbn pour grands réseaux (508 nœuds) défendable et bien argumenté.

---

## 4. Recommandations spécifiques

| Priorité | Action |
|---|---|
| **R1.1** | Ajouter une analyse de stable motifs (pystablemotifs ou succession diagram) pour identifier les MIS sans définir le disease attractor par filtre arbitraire. |
| **R1.2** | Tester au moins une condition `Naive` avec inputs aux valeurs biologiquement plausibles (revue des 104 inputs, classement basal/inductible). |
| **R1.3** | Étendre le crible aux perturbations doubles, au moins sur les paires { JAK1, MAPK11-14 } et { BTK, AP1 } annoncées comme prédictions cliniques. |
| **R1.4** | Comparer mpbn à au moins une seconde sémantique (asynchrone bioLQM ou stochastique MaBoSS) pour valider l'absence d'attracteurs cycliques. |
| **R1.5** | Documenter combien de règles CaSQ ont été perdues lors de la déduplication par sanitisation, et l'impact biologique éventuel. |
| **R1.6** | Ajouter un test de non-régression sur la Phase 2 (`tests/test_phase2_attractors.py`). |
| **R1.7** | Audit topologique du module AP1/p38 : la voie est-elle redondante (TAK1, MAP3K7, MEKK1) dans le BNET ? Si non, indiquer que le résultat est conditionnel à la complétude du modèle SjD Map. |

---

## 5. Verdict du relecteur

**Recommandation : Major Revision.**

Le travail repose sur des fondations méthodologiques saines mais les conclusions translationnelles débordent ce que le crible mono-nœud permet d'établir. Les corrections demandées sont compatibles avec une révision majeure (et non un rejet) car le code et les données sont bien organisés ; l'auteur peut ré-exécuter le pipeline avec les modifications demandées en quelques semaines.

Si les recommandations R1.1, R1.3, R1.4 et R1.7 sont satisfaites de manière convaincante, je serais favorable à l'acceptation.
