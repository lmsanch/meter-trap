# Meter-Trap — public evidence repo

> **Analytical opinion, not investment advice.**

A probabilistic analysis of the Anthropic IPO (reported for ~October 2026 at a reported ~$2 trillion valuation). This repository holds only the *published* artifacts of the analysis: charts, the issues register from the analyst panel, data provenance, and dated directional calls. The engine (code, parameters, calibrations, prompts, model weights) is private; before the IPO prices, a SHA-256 hash of the private methodology file is published here so that the analysis can later be shown to pre-date the event unaltered.

## What is here

| folder | contents |
|---|---|
| `figures/` | fan charts and probability exhibits (fundamental lens, market-behaviour lens, agreement zone, panel trajectories) |
| `register/` | the analyst panel's issues register: each disagreement, its category (market / regulatory / technical / competitive), whether it is falsifiable, and what data would settle it |
| `provenance/` | every quantitative input, dated and sourced, with confidence flags (verified-primary / secondary / single-source / estimate) |
| `predictions/` | dated directional calls with numbers, and the methodology hash; outcomes are scored (Brier) as quarters resolve |

## Methodology (techniques named; parameters withheld)

1. **Regime-switching Monte Carlo (fundamental lens).** Five correlated quarterly drivers from a 2026Q4 entry to a 2031Q4 exit — metered-revenue growth with momentum / deceleration / shock regimes, revenue-mix shift, gross-margin path, a Poisson regulatory-access shock process calibrated to the June-2026 export episode, and a valuation multiple conditional on growth, margin and revenue commitment. 100,000 seeded paths. Before any headline number is produced the engine must reproduce, deterministically, the leaked Coatue base case (entry, 2030 ARR, exit value, IRR); this gate passed.
2. **Kernel-weighted similarity over IPO comparables (market-behaviour lens).** Standardised at-IPO features of 14 large technology listings, a Mahalanobis kernel, and resampling of their 8-quarter post-IPO return paths. Leave-one-out validation retrodicts Snowflake's 2022 re-rating and CoreWeave's post-IPO drawdown.
3. **Multi-model adversarial analyst panel with belief-revision tracking.** Bull / bear / neutral personas played by several open-weight model families, roles rotating each round; an independent open-weight judge model applies a fixed rubric, accepts a score revision only when it is tied to cited evidence or a simulation result, and logs evidence-driven versus conformity updates separately. Analysts may request engine runs with parameter changes; results enter the next round. Stopping rule: score deltas below threshold for two consecutive rounds, or issues register exhausted.
4. **State-space backfill** for GPU-rental price series used in the compute-cost discussion (documented separately with per-segment anchor density).

Headline outputs, the fan charts, the register and the convergence trajectories are published here; the private repo holds everything reproducible (`make all` from raw CSVs).

*Analytical opinion, not investment advice.*
