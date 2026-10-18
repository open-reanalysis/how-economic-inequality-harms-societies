# Worklist

This file holds the schedule, the approved assumptions and the decisions of the current run. The research method and the implementation plan do not depend on them. The integrator keeps this file up to date.

## Current run

The implementation runs in one day, 19 October 2026. No step waits for material that cannot be obtained that day. The threads start in the wave order of the plan as soon as their gates pass.

| Order | Work | Waits for the maintainer |
|---|---|---|
| 0 | Approval of the assumptions below | Approval |
| 1 | Scaffold | Merge of the planning pull request |
| 2 | Original access, supporting sources, controversy sources and register, claims register | None |
| 3 | Source lineage, then historical reproduction with the result catalogue. The historical state specification and its tolerance are committed before any state correlation is computed | A point the approved assumptions do not cover, before the computation that depends on it |
| 4 | Inequality data, outcome data | Acceptance of the CDC WONDER terms of use |
| 5 | Reproduction lock | None |
| 6 | Milestone 1 review | Review and approval of the catalogue, the method rationale, the historical specifications and the lock |
| 7 | Updated reproduction with the headline table and the discrepancy summary, controversy test data | None |
| 8 | Release check, milestone 2 review and `deliverables-v1` release | Review |
| 9 | Site, release check, milestone 3 review | Review |

The tags `milestone-1`, `deliverables-v1` and `results-v1` already exist on the planning commit `1a26437`. At each approval the integrator asks whether to move the tag or to use a new name.

## Assumptions approved before the run

These fill points the authors' published material leaves open. The historical reproduction thread writes them into the specifications and their reasons into the method rationale.

- The method is taken from the released international data with its sources sheet and errata, the notes on statistical sources and methods, the frequently asked questions and the authors' 2010 responses.
- For reproduction of the available released file, its values are primary and compatible secondary sources may fill only documented gaps, flagged as reconstruction. A conflict with the notes or a dated correction is evaluated against the historical version being reproduced under the research method; the available file does not automatically override evidence about the original publication or a later correction.
- The inequality measure is the ratio of the incomes of the richest and the poorest fifths, averaged from the UN Human Development Reports of 2003 to 2006, as the notes describe it.
- The original country sample is the 23 countries in the released file. The original state sample is the 50 states without the District of Columbia, and the state index uses the nine components the notes list.
- The comparisons reproduced are those the notes and the released file report for these data, including those with average income.
- Index components and their direction follow the released file and the notes. The handling of missing components follows the authors' rule if the released file and the notes establish it. If they do not, the choice is put to the maintainer before any index is computed, and no minimum number of components is set without that approval.
- For the historical eligibility check, the 50 richest countries are ranked by gross national income per capita by the Atlas method from the April 2004 World Development Indicators. The other details that change which countries are eligible are put to the maintainer if the authors' material does not settle them.
- The U.S. state reconstruction may remain partial in the first release, with its gaps documented.
- The search cut-off date for both source packages is 19 October 2026.

## Decisions for this run

- The book is not used.
- The released U.S. state data cannot be requested from the Equality Trust within the day, so the historical state data are rebuilt. The released file is a later addition.
- The restricted General Social Survey state identifiers are not applied for in this run. Record this as an acquisition/access barrier and document which data are missing. Verify the current trust series' comparability separately in the lineage; lack of permission alone never justifies NO_CURRENT_EQUIVALENT.
- The current homicide source for the states is CDC WONDER. The maintainer accepts its terms of use.
- Git LFS is not used.
- Connecting the repository to Zenodo is left for later.
- Whether to register research use of *The Spirit Level at 15* with the Equality Trust is still the maintainer's decision.
