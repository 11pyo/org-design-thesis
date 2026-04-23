# Research Proposal (English)

> **[Repositioning + correction note — 2026-04-22]** This proposal originally aimed to test a τ*(K) boundary condition between vertical and horizontal structures. An initial robustness extension produced a spurious result ("hybrid dominates under volatility") caused by a simulation bug (the dynamic hybrid trajectory did not receive landscape shocks). After fixing the bug and re-running the experiment, the corrected finding is that **environmental volatility REVERSES the horizontal-organization advantage. Under any non-trivial volatility, vertical beats horizontal across all τ.** This contradicts Burns & Stalker's (1961) claim that organic structures fit turbulent environments. The current manuscript at `paper/manuscript.md` reports the corrected finding with a transparent disclosure of the revision history. The text below preserves the original methods-and-empirics strategy for the record.

---

## Title (original)
**When does horizontal beat vertical? Information accessibility as a boundary condition for organizational structure effectiveness**

## Title (current)
**Volatility reverses the horizontal-organization advantage: How environmental turbulence inverts the information-accessibility prescription for organizational structure**

## Abstract

The claim that "horizontal organizations outperform hierarchies" is a popular overgeneralization with well-known counterexamples (Zappos, Oticon, Valve). The organizational design literature, meanwhile, has spent sixty years articulating structure-environment fit without cleanly isolating *information accessibility* as a distinct moderator. This study formalizes the conditional claim: there exists a threshold $\tau^*$ of information accessibility such that, for $\tau < \tau^*$, vertical structures dominate in expected performance, and for $\tau > \tau^*$, horizontal structures dominate. We further predict that $\tau^*$ is a decreasing function of task complexity $K$. We test the prediction using a triangulated design: (1) theoretical re-reading of the information-processing tradition, (2) archival regression and difference-in-differences analysis on public SEC EDGAR + LinkedIn data, and (3) an empirically-calibrated agent-based model on NK landscapes. The contribution is (a) separating information accessibility from general IT investment, (b) quantifying $\tau^*$, and (c) providing falsifiable predictions about generative-AI-era organizational redesign.

---

## 1. Motivation

Popular management discourse treats "flat is better" as a received wisdom of the post-industrial economy. The academic record is equivocal. Zappos' holacracy was partially walked back (Bernstein et al. 2016). Oticon's "spaghetti organization" collapsed (Foss 2003). Yet Morning Star, Buurtzorg, and W. L. Gore have operated flat for decades. Given a population of firms all nominally adopting horizontal designs, outcomes diverge sharply.

This divergence suggests the "flat vs hierarchical" framing is mis-specified. The scientifically tractable question is **"under what conditions does flat beat hierarchical?"** This study isolates one candidate condition — information accessibility $\tau$ — and formalizes its role as a boundary condition.

## 2. Theoretical frame

We build on Galbraith's (1974) **information-processing view**: organizations are devices that process information into decisions. As task uncertainty rises, information-processing demand rises, and organizations respond by (a) reducing demand (slack, self-contained tasks) or (b) raising capacity (lateral relations, vertical information systems). Modern incarnations of Galbraith's "vertical information systems" — ERP, BI, shared data lakes, AI assistants — raise **individual** information accessibility $\tau$.

Our central theoretical proposition:

> When classical contingency theory finds that environmental uncertainty favors organic structures, part of the mechanism is that environmental complexity forces the per-individual information burden above $\tau$, at which point distributed decision-making dominates centralized decision-making.

This rereads contingency theory's "environment" as a compound of (complexity, accessibility) and carves accessibility off as the cleanly-moderating component.

## 3. Hypotheses

Formal statements in `hypotheses.md`. Prose summaries:

- **H1**: When $\tau$ is low, vertical dominates horizontal — concentrated authority with partial information beats distributed authority with worse-partial information.
- **H2**: When $\tau$ is high, horizontal dominates vertical — parallel search across diverse well-informed agents decisively outperforms serial escalation.
- **H3**: A crossover threshold $\tau^*$ exists and is identifiable.
- **H4**: $\partial \tau^* / \partial K < 0$. Harder tasks lower the accessibility bar for horizontal victory.

## 4. Method

### 4.1 Logic of the mixed design

| Method | Strength | Weakness | Complement |
|---|---|---|---|
| Theory | Interpretability | No data | Empirics + ABM provide evidence |
| Archival regression | External validity | Endogeneity, measurement error | ABM provides the mechanism |
| ABM | Causal identification | External validity doubts | Empirics provide calibration |

This is Davis, Eisenhardt & Bingham's (2007) empirically-grounded-simulation template.

### 4.2 Phase 1 — Theory

Completed in the literature and gap documents.

### 4.3 Phase 2 — Archival study

**Data (all public/free):**
- SEC EDGAR 10-K filings (via `sec-edgar-downloader` Python package).
- Parsed organizational-depth proxies from 10-K "Executive Officers" and "Properties/Organization" sections (Rajan-Wulf 2006 approach, simplified).
- $\tau$ composite index from: (i) IT spend per employee, (ii) SG&A IT share, (iii) keyword frequency of data-orientation terms in 10-K narrative, (iv) analytics-role share on LinkedIn public profiles. Index via PCA.
- $K$ proxy: Fleming-Sorenson (2001) industry-level technological ruggedness from patent citations.

**Moderation regression:**

$$
\text{ROA}_{it} = \beta_0 + \beta_1 \text{Flat}_{it} + \beta_2 \tau_{it} + \beta_3 (\text{Flat}_{it} \times \tau_{it}) + \beta_4 (\text{Flat}_{it} \times \tau_{it} \times K_i) + X_{it}'\gamma + \mu_j + \delta_t + \varepsilon_{it}
$$

with industry $\mu_j$ and year $\delta_t$ fixed effects. Predictions: $\beta_3 > 0$ for H3; $\beta_4$ signed by H4 once reconciled with ABM $\tau^*(K)$ curve.

**Difference-in-Differences:** Firms flattening after exogenous shocks (mergers, trade-liberalization events as in Guadalupe-Wulf 2010). Parallel-trends diagnostics required.

### 4.4 Phase 3 — ABM

**Core design:**
- NK landscape (Kauffman 1993): $N = 15$, $K \in \{2, 5, 10\}$.
- 100 agents per organization, 50 replications per cell.
- Structures:
  - *Vertical*: single authority node selects among escalated proposals. Communication traverses hierarchy, incurring delay.
  - *Horizontal*: peer communication, weighted-vote aggregation. No delay but vulnerable to majority error.
  - *Hybrid*: 4–5-agent clusters, local horizontalism + coordinating council.
- Information accessibility $\tau$: per-agent sampling fraction of the NK landscape.
- Outputs: terminal fitness, time-to-convergence, solution-diversity index.

**Full factorial:**
Structure (3) × $\tau$ (9 levels from 0.1 to 0.9) × $K$ (3) × seeds (50) = **4,050 runs**.

**Analysis:**
- Mixed-effects ANOVA on terminal fitness with structure × $\tau$ × $K$ interactions.
- Spline root-finding on $\Delta\pi(\tau) = \pi_H - \pi_V$ per $K$ gives $\hat{\tau}^*(K)$.
- Regression of $\hat{\tau}^*(K)$ on $K$ tests H4.

**Calibration:**
- $K$ levels calibrated to Fleming-Sorenson industry distribution quantiles.
- Baseline $\tau$ distribution from Brynjolfsson-McElheran DDD diffusion rates.

### 4.5 Phase 4 — Triangulation

1. $\beta_3$ sign (empirics) vs $\partial \Delta\pi / \partial \tau$ sign (ABM).
2. Spline inflection in empirics vs $\hat{\tau}^*$ in ABM.
3. Triple-interaction (empirics) vs $\partial \tau^* / \partial K$ (ABM).

Two-of-three agreement = strong evidence. Three-of-three = very strong. All-disagreement = interesting negative finding reported transparently.

## 5. Timeline (AI-accelerated)

| Phase | Traditional human-only | AI-accelerated |
|---|---|---|
| Literature review | 2–3 months | 1–2 weeks |
| Data collection (public only) | 2 months | 2–3 weeks (automated EDGAR parsing) |
| Empirical analysis | 2–3 months | 2–3 weeks |
| ABM build & run | 3–4 months | 1–2 weeks (draft shipped in this deliverable) |
| Integration & writing | 4–6 months | 1–2 months |
| **Total** | **15–18 months** | **3–5 months** |

## 6. Target outlets

Priority: *Organization Science*, *Strategic Management Journal*, *Administrative Science Quarterly*, *Management Science*. Backup: *Journal of Organization Design*, *Strategic Organization*.

## 7. Ethics and reproducibility

- Public data only. No IRB involvement needed.
- Code and intermediate data released in this repository from day zero.
- All figures reproducible from `results/` with fixed seeds.

## 8. Limitations and extensions

- **Within-firm heterogeneity of $\tau$.** We use firm-averaged $\tau$; functional/level variation may matter.
- **AI endogeneity.** Generative AI raises $\tau$ but also lowers effective $K$. The two must be disentangled in post-2022 samples.
- **Cultural moderation.** Power-distance (Hofstede) likely modulates horizontal-org effectiveness; cross-country extension is valuable.

## 9. Conclusion

This study reframes "is horizontal better?" as "when is horizontal better?", quantifies the crossover condition with a composite triangulated design, and delivers a falsifiable prediction about the direction of organizational design in an AI-rich era. The contribution is simultaneously theoretical (construct separation), computational (quantified $\tau^*$ surface), and empirical (archival + quasi-experimental validation).
