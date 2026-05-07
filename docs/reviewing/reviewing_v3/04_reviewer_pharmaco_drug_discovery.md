# Rapport de relecteur n° 4 — Pharmacologie / drug discovery

**Profil :** Pharmacologue des réseaux, drug repositioning, ADMET, expérience industrielle (Pfizer, Servier) sur cibles kinases en oncologie et inflammation.
**Statut :** Pair externe.
**Conflit d'intérêts :** Aucun déclaré.

---

## 1. Évaluation générale

Le manuscrit fait quelque chose que peu de papiers de modélisation booléenne osent : il *cadre honnêtement la portée prédictive* de son framework. La Section 3.7 catégorise les 12 médicaments simulés en *modellable / not modellable / predicted novel* et reconnaît que 9/12 ne sont pas modélisables sous l'encodage actuel. La Section 4.6 *Limitations of the SjD Map for SjD drug repurposing* enchaîne en quantifiant que 25/39 cibles cliniques (64 %) sont structurellement absentes ou input-only dans le BNET dérivé. C'est *exactement* le type d'auto-critique que la communauté drug-discovery attend des études computationnelles et qu'elle obtient rarement.

La Section 4.4 *Translational feasibility of SYK + p38 / PKR predictions* ajoute la couche concrète qui manque souvent : compound availability (fostamatinib approuvé ITP, entospletinib Phase 2 DLBCL, losmapimod Phase 2, doramapimod Phase 2 — vs C16 et imoxin précliniques only), modèles de validation (TMD8, OCI-Ly10 ABC-DLBCL ; NOD.B10.H2b SjD), précédents dans d'autres pathologies BCR-driven (Davis 2010 chronic active BCR signalling). C'est testable.

Mes recommandations sont **mineures**. **Accept after minor revisions.**

---

## 2. Points forts

- **Tableau 5 en 3 catégories** (Modellable / Not modellable / Predicted novel) avec colonne *Compound availability* : grande lisibilité pour un drug developer. Le fait de ne pas mettre p38 et PKR sur le même plan (Phase 2 disponibilité vs research tools only) est une honnêteté nécessaire.
- **Anifrolumab simulé via input flip** (Section 3.7) : malin. Forcer `IFNAR_complex = 0` reste dans le périmètre du modèle et donne une prédiction concrète (réduction ISG sans collapse phénotypique) qui s'aligne avec la Phase 2 modérée observée. Bonne réponse à la limitation "input nodes not modellable".
- **Telitacicept et ianalumab Phase 3** explicitement intégrés (Section 4.6) : la mention que telitacicept (TACI-Fc, BAFF + APRIL) a été approuvé en Chine en 2025 est précisément l'exemple qui illustre le coût clinique du blind spot du modèle. Cite-toi cet exemple.
- **JAK + p38 *non synergique*** (Section 4.3) : c'est un résultat négatif présenté en clair dans l'abstract et la conclusion, ce qui est rare. Le modèle "casse" une hypothèse plausible et cela renforce la crédibilité des hypothèses qu'il *soutient* (SYK + p38 / PKR en BCR-stim).
- **HCQ traité avec une note explicite** (Section 3.7) : "the model cannot speak to its efficacy because TLR7 and TLR9 are encoded as input nodes; this is a structural limitation of the SjD Map, not a clinical falsification". Précisément la phrase qu'il fallait écrire.

---

## 3. Points qui restent à clarifier

### 3.1 SYK + p38 — quelle stratégie de développement réaliste ?

La Section 4.4 cite fostamatinib + losmapimod comme combinaison candidate. Pharmacologiquement :

- **Fostamatinib** est un *prodrug* (R788) hydrolysé en R406, inhibiteur SYK avec sélectivité modérée (off-target sur Lyn, FLT3, JAK). Son utilisation en monothérapie en DLBCL a été décevante (STELLAR-DLBCL, Friedberg 2010). **Sa place comme partenaire en combinaison serait davantage justifiée par la sélectivité modérée que comme inhibiteur SYK strict.**
- **Losmapimod** a été abandonné en RA, COPD, post-MI et est aujourd'hui en repositionnement FSHD (myopathie). Il existe encore un compound supply mais le développement industriel actif est limité.
- **Entospletinib** (SYK plus sélectif) en combinaison avec un inhibiteur p38 serait pharmacologiquement plus propre, mais il n'a pas la même base de safety data que fostamatinib.

**Demande :** Section 4.4 doit reconnaître que la sélectivité des SYK inhibiteurs cliniques est *modérée* et que la combinaison SYK + p38 prédite par le modèle est en réalité une combinaison "kinase polypharmacologique + p38" — la prédiction reste valide mais la matérialisation en compound spécifique demande une discussion. Une phrase suffit.

### 3.2 PKR (EIF2AK2) — la prédiction la plus fragile

Le manuscrit mentionne C16 et imoxin comme inhibiteurs PKR. Pour être complet :

- **C16** (8H-indol-3-ylmethyl-azolidino-benzothiazol-7-one) est un compound research-only avec sélectivité modérée vs HRI/PERK/GCN2 (les autres EIF2 kinases). Pas de Phase 1 humaine en aucune indication.
- **Imoxin** (TAT-PKR-inhibiting peptide) est délivré en peptide membrane-permeable ; pas de pharmacocinétique compatible avec un développement systémique humain.
- **Aucun inhibiteur PKR sélectif n'a atteint la Phase 1** dans aucune indication. À ma connaissance, le programme le plus avancé était celui de Genentech/Roche dans les années 2010 sur les neurodegenerative disorders, abandonné.

Donc la prédiction "PKR inhibition as monotherapy in SjD" est essentiellement **non-développable à moyenne terme**, sauf si un industriel décide de développer un inhibiteur PKR sélectif *de novo*. Cela ne disqualifie pas la prédiction biologique, mais le manuscrit gagnerait à être encore plus explicite que la maturité translationnelle de PKR est *radicalement* différente de celle de p38.

**Demande :** Section 4.4 doit ajouter une phrase claire du type "translation of PKR inhibition to clinical SjD requires *de novo* compound development; no clinically advanced PKR inhibitor exists at the time of writing. The PKR prediction is therefore an *orphan therapeutic target* whose value is to motivate medicinal-chemistry investment, not direct repositioning."

### 3.3 Combinaisons — pourquoi seulement 91 paires ?

Le crible combinatoire (Section 2.11, 3.5) teste 91 paires sélectionnées (toutes les 2-combinations parmi 14 nœuds drug-target). L'auteur justifie pharmacologiquement. C'est correct mais le lecteur drug-discovery se demande : **les paires testées représentent-elles le bon univers ?** Notamment :

- Pas de **anti-IFN-α + anti-CD40** (potentiellement intéressant en SjD).
- Pas de **anti-BAFF + JAK** (combinaison déjà discutée cliniquement par certains auteurs).
- Pas de **anti-IFNAR + p38** (anti-IFN backbone + AP1 collapse).

Bien sûr, ces combinaisons sont en partie *non-modellable* puisqu'elles impliquent des inputs (BAFF, CD40, IFNAR, IFN-α). Le modèle ne peut pas les traiter dynamiquement. Mais pour la lecture clinique, mentionner explicitement que ces combinaisons cliniquement attractives ont été *exclues* du crible pour des raisons d'encodage est utile.

**Demande :** Section 2.11 ou 4.6 doit lister explicitement les combinaisons non-testées (au moins 3-5) qui auraient un intérêt clinique mais sortent du périmètre dynamique du modèle.

### 3.4 ADMET et toxicité — absent

Le manuscrit prédit p38 inhibition comme cible, mentionne (à juste titre) les échecs historiques en RA / COPD / post-MI (Section 4.5), mais ne discute pas le profil ADMET / hépatotoxique des compounds candidats. Pour une publication dans *npj Syst Biol Appl*, c'est probablement hors-scope strict, mais une demi-page récapitulant pour les 3 prédictions actionnables (p38, PKR, SYK + p38) le profil de sécurité connu serait précieux pour le lecteur drug-discovery.

**Demande optionnelle :** SI table récapitulant pour chaque prédiction (p38 inh, PKR inh, SYK + p38) :
- statut clinique (Phase, indication)
- profil de sécurité connu (hépatotox, cardiotox, ON-target effects)
- développeur historique
- accessibilité du compound (R&D supply, GMP availability)

### 3.5 Modèles précliniques SjD — quel modèle privilégier ?

La Section 4.4 cite NOD.B10.H2b, IL-14α-transgénique et Aire⁻/⁻ comme modèles précliniques SjD pertinents. Pour un développement de combinaison SYK + p38 en SjD-DLBCL, le choix entre ces modèles est non-trivial :

- **NOD.B10.H2b** : modèle classique, sialadenitis avec auto-anticorps SSA/SSB, mais le risque lymphomateux est faible (besoin de longue observation).
- **IL-14α-Tg** : développe un sialadenitis suivi par un B-cell lymphoma chez la souris âgée — modèle naturellement compatible avec l'évaluation SYK + p38 sur le risque lymphomateux. **Probablement le meilleur choix pour la prédiction principale.**
- **Aire⁻/⁻** : sialadenitis et thyroidite mais davantage axé sur le défaut de tolérance centrale.

**Demande :** Section 4.4 doit recommander un modèle préférentiel (probablement IL-14α-Tg) plutôt que de lister trois modèles à plat.

### 3.6 Repositionnement existant et brevets

Le manuscrit ne mentionne pas la situation propriété intellectuelle des compounds candidats. Pour un drug-developer :

- **Losmapimod** : brevet GSK initialement, repositionné par Fulcrum Therapeutics en FSHD. Statut royalty / licensing à clarifier pour repositionnement SjD.
- **Doramapimod** : brevet Boehringer-Ingelheim, abandon clinique RA. Compound disponible en research supply mais redéveloppement industriel improbable.
- **Fostamatinib** : approuvé (ITP) — supply commercial OK, mais l'utilisation en SjD nécessite un programme de développement spécifique.

**Demande optionnelle :** une note SI sur la disponibilité IP / compound supply pour les 3 prédictions actionnables. Une demi-page suffit.

---

## 4. Points secondaires

### 4.1 ABC vs GCB DLBCL

La Section 4.4 distingue ABC vs GCB DLBCL et argumente que la prédiction est probablement transférable au sous-type ABC (chronic active BCR). Bien. Pour compléter : SjD-DLBCL est *préférentiellement* ABC dans les séries publiées (Voulgarelis 2007, Ekström-Smedby 2008, Duret 2023), donc le ciblage ABC est justifié par les données. Citer cette concordance épidémiologique renforcerait l'argument.

### 4.2 Combinaisons triplets ?

Le crible s'arrête aux paires. Pour DLBCL en particulier, des combinaisons triplets (SYK + p38 + anti-CD20 ; SYK + p38 + BTK) sont cliniquement réalistes (R-CHOP backbone). Le manuscrit pourrait mentionner que l'extension aux triplets est un *next step* méthodologique. Pas une demande.

### 4.3 Coût opérationnel

Le manuscrit ne mentionne pas le coût (financier, temps) attendu pour une étude préclinique de combinaison SYK + p38 en SjD-DLBCL. Pour orienter un lecteur drug-developer décideur, une fourchette d'ordre de grandeur (e.g. "Approximate operational cost: in vitro screen TMD8/OCI-Ly10 ~$50k, in vivo IL-14α-Tg ~$300k") serait utile mais clairement hors-scope d'un papier *npj Syst Biol Appl*.

---

## 5. Recommandation

**Accept after minor revisions.** Les demandes (3.1 sélectivité SYK inhibiteurs, 3.2 PKR comme orphelin de novo, 3.3 combinaisons non-testées explicitées, 3.4 SI ADMET optionnel, 3.5 modèle préclinique préférentiel) sont des additions de prose ciblées. **Estimation délai révision : 3-5 jours.**

C'est un manuscrit qui rend le framework "Boolean attractor analysis of MIM" *utile* à un drug developer, pas seulement à un méthodologiste. C'est une qualité que je vois trop rarement dans la littérature de modélisation. Je le recommande avec enthousiasme à *npj Systems Biology and Applications*.
