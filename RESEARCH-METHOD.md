# Research Method: Reproducing and Presenting Wilkinson and Pickett’s Data Without Issuing a Verdict

## Purpose

This project acquires, documents, reproduces, updates, and visualises the data and calculations cited by Richard Wilkinson and Kate Pickett. Its purpose is to let users inspect the observations, sources, calculations, figures, and deviations and draw their own conclusions.

The project does not decide whether Wilkinson and Pickett are right or wrong. It does not attempt to prove or disprove causality, resolve the published controversies, or issue an overall verdict. Supporting and critical materials are collected and presented transparently, but neither is adopted as the project’s own position.

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

A compact result specification lists the target results before calculation:

```text
result_id
dataset
indicator_or_index
predictor
reported_statistic
reported_value
source_reference
historical_reproduction_required
current_reproduction_required
notes
```

The list prevents selective reproduction without creating a larger claims-adjudication programme.

## Result categories

The project uses four result categories:

- `HISTORICAL_REPRODUCTION`: the calculation uses the historical data and the documented historical method.
- `CURRENT_REPRODUCTION`: the documented calculation is applied to a sufficiently comparable current dataset.
- `CURRENT_REPLICATION_WITH_DEVIATION`: the current calculation contains a disclosed change, such as a conceptual successor series or another necessary data difference.
- `RECONSTRUCTION`: original data or a material method detail was unavailable and was reconstructed from identified sources and recorded assumptions.

Variable comparability is recorded separately in the source lineage, for example as an exact successor, conceptual successor, substitute measure, no current equivalent, or not yet verified. A substitute measure is never presented as an unchanged data update.

## Source lineage

Each reproduced variable has a lineage from the historical source to the current source. The record contains only information needed to understand and reproduce the calculation:

```text
variable_id
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
local_path
source_url
retrieval_date
sha256
```

Where more than one current source is plausible, the primary source is selected by a documented source rule before examining the result. Other valid sources may be presented as labelled alternatives. They are not silently averaged, spliced, or selected according to which produces the closest correlation.

## Historical method uncertainty

Published data, methodological notes, author responses, and legally accessible primary materials are used to reconstruct the historical method. Missing access to a book or source does not stop all work, but the project must not convert an inference into a verified historical fact.

Method details use statuses such as:

- `VERIFIED_FROM_PRIMARY_SOURCE`;
- `VERIFIED_FROM_RELEASED_DATA`;
- `INFERRED_FROM_AUTHOR_MATERIALS`;
- `USER_APPROVED_ASSUMPTION`; and
- `UNRESOLVED`.

User approval determines how the project proceeds when a decision is unavoidable. It does not prove that the approved choice was the original authors’ choice. Any material uncertainty appears with the relevant result.

## Samples and eligibility

The project distinguishes three samples:

1. the historical sample used for historical reproduction;
2. the fixed historical sample populated with current data; and
3. an eligibility-refreshed current sample, when the historical eligibility rule can be applied to current data.

The refreshed sample applies the documented rule to a declared current data vintage. At minimum, the project records the ranking series and period, the population threshold, and the source used to determine whether comparable income-distribution data exist. Outcome values and outcome availability never determine master-sample eligibility.

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

## United States state reconstruction

When a released state-level file is unavailable, the project reconstructs the variables from the sources, periods, and transformations stated in the authors’ methodological materials. Those choices and the acceptance tolerance are recorded before calculating the target correlation.

Agreement with the reported statistic is a validation check, not a tuning objective. Inputs are not revised after seeing the statistic except to correct a documented extraction or coding error. If the independently selected inputs produce the reported result within the declared tolerance, the comparison is recorded. If important source or method details remain uncertain, the result is labelled as a reconstruction.

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

Legally obtainable texts are downloaded into the declared research workspace. Redistributable files may be published when the terms for the exact version permit it. Other files remain in a documented local location where lawful, with provenance and a checksum recorded. A public link or open-access label alone is not treated as permission to redistribute a file.

## Controversy-related datasets

Additional datasets are collected because they are needed to investigate identified controversies, not because the project presumes that they support either side. Each testable controversy is mapped to the variables, geography, years, and candidate sources it would require.

The acquisition goal is complete when the relevant datasets have been obtained with provenance or when a concrete access, licensing, or availability barrier has been recorded. Statistical resolution of the controversy is outside the required reproduction scope.

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

A reported value that cannot be independently recreated is retained as a cited comparison value, not silently treated as reproduced.

## Visual presentation

The GitHub Pages site is a transparent data presentation, not an argumentative verdict. For each included result, it should show where available:

1. the result reported by Wilkinson and Pickett;
2. the historical reproduction;
3. the fixed-sample current result;
4. the eligibility-refreshed current result;
5. the observations underlying the plot;
6. the countries or states included and missing;
7. source, period, variable, and comparability information;
8. disclosed deviations from the historical calculation; and
9. a downloadable table containing the displayed data.

Useful interactions include switching between historical and current data, identifying a country or state from its plotted point, showing or hiding the fitted line, viewing the reported correlation, and downloading the exact data shown.

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
- every target result has a historical reproduction, reconstruction, or documented barrier;
- current counterparts are calculated where sufficiently comparable data exist;
- the supporting package contains academic and non-academic sources found under the documented procedure;
- the controversy package identifies criticisms and responses through resolvable sources;
- controversy-related datasets or documented barriers are present;
- each figure and table can be traced to data, code, source metadata, and a declared sample;
- the Pages site exposes the data and calculations needed for independent inspection; and
- neither the report nor the site issues an overall verdict.

The governing test is simple: a user should be able to see what Wilkinson and Pickett reported, inspect what the project reproduced with historical and current data, understand every material deviation, download the observations, consult supporting and critical sources, and form an independent conclusion.