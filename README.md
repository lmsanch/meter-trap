# Meter-Trap — Anthropic IPO Quantitative Analysis

> **Analytical opinion, not investment advice.**

> **Analytical opinion, not investment advice.**

> **Analytical opinion, not investment advice.**

---

## What this is

This repository is the **public evidence repo** for the Meter-Trap program: a
probabilistic analysis of the Anthropic IPO (approximately October 2026, with a
reported target valuation near $2 trillion).

It contains only published artifacts — charts, registers, provenance records, and
dated directional calls. The private engine repo (`meter-trap-engine`) holds all
code, calibrations, prompts, weights, and model parameters. **Nothing executable
or configurable appears here.**

*Analytical opinion, not investment advice.*

---

## Methodology

The analysis combines four techniques. Only the names and high-level descriptions
are disclosed; parameters, calibrations, prompts, weights, and implementation
details are deliberately withheld.

### Regime-switching Monte Carlo

A regime-switching Monte Carlo simulation models the IPO outcome distribution
using five correlated quarterly macroeconomic and firm-level drivers. One hundred
thousand paths are drawn per scenario to produce fan charts and probability
tables over valuation, raise size, and post-IPO trajectory.

*Analytical opinion, not investment advice.*

### Kernel-weighted similarity

A kernel-weighted similarity estimator ranks the target against historical IPO
comparables using Mahalanobis-distance k-nearest-neighbors. The kernel weighting
emphasizes closer comps and downweights distant ones, producing a similarity-
weighted valuation anchor that feeds into the Monte Carlo prior.

*Analytical opinion, not investment advice.*

### Multi-model adversarial analyst panel

A multi-model adversarial analyst panel deliberates on the evidence. Multiple
independent analyst instances argue opposing positions, challenge each other's
assumptions, and revise their beliefs through structured rounds. An issues
register records every disagreement, resolution, and residual uncertainty.

*Analytical opinion, not investment advice.*

### State-space backfill for gapped GPU price series

A state-space model backfills gaps in GPU pricing time series that arise from
thin trading and data-source discontinuities. The backfilled series provides
continuous inputs for the similarity and Monte Carlo components.

*Analytical opinion, not investment advice.*

---

## Repository structure

```
figures/       Fan charts, distributions, probability tables (PNG/SVG only)
register/      Issues register CSV from the deliberation panel
provenance/    Data provenance CSV — every input dated and sourced
predictions/   Dated directional calls and pre-commitment hash
scripts/       Publish script (whitelist-gated; copies from private engine)
README.md      This file
```

No source code, YAML files, prompts, weights, model parameters, or notebooks are
published here. The `scripts/publish.py` whitelist enforces this automatically.

*Analytical opinion, not investment advice.*

---

## Pre-commitment device

Before IPO pricing, this repository will contain:

1. **Dated directional calls** — specific, timestamped predictions about
   valuation range, raise size, and first-day / first-month direction, committed
   to `predictions/directional_calls.csv` before the event.

2. **A SHA-256 hash** of the full private methodology file, committed to
   `predictions/methodology_hash.txt`. This allows post-hoc verification that
   the methodology was not retroactively altered to fit the outcome, without
   disclosing the methodology itself.

This is a pre-commitment device: the predictions and hash are published before
the event, making it impossible to silently revise the analysis after the fact.

*Analytical opinion, not investment advice.*

---

## Data provenance

Every input is dated and sourced. The `provenance/provenance.csv` file records,
for each data point used in the analysis: the source URL, the as-of date, the
confidence level, and the collection method. No input enters the analysis without
a provenance entry.

*Analytical opinion, not investment advice.*

---

## Publish process

Artifacts flow from the private engine repo to this public repo through
`scripts/publish.py`, which enforces a strict whitelist:

- `figures/*.png` and `figures/*.svg` — chart images only
- `register/issues_register.csv` — deliberation panel issues register
- `provenance/provenance.csv` — data provenance
- `predictions/directional_calls.csv` — dated directional calls
- `predictions/methodology_hash.txt` — SHA-256 hash of private methodology
- `README.md` — this file

Any file not matching the whitelist is refused. The script exits with error code
1 if any non-whitelisted file is attempted.

*Analytical opinion, not investment advice.*
