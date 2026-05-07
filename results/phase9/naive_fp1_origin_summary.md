# Origin of activity in the Naive fixed point


The Naive condition fixes every external input to 0; only HDAC3 
and KPNB1 are constitutively at 1 by construction (Section 2.3 of 
the manuscript). The fixed point FP1 nonetheless contains active 
nodes (state = 1). This document traces, for each active node, 
the source of its activation.

**Total active nodes in Naive FP1:** 45

## Classification by origin of activation

| Origin | Count | Definition |
|---|---|---|
| `constitutive_only` | 1 | depends only on HDAC3 and/or KPNB1 |
| `cascaded_from_active` | 22 | depends on other already-active nodes (downstream relay) |
| `constitutive+cascade` | 0 | mixed (HDAC3/KPNB1 + cascaded) |
| `self_loop_input` | 0 | self-regulatory input (rare in Naive — should be 0) |
| `constant` | 2 | rule is a Boolean constant |
| `mixed` | 20 | depends on inactive nodes; encoding artefact |

## Interpretation

The activity in Naive FP1 is propagated downstream from the 
constitutive activation of HDAC3 and KPNB1. The first nodes to 
switch on are those whose rules depend exclusively on HDAC3 / 
KPNB1 (e.g. STAT1 = HDAC3); these then cascade to downstream 
regulators that take their place in the active set. The Naive 
fixed point should therefore not be read as the model's view of 
a *rest* state but as a *baseline competence* state where the 
network is poised to amplify any extracellular signal through a 
transcription-factor backbone that is already chromatin- and 
transport-competent.

Per-node table with rule and origin classification: `results/phase9/naive_fp1_active_origin.csv`.