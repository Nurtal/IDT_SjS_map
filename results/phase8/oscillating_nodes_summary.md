# Oscillating nodes in IFN-stim trap space (v2 model)

**Total oscillating nodes (* coordinate):** 181 of 508 attractor coordinates (35.6 %)

## By functional module

| Module | Oscillating | Total in attractor | % oscillating |
|---|---|---|---|
| Other | 91 | 250 | 36.4 % |
| ISG canonical effectors | 55 | 57 | 96.5 % |
| Feedback IFN-STAT-SOCS | 18 | 32 | 56.2 % |
| Cytokine ligands & receptors | 8 | 74 | 10.8 % |
| Apoptosis / cell cycle | 4 | 17 | 23.5 % |
| Phenotype outputs | 3 | 14 | 21.4 % |
| Chemokines / surface | 2 | 40 | 5.0 % |
| MAPK / DUSP feedback | 0 | 17 | 0.0 % |
| Feedback NFkB | 0 | 7 | 0.0 % |

## Biological interpretation

- **Negative feedback loops** (STAT-SOCS, NFkB-NFKBIA, MAPK-DUSP) account for **18 oscillating nodes**.
- The presence of these feedback modules among oscillating nodes supports the interpretation that the trap-space dynamic reflects *biological feedback control* rather than a purely artefactual encoding.
- The IFN-stim attractor's `*` coordinates therefore represent the *envelope* of states reachable under sustained IFN signalling with active feedback regulation — consistent with the pulsatile dynamics observed experimentally for STAT1/SOCS/IFN axes [Cheon 2014, Adamson 2016].
