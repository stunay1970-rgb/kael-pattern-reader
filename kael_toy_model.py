"""
KAEL – Pattern Reader (TOY MODEL)

Author: Süreyya Tunay
Purpose:
This file contains a deliberately simplified (toy) version of the KAEL framework.
It demonstrates structural pattern sensitivity under noisy or difficult data,
without revealing the full KAEL pipeline, scaling rules, or optimization logic.

IMPORTANT:
- This is NOT the full KAEL model.
- This code is for conceptual demonstration and independent inspection only.
- It is not intended for production or commercial use.
"""

import numpy as np
from dataclasses import dataclass


@dataclass(frozen=True)
class KaelConfig:
    window: int = 32
    eps: float = 1e-12


def kael_feature(x: np.ndarray, cfg: KaelConfig) -> np.ndarray:
    """
    Extract a simple structural feature from a numeric sequence.
    This toy feature focuses on local variation stability.
    """
    x = np.asarray(x, dtype=float)

    if x.size < 2:
        return np.array([])

    # Local differences
    d = np.abs(np.diff(x))

    # Smoothing (structural aggregation)
    w = max(2, cfg.window)
    kernel = np.ones(w) / w
    smoothed = np.convolve(d, kernel, mode="same")

    # Robust normalization
    lo = np.percentile(smoothed, 5)
    hi = np.percentile(smoothed, 95)
    denom = max(cfg.eps, hi - lo)

    return np.clip((smoothed - lo) / denom, 0.0, 1.0)


def kael_score(x: np.ndarray, cfg: KaelConfig) -> float:
    """
    Aggregate the extracted feature into a single stability score.
    """
    f = kael_feature(x, cfg)

    if f.size == 0:
        return 0.0

    return float(np.mean(f ** 2))


if __name__ == "__main__":
    # Example usage with a toy sequence
    toy_data = np.array([1, 2, 1.5, 3, 2.8, 3.1, 2.9, 3.0])
    cfg = KaelConfig(window=4)

    score = kael_score(toy_data, cfg)
    print("KAEL toy score:", score)
