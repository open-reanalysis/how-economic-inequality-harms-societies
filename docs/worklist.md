# Worklist

This file holds the schedule and the decisions of the current run. The technical plan in [IMPLEMENTATION_PLAN.md](../IMPLEMENTATION_PLAN.md) does not depend on them. The integrator keeps this file up to date.

## Current run

The implementation runs in one day, 19 October 2026. No step waits for material that cannot be obtained that day. The threads start in the wave order of the plan as soon as their gates pass.

| Order | Work | Waits for you |
|---|---|---|
| 1 | Scaffold | Merge of the planning pull request |
| 2 | Original access, supporting sources, controversy sources and register, claims register | None |
| 3 | Source lineage, historical reproduction | Agreement on each open point of the method rationale |
| 4 | Inequality data, outcome data | Acceptance of the CDC WONDER terms of use |
| 5 | Reproduction lock | None |
| 6 | Milestone 1 review and `milestone-1` tag | Your review and approval of the method rationale, the historical specifications and the lock |
| 7 | Updated reproduction, controversy test data | None |
| 8 | Release check, milestone 2 review and `deliverables-v1` tag | Your review |
| 9 | Report, release check, milestone 3 review and `results-v1` tag | Your review |

## Decisions for this run

- The book is not used.
- The released U.S. state data cannot be requested from the Equality Trust within the day, so the historical state data are rebuilt. The released file is a later addition.
- The restricted General Social Survey state data are not applied for, so trust has no current equivalent for the states.
- The current homicide source for the states is CDC WONDER. You accept its terms of use.
- Git LFS is not used.
- Connecting the repository to Zenodo is left for later.
- Whether to register research use of *The Spirit Level at 15* with the Equality Trust is still yours to decide.
