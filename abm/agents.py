"""
Agents propose one-bit flips under information accessibility tau.

An agent sees a random fraction tau of the N possible one-bit-flip neighbors,
plus the null move. Among visible options, the agent proposes the highest-fitness
one. If nothing in view improves over current, they propose "no move" (-1).

tau is the core theoretical construct: the fraction of decision-relevant
alternatives the individual can actually reach within their search budget.
"""

from __future__ import annotations
import numpy as np
from dataclasses import dataclass


@dataclass
class Agent:
    agent_id: int
    role: str  # 'ceo', 'mgr', 'worker', 'leader', 'member', 'peer'
    tau_personal: float  # may be boosted vs firm-wide tau

    def propose(self, state_int: int, landscape, rng: np.random.Generator) -> int:
        """Return the bit index to flip (0..N-1), or -1 for no move."""
        N = landscape.N
        neighbor_fits = landscape.all_one_bit_flip_fitnesses(state_int)
        current = landscape.current_fitness_idx(state_int)

        k_visible = max(1, int(round(self.tau_personal * N)))
        visible = rng.choice(N, size=k_visible, replace=False)

        best_idx = -1
        best_fit = current
        for b in visible:
            if neighbor_fits[b] > best_fit:
                best_fit = neighbor_fits[b]
                best_idx = int(b)
        return best_idx


def build_agents(structure: str, tau: float, n_agents: int,
                 ceo_boost: float = 1.3) -> list[Agent]:
    """
    Build a roster of agents according to the organization type.

    - Vertical: CEO (boosted tau) + managers + workers.
    - Horizontal: all peers at firm-wide tau.
    - Hybrid: cluster leaders (mildly boosted) + members.
    """
    if structure == "V":
        agents = []
        tau_ceo = min(1.0, tau * ceo_boost)
        agents.append(Agent(0, "ceo", tau_ceo))
        n_mgr = max(1, n_agents // 6)
        tau_mgr = tau
        for i in range(n_mgr):
            agents.append(Agent(1 + i, "mgr", tau_mgr))
        n_worker = n_agents - 1 - n_mgr
        tau_worker = tau
        for i in range(n_worker):
            agents.append(Agent(1 + n_mgr + i, "worker", tau_worker))
        return agents

    if structure == "H":
        return [Agent(i, "peer", tau) for i in range(n_agents)]

    if structure == "Hy":
        agents = []
        cluster_size = 5
        n_clusters = max(1, n_agents // cluster_size)
        idx = 0
        for c in range(n_clusters):
            agents.append(Agent(idx, "leader", min(1.0, tau * 1.1)))
            idx += 1
            for _ in range(cluster_size - 1):
                if idx < n_agents:
                    agents.append(Agent(idx, "member", tau))
                    idx += 1
        while idx < n_agents:
            agents.append(Agent(idx, "member", tau))
            idx += 1
        return agents

    raise ValueError(f"Unknown structure: {structure}")
