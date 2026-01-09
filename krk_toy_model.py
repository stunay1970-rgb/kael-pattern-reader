"""
KRK – Toy Model (Conceptual Demonstration)

Author: Süreyya Tunay

Purpose:
This file provides a deliberately simplified (toy) version of the KRK stack
(KAEL-2 + Router + KAEL-H).

It is designed to demonstrate:
- how structural signals are stabilized under stress,
- how crisis-like perturbations are routed,
- how interpretation is preserved even when prediction degrades.

IMPORTANT:
- This is NOT the full KRK system.
- This code is for conceptual demonstration only.
- It is not optimized, trained, or intended for production use.
"""

import numpy as np


def generate_signal(n=200, noise_level=0.2, crisis=False):
    """
    Generate a simple 1D signal.
    Optionally inject a crisis (sudden structural distortion).
    """
    x = np.linspace(0, 4 * np.pi, n)
    signal = np.sin(x)

    noise = noise_level * np.random.randn(n)
    signal = signal + noise

    if crisis:
        spike = np.zeros(n)
        spike[n // 2 : n // 2 + 5] = 3.0
        signal = signal + spike

    return signal


def kael2_feature(signal):
    """
    Simplified KAEL-2 style feature:
    energy-like stabilization via logarithmic compression.
    """
    return np.log1p(np.abs(signal))


def kaelh_feature(signal):
    """
    Simplified KAEL-H style feature:
    slow harmonic structure via cumulative mean.
    """
    return np.cumsum(signal) / (np.arange(len(signal)) + 1)


def r3_router(signal, threshold=1.0):
    """
    Very simple router:
    decides whether the signal is in 'normal' or 'crisis' regime.
    """
    if np.max(np.abs(signal)) > threshold:
        return "CRISIS"
    return "NORMAL"


def krk_toy_pipeline(signal):
    """
    Minimal KRK pipeline:
    - route the signal
    - extract KAEL-2 and KAEL-H inspired features
    """
    route = r3_router(signal)
    e_feat = kael2_feature(signal)
    h_feat = kaelh_feature(signal)

    return {
        "route": route,
        "energy_feature": e_feat,
        "harmonic_feature": h_feat,
    }


if __name__ == "__main__":
    # Demo run
    normal_signal = generate_signal(crisis=False)
    crisis_signal = generate_signal(crisis=True)

    out_normal = krk_toy_pipeline(normal_signal)
    out_crisis = krk_toy_pipeline(crisis_signal)

    print("Normal route:", out_normal["route"])
    print("Crisis route:", out_crisis["route"])