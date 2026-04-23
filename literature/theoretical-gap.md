# Theoretical Gap and Contribution

## The gap in one paragraph

Contingency theory established 60 years ago that the optimal organizational structure depends on the environment. Subsequent empirical work (Bloom, Sadun & Van Reenen 2012; Brynjolfsson & McElheran 2016) has shown that IT and decentralization *interact*: firms with more information technology benefit more from flatter hierarchies. Computational work (Csaszar 2013; Lazer & Friedman 2007) has modeled how structural aggregation rules trade off exploration and exploitation on rugged landscapes. **What no paper has done** is: (a) *isolate information accessibility as a distinct moderator* rather than bundling it with IT investment, (b) *formalize the threshold τ\* at which horizontal overtakes vertical*, and (c) *derive τ\*'s dependence on task complexity*. This paper fills that gap.

---

## Why the gap persists

1. **Construct conflation.** Prior empirical work proxies "information environment" with IT spending. But IT spending mixes capex, software, data, cloud, training, and AI tools. "Information accessibility to the individual decision-maker" is a distinct sub-construct that has not been separately measured at scale.

2. **Threshold questions need computation.** Identifying τ\* requires sweeping parameter space with controls on everything else. Field data cannot do this; only simulation can.

3. **Conditional hypotheses are harder to publish.** Reviewers reward clean main effects. "Horizontal works, conditional on τ, interacted with K" is a harder sell than "horizontal works." But it is correct, and the boundary-condition literature in organization science now rewards such nuance (Busse, Kach & Wagner 2017 on boundary conditions in management research).

---

## Contribution map

| Field | Existing state | Our contribution |
|---|---|---|
| Contingency theory | Environment → structure fit; environment loosely operationalized | τ as explicit, measurable moderator; threshold τ\* quantified |
| Self-management literature | Case studies conclude "it depends" | Formal theory of what it depends on |
| Organizational simulation | Structure effects on exploration/exploitation | Three-way interaction (structure × τ × K) mapped; τ\*(K) curve derived |
| IT-productivity empirics | IT × decentralization interaction documented | Separates "information accessibility" from "IT infrastructure"; provides mechanism |
| Future-of-work prognostication | Qualitative claims that AI flattens organizations | Falsifiable conditions under which the claim holds |

---

## The specific claims our paper adds to the literature

1. **Primary claim**: There exists a threshold τ\* of information accessibility such that for τ < τ\*, vertical > horizontal in expected fitness-after-T; for τ > τ\*, the ordering reverses. (H3)
2. **Secondary claim**: τ\* is a decreasing function of task complexity K — the more complex the task, the *lower* the information-accessibility bar that horizontal needs to clear to beat vertical. (H4)
3. **Methodological claim**: "Information accessibility" and "IT investment" are distinguishable constructs; treating them interchangeably (as prior empirics often do) masks the moderation effect we document.
4. **Policy-adjacent claim**: Contemporary AI deployment is raising τ across all firms, meaning that, controlling for task complexity, the population of firms for which horizontal-wins is expanding. This is a *testable prediction*, not a prognostication.

---

## What could kill the contribution (pre-mortem)

We name the threats so reviewers cannot claim we missed them.

1. **Construct validity of τ.** If our empirical proxy (IT-per-employee, data-infrastructure index, AI-tool adoption) is indistinguishable from "IT investment," our separation is illusory. *Mitigation*: principal-component analysis of candidate proxies; show that our τ factor is distinct from a general-IT factor.

2. **External validity of the ABM.** NK landscapes are a stylization. Reviewers will ask "why this landscape, why these parameters?" *Mitigation*: robustness checks across landscape families (NK, NKC, rugged random); calibrate K to observed patent-citation roughness per industry (Fleming & Sorenson 2001).

3. **Endogeneity in the archival study.** Flat firms might have high τ because they chose to invest in information systems to support flatness. Reverse causality. *Mitigation*: natural-experiment identification — firms that flattened after exogenous events (mergers, CEO turnover, trade shocks à la Guadalupe-Wulf).

4. **Publication bias against conditional results.** *Mitigation*: pre-register predictions; frame the paper as "boundary condition" work, citing the methodological literature that specifically rewards this (Busse et al. 2017).

---

## Expected criticisms and responses

- *"This just restates Bloom-Sadun-Van Reenen."* No — they study IT × decentralization. We separate information *accessibility* from IT *infrastructure* and find that only the former drives the interaction. We also provide the mechanism via ABM, which they don't.
- *"Simulations prove nothing about the real world."* True for standalone simulations. Our ABM is **empirically grounded** (Davis, Eisenhardt & Bingham 2007): parameters calibrated from observable firm data; predictions cross-validated against archival patterns. Evidence strength comes from triangulation, not from any single component.
- *"Why not study real organizations directly?"* We do, in Phase 2. But only simulation can manipulate τ holding structure constant, which is required to identify τ\*. We use both methods because each covers the other's weakness.
