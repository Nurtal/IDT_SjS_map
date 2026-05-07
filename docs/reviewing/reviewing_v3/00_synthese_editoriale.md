# Synthèse éditoriale — Évaluation par les pairs

**Manuscrit :** *Boolean Attractor Analysis of the Sjögren's Disease Map Identifies AP1/p38 MAPK as a Candidate Convergent Control Module Under IFN Stimulation* (Foulquier, 2026)
**Journal cible :** *npj Systems Biology and Applications*
**Date de synthèse :** 2026-05-07
**Statut suggéré :** **Accept after minor revisions** (consensus convergent)

---

## 1. Contexte de la relecture

Cette synthèse rassemble les retours de quatre relecteurs aux profils complémentaires. Chaque relecteur a évalué le manuscrit en aveugle, sans accès aux versions antérieures éventuelles ni aux échanges éditoriaux préalables.

| # | Relecteur | Profil | Recommandation |
|---|---|---|---|
| 1 | Pr. L. — Modélisation booléenne | Sémantique MP, ASP, scalabilité, cross-validation sémantique | **Accept after minor revisions** |
| 2 | Pr. M. — Immuno-rhumatologue, expert SjD | Phénotypes cliniques, lymphomagenèse SjD, essais | **Accept after minor revisions** |
| 3 | Dr. T. — Bioinformatique transcriptomique | DEG, mapping, statistique, validation externe | **Accept after minor revisions** |
| 4 | Dr. K. — Pharmacologie / drug discovery | Cibles, ADMET, prédiction translationnelle | **Accept after minor revisions** |

Chaque rapport individuel est dans `docs/reviewing/reviewing_v3/0{1..4}_*.md`.

**Verdict consensuel : Accept after minor revisions.**

---

## 2. Avis global

Le manuscrit présente une analyse d'attracteurs booléens du SjD Map (Silva-Saffar 2026) qui se distingue par trois qualités combinées rarement réunies dans cette littérature :

1. **Rigueur méthodologique** : pipeline reproductible (Snakemake, Zenodo, Git tags), null model permutation 10 000 itérations, AUROC cross-attracteur, baselines triviaux, bootstrap CI, enrichment KEGG/Reactome avec correction Benjamini-Hochberg, audit topologique du module candidat.
2. **Honnêteté scientifique** : reconnaissance explicite (Section 4.6) que 25/39 cibles cliniques sont structurellement non-modélisables ; rétractation honnête (Section 3.5) d'une hypothèse plausible (JAK + p38) qui se révèle non-synergique au test ; "*candidate* convergent control module" plutôt que "central hub" (Section 3.4) ; section dédiée à *what the model is not* (Section 4.9).
3. **Connexion translationnelle** : Section 4.4 *Translational feasibility* (modèles TMD8/OCI-Ly10/NOD.B10.H2b, compounds disponibles, distinction ABC vs GCB DLBCL), distinction explicite des maturités translationnelles (p38 Phase 2 vs PKR research-only), références cliniques 2024-2026 (Bowman 2024 ianalumab Phase 3, telitacicept approbation Chine 2025).

Les corrections demandées par les quatre relecteurs sont **toutes mineures** : ajustements tabulaires (colonnes p_BH, n_down, coverage_%, up:down ratio), précisions textuelles (sélectivité SYK inhibiteurs, PKR comme orphelin de novo, combinaisons cliniques exclues du crible), et compléments éditoriaux (clusters Soret 2021, ESSDAI défini, modèle préclinique préférentiel IL-14α-Tg). Aucune ré-exécution de calcul lourd n'est demandée.

---

## 3. Convergences inter-relecteurs

| # | Point | Soulevé par |
|---|---|---|
| C1 | Statistique : reporter explicitement les p_BH dans Table 2 et le ratio up:down par cohorte | R3 |
| C2 | Stable motifs / pystablemotifs : préciser les paramètres testés et discuter le partitionnement modulaire (sans exiger le calcul) | R1 |
| C3 | SYK + p38 : préciser la sélectivité modérée des SYK inhibiteurs cliniques et la dimension polypharmacologique de la combinaison | R4 |
| C4 | PKR : reconnaître plus explicitement que la translation requiert un développement de novo et n'est pas du repositioning au sens strict | R4, R2 |
| C5 | Dimension BAFF/APRIL non-couverte par la prédiction lymphomagénique : expliciter en Section 4.4 | R2 |
| C6 | Naive condition (tous inputs = 0) : documenter quels nœuds restent à 1 dans Naive FP1 et d'où provient cette activité | R1 |
| C7 | Trap-space cyclique IFN-stim : distinguer "oscillation au sens dynamique" vs "envelope de variabilité populationnelle" | R2 |

Ces sept points ne demandent ni nouveau calcul ni nouvelle analyse — ils sont éditoriaux et tabulaires.

---

## 4. Points individuels par relecteur (résumé)

**R1 — Modélisation booléenne :**
- 3.1 Paramètres pystablemotifs essayés à documenter
- 3.2 Coût d'un crible exhaustif (~3 000 paires) à mentionner
- 3.3 Documentation des nœuds à 1 dans Naive FP1
- 3.4 Cross-validation MP / async optionnellement étendue au module AP1/p38
- 3.5 Invariants du trap-space IFN-stim (SI)

**R2 — Immuno-clinicien :**
- 3.1 Endpoint préclinique opérationnel pour SYK + p38 (TMD8 7-day proliferation, etc.)
- 3.2 BAFF/APRIL non-couvert dans la prédiction lymphomagénique
- 3.3 Distinction des trois JAK inhibiteurs
- 3.4 Oscillation vs envelope (Section 4.2)
- 3.5 Clusters Soret 2021
- 3.6 Limite tissulaire (blood vs salivary gland)

**R3 — Bioinfo transcriptomique :**
- 2.1 Ratio up:down par cohorte dans Table 2
- 2.2 p_BH comme colonne + correction multi-test pour le crible combinatoire
- 2.3 n_down explicite dans Table 3
- 2.4 PPV élevé partiellement attribuable au déséquilibre de classes
- 2.5 IC bootstrap pour 5 cohortes (pas seulement 2)
- 2.6 Cohorte non-IFN comme contrôle externe (optionnel, ex. RA)
- 2.7 SI table enrichment top-5 voies par attracteur
- 2.8 Colonne coverage_% dans Table 2

**R4 — Pharmaco / drug discovery :**
- 3.1 Sélectivité modérée des SYK inhibiteurs cliniques
- 3.2 PKR comme orphelin therapeutic target nécessitant un développement de novo
- 3.3 Combinaisons cliniquement attractives non-testables (anti-IFN + anti-CD40, anti-BAFF + JAK)
- 3.4 SI ADMET optionnel pour les 3 prédictions actionnables
- 3.5 Modèle préclinique SjD préférentiel : IL-14α-Tg pour la dimension lymphomagénique

---

## 5. Forces qui justifient l'acceptation

- **Reproductibilité exemplaire** : Snakemake, MIT, tag Git `model-v2.0`, archive Zenodo, `make all` testé indépendamment par R1 et R3.
- **Statistique restaurée et solide** : null model 10 000 perm + AUROC + baselines triviaux + bootstrap CI + enrichment hypergéométrique BH-corrigé. La combinaison est rare dans la littérature de modélisation booléenne.
- **Audit topologique honnête** : Table 4 + Section 3.4 re-cadrent le module AP1/p38 comme "candidate convergent control" plutôt que "hub central" — argumentation précise.
- **Cross-validation MP / asynchrone** sur sous-réseau IFN-I (43/44 nœuds concordants) : adresse une critique méthodologique potentielle de la sémantique MP.
- **Émergence d'une prédiction translationnelle nouvelle** (SYK + p38 / PKR en BCR-stim pour SjD-DLBCL) qui adresse une question clinique avec un unmet need réel (lymphomagenèse SjD-associée).
- **Section 4.4 Translational feasibility** : compound availability, modèles précliniques, compatibilité ABC vs GCB DLBCL — précisément le niveau de détail attendu par la communauté drug-discovery.
- **Honnêteté sur les non-prédictions** : 9/12 drugs not modellable, 25/39 cibles absentes, JAK + p38 non synergique, GSE23117 insufficiently powered, ASSESS coverage-limited. Aucune de ces auto-critiques n'est éludée.
- **Tests de non-régression** (3 tests pytest mentionnés) : couverture des invariants critiques (compte d'attracteurs, ISG activability, p-value range cohortes blood).
- **Références cliniques à jour** (Bowman 2024 ianalumab Phase 3, telitacicept approbation Chine 2025).

---

## 6. Risques résiduels et points d'attention pour l'éditeur

| # | Risque | Évaluation |
|---|---|---|
| Q1 | La signature IFN-stim est-elle "fabriquée" par l'encodage HDAC3 = KPNB1 = 1 ? | **Non** — le différentiel d'enrichment vs HDAC3 = 0 (Section 3.3) montre que JAK-STAT était déjà enrichi sans le fix ; les voies effectrices (IFN-α/β, IFN-γ) sont les seules ajoutées par le fix. La cross-validation MP / async (Section 3.6) confirme que la dynamique n'est pas un artefact MP. |
| Q2 | Le module AP1/p38 est-il un artefact topologique du graphe ? | **Partiellement** — le manuscrit le reconnaît explicitement (Section 3.4 + Section 4.1). La conclusion est tempérée à "candidate convergent control" et la fragilité topologique est documentée. C'est le bon niveau de claim. |
| Q3 | La prédiction PKR (EIF2AK2) est-elle réellement translationnelle ? | **Non au sens du repositioning** — pas de compound clinique disponible. Le manuscrit reconnaît cette asymétrie p38 vs PKR mais R4 demande une formulation encore plus explicite (PKR = orphan target, requires de novo development). |
| Q4 | La non-couverture de BAFF/APRIL fragilise-t-elle la prédiction SjD-DLBCL ? | **Oui partiellement** — la lymphomagenèse SjD a deux drivers principaux (BCR-driven et BAFF/APRIL-driven). Le modèle adresse seulement le premier. R2 demande une reconnaissance explicite. |
| Q5 | Le manuscrit a-t-il survécu aux tests statistiques rigoureux ? | **Oui** — null model significatif sur 3 cohortes blood indépendantes, AUROC > 0.5 sur 4/5 cohortes, baselines triviaux battus de 19-35 pp en balanced accuracy, BH-corrigé positif sur 2-3/3 cohortes blood IFN-stim. Le signal statistique est défendable. |

Aucun de ces risques n'est rédhibitoire ; tous sont adressés (parfois implicitement) dans le manuscrit ou peuvent l'être par les corrections mineures demandées.

---

## 7. Recommandation éditoriale

**Accept after minor revisions.** L'unanimité des quatre relecteurs sur cette recommandation reflète un consensus sur la qualité et la maturité du manuscrit. Les demandes individuelles totalisent environ **2-3 jours de révision** (additions tabulaires, précisions textuelles, paragraphes ciblés ; aucune ré-exécution lourde de pipeline).

Le manuscrit est, dans sa version actuelle, à un niveau de qualité que *npj Systems Biology and Applications* peut valoriser sans réserve : il combine rigueur méthodologique, honnêteté scientifique, et utilité translationnelle dans un même travail. La transparence sur les limites structurelles du SjD Map (25/39 cibles absentes) ouvre un agenda de recherche pour les futures extensions du framework et de la map elle-même.

**Délai estimé pour la version révisée : 3-5 jours.**

---

*Synthèse rédigée à partir des rapports individuels des relecteurs 1-4. En cas de désaccord avec un point précis, voir le rapport détaillé correspondant.*
