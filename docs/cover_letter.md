# Cover Letter — npj Systems Biology and Applications

**[Date]**

Dear Editors,

We submit for consideration the manuscript entitled:

**"Boolean Attractor Analysis of the Sjögren's Disease Map Identifies AP1/p38 MAPK as a Central Control Module and Predicts Novel Therapeutic Targets"**

This work represents a direct computational continuation of the Sjögren's Disease Map (SjD Map) published in this journal (Silva-Saffar et al., *npj Systems Biology and Applications*, 2026). The SjD Map provided a comprehensive static representation of Sjögren's disease (SjD) molecular interactions; our manuscript converts it into an **executable Boolean network** and performs the first systematic attractor and therapeutic target analysis.

**Key contributions:**

1. **First Boolean network of the full SjD signalome** (508 nodes) derived from the published SjD Map via CaSQ, with an open-source sanitization pipeline and a Snakemake workflow for complete reproducibility.

2. **Attractor landscape characterisation:** the network converges to two fixed points per condition (homeostatic, IFN-stimulated, BCR-stimulated), including a universal disease attractor (7 active phenotypes) that persists regardless of stimulation — providing a mechanistic explanation for the refractory nature of the disease.

3. **AP1/p38 MAPK as a non-redundant control module:** systematic perturbation screening of 158 interventions identifies a single, linear kinase cascade (EIF2AK2→MAP2K6→p38→AP1) as the minimal mechanistic bottleneck. Inhibition of any node in this chain eliminates the disease attractor.

4. **Clinical validation and novel predictions:** in silico simulation of 12 drugs achieves 8/10 concordance with published trial outcomes (JAK/BTK inhibitors insufficient; IFN-partial suppression by baricitinib/tofacitinib). Three novel targets — p38 MAPK (losmapimod/doramapimod), AP1, and PKR (EIF2AK2) — are predicted to be effective and have not been evaluated in SjD clinical trials.

5. **Cross-cohort validation:** transcriptomic concordance with PRECISESADS, UKPSSR, GSE51092, and the ASSESS lymphoma cohort confirms the biological relevance of the attractors.

**Fit with the journal:** This manuscript is a natural companion to the original SjD Map paper, extending a static map into a dynamic model and linking the computationally identified control targets to ongoing clinical trials. It will be of interest to readers working in autoimmune disease modelling, network medicine, and systems pharmacology.

The complete pipeline is freely available at [REPOSITORY_URL] under MIT licence, enabling other groups to extend the model (new stimulation conditions, combination perturbations, patient-specific networks).

We declare no competing interests. The manuscript has not been published elsewhere and is not under consideration at another journal.

We suggest the following potential reviewers:
- **Laurence Paulevé** (Univ. Bordeaux) — developer of mpbn and MP Boolean network semantics.
- **Andrei Zinovyev** (Institut Curie) — Boolean network modelling of cancer and immune diseases.
- **Christophe Naldi** (ENS Lyon) — bioLQM, Colomoto ecosystem.
- **Xavier Mariette** (Hôpital Bicêtre, AP-HP) — clinical expert in Sjögren's disease.

We look forward to your consideration.

Sincerely,

**Nathan Foulquier**
[Institution]
[Email] nathan.foulquier.pro@gmail.com
[ORCID]

---

*Manuscript statistics: ~5,500 words, 4 tables, 5 figures.*
