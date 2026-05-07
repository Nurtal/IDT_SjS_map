# Stable motifs / minimum intervention sets — status

## Verdict

A complete stable-motif / minimum-intervention-set decomposition of the 508-node Boolean network was attempted with `pystablemotifs` (Rozum et al., 2021) but did not terminate within the project's compute budget. The bottleneck is the prime-implicant computation performed by the underlying BNetToPrime backend, which is exponential in the network size and sensitive to in-degree.

## Parameters tried

`pystablemotifs.format.import_primes` was invoked under several parameter settings; in each case BNetToPrime exceeded the 180-second per-call budget, and the in-process `Process` subprocess returned a timeout signal:

| Attempt | `max_simulate_size` | `max_in_degree` | Outcome |
|---|---|---|---|
| 1 | default (15) | default (∞) | Timeout > 180 s |
| 2 | 0 (no local simulation) | default | Timeout > 180 s |
| 3 | 20 | 10 | Timeout > 180 s |
| 4 | 10 | 5 | Timeout > 180 s |

The CaSQ-derived BNET has a heavy-tailed in-degree distribution (a few nodes with > 20 regulators), which is the principal driver of the prime-implicant blow-up. Restricting `max_in_degree` does not reduce the cost on the dominant nodes — it merely truncates the search and produces incomplete primes.

## Mitigation strategies

Three options were considered:

1. **Modular partitioning** (Klamt and Tournier, 2018; Naldi et al., 2017). The network would be partitioned into functional sub-modules (B-cell, T-cell, IFN-I, BCR, MAPK / AP1) by either (a) curated cut sets at boundary nodes or (b) modularity-based clustering of the regulatory graph. `pystablemotifs` would be applied to each sub-module and the resulting MIS recombined. **Estimated effort:** 1-2 days of methodological work plus careful validation that the recombination preserves the global stability conditions. **Status:** not implemented.
2. **Perturbation screen as a practical upper bound.** Every node that participates in a minimum intervention set must be a hit in the single-node perturbation screen; equivalently, every pair in a 2-node MIS must be hit by the combinatorial screen. The mono- and di-genic screens reported in the manuscript therefore provide an **upper bound** on the candidate intervention space. They do not certify that no asynchronous trajectory bypasses a perturbation, which is the property a stable-motif / MIS analysis would establish.
3. **Cross-validation against asynchronous semantics on a sub-network.** This is reported in the manuscript (Section 3.6, IFN-I sub-network, 43 / 44 node-state agreement between MP and classical asynchronous semantics) and partially substitutes for a global stable-motif analysis on the cascade most relevant to the IFN signature.

## Decision

The manuscript reports the perturbation and combinatorial screens as practical control analyses, with the explicit caveat that they give an *upper bound* on minimum intervention sets and that a full stable-motif decomposition is left for future methodological work. Modular partitioning is identified as the most promising path forward when computational budget permits.
