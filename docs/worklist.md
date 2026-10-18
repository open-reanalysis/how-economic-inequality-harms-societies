# Worklist

This file holds the schedule and the decisions of the current run. The technical plan in [IMPLEMENTATION_PLAN.md](../IMPLEMENTATION_PLAN.md) does not depend on them. The integrator keeps this file up to date.

## Current run

The implementation runs in one day, 19 October 2026. No step waits for material that cannot be obtained that day. The threads start in the wave order of the plan as soon as their gates pass.

| Order | Work | Waits for you |
|---|---|---|
| 0 | Approval of the assumptions below | Your approval |
| 1 | Scaffold | Merge of the planning pull request |
| 2 | Original access, supporting sources, controversy sources and register, claims register | None |
| 3 | Source lineage, historical reproduction. The historical state specification and its tolerance are committed before any state correlation is computed | Only a point the approved assumptions do not cover |
| 4 | Inequality data, outcome data | Acceptance of the CDC WONDER terms of use |
| 5 | Reproduction lock | None |
| 6 | Milestone 1 review and `milestone-1` tag | Your review and approval of the method rationale, the historical specifications and the lock |
| 7 | Updated reproduction, controversy test data | None |
| 8 | Release check, milestone 2 review and `deliverables-v1` tag | Your review |
| 9 | Report, release check, milestone 3 review and `results-v1` tag | Your review |

## Assumptions approved before the run

These fill the points the authors' published material leaves open. The historical reproduction thread writes them into the specifications and their reasons into the method rationale.

- The method is taken from the released international data with its sources sheet and errata, the notes on statistical sources and methods, the frequently asked questions and the authors' 2010 responses.
- Where the released file and the notes disagree, the released file is primary and the notes only fill its gaps, under the rule for parallel data.
- The inequality measure is the ratio of the incomes of the richest and the poorest fifths, averaged from the UN Human Development Reports of 2003 to 2006, as the notes describe it.
- The fixed country sample is the 23 countries in the released file.
- The state sample is the 50 states without the District of Columbia, and the state index uses the nine components the notes list.
- Index components, their direction and the handling of missing components follow the released file and the notes. A point neither settles is put to you.
- For the historical eligibility check, the 50 richest countries are ranked by gross national income per capita by the Atlas method from the April 2004 World Development Indicators. The other details that change which countries are eligible, the measurement year, the source of comparable income distribution data, non-sovereign economies and ties at rank 50, are put to you if the authors' material does not settle them.
- The analyses are the correlations the authors reported, as listed by the lineage rows with a reported correlation.

## Decisions for this run

- The book is not used.
- The released U.S. state data cannot be requested from the Equality Trust within the day, so the historical state data are rebuilt. The released file is a later addition.
- The restricted General Social Survey state data are not applied for, so trust has no current equivalent for the states.
- The current homicide source for the states is CDC WONDER. You accept its terms of use.
- Git LFS is not used.
- Connecting the repository to Zenodo is left for later.
- Whether to register research use of *The Spirit Level at 15* with the Equality Trust is still yours to decide.
