# Milestone 1 implementation status

Milestone 1 is **not complete or approved**. This integration PR delivers an executable foundation and historical calculations while keeping unfinished verification visible. No current-data association has been calculated and no release tag has been created or moved.

| Work | Implemented evidence | Remaining acceptance work |
|---|---|---|
| Scaffold | Locked Pixi environment for Linux and Apple silicon; numerical core; source readers; file verification; offline tests; Make commands; immutable run records; Linux/macOS CI and fresh-clone replay pass | Live repository protection settings await separate approval; see docs/repository-setup.md |
| Original access | Official international workbook obtained locally with the recorded planning hash; 23-country and 50-state registries; presence-flag recovery | Full-workbook redistribution permission remains unverified; no released U.S. state file obtained |
| Source lineage | 47 named historical/current-variable rows and original-source records | Each row links to an actual source-route or candidate acquisition attempt; exact counterparts and analysis periods remain unverified. Candidate acquisition is not a comparability finding |
| Historical international reproduction | 26 calculations from supplied values; three named average-income comparisons have explicit missing-input barriers | Independent index rebuilding, source/version conflicts and historical income recovery remain unresolved |
| Historical state reconstruction | Census S4 and FBI 1999 sources obtained; one 49-state homicide reconstruction computed from a prospective specification; 16 other comparisons remain barriers | Remaining historical state outcomes and the independent state-index reconstruction are not yet recovered |
| Current acquisitions | Nine small World Bank indicator responses preserved; current presence flags; Census access failure and 15 source-family verification attempts recorded | Other source families, latest-vintage checks, indicator definitions and populations, and temporal/unit correspondence still need work |
| Reproduction lock | Draft machine-readable gate and current specifications; code rejects current computation before approval | The preliminary component assessment is available in docs/current-index-assessment.md; complete counterpart verification, prospective choices, refreshed eligibility and lock hashes before approval |

## Maintainer decision

On 19 October 2026 the maintainer chose to defer locking the current index until component availability and the consequences of missing components have been documented. Do not introduce a minimum-component threshold or final missingness rule before that assessment. This decision preserves the current gate and does not prevent historical calculations or acquisition/coverage work.

## Verification commands

Run pixi install --locked, then make lint test verify-data check-data check-contracts and make all. The exact restricted international input is documented in data/local_data_required/original-access.md. Without it, the compatible committed result table is retained against its producer record; it is not recomputed. CI executes the public-checkout path on Linux and macOS. The comprehensive final release check remains a separate acceptance step.

## Next work toward milestone acceptance

1. Finish version-specific counterpart verification and obtain nominated statistical tables. Recorded route probes distinguish real attempts from an asserted absence of a current series, but do not establish comparability.
2. Complete the component assessment beyond the preliminary candidate-presence table, including verified source definitions, periods and populations. The present acquisition covers only four of ten international dimensions and cannot justify silently adopting a reduced index.
3. Recover historical state source tables as far as possible and report each real barrier. Resolve historical source/version differences without changing inputs to improve agreement.
4. Resolve the updated period and sample rules, build refreshed eligibility where possible, then complete the prospective lock for review. The existing planning tags do not satisfy this gate.

The previous feasibility corrections are implemented in IMPLEMENTATION_PLAN.md. This status file does not relax its acceptance criteria or claim that an acquired candidate is analysis-ready.

## Validation evidence and counterpart follow-up

CI run [39181200683](https://github.com/open-reanalysis/how-economic-inequality-harms-societies/actions/runs/39181200683), at head a242512, passed on Linux and macOS, including public replay and the numerical committed-output comparison. Local lint, all 25 offline tests, 14 focused integrity/reader tests and full record checks passed. A fresh temporary clone then installed the locked environment, passed 25 tests and completed the public replay without copying restricted inputs. An earlier local fresh-clone attempt failed while loading NumPy late in replay; the cause was not established, and the subsequent fresh installation/replay passed. Do not report the failed attempt as a successful run.

The [index counterpart review](source_verification/index-counterparts.md) adds official metadata checks and joint period coverage. All four acquired international candidate dimensions have common coverage of 23 countries in 2021, but only 18 in 2023 and none in 2024 in the stored responses. This is not a period selection: six dimensions remain unacquired, continuity is unresolved, and the consequences for the index still require a prospective decision. No current index or association was calculated.
