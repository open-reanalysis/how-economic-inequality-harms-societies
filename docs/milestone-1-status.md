# Milestone 1 implementation status

Milestone 1 is **not complete or approved**. This integration PR delivers an executable foundation and historical calculations while keeping unfinished verification visible. No current-data association has been calculated and no release tag has been created or moved.

| Work | Implemented evidence | Remaining acceptance work |
|---|---|---|
| Scaffold | Locked Pixi environment for Linux and Apple silicon; numerical core; source readers; file verification; offline tests; Make commands; immutable run records; CI workflow | Check both CI platforms and fresh-clone replay before treating the scaffold as accepted |
| Original access | Official international workbook obtained locally with the recorded planning hash; 23-country and 50-state registries; presence-flag recovery | Full-workbook redistribution permission remains unverified; no released U.S. state file obtained |
| Source lineage | 47 named historical/current-variable rows and original-source records | Rows explicitly marked not_started need real counterpart verification; candidate acquisition is not a comparability finding |
| Historical international reproduction | 26 calculations from supplied values; three named average-income comparisons have explicit missing-input barriers | Independent index rebuilding, source/version conflicts and historical income recovery remain unresolved |
| Historical state reconstruction | All 17 reported comparisons remain visible as barriers | Numerical source recovery has not yet been completed; a barrier table is not described as a completed reconstruction |
| Current acquisitions | Nine small World Bank indicator responses preserved; current presence flags; Census Missing Key response recorded as an access failure | Other source families, latest-vintage checks, indicator definitions and populations, and temporal/unit correspondence still need work |
| Reproduction lock | Draft machine-readable gate and current specifications; code rejects current computation before approval | Complete current-component availability and consequences; resolve prospective choices, refreshed eligibility and lock hashes; maintainer review |

## Maintainer decision

On 19 October 2026 the maintainer chose to defer locking the current index until component availability and the consequences of missing components have been documented. Do not introduce a minimum-component threshold or final missingness rule before that assessment. This decision preserves the current gate and does not prevent historical calculations or acquisition/coverage work.

## Verification commands

Run pixi install --locked, then make lint test verify-data check-data check-contracts and make all. The exact restricted international input is documented in data/local_data_required/original-access.md. Without it, the compatible committed result table is retained against its producer record; it is not recomputed. CI executes the public-checkout path on Linux and macOS. The comprehensive final release check remains a separate acceptance step.

## Next work toward milestone acceptance

1. Complete source-family verification and acquisition attempts for the remaining lineage rows, distinguishing a failed attempt from work not started and from an absent current series.
2. Produce the component-by-country availability assessment, including which index components and populations would change. Record the consequences before proposing an index rule.
3. Recover historical state source tables as far as possible and report each real barrier. Resolve historical source/version differences without changing inputs to improve agreement.
4. Resolve the updated period and sample rules, build refreshed eligibility where possible, then complete the prospective lock for review. The existing planning tags do not satisfy this gate.

The previous feasibility corrections are implemented in IMPLEMENTATION_PLAN.md. This status file does not relax its acceptance criteria or claim that an acquired candidate is analysis-ready.
