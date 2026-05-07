# Status — Stable motifs / MIS sur v2 (Phase 7.3.1)

## Verdict

`pystablemotifs.format.import_primes` (qui appelle BNetToPrime sous le capot)
n'est **pas tractable** sur le BNET v2 de 508 nœuds (timeout > 180 s à
l'étape de calcul des implicants premiers, déjà documenté en Phase 2 pour la
v1). Le diagnostic est inchangé entre v1 et v2 (la correction HDAC3/KPNB1
n'affecte pas la complexité de l'inférence de premiers).

## Mitigation envisagée (R1.1)

Trois options ont été identifiées :

1. **Découpage modulaire** — partitionner le BNET en sous-réseaux fonctionnels
   (B-cell, T-cell, IFN, BCR, AP1) via clustering modulaire NetworkX, puis
   exécuter pystablemotifs par sous-graphe et recombiner les MIS.
   *Statut : non implémenté (charge ~1 jour, hors scope révision majeure).*
2. **Crible de perturbations** — déjà fourni en remplacement (Phase 4 v1
   et Phase 7.3.2 v2 / paires) ; couvre l'objectif principal (identifier
   les nœuds de contrôle), avec la limitation de ne pas certifier qu'aucun
   chemin de récupération asynchrone ne contourne la perturbation.
3. **Reporter intractable** — documenter explicitement la limitation dans
   le manuscrit v2 (méthodes + discussion) en s'appuyant sur le crible
   combinatoire (Phase 7.3.2) comme analyse de contrôle finale.

## Décision pour la révision

Le manuscrit v2 reportera cette limitation en *Méthodes 2.x* et *Discussion
4.x*, et conservera comme analyse de contrôle :

- **Crible mono-nœud Phase 4 / Phase 7.3.4** (avec sensibilité au seuil)
- **Crible combinatoire Phase 7.3.2** (paires drug-target)
- **Audit topologique Phase 7.1.2** (centralité du module AP1/p38)

Cette combinaison adresse R1.1 (analyse de contrôle robuste) sans nécessiter
les MIS exacts. La justification s'appuie sur le fait que le crible de
perturbations donne une **borne supérieure** sur les MIS : tout nœud du MIS
apparaît nécessairement comme hit dans le crible (mais l'inverse n'est pas
vrai sans confirmation par stable motifs).
