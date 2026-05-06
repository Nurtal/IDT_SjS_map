# Synthèse éditoriale — Évaluation par les pairs

**Manuscrit :** *Boolean Attractor Analysis of the Sjögren's Disease Map Identifies AP1/p38 MAPK as a Central Control Module and Predicts Novel Therapeutic Targets* (Foulquier, 2026)
**Journal cible :** *npj Systems Biology and Applications*
**Date de synthèse :** 2026-05-06
**Statut suggéré :** **Major revision** (avis convergent des relecteurs)

---

## 1. Contexte de la relecture

Cette synthèse rassemble les retours simulés de quatre relecteurs aux profils complémentaires, chacun expert dans un pan distinct du champ couvert par le manuscrit :

| # | Relecteur | Profil | Focalisation |
|---|---|---|---|
| 1 | Pr. L. — Modélisation booléenne (Bordeaux/INRIA) | Sémantique MP, calcul d'attracteurs, scalabilité | Méthode de modélisation |
| 2 | Pr. M. — Immuno-rhumatologue, expert SjD | Phénotypes cliniques, pertinence biologique, essais | Crédibilité biologique |
| 3 | Dr. T. — Bioinformatique transcriptomique | DEG, mapping gènes→nœuds, statistique, validation externe | Robustesse statistique |
| 4 | Dr. K. — Pharmacologie des réseaux / drug discovery | Cibles thérapeutiques, prédiction médicaments, ADMET | Prédiction translationnelle |

Chaque rapport individuel est dans `docs/reviewing/0{1..4}_*.md`. Le présent fichier en propose la synthèse à l'attention de l'éditeur en chef.

---

## 2. Avis global

L'étude présente une qualité de mise en œuvre exemplaire (pipeline Snakemake, audit-trail complet, conversion CaSQ rigoureuse, code MIT) et adresse une question scientifique importante : la conversion d'une carte d'interactions statique en modèle exécutable. Elle est cohérente avec la vocation de *npj Syst Biol Appl* en tant que prolongement direct de Silva-Saffar et al. (2026).

Cependant, quatre limitations majeures convergent dans les retours :

1. **Validation transcriptomique faible** — les distances de Hamming (0.755–0.964) ne sont pas comparées à un null modèle ; l'ampleur du « match » revendiqué pour FP1 IFN-stimulé est insuffisante pour soutenir la conclusion d'un attracteur SjD biologiquement représentatif.
2. **Encodage de la voie IFN-I défaillant** — la dépendance imposée par CaSQ `STAT1 = HDAC3` (HDAC3 input fixé à 0) bloque la production de tous les ISGs (MX1, OAS1-3, ISG15, IRF7…), ce qui rend impossible la reproduction de la signature « IFN-high » qui est *la* signature la plus reconnue de la SjD. L'auteur le mentionne en limitations mais n'y remédie pas dans le modèle soumis.
3. **Robustesse de la prédiction « AP1/p38 MAPK »** — six des sept perturbations « efficaces » concernent des nœuds adjacents d'une seule chaîne linéaire (`EIF2AK2 → MAP2K6 → MAPK11-14 → FOS/JUN → AP1`). Cette concentration peut refléter une propriété topologique du graphe (point de passage obligé en aval, sans redondance), donc un artefact d'encodage CaSQ, plutôt qu'une véritable hiérarchie de contrôle biologique. Aucune analyse de stable motifs ni de minimum intervention set n'est fournie pour appuyer le résultat — alors qu'elle figurait pourtant dans la roadmap initiale.
4. **Concordance clinique surévaluée** — le « 8/10 concordance » avec les essais cliniques résume essentiellement le fait que le modèle prédit *aucun effet* pour des médicaments dont les essais ont échoué. Ce n'est pas une validation prospective. Aucun médicament n'a été simulé en condition où sa signature clinique est *positive* (par exemple, l'efficacité partielle de l'hydroxychloroquine, qualifiée à juste titre de discordante).

Aucun de ces points ne disqualifie le travail, mais leur combinaison fragilise les trois affirmations centrales de l'abstract : (i) attracteur SjD universel ; (ii) AP1/p38 comme module de contrôle non-redondant ; (iii) concordance clinique 8/10 et prédictions thérapeutiques nouvelles.

---

## 3. Décisions clés en suspens

| # | Question | Recommandation |
|---|---|---|
| Q1 | L'attracteur FP1 est-il biologiquement « SjD », ou simplement le seul état où les phénotypes-output peuvent prendre la valeur 1 quand les inputs sont à 0 ? | Tester un null modèle (rules randomisées préservant le degré) ; comparer FP1 à des attracteurs de cartes contrôles (e.g. Atlas of Inflammation Resolution, AlzPathway). |
| Q2 | La concentration des hits sur AP1/p38 est-elle un signal mécaniste ou un artefact topologique ? | Ajouter une analyse de stable motifs (pystablemotifs) et de minimum intervention sets ; comparer aux hubs structurels par centralité bivariée. |
| Q3 | Le blocage HDAC3/STAT1 doit-il être corrigé avant publication ? | Oui — proposer une variante du modèle avec HDAC3=1 par défaut et re-tourner toute la Phase 3. La signature IFN-high est trop centrale pour rester non-modélisable dans une étude sur SjD. |
| Q4 | La métrique Hamming est-elle adaptée pour un modèle booléen vs DEG continus ? | Compléter par AUROC sur le rang des nœuds, ou test d'enrichissement hypergéométrique au lieu d'une distance moyenne. |
| Q5 | Les 12 médicaments simulés et 158 perturbations mono-nœud constituent-ils un crible suffisant ? | Étendre aux perturbations doubles pour tester la prédiction de synergie JAK + p38 dont le manuscrit fait explicitement l'apologie. |

---

## 4. Recommandation éditoriale

**Major revision.** Le travail mérite publication après correction des points Q1–Q5. Ne pas rejeter : la qualité de l'ingénierie logicielle, la transparence des limites, et l'inscription dans la continuité directe d'un papier *npj* récent constituent une base solide. Mais en l'état, les conclusions translationnelles ne sont pas soutenues par les données présentées.

Les délais nécessaires aux corrections (re-tour des Phases 3–5 après correction HDAC3, ajout de stable motifs, null model statistique, perturbations combinatoires) sont estimés à 4–8 semaines.

---

## 5. Aspects positifs à conserver

Pour mémoire dans la lettre de réponse aux relecteurs, l'éditeur soulignera ces points forts qui *justifient* le passage en révision majeure (et non un rejet) :

- Reproductibilité exemplaire (Snakemake, MIT, CITATION.cff, Zenodo, journal.md).
- Audit topologique reproduisant exactement les valeurs publiées (412 nœuds / 692 arêtes).
- Honnêteté méthodologique : les trois limitations majeures (HDAC3, cell-type agnostique, HCQ discordance) sont nommées par l'auteur lui-même.
- Adoption de la sémantique MP (Paulevé, *Nat Commun* 2020), techniquement correcte et adaptée à la taille du réseau.
- Cadre conceptuel clair (5 hypothèses formulées explicitement, statut documenté).
- Croisement multi-cohortes (PRECISESADS, UKPSSR, GSE51092, ASSESS, GSE23117) — ambition qu'il faut récompenser même si l'exécution statistique est à renforcer.

---

*Synthèse rédigée à partir des rapports individuels des relecteurs 1–4. En cas de désaccord avec un point précis, voir le rapport détaillé correspondant.*
