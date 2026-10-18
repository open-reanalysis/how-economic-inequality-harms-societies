# Research Method: Reproducing and Presenting Wilkinson and Pickett’s Data Without Issuing a Verdict

## Purpose

This project acquires, documents, reproduces, updates, and visualises the data and calculations cited by Richard Wilkinson and Kate Pickett. Its purpose is to let users inspect the observations, sources, calculations, figures, and deviations and draw their own conclusions.

The project does not decide whether Wilkinson and Pickett are right or wrong. It does not attempt to prove or disprove causality, resolve the published controversies, or issue an overall verdict. Supporting and critical materials are collected and presented transparently, but neither is adopted as the project’s own position.

## Documents

This document is the research method. [INTENT.md](INTENT.md) sets the goals and the scope, and [IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md) sets the technical implementation and the order of the work. The exact choices of each calculation are in the machine-readable analysis specifications in `config/specs/`, and `docs/method_rationale.md` records the source, the reason and the status of each choice. Other documents summarise this one and link to it.

## Research goals

The project has six goals, in priority order:

1. Download current versions of the datasets used by Wilkinson and Pickett.
2. Reproduce their reported findings from the historical data and apply the documented calculations to current data.
3. Download a folder-based package of sources supporting their findings, including academic and non-academic sources.
4. Download a folder-based package of sources setting out controversies about their findings.
5. Download additional datasets needed to investigate those controversies.
6. Publish the reproduced data, figures, calculations, sources, and deviations through a GitHub Pages site.

Goals 1–5 produce the research deliverables. Goal 6 presents those deliverables for public inspection. Publication must not redefine the analyses or add substantive conclusions.

## Governing principle

The method follows the smallest set of rules needed to make the same inputs produce the same published outputs. It does not invent general methodological rules for hypothetical edge cases that do not occur in the data.

A choice is specified in advance when all three conditions hold:

1. a real ambiguity exists in the available sources or data;
2. alternative treatments could change the observations or reported result; and
3. the choice must be made before the result is calculated.

If an ambiguity does not affect the result, it is documented only when encountered. If an original methodological choice cannot be verified, the project records the assumption and does not present it as a verified decision by Wilkinson and Pickett.

## Role of the research system

The research system performs source tracing, data acquisition, documentation, calculation, validation, and visualisation. It may make technical choices required to execute the documented analysis, but it must distinguish those choices from substantive interpretation.

The system must:

- identify the historical datasets and variables;
- obtain the closest current versions of those variables;
- preserve provenance, definitions, periods, units, transformations, and source links;
- reproduce the reported calculations;
- present historical and current results separately;
- expose the plotted observations and downloadable data;
- document missing data and departures from the historical calculation;
- collect supporting and critical sources without adopting either position; and
- state clearly when a result could not be reproduced.

The system must not:

- declare Wilkinson and Pickett correct or incorrect;
- infer causality from reproduced correlations;
- decide that a criticism is correct merely because a reproduced value differs;
- choose a source, period, transformation, or sample because it produces a preferred result;
- introduce new models solely to strengthen or weaken the original argument;
- silently replace the reported construct with a different measure; or
- issue an overall evidential or policy verdict.

## Reproduction scope

“Reproduce their findings” means reproducing the reported international-country and United States state-level associations that are identifiable in the released data and methodological materials and computable from the historical datasets assembled by the project.

The scope includes:

- each identified indicator-level correlation;
- each identified composite-index correlation;
- the corresponding country or state observations;
- comparisons with average income when these are reported from the same datasets;
- the calculation of the same identified results using current data when a sufficiently comparable current series is available; and
- the separate presentation of international and United States state results.

The scope does not automatically include every figure, sentence, mechanism claim, causal claim, or policy recommendation made across Wilkinson and Pickett’s publications. Such claims may be recorded in a claims register, but they are tested only when the project explicitly includes the underlying reported analysis.

A compact result catalogue, `config/results_catalogue.csv`, lists the target results before calculation. Calculation and reporting both read it, and no other list of target results is kept. The source lineage does not define a result, because one variable can appear in several comparisons.

```text
result_id
dataset
indicator_or_index
predictor
sample
reported_statistic
reported_value
source_reference
historical_reproduction_required
current_reproduction_required
notes
```

The list prevents selective reproduction without creating a larger claims-adjudication programme.

## Results and their properties

Every target result is calculated as a historical result and, where the data allow, as three current results, all within the agreed scope.

- **Historical result.** The historical data and the documented historical method, on the historical sample.
- **Primary current result.** The fixed historical sample populated with current data, using exact and conceptual successor series.
- **Parallel current result with a refreshed sample.** The eligibility-refreshed current sample, with the same series.
- **Parallel current result with substitutes.** The fixed historical sample, adding substitute measures.

No other sample, outcome, measure or model is calculated.

Each result records five properties separately, because no single category can express them all.

- **Data provenance.** Released historical data, reconstructed data, combined data or current data, and for a historical result the access label of its dataset.
- **Sample.** Historical, fixed or refreshed, with the units included and missing.
- **Series comparability.** For a current result, the lowest comparability class among the series it uses.
- **Method deviations.** Every disclosed change from the historical calculation, such as a conceptual successor series, a changed index component set or an approved assumption.
- **Replay state.** Whether the result was calculated in the run, retained because a required input was missing, or not produced.

A substitute measure is never presented as an unchanged data update.

## Access to the original data

Access is decided separately for the international data and for the United States state data, from the records of the retrieval attempts, and it gives the label of every historical result of that dataset.

| Status | Definition | Label |
|---|---|---|
| `verified_release` | Files download and hash, contain usable original data, and carry enough documentation to identify variables and units. | `DIRECT REPRODUCTION` |
| `incomplete_release` | Some files download, but required sheets, metadata, source notes or formulas are missing. | `PARTIAL REPRODUCTION` |
| `archived_copy` | A credible archive or third party supplies historical files, but provenance to the original release cannot be fully verified. | `ARCHIVE-BASED RECONSTRUCTION` |
| `unavailable` | No usable original package is accessible. | `INDEPENDENT RECONSTRUCTION` |

## Source lineage

Each reproduced variable has a lineage from the historical source to the current source. The record contains only information needed to understand and reproduce the calculation:

```text
variable_id
dataset
role
historical_definition
historical_source
historical_period
historical_unit
historical_transformation
current_source
current_series
current_period
comparability_class
deviation_reason
verification_status
notes
```

The technical record of each retrieval, with its request, date, files, sizes and checksums, is kept once in the acquisition records described in the implementation plan, and the lineage refers to data sources by their IDs. The lineage covers the inequality measure, average income, every index component and extra measure, and the income and population series of the eligibility rule. The comparability classes are `EXACT_SUCCESSOR`, `CONCEPTUAL_SUCCESSOR`, `SUBSTITUTE`, `NO_CURRENT_EQUIVALENT` and `NOT_YET_VERIFIED`, and a row stays `NOT_YET_VERIFIED` only with a logged verification attempt and its reason.

Where more than one source is plausible, the primary source is selected by a documented source rule before examining the result. Where two sources give values for the same variable and unit, the values are compared and every difference is published. The other source then fills only the gaps of the primary one, after units are harmonised, and the combined series is the project's own, with every value keeping its source. Values are never averaged, and no source is selected according to which produces the closest correlation. In historical data the released file is primary, and a value filled from another source counts as reconstructed. Three disagreements between the released international file and the authors' notes are known: infant mortality is World Bank 2000 in the notes and OECD 2005 in the file, homicides are a rate per 100,000 for 1990 to 2000 in the notes and per million for 1999 to 2000 in the file, and the education score is PISA 2000 in the notes and PISA 2003 in the file.

## Historical method uncertainty

Published data, methodological notes, author responses, and legally accessible primary materials are used to reconstruct the historical method. Missing access to a book or source does not stop all work, but the project must not convert an inference into a verified historical fact.

Method details use statuses such as:

- `VERIFIED_FROM_PRIMARY_SOURCE`;
- `VERIFIED_FROM_RELEASED_DATA`;
- `INFERRED_FROM_AUTHOR_MATERIALS`;
- `USER_APPROVED_ASSUMPTION`; and
- `UNRESOLVED`.

User approval determines how the project proceeds when a decision is unavoidable. It does not prove that the approved choice was the original authors’ choice. Any material uncertainty appears with the relevant result. Each choice in a specification records its status.

The book itself is not used, and every report states this as a limitation. The method rests on the released international data with its sources sheet and errata, the Equality Trust's notes on statistical sources and methods, its frequently asked questions, the authors' 2010 responses to their critics and the released United States state data when they can be obtained. *The Spirit Level at 15* and its technical appendix are used only for what they say about the original method, its timing and the meaning of 80:20, and the results are not compared with the 2024 update. The assumptions approved before the run are listed in `docs/worklist.md`. A point they do not cover is put to the user before the calculation that depends on it. No country count or correlation from a secondary source, such as the draft brief's 21 countries or r ≈ 0.85, is used as a target.

### Facts to establish

- The source the authors used for each variable, and whether that series still exists.
- The ranking series and vintage of the eligibility rule, and the source that counted as comparable income distribution data.
- The historical country list and the sample of each target result.
- The inequality measure and its years. The appendix calls 80:20 a decile ratio, while the notes describe the 20:20 ratio of the incomes of the richest and the poorest fifths, averaged from the UN Human Development Reports of 2003 to 2006, and the notes' description is used.
- The average income measure of each dataset and the comparisons reported with it.
- The direction coding of every index component, fixed per measure rather than per concept.
- The historical handling of missing index components.
- The historical timing, which the appendix describes as an inequality measure averaged from values reported in 2003 to 2006 and measured in 1992 to 2001, with outcomes from 1999 to 2004, checked against the notes.

## Samples and eligibility

The project distinguishes three samples:

1. the historical sample used for historical reproduction;
2. the fixed historical sample populated with current data; and
3. an eligibility-refreshed current sample, when the historical eligibility rule can be applied to current data.

The fixed sample is the primary current sample, and the refreshed sample gives a parallel result. The historical country sample is the 23 countries in the released international data, and the historical state sample is the 50 states, with the District of Columbia excluded unless the original material shows otherwise. The authors state the eligibility rule in their 2010 response to Peter Saunders's report for Policy Exchange: a country is eligible when it is among the 50 richest countries in the world, has more than 3 million people and has comparable income distribution data. Market democracy is the authors' reason for the rule, not a condition of it. For the states the rule is all 50 states, so the refreshed state sample equals the fixed one and is reported once with that note.

The refreshed sample applies the documented rule to a declared current data vintage. A historical check applies the rule to the ranking vintage in the approved assumptions and compares the result with the released 23 countries. If that vintage cannot be obtained, the check is not made and the reason is recorded. At minimum, the project records the ranking series and period, the population threshold, and the source used to determine whether comparable income-distribution data exist. Outcome values and outcome availability never determine master-sample eligibility.

Only ambiguities that actually affect country inclusion require an additional decision. For example, a tie rule is needed only if a consequential tie occurs. Every included and excluded country is listed with a short reason, while common source information is stored once in the sample metadata rather than duplicated unnecessarily.

A minimal eligibility table is:

```text
country
rank_value
rank
population
comparable_inequality_data
eligible
exclusion_reason
```

Outcome-specific missingness is reported separately. A country may remain eligible for the master sample while being absent from one result because that outcome is unavailable.

## Index and missing components

The index is standardised and combined as the documented historical procedure did it. A unit with missing components is handled by the historical rule if that rule can be established. If it cannot, the choice is approved by the user before any index is calculated and recorded as an assumption. No numeric comparability threshold, such as a minimum number of components, is introduced without a stated basis and that approval.

Every index result reports the component set it used, the availability of each component per unit, and how its component set differs from the historical index. A current index whose component set changed is reported as a changed index, never as the historical index with newer data. The reproductions impute nothing and delete no outliers.

## United States state reconstruction

When a released state-level file is unavailable, the project reconstructs the variables from the sources, periods, and transformations stated in the authors’ methodological materials. Those choices and the acceptance tolerance are recorded before calculating the target correlation.

Agreement with the reported statistic is a validation check, not a tuning objective. Inputs are not revised after seeing the statistic except to correct a documented extraction or coding error. If the independently selected inputs produce the reported result within the declared tolerance, the comparison is recorded. If important source or method details remain uncertain, the result is labelled as a reconstruction.

The first release may be completed with a partial state reconstruction. The acquisition attempts, the missing inputs, the uncertain method points and the target results that could not be reproduced are then documented, and the partial status is shown with every state result. The access and reproduction labels of the international data and of the state data are decided separately, and the two datasets are never pooled.

The historical state sources come from the authors' notes. The candidate current series are starting points for the source lineage, which confirms each one and assigns its class.

| Variable | Historical definition, period and source | Candidate current series | Expected class |
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
| Average income | As the notes name it | As the source lineage finds it | Assigned by the source lineage |

The notes list nine index components for the states but say that 40 states have all eight measures, and the state index uses all nine until the released file settles which is right. The notes report trust as missing for Alaska, Delaware, Hawaii, Idaho, Maine, Nebraska, New Mexico, Nevada and South Dakota, and homicides as missing for Wyoming.

## Source packages

Supporting and controversy materials are kept in separate folder-based packages with a shared documentation standard:

```text
sources/
  supporting/
    academic/
    original-authors/
    responses/
    non-academic/
    manifest.csv
    README.md
  controversies/
    academic/
    books/
    reports/
    responses/
    manifest.csv
    README.md
```

The supporting package includes academic sources as well as relevant non-academic materials. The controversy package identifies each criticism through an author, exact title, year, publication, and stable identifier or URL. Replies and responses are linked to the relevant criticism rather than treated as the project’s conclusion.

Both packages are searched and screened by one protocol.

- **Topics.** Income inequality and health and social outcomes across rich countries and across United States states, the data, index and analyses of *The Spirit Level*, and the critiques of them and the replies.
- **Services.** OpenAlex, Crossref and PubMed, the Equality Trust site, and the works the authors and their critics cite.
- **Cut-off.** One search cut-off date, recorded in the worklist and in each package README.
- **Citation chaining.** One step backward through the references and one step forward through the citing works of the seed works in the controversy register and of the authors' own works, and no further.
- **Inclusion.** A source with an identifiable author, a citable record and an argument or evidence about the findings or the hypothesis behind them. Whether it supports or criticises the findings never decides inclusion.

Every search is logged in the package's `search_log.csv` and every screening decision in its `screening_log.csv`, and the package README states the known gaps. A package is complete when the protocol has been carried out and documented. Completion does not mean finding every possible source, and the two packages need not hold equal numbers of sources. The supporting package needs at least one peer-reviewed study by authors other than Wilkinson and Pickett.

Legally obtainable texts are downloaded into the declared research workspace. Redistributable files may be published when the terms for the exact version permit it. Other files remain in a documented local location where lawful, with provenance and a checksum recorded. A public link or open-access label alone is not treated as permission to redistribute a file.

## Controversy-related datasets

Additional datasets are collected because they are needed to investigate identified controversies, not because the project presumes that they support either side. Each testable controversy is mapped to the variables, geography, years, and candidate sources it would require.

Before anything is acquired, the variables, geographic coverage and years each controversy needs are defined in its row of the controversy data map. The smallest justified data package that meets that definition is then acquired, and a dataset that several controversies need is acquired once and linked to each of them. Each row ends as `acquired`, `partially_acquired` or `barrier_documented`, the last with the concrete access, licensing or availability barrier. The map keeps the coverage obtained apart from what the data could later be used to study. No statistical test of any controversy is run in this project.

## Calculations and validation

The project calculates only the statistics needed to reproduce the identified findings and current-data counterparts. It does not add models or diagnostics merely to comment on the adequacy of the original research.

Validation checks that:

- the intended source files and versions were used;
- transformations follow the documented method;
- sample membership is recorded;
- missing observations are visible;
- calculated values can be regenerated from stored inputs;
- reported comparison values resolve to conventional source citations; and
- no source or processing choice was selected after examining whether it favoured Wilkinson and Pickett or their critics.

A reported value that cannot be independently recreated is retained as a cited comparison value, not silently treated as reproduced. A difference between a reproduced and a reported value is a research result. It is logged in the discrepancy log with its likely cause, does not by itself mean a software error, and is never used to tune the calculation.

## Visual presentation

The GitHub Pages site is a transparent data presentation, not an argumentative verdict. For each included result, it should show where available:

1. the result reported by Wilkinson and Pickett;
2. the historical reproduction;
3. the fixed-sample current result;
4. the parallel current results with the refreshed sample and with substitutes;
5. the observations underlying the plot;
6. the countries or states included and missing;
7. source, period, variable, and comparability information;
8. disclosed deviations from the historical calculation; and
9. a downloadable table containing the displayed data.

The download contains exactly the observations the figure plots, where the licensing terms allow publishing them. Interactive features, such as switching between historical and current data, identifying a country or state from its plotted point or showing and hiding the fitted line, are a later addition, not a condition of the first version, and need no new application framework.

The site may make descriptive statements such as:

> Wilkinson and Pickett reported this association.

> The historical reproduction produced the following value.

> Applying the documented calculation to the current dataset produced the following result.

> This variable differs from the historical definition in the following way.

The site must not state that the reproduced association proves or disproves Wilkinson and Pickett, establishes causality, resolves a criticism, or confirms a policy effect.

## Symmetry and neutrality

Neutrality means preserving the distinction between source claims, reproduced calculations, and project interpretation.

- Wilkinson and Pickett’s claims are stated accurately before any criticism is linked to them.
- Criticisms are attributed to identifiable sources and represented faithfully.
- Responses are linked to the claims or criticisms they address.
- Supporting and critical materials use the same bibliographic and provenance requirements.
- Data and method decisions are not changed according to the direction or significance of a result.
- Deviations are reported whether they strengthen, weaken, or leave unchanged the reported association.

The project does not manufacture false balance. It reports what was found under the documented collection procedure and leaves the evidential assessment to users.

## Reporting boundaries

The final report explains what was reproduced, reconstructed, updated, or not reproducible. It distinguishes calculation from interpretation and uses conventional citations that resolve to stable sources.

The report does not infer a mechanism from an aggregate association. It also does not introduce an opposing methodological standard that was not part of the reproduction. Questions about mechanisms, causality, policy effects, or the ultimate merits of published criticisms remain visible through the claims and source packages but outside the project’s own verdict.

## Completion criteria

The research is complete when:

- current versions or documented absence statuses exist for the historical variables;
- every target result has a historical reproduction, reconstruction, or documented barrier, and a partial United States state reconstruction is documented as partial;
- current counterparts are calculated where sufficiently comparable data exist;
- the supporting package contains academic and non-academic sources found under the documented search protocol, with its known gaps stated;
- the controversy package identifies criticisms and responses through resolvable sources;
- controversy-related datasets or documented barriers are present;
- each figure and table can be traced to data, code, source metadata, and a declared sample;
- the research deliverables of goals 1 to 5, with a headline table and a short summary of the deviations, can be read on their own without the site;
- the Pages site exposes the data and calculations needed for independent inspection; and
- neither the report nor the site issues an overall verdict.

The governing test is simple: a user should be able to see what Wilkinson and Pickett reported, inspect what the project reproduced with historical and current data, understand every material deviation, download the observations, consult supporting and critical sources, and form an independent conclusion.