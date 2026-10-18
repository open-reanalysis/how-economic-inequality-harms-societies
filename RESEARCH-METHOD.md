# Research method

This document is the research method. It says what the project computes and collects, and by which rules. [INTENT.md](INTENT.md) sets the goals and the scope. [IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md) sets how the method is implemented and in which order the work is done. The exact choices of each computation, such as years, directions, weights and samples, are in the machine-readable analysis specifications in `config/specs/`, and `docs/method_rationale.md` records the source or the reason for each of those choices. Other documents summarise this one and link to it.

## Original material

The book itself is not used, and every report states this as a limitation. The method rests on what the authors and the Equality Trust published about the book's data and methods:

- the released international data, `international-inequality.xls`, with its sources sheet and errata
- the Equality Trust page "Notes on Statistical Sources and Methods", read through its Internet Archive copy of 7 January 2017
- the Equality Trust's frequently asked questions and the authors' 2010 responses to their critics
- the released U.S. state data, when they can be obtained

*The Spirit Level at 15* and its technical appendix are used only for what they say about the original method, its timing and the meaning of 80:20. The project does not compare its results with the 2024 update.

Every fact a rule relies on is logged in `docs/source_verification/` with the passage, table or file it came from. Where the material leaves a point open, an assumption fills it. The assumptions are listed in [docs/worklist.md](docs/worklist.md) and approved by the user before the run. A point they do not cover is put to the user before anything that depends on it is computed.

No country count or correlation from a secondary source is used as a target. The draft brief's 21 countries and r ≈ 0.85 are not benchmarks. Reconstructed sample sizes and coefficients are reported exactly as observed.

## What is reproduced

The reproduction covers the comparisons the authors reported for the international and the U.S. state data:

- income inequality against the Index of Health and Social Problems and against each measure for which the notes give a correlation
- average income against the index or against a measure, wherever the authors reported such a comparison for the same data

Other analyses in the book or in later publications are not included unless a decision adds them.

Each comparison is one row of the result catalogue, `config/results_catalogue.csv`. A row names the dataset, the explanatory variable, the outcome or the index, the sample, the statistic, the published value and the passage it comes from. Computation and reporting both read the catalogue, so a comparison exists once.

## Data sources and their lineage

For each variable and dataset, `docs/source_lineage.csv` records what the variable means, the data source the authors used and the current data source that corresponds to it. The original source is taken from the released file's sources sheet and from the notes, never from a later summary. Where the two disagree, the released file comes first, because it describes the values in the file, and both are recorded. The lineage covers the inequality measure, average income, every index component and extra measure, and the income and population series of the eligibility rule.

Each current series gets one comparability class.

- `EXACT_SUCCESSOR`. The same series from the same provider, with the same definition, unit and population.
- `CONCEPTUAL_SUCCESSOR`. A series that measures the same concept for the same population, but whose provider, survey or method has changed.
- `SUBSTITUTE`. A different measure of a related concept, such as self-reported obesity in place of obesity corrected for self-report bias, or a Gini coefficient in place of an income ratio.
- `NO_CURRENT_EQUIVALENT`. No current series measures the concept for the original units.
- `NOT_YET_VERIFIED`. The original or the current series has not been confirmed. A row stays in this class only with a logged verification attempt and its reason.

Only the series the lineage names are downloaded, so "the data Wilkinson used" never becomes "comparable data" without a recorded reason. A source is never chosen by the strength of the correlation it produces.

## Access to the original data

Access is decided separately for the international data and for the U.S. state data, from the records of the retrieval attempts. A 2017 Equality Trust post saying the data could be downloaded establishes nothing about today.

| Status | Definition | Label |
|---|---|---|
| `verified_release` | Files download and hash, contain usable original data, and carry enough documentation to identify variables and units. | `DIRECT REPRODUCTION` |
| `incomplete_release` | Some files download, but required sheets, metadata, source notes or formulas are missing. | `PARTIAL REPRODUCTION` |
| `archived_copy` | A credible archive or third party supplies historical files, but provenance to the original release cannot be fully verified. | `ARCHIVE-BASED RECONSTRUCTION` |
| `unavailable` | No usable original package is accessible. | `INDEPENDENT RECONSTRUCTION` |

**U.S. state data.** Until the released U.S. state file is obtained, the historical state data are rebuilt from the vintages the notes name, from the agencies' archives and from the two articles' state tables, and every value is flagged reconstructed. The historical state specification, with its sources, years and transformations, and the tolerance of the check against the published values are committed before any state correlation is computed, and are not changed in response to it. A match within the tolerance confirms the rebuild. A mismatch is logged with its likely cause, and the rebuild is not adjusted to close it. The rebuild may remain partial. The acquisition attempts, the missing inputs, the uncertain method points and the catalogue rows that could not be reproduced are then documented, and the partial status is shown in every state result. The state data and the country data are never pooled.

## Samples and eligibility

**Original samples.** The original country sample is the 23 countries in the released international data. The original state sample is the 50 states, with the District of Columbia excluded unless the original material shows otherwise. The sample of a single comparison is the units of its original sample that have both values.

**Fixed sample.** The primary current result keeps the original sample.

**Refreshed sample.** A parallel current result applies the authors' eligibility rule, stated in their 2010 response to Peter Saunders's report for Policy Exchange, published by the Equality Trust. A country is eligible when it meets three conditions, applied in this order.

1. It is among the 50 richest countries in the world.
2. Its population is more than 3 million.
3. It has comparable income distribution data.

The specification fixes only the details that change which countries are eligible: the income measure and data vintage that rank the 50 richest, the year in which income and population are measured, the source that counts as comparable income distribution data, whether economies that are not sovereign states are ranked, and how a tie at rank 50 is broken. The historical check ranks countries by the vintage in the approved assumptions and compares the result with the released 23 countries. If that vintage cannot be obtained, the check is not made and the reason is recorded. The refreshed sample uses the current release of the same income series and the current inequality series. Market democracy is not a condition, because the authors give it as the reason for the rule, not as part of it. For the U.S. states the rule is all 50 states, so the refreshed state sample equals the fixed one, and that result is reported once with this note.

**Independence from outcomes.** Outcome data never decide eligibility. Neither the availability of an outcome nor its value, a correlation, an outlier or significance adds or removes a unit. A unit without a value for one comparison stays in the sample and is left out of that comparison only, and the result lists it among the missing units.

## Variables, years and transformations

For each variable the specification states its series, its reference year or period, its unit, any unit conversion, any transformation and its direction coding, which is fixed per measure rather than per concept. The original timing is taken from the notes and checked against the appendix's description of an inequality measure averaged from values reported in 2003 to 2006 and measured in 1992 to 2001, with outcomes from 1999 to 2004. The inequality measure is the ratio of the incomes of the richest and the poorest fifths, averaged from the UN Human Development Reports of 2003 to 2006, as the notes describe it.

**Parallel data.** Where two sources give values for the same variable and unit, the values are compared, and every differing value is published in a comparison table. They are then combined into the project's own series. The source the specification ranks first is primary, the other fills only its gaps, units are harmonised first, and values are never averaged. Every value keeps its source. In historical data the released file is primary, and a value filled from another source is flagged reconstructed, so the access label shows it. The combining rule is fixed before any correlation is computed. Three disagreements between the released file and the notes are known. Infant mortality is World Bank 2000 in the notes and OECD 2005 in the file. Homicides are a rate per 100,000 for 1990 to 2000 in the notes and per million for 1999 to 2000 in the file. The education score is PISA 2000 in the notes and PISA 2003 in the file.

## The index and missing components

The index is standardised and combined as the authors' documented procedure did it, including the reference population of the z-scores and the weights.

A unit with missing components is handled by the authors' rule if that rule can be established from the released file and the notes. If it cannot, the choice needed is approved by the user before any index is computed and recorded as an assumption. No numeric threshold of comparability, such as a minimum number of components, is introduced without a stated basis and that approval.

Every index result reports the components it used, the availability of each component per unit, and how its component set differs from the historical index. A current index whose component set changed, because a component has no current equivalent or only a substitute, is reported as a changed index, never as the same index with newer data. The reproductions use no imputation and delete no outliers.

## Statistics

The statistics are those the original study reported: the Pearson correlation, its p-value and the number of units. The project adds no statistics of its own. Each figure follows the original graphic conventions and plots exactly the observations of its comparison.

Agreement with a published value is a research result, not a software test. A difference is logged in the discrepancy log with its likely cause. A difference alone does not mean a software error, and the published value is never used to tune the computation.

## Results

Every catalogue row is computed as a historical result and as current results. Three current results are in scope.

| Result | Data | Sample | Series | Role |
|---|---|---|---|---|
| Historical reproduction | Original data | Original sample | Original series | The answer to whether the released data reproduce the reported values |
| Updated reproduction | Current releases | Fixed sample | `EXACT_SUCCESSOR` and `CONCEPTUAL_SUCCESSOR` | The primary current result |
| Updated reproduction, refreshed sample | Current releases | Refreshed sample | As the primary result | Parallel result |
| Updated reproduction, with substitutes | Current releases | Fixed sample | Adds `SUBSTITUTE` series | Parallel result |

In the primary result a component whose only current series is a substitute is treated as missing under the index rule, and the change is reported. A component with `NO_CURRENT_EQUIVALENT` is missing from all current results. If the inequality measure has no exact or conceptual successor, the eligibility rule's third condition cannot be applied, and the refreshed result is reported as not possible with that reason. No other sample, outcome, measure or model is computed.

Each result records five properties separately, because no single label can carry them all.

- **Data provenance.** Released, reconstructed, combined or current data, and for historical results the access label of its dataset.
- **Sample.** Original, fixed or refreshed, with the units used and the units missing.
- **Series comparability.** For current results, the lowest comparability class among the series used.
- **Method deviations.** Every departure from the original method, such as a changed component set or an approved assumption, each with its entry in the discrepancy log.
- **Replay state.** Whether the result was computed in the run, retained because a required input was missing, or not produced, from the run record.

## Declared before examined

The specifications of the current results are fixed before anyone computes, views or infers an association between current inequality data and current outcome data. The reproduction lock identifies them. The blinding is procedural only. The original correlations and the 2024 update's correlations are published, so the lock records which of them its author had seen. A later change to a locked specification is a new version recorded in the lock, and affected results are reported under both versions. Downloading data, reading metadata and checking coverage before the lock are allowed.

## U.S. state sources

The original source of each state variable comes from the notes. The candidate current series are starting points for source lineage, which confirms each one and assigns its class.

| Variable | Original definition, period and source | Candidate current series | Expected class |
|---|---|---|---|
| Income inequality | Gini coefficient by state, 1999, US Census Bureau table S4 | American Community Survey table B19083 | `CONCEPTUAL_SUCCESSOR` |
| Trust | Share agreeing that most people can be trusted, 1999, General Social Survey, reverse coded | General Social Survey by state, whose state identifier is restricted and needs a data agreement with NORC | `NO_CURRENT_EQUIVALENT` unless the restricted data are obtained |
| Life expectancy | At birth, men and women, 2000, Census Population Division interim projections, reverse coded | NCHS U.S. State Life Tables | `EXACT_SUCCESSOR` or `CONCEPTUAL_SUCCESSOR` |
| Infant mortality | Deaths in the first year per 1000 live births, 2002, NCHS | CDC WONDER linked birth and infant death data | `EXACT_SUCCESSOR` |
| Obesity | BMI above 30, men and women averaged, 1999 to 2002, corrected for self-report bias by Ezzati and others, J R Soc Med 2006, PMID 16672759, PMC1457748 | Behavioral Risk Factor Surveillance System, self-reported | `SUBSTITUTE` |
| Mental health | Days in the past month when mental health was not good, 1993 to 2001, BRFSS, as published by Zahran and others, MMWR Surveillance Summaries 2005, PMID 16251867 | BRFSS health-related quality of life, mentally unhealthy days | `EXACT_SUCCESSOR` |
| Education | Grade 8 maths and reading scores combined, 2003, NAEP, reverse coded | NAEP, latest grade 8 maths and reading | `EXACT_SUCCESSOR` |
| Teenage births | Births per 1000 women aged 15 to 19, 2000, National Vital Statistics | CDC WONDER natality | `EXACT_SUCCESSOR` |
| Homicides | Homicides per 100,000, 1999, FBI Crime in the United States | CDC WONDER mortality by homicide, because the FBI series has gaps from the 2021 change to NIBRS | `CONCEPTUAL_SUCCESSOR` |
| Imprisonment | Prisoners per 100,000, 1997 to 1998, Bureau of Justice Statistics, not log transformed | BJS Prisoners series | `EXACT_SUCCESSOR` |
| Average income | As the notes name it | As source lineage finds it | To be assigned by source lineage |

The notes list nine index components for the states but say that 40 states have all eight measures. The state index uses all nine until the released file settles which is right. The notes report trust as missing for Alaska, Delaware, Hawaii, Idaho, Maine, Nebraska, New Mexico, Nevada and South Dakota, and homicides as missing for Wyoming.

## Source packages

The supporting package and the controversy package are searched and screened by one protocol, so the inclusion standard is the same for both.

- **Topics.** Income inequality and health and social outcomes across rich countries and across U.S. states, *The Spirit Level*'s data, index and analyses, and the critiques of them and replies to those critiques.
- **Services.** OpenAlex, Crossref and PubMed, the Equality Trust site, and the works the authors and their critics cite.
- **Cut-off.** One search cut-off date, recorded in the worklist and in each package README.
- **Citation chaining.** One step backward through the references and one step forward through the citing works of the seed works in the controversy register and of the authors' own works, and no further.
- **Inclusion.** A source is included when it has an identifiable author, a citable record and an argument or evidence about Wilkinson and Pickett's findings or the hypothesis behind them. Whether it supports or criticises the findings never decides inclusion.

Every search is logged in the package's `search_log.csv` with its service, query, date and number of hits, and every screened source in its `screening_log.csv` with the decision and its reason. The package README states the known gaps. A package is complete when the protocol has been carried out and documented. Completion does not mean that every possible source was found, and the two packages need not hold equal numbers of sources. The supporting package needs at least one peer-reviewed study by authors other than Wilkinson and Pickett.

Every legally obtainable text is downloaded. A text whose terms allow publishing is published in its package. Any other text is kept locally and recorded with its link, an archived landing page where it has no DOI, and the SHA-256 of the file read.

## Controversies and their data

A controversy enters the register only with the author's name, the exact title, the year and a stable DOI, PMID, PMCID, ISBN or URL, checked against its record, and a book also needs its edition. Generic critiques that no named author made are excluded. A criticism that predates *The Spirit Level* or addresses the hypothesis in general, such as Ken Judge 1995 or Hugh Gravelle 1998, is recorded as a general-hypothesis criticism with the result it bears on.

For each registered controversy with a testable statement, the variables, the geographic coverage and the years needed are defined in its row of the controversy data map before anything is acquired. The smallest justified data package that meets that definition is then acquired. A dataset that several controversies need is acquired once and linked to each of them. A row ends in one of three states: `acquired`, `partially_acquired` or `barrier_documented`, the last with the concrete access, licence or availability barrier. The map keeps the coverage obtained apart from what the data could later be used to study. The project runs no statistical test of any controversy. The data may later support a criticism, weaken it, support the original finding or leave the question open, and the map describes them in those neutral terms.

## Facts to establish

Each of these is logged in the source-verification log before use. Where the material does not settle one, the approved assumptions or a decision by the user settle it.

- The data source the authors used for each variable, and whether that series still exists.
- The measure and data vintage that rank the 50 richest countries, and the source that counted as comparable income distribution data.
- The original country list, the sample of each comparison and the index sample.
- The inequality measure and its years. The appendix calls 80:20 a decile ratio, while the notes describe the 20:20 ratio of the incomes of the richest and the poorest fifths, and the notes' description is used.
- The average income measure in each dataset, and which comparisons with it the authors reported.
- The direction coding of every index component, fixed per measure rather than per concept.
- The original handling of missing index components.
- The original timing, as described above.
- The current availability and terms of the Equality Trust data files.
