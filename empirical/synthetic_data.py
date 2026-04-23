"""
Generate synthetic firm-year data that PLAUSIBLY mimics what SEC EDGAR 10-K +
LinkedIn extraction would produce. Used to validate the regression pipeline
end-to-end before real-data deployment.

Data model:
- N_FIRMS firms observed over T_YEARS years
- Each firm has industry-fixed K (task complexity), τ (info accessibility),
  Flat (flatness score in [0,1]), and unobserved quality q
- True DGP embeds H1–H4 so the regression can recover the moderation pattern

If the regression.py script, run on this data, correctly recovers the
signs/significance we expect, the pipeline is validated. Replace this module
with real data loaders before publishing.
"""

from __future__ import annotations
import os
import numpy as np
import pandas as pd

N_FIRMS = 500
T_YEARS = 8
INDUSTRIES = ["tech", "finance", "manuf", "pharma", "retail", "energy"]

INDUSTRY_K = {
    "tech": 9.0, "pharma": 8.5, "finance": 6.0,
    "manuf": 4.0, "retail": 3.0, "energy": 3.5,
}

RNG_SEED = 42


def generate(out_path: str, seed: int = RNG_SEED) -> pd.DataFrame:
    rng = np.random.default_rng(seed)

    rows = []
    for firm_id in range(N_FIRMS):
        ind = rng.choice(INDUSTRIES)
        K = INDUSTRY_K[ind] + rng.normal(0, 0.5)
        q = rng.normal(0, 0.5)
        flat_base = np.clip(rng.beta(2, 5), 0, 1)
        tau_base = np.clip(rng.beta(2, 3), 0, 1)

        log_size = rng.normal(7, 1.5)
        log_age = rng.normal(3, 0.8)

        for t_idx, year in enumerate(range(2015, 2015 + T_YEARS)):
            flat = np.clip(flat_base + rng.normal(0, 0.05) + 0.01 * t_idx, 0, 1)
            tau = np.clip(tau_base + rng.normal(0, 0.04) + 0.03 * t_idx, 0, 1)

            K_c = K - 5.75
            beta_flat = -0.06 + 0.14 * tau + 0.006 * K_c + 0.015 * tau * K_c

            roa = (
                0.08
                + 0.02 * log_size * 0.05
                + 0.005 * (8 - abs(log_age - 3))
                + 0.05 * q
                + beta_flat * flat
                + rng.normal(0, 0.03)
            )

            rows.append({
                "firm_id": firm_id, "year": year, "industry": ind,
                "log_size": log_size, "log_age": log_age,
                "flat": flat, "tau": tau, "K": K,
                "quality_latent": q,
                "ROA": roa,
            })

    df = pd.DataFrame(rows)
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    df.to_csv(out_path, index=False)
    print(f"Wrote {len(df)} rows to {out_path}")
    return df


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(here, "synthetic_firms.csv")
    df = generate(out)
    print(df.head())
    print("\nSummary:")
    print(df.describe(include="all").T.head(10))
