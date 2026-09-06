# End-to-End-Propfirm-Pricing-Engine


# PropFirm Pricing & Execution Engine

A quantitative research and execution framework modeling Proprietary Trading Firm evaluations as **exotic path-dependent options**.

## 📌 Project Overview
The retail trading industry treats Prop Firm evaluations (e.g., FTMO, Topstep, Apex) as standard trading accounts. Quantitatively, purchasing an evaluation is equivalent to buying a **Double-Barrier Knock-Out Option** (for static drawdowns) or a **Lookback/Trailing Barrier Option** (for High-Water Mark trailing drawdowns).

This repository aims to mathematically deconstruct these financial products, calculate the true risk of ruin, and deploy a stochastic optimal control policy to maximize the probability of funding: $P(\tau_K < \tau)$.

## 📐 Mathematical Framework
This engine relies on advanced financial engineering concepts:
- **Underlying Dynamics:** The equity curve ($X_t$) is modeled as a continuous-time stochastic process (Jump-Diffusion / Ornstein-Uhlenbeck for Mean Reversion edges).
- **Barrier Mechanics:** Formalization of the daily loss limit and trailing drawdown as dynamic stopping times ($\tau$).
- **Optimal Sizing (Risk Sequencing):** Replaces the static Kelly Criterion (which guarantees ruin against a trailing barrier) with an **Asymmetric Risk Scaling** policy derived from Hamilton-Jacobi-Bellman (HJB) equations and Dynamic Programming.

## 🏗️ Architecture
- `docs/` : Mathematical proofs and LaTeX research papers.
- `src/core/` : State managers for Prop Firm constraints (Trailing Drawdown logic).
- `src/alpha/` : OLS calibration for stochastic processes (Signal generation).
- `src/execution/` : Risk management and optimal position sizing logic.
- `notebooks/` : Monte Carlo simulations and Heatmap generations.



## ⚠️ Disclaimer

This project is strictly for quantitative research and educational purposes. Financial markets are stochastic, and past statistical edges do not guarantee future performance.
