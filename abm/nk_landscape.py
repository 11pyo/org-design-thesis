"""
NK fitness landscape (Kauffman 1993).

Each of N binary loci contributes a fitness value that depends on itself and K
other loci. Overall fitness = mean of per-locus contributions.

We precompute all 2^N fitnesses for N <= 18 so hot-loop lookups are O(1).
"""

from __future__ import annotations
import numpy as np


class NKLandscape:
    def __init__(self, N: int, K: int, seed: int):
        assert 0 <= K < N, "K must satisfy 0 <= K < N"
        assert N <= 18, "N too large for exhaustive precompute"
        self.N = N
        self.K = K
        self.rng = np.random.default_rng(seed)

        self.epistasis = np.stack([
            np.concatenate([[i], self.rng.choice(
                [j for j in range(N) if j != i], size=K, replace=False
            )])
            for i in range(N)
        ])

        self.contrib_tables = self.rng.random(size=(N, 1 << (K + 1)))

        self._fitness_cache = self._precompute_all()

    def _precompute_all(self) -> np.ndarray:
        total = 1 << self.N
        table = np.zeros(total, dtype=np.float64)
        bits = (np.arange(total)[:, None] >> np.arange(self.N)) & 1
        for i in range(self.N):
            idx_bits = bits[:, self.epistasis[i]]
            weights = 1 << np.arange(self.K + 1)
            local_idx = (idx_bits * weights).sum(axis=1)
            table += self.contrib_tables[i, local_idx]
        table /= self.N
        return table

    def fitness(self, state: np.ndarray) -> float:
        idx = int(np.dot(state, 1 << np.arange(self.N)))
        return float(self._fitness_cache[idx])

    def fitness_idx(self, state_int: int) -> float:
        return float(self._fitness_cache[state_int])

    def all_one_bit_flip_fitnesses(self, state_int: int) -> np.ndarray:
        """Fitness of each of N one-bit-flip neighbors. Index i = flip bit i."""
        masks = 1 << np.arange(self.N)
        neighbor_ints = state_int ^ masks
        return self._fitness_cache[neighbor_ints]

    def current_fitness_idx(self, state_int: int) -> float:
        return float(self._fitness_cache[state_int])


def state_int_to_array(x: int, N: int) -> np.ndarray:
    return np.array([(x >> i) & 1 for i in range(N)], dtype=np.int8)


def array_to_state_int(s: np.ndarray) -> int:
    return int(np.dot(s, 1 << np.arange(len(s))))
