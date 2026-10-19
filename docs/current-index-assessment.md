# Current-index availability assessment

This is a prospective availability assessment, not an index result or a reproduction lock. It uses only recorded presence flags across the acquisition window. A candidate observation in any year does not establish that an admissible observation exists for the final analysis period. Blank availability means no parsed candidate in this run, not an absent series.

| Dataset | Historical component | Units with a nonmissing candidate in at least one acquired year | Master sample |
|---|---|---:|---:|
| international | trust | 0 | 23 |
| international | life_expectancy | 23 | 23 |
| international | infant_mortality | 23 | 23 |
| international | obesity | 23 | 23 |
| international | mental_illness | 0 | 23 |
| international | education | 0 | 23 |
| international | teenage_births | 23 | 23 |
| international | homicides | 23 | 23 |
| international | imprisonment_log | 22 | 23 |
| international | social_mobility | 22 | 23 |
| us_states | trust | 0 | 50 |
| us_states | life_expectancy | 0 | 50 |
| us_states | infant_mortality | 0 | 50 |
| us_states | obesity | 0 | 50 |
| us_states | mental_illness | 0 | 50 |
| us_states | education | 0 | 50 |
| us_states | teenage_births | 0 | 50 |
| us_states | homicides | 0 | 50 |
| us_states | imprisonment | 0 | 50 |

## Consequences before locking

The table separates source correspondence from availability. The lineage nominates conceptual successors for life expectancy, infant mortality, teenage births, homicide and imprisonment. WHO adult obesity is held as a substitute pending resolution of historical age/sex conventions; GDIM income elasticity is a substitute for the historical intergenerational income correlation. Neither substitute enters the primary series set merely because it downloaded successfully.

Trust, diagnostic mental-health prevalence and education still have access or aggregate-table verification barriers. No acquired primary candidate covers all ten historical dimensions. The international primary index cannot currently reproduce the intended component set; its complete-case sample across all ten is empty. A substitute variant would still lack three dimensions, and mobility refers to cohorts rather than a recent annual period.

Averaging only available dimensions changes the construct and gives countries different effective weights. Restricting to complete cases loses every country while unresolved components remain absent. A lower minimum, new weights or a wider date window would be scientific choices, not consequences of a download. No current index is calculated. The concrete proposed disposition is to keep individual eligible measures and mark current index variants not_produced until a prospective rule is approved.

The U.S. state index has its own source targets. National international-series availability cannot fill state cells. The Census income request returned Missing Key HTML and current state outcome tables have not been parsed. State BRFSS mentally unhealthy days are distinct from diagnostic prevalence, corrected historical obesity differs from raw self-report, and national GSS trust cannot replace state identifiers.

## Maintainer decision

On 19 October 2026 the maintainer chose to defer the current-index lock until component availability and its consequences are documented. This assessment records the present evidence and exposes remaining verification work. It does not treat that decision as approval of a reduced index. Updated specifications and the executable lock remain in draft; no current association was computed.
