"""Gera uma série horária sintética de volume de transações em um app de pagamentos, com anomalias injetadas.

Os dados são simulados: nenhum dado real é usado.
"""
import numpy as np
import pandas as pd


def gerar_serie(dias=120, seed=7):
    rng = np.random.default_rng(seed)
    ts = pd.date_range("2025-03-01", periods=dias * 24, freq="h")
    h = ts.hour.values
    dow = ts.dayofweek.values
    diario = 1 + 0.8 * np.exp(-((h - 10) ** 2) / 8) + 0.6 * np.exp(-((h - 15) ** 2) / 6) - 0.5 * ((h < 6) | (h > 21))
    semanal = np.where(dow >= 5, 0.55, 1.0)
    tendencia = 1 + 0.15 * np.arange(len(ts)) / len(ts)
    lam = 20 * diario * semanal * tendencia
    y = rng.poisson(lam).astype(float)

    anomalia = np.zeros(len(ts), dtype=int)
    inicio_teste = len(ts) - 30 * 24
    eventos = [(inicio_teste + 50, 3, 3.0), (inicio_teste + 170, 2, 2.6), (inicio_teste + 300, 4, 2.2),
               (inicio_teste + 410, 3, 2.8), (inicio_teste + 600, 2, 3.2)]
    for ini, dur, fator in eventos:
        y[ini:ini + dur] = rng.poisson(lam[ini:ini + dur] * fator)
        anomalia[ini:ini + dur] = 1
    # queda: o app ficou fora do ar no meio do horário comercial
    ini = inicio_teste + 490
    while not (10 <= ts[ini].hour <= 14 and ts[ini].dayofweek < 5):
        ini += 1
    y[ini:ini + 3] = rng.poisson(lam[ini:ini + 3] * 0.1)
    anomalia[ini:ini + 3] = 1
    return pd.DataFrame({"ds": ts, "y": y, "anomalia": anomalia})
