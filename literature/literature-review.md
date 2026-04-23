# Literature Review

> Synthesis of ~15 core references across organizational theory, agent-based modeling, and empirical work on firm structure. Each entry includes the **finding**, **method**, and **what it contributes to our paper**.

---

## 1. Contingency theory — the foundation

### Burns & Stalker (1961). *The Management of Innovation.*
- **Finding**: In stable environments, "mechanistic" (hierarchical, rule-based) structures outperform; in turbulent environments, "organic" (decentralized, loosely-coupled) structures outperform.
- **Method**: Comparative case study of 20 Scottish/English electronics firms during the postwar transition.
- **Use**: Classical antecedent. Our hypothesis is a 21st-century restatement — we replace their vague "environmental turbulence" with the measurable construct *information accessibility (τ)*.

### Lawrence & Lorsch (1967). "Differentiation and Integration in Complex Organizations." *Administrative Science Quarterly.*
- **Finding**: Firms in uncertain environments use more differentiated subunits AND need more integration mechanisms.
- **Method**: Comparative field study (plastics, food, containers industries).
- **Use**: Establishes that fit between structure and environment matters; we extend by asking: fit with *what specifically* about the environment?

### Galbraith (1974). "Organization Design: An Information Processing View." *Interfaces.*
- **Finding**: Organizations are information-processing devices. As task uncertainty grows, either (a) reduce information-processing needs (slack, self-contained tasks) or (b) increase capacity (lateral relations, investment in vertical information systems).
- **Use**: **Theoretical backbone of our paper.** Our τ = information accessibility is a direct operationalization of Galbraith's "vertical information systems" capacity at the individual-agent level.

### Mintzberg (1979). *The Structuring of Organizations.*
- **Finding**: Five structural configurations (simple, machine bureaucracy, professional bureaucracy, divisional, adhocracy), each fit to different contingencies.
- **Use**: Source for our operationalization of "vertical" (machine bureaucracy) vs "horizontal" (adhocracy).

---

## 2. Self-managing / flat organizations — the modern empirical wave

### Lee & Edmondson (2017). "Self-Managing Organizations." *Research in Organizational Behavior.*
- **Finding**: Meta-review of radical decentralization. Self-management works when tasks are complex AND information distribution is wide; fails when coordination requirements are tight AND information is concentrated.
- **Method**: Narrative literature review covering 30+ cases including Valve, Morning Star, Zappos, Buurtzorg.
- **Use**: **Most important modern antecedent.** Their qualitative conclusion is precisely the conditional relationship our paper formalizes and tests.

### Bernstein, Bunch, Canner & Lee (2016). "Beyond the Holacracy Hype." *Harvard Business Review.*
- **Finding**: Zappos' holacracy implementation produced mixed results; 14% of staff quit during the transition; coordination costs rose.
- **Use**: Evidence that horizontal ≠ universally better. Motivates our boundary-condition framing.

### Puranam, Alexy & Reitzig (2014). "What's 'New' About New Forms of Organizing?" *Academy of Management Review.*
- **Finding**: All organizations must solve 4 universal problems: task division, task allocation, reward distribution, information provision. "New" forms (flat, self-managing) differ in HOW they solve them, not WHETHER.
- **Use**: Gives us the conceptual lens — we focus on the *information provision* problem, arguing τ changes which solution is optimal.

### Foss (2003). "Selective Intervention and Internal Hybrids: Interpreting and Learning from the Rise and Decline of the Oticon Spaghetti Organization." *Organization Science.*
- **Finding**: Oticon's radical flat experiment (1991–1996) partially reverted. Pure horizontalism suffers from selective-intervention problems: CEOs can't commit to never intervene, which undermines the promised autonomy.
- **Use**: Source of a key control in our ABM — pure structures are unstable; hybrid configurations dominate in practice.

---

## 3. Computational / agent-based foundations

### Kauffman (1993). *The Origins of Order.*
- **Finding**: NK fitness landscapes formalize the trade-off between exploration and exploitation. K controls ruggedness (epistatic interactions among N elements).
- **Use**: **The core of our ABM.** Task complexity = K.

### Levinthal (1997). "Adaptation on Rugged Landscapes." *Management Science.*
- **Finding**: Imports NK into organizational science. Firms get stuck on local optima when K is high; distant search is valuable but costly.
- **Use**: Template for how we connect NK to firm-level performance.

### Csaszar (2013). "An Efficient Frontier in Organization Design: Organizational Structure as a Determinant of Exploration and Exploitation." *Organization Science.*
- **Finding**: Different aggregation rules (unanimity, majority, dictatorship) trade off exploration vs exploitation. Hierarchical ("dictatorship") favors exploitation; flat ("majority") favors exploration.
- **Use**: **Direct methodological parent.** Our ABM generalizes Csaszar by adding τ as a second control dimension.

### Lazer & Friedman (2007). "The Network Structure of Exploration and Exploitation." *Administrative Science Quarterly.*
- **Finding**: In NK simulations, densely-connected networks find good solutions fast but converge prematurely; sparse networks explore longer and find better global optima.
- **Use**: Empirical template for how to parameterize communication topology in our vertical vs horizontal treatments.

### March (1991). "Exploration and Exploitation in Organizational Learning." *Organization Science.*
- **Finding**: Slower learners (low code-to-individual learning rate) preserve variance longer and find better long-run equilibria. Mirrors the flat/hierarchy trade-off.
- **Use**: Canonical citation for exploration/exploitation language.

---

## 4. Empirical work on flatness and firm performance

### Rajan & Wulf (2006). "The Flattening Firm: Evidence from Panel Data on the Changing Nature of Corporate Hierarchies." *Review of Economics and Statistics.*
- **Finding**: US firms 1986–1999 measurably flattened: fewer layers between CEO and division heads; wider spans of control. Correlates with increased equity-based compensation for middle managers.
- **Method**: Panel data on ~300 large US firms from an executive-compensation survey.
- **Use**: **Template for our Phase 2 archival study.** Their structural-proxy variables are what we'll extract from 10-Ks.

### Guadalupe & Wulf (2010). "The Flattening Firm and Product Market Competition." *American Economic Journal: Applied Economics.*
- **Finding**: Flattening intensified after trade liberalization. Competition pushes firms toward horizontalism.
- **Use**: Evidence of a mechanism — environmental pressure changes optimal structure. Consistent with our τ-moderator claim if we treat competition as proxy for information-flow demands.

### Bloom, Sadun & Van Reenen (2012). "Americans Do IT Better: US Multinationals and the Productivity Miracle." *American Economic Review.*
- **Finding**: Decentralized decision-making raises the return to IT investment. Firms with more IT AND more decentralization outperform; either alone does less.
- **Use**: **Strongest existing empirical evidence for our interaction hypothesis.** Their IT×decentralization interaction is structurally identical to our τ×horizontal interaction.

### Brynjolfsson & McElheran (2016). "The Rapid Adoption of Data-Driven Decision-Making." *American Economic Review P&P.*
- **Finding**: Firms that combine data infrastructure with decentralized decision rights see the largest productivity gains.
- **Use**: Additional corroboration and source for our τ proxy (IT/data-infrastructure intensity).

---

## 5. Information, AI, and the future-of-work angle

### Zuboff (1988). *In the Age of the Smart Machine.*
- **Use**: Historical touchstone for the "informating" thesis — that IT doesn't just automate, it reshapes who can see what. Precursor to our τ construct.

### Malone (2004). *The Future of Work.*
- **Use**: Popular framing of decentralization as driven by falling communication costs. Useful for the Introduction.

### Brynjolfsson, Li & Raymond (2023). "Generative AI at Work." *NBER Working Paper.*
- **Finding**: AI tools help low-skill workers more than high-skill. Flattens the intra-firm skill distribution.
- **Use**: Contemporary relevance — AI is pushing τ upward for everyone, making the boundary condition we study empirically urgent.

---

## 6. Methodological references

### Davis, Eisenhardt & Bingham (2007). "Developing Theory Through Simulation Methods." *Academy of Management Review.*
- **Use**: Our **methods-section template**. Defines "empirically-grounded simulation" as a legitimate theory-development mode for top-tier management journals.

### Harrison, Lin, Carroll & Carley (2007). "Simulation Modeling in Organizational and Management Research." *Academy of Management Review.*
- **Use**: Defends ABM/computational methods in management. Useful for reviewer responses.

---

## Synthesis

The existing literature tells us:
1. Structure-environment fit matters (contingency theory).
2. Horizontal organizations have documented successes AND failures (Bernstein; Foss; Lee & Edmondson).
3. IT × decentralization interactions are real (Bloom-Sadun-Van Reenen; Brynjolfsson-McElheran).
4. ABM on NK landscapes can discriminate structural configurations (Csaszar; Lazer & Friedman).

**What it doesn't tell us** is covered in `theoretical-gap.md`.
