# Formal Hypotheses

## Notation

- $S \in \{V, H, \text{Hy}\}$ — organizational structure (Vertical, Horizontal, Hybrid).
- $\tau \in [0, 1]$ — information accessibility.
- $K \in \mathbb{Z}_{\geq 0}$ — task complexity (NK epistatic interactions).
- $\omega \geq 0$ — environmental volatility, operationalized as shock frequency (1 / SHOCK_EVERY).
- $\pi(S, \tau, K, \omega)$ — expected organizational performance.

---

## Headline hypothesis

### H5 — Volatility reverses the horizontal advantage

Static environments support the classical τ\*(K) boundary; dynamic environments erase it by shifting the entire V-vs-H relationship toward vertical. Formally:

$$
\frac{\partial \left[ \pi(V, \tau, K, \omega) - \pi(H, \tau, K, \omega) \right]}{\partial \omega} > 0
$$

and there exists a threshold volatility ω\* > 0 above which vertical dominates horizontal uniformly in τ for any K ≥ K_0:

$$
\exists \omega^* > 0:\ \forall \omega > \omega^*,\ \forall \tau,\ \forall K \geq K_0:\ \pi(V, \tau, K, \omega) > \pi(H, \tau, K, \omega).
$$

**Rationale.** Horizontal's high-τ advantage in static settings depends on accumulated parallel exploration — multiple trajectories jointly covering the landscape. Environmental shocks erase accumulated exploration: after each shock, yesterday's good states are no better than random, and the firm must re-coordinate its scattered agents. Vertical's single-path, single-decision structure does not suffer this fragmentation cost; the CEO's one trajectory simply resumes searching from wherever it is.

This reverses the popular reading of Burns & Stalker (1961) that "organic structures fit turbulent environments." The NK operationalization suggests the opposite direction.

**Testable prediction — ABM.** On dynamic NK landscapes, Spearman ρ(shock frequency, V − H) is positive and approaches +1 across the volatility gradient; the V − H gap transitions from negative (H wins) to positive (V wins) at a small non-zero ω.

**Testable prediction — empirics.** Flat firms in high-volatility industries (top-quartile margin variance or equivalent proxy) show weaker or negative flatness-performance correlations compared to flat firms in low-volatility industries, controlling for τ and K.

---

## Supporting (static-regime) hypotheses

These four recover the classical contingency story. They are our sanity check that the model can reproduce what decades of theory predict, before we add volatility and show that the prediction gets overturned.

### H1 — Static, low-τ vertical advantage

$$
\exists \underline{\tau} > 0:\quad \forall \tau < \underline{\tau},\ \forall K,\ \omega = 0:\quad \pi(V) > \pi(H)
$$

### H2 — Static, high-τ horizontal advantage

$$
\exists \overline{\tau} < 1:\quad \forall \tau > \overline{\tau},\ \forall K \geq K_0,\ \omega = 0:\quad \pi(H) > \pi(V)
$$

### H3 — Static crossover threshold

For each K, there exists $\tau^*(K) \in (0, 1)$ at which $\pi(V) = \pi(H)$ on a static landscape.

### H4 — Complexity lowers the static crossover

$$
\frac{\partial \tau^*}{\partial K} < 0\quad (\omega = 0)
$$

---

## Auxiliary: where does Hybrid sit?

We initially conjectured (and an earlier draft of this paper claimed) that cluster-based hybrids would dominate both pure forms under volatility. The corrected ABM does not support that conjecture. The hybrid performs between V and H across most (τ, K, ω) cells — better than H, worse than V, in the dynamic regime. Modularity does not resolve the speed-vs-parallelism trade-off that volatility imposes.

This negative result is itself informative. A simpler pure structure (vertical) dominates a more complex modular structure (hybrid) under shocks. The parsimony principle applies: when the environment disrupts accumulated state frequently, having less state to disrupt is an advantage.

---

## Falsification conditions

H5 fails if, on calibrated dynamic landscapes:

1. $\partial (\pi_V - \pi_H) / \partial \omega \leq 0$ (no volatility dose-response or wrong-direction dose-response).
2. V does not dominate H in the high-volatility limit (would mean the reversal isn't real).
3. H1–H4 fail in the static limit (would mean the static baseline is broken).

Reporting any of these is informative; failure of H5 would mean environmental volatility is not in fact a moderator of structural advantage in the NK operationalization.

---

## Mapping to analyses

| Hypothesis | ABM analysis | Archival analysis (future work) |
|---|---|---|
| H1 | π(V) > π(H) at τ=0.1, ω=0 | Flat × low-τ subsample coefficient |
| H2 | π(H) > π(V) at τ=0.9, K≥5, ω=0 | Flat × high-τ subsample coefficient |
| H3 | Spline root of Δπ(τ) at ω=0 | Spline inflection in flat × τ |
| H4 | Regression of τ̂*(K) on K at ω=0 | Triple interaction flat × τ × K |
| **H5 (main)** | ∂(V − H)/∂ω > 0; V > H uniformly at ω > ω\* | Flat × industry-volatility-proxy coefficient negative (i.e. flatness pays less in volatile industries) |
