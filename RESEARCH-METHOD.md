# Research method

This document defines what the project reproduces and collects, how research choices are made, and what the results establish. [INTENT.md](INTENT.md) sets the goals and scope. [IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md) describes the technical implementation and work organisation. Machine-readable analysis specifications hold the exact computational choices; [docs/method_rationale.md](docs/method_rationale.md) explains their sources and reasons. Technical schemas, storage rules, software tests and publication requirements belong in the implementation plan rather than being maintained again here.

## Purpose and boundaries

The project has six goals, in priority order:

1. Obtain current versions of the datasets Wilkinson and Pickett used.
2. Reproduce their reported findings from released or reconstructed historical data and apply the documented calculations to current data.
3. Assemble a package of supporting sources, academic and non-academic.
4. Assemble a package of sources describing controversies and relevant responses.
5. Obtain datasets needed to investigate the identified controversies.
6. Publish the data, calculations, figures, sources and deviations on a GitHub Pages site.

Goals 1–5 form a research release that can be inspected without the website. The website presents those deliverables. Its implementation does not redefine the analyses.

The project reports what the authors published, what its calculations produce and where the two differ. It does not issue an overall verdict on the authors or their critics, test the controversies, estimate policy effects or assess causality. A reproduced correlation does not establish a causal claim, and a discrepancy does not establish a critic's explanation. These boundaries permit conclusions about whether a specified calculation was reproduced, which observations were available and whether a variable or method changed.

## Target results

The scope covers identified international-country and U.S. state comparisons in the released data and the authors' methodological materials:

- income inequality against each reported health or social measure and the Index of Health and Social Problems;
- average income against the index or a measure where the authors reported that comparison for the same data; and
- current counterparts of those calculations where the required series can be obtained.

Countries and U.S. states are separate datasets and are never pooled. Other figures, later analyses, mechanisms and policy claims are outside the scope unless an explicit decision adds their underlying analysis. A claims register may document statements without making them reproduction targets.

[config/results_catalogue.csv](config/results_catalogue.csv) is the single list of target comparisons. Each row identifies the dataset, predictor, outcome or index, sample, statistic, published comparison value and source locator. It is fixed before reproduction begins. Every row remains visible, including a result that cannot be calculated; availability determines its outcome, not whether it enters the list. Later additions or corrections are dated and explained.

## Historical evidence and reconstruction

### Evidence and versions

The project currently proceeds without the book itself and states this limitation. It uses the released international file, its sources sheet and errata, the Equality Trust's notes on statistical sources and methods, frequently asked questions and the authors' responses, and the released U.S. state file if obtained. Archived copies are identified by version or capture date. The notes have been located through an Internet Archive capture of 7 January 2017.

The Spirit Level at 15 and its technical appendix are used for their descriptions of the original method, timing and income ratio. Comparing the project's results with the 2024 update is outside scope.

Evidence is ranked according to the question being answered. A released file establishes the values in that file; methodological notes describe an intended calculation; a dated correction may supersede an earlier value or instruction. A later file is not automatically evidence of exactly what was analysed for the original publication. Secondary accounts can identify leads but do not silently override primary evidence. Later access to stronger primary evidence triggers a documented verification and, where needed, a new analysis version rather than silent replacement.

Three questions are kept apart:

1. Does the calculation reproduce the contents of the available released file?
2. Does that file represent the data version behind the cited publication?
3. Does the computed statistic match the value reported in that publication?

Known revisions, conflicting source years and unit differences are documented against the affected comparison. If a correction defines a different historical version, that version is identified explicitly.

### Method uncertainty

Each consequential method choice has a source or a recorded assumption. Its evidence status distinguishes verification from released data or primary documentation, inference from author materials, a user-approved assumption, and an unresolved point. Approval allows the work to proceed; it does not prove that the authors made that choice.

The current run's assumptions and decisions are in [docs/worklist.md](docs/worklist.md). An unresolved choice that can change a deliverable is decided before the affected calculation. Hypothetical cases need no elaborate advance rule. The final specification must nevertheless identify all choices needed to reproduce its calculation, including choices that were unambiguous.

### Access and reconstruction

Access is assessed separately for the international and U.S. state datasets from recorded retrieval attempts.

| Access status | Meaning | Historical label |
|---|---|---|
| verified_release | A provenance-verified release contains usable data and enough documentation to identify its variables and units | DIRECT REPRODUCTION |
| incomplete_release | Released material is accessible but required data or method details are missing | PARTIAL REPRODUCTION |
| archived_copy | Historical material is available but its provenance to the original release is not fully verified | ARCHIVE-BASED RECONSTRUCTION |
| unavailable | No usable released package is accessible | INDEPENDENT RECONSTRUCTION |

The dataset access label is accompanied by result-level provenance and uncertainty. Access to a file does not by itself verify every method detail. Released, reconstructed and combined observations are distinguishable.

Where released data are unavailable, reconstruction uses the original sources and vintages identified in the authors' documentation. Source versions, periods, transformations, index rules and the precision of comparison with the published statistic are recorded before calculating it. For U.S. states this includes the archived agency series and published state tables identified in the source lineage.

Matching a reported correlation within the declared tolerance establishes numerical agreement at that precision. It does not establish that the reconstructed observations or every method choice are identical to the original ones; those require separate source evidence. A mismatch is recorded with its likely cause or an explicit statement that its cause remains unresolved. Inputs are never changed merely to improve agreement.

A partial state reconstruction is an acceptable documented outcome. Missing inputs, attempted acquisitions, uncertain method details and uncomputed catalogue rows are listed. It neither changes the country dataset's access label nor prevents the independent research release.

## Current series and comparability

[docs/source_lineage.csv](docs/source_lineage.csv) connects each variable's historical meaning and source to its current counterpart. It covers inequality, average income, index components, other included measures, and eligibility variables. Requests, files, retrieval times, licences and checksums are maintained in the acquisition and source records to which it refers, rather than copied into the lineage.

Series are chosen by documented correspondence to the historical variable before inspecting their associations.

| Class | Meaning |
|---|---|
| EXACT_SUCCESSOR | Continuation of the same series with no material change in definition, unit or population |
| CONCEPTUAL_SUCCESSOR | The same intended concept and target population, with a documented provider, survey, coverage or method difference |
| SUBSTITUTE | A related but different measure |
| NO_CURRENT_EQUIVALENT | No defensible current counterpart was identified |
| NOT_YET_VERIFIED | Verification was attempted but remains incomplete, with the reason recorded |

Comparability is separate from access. A corresponding series may exist but require permission, be unavailable to this run or have an unsuccessful retrieval. Such a barrier is recorded as an acquisition status; it is not by itself evidence that no current equivalent exists.

A conceptual successor's differences are disclosed with the result. Substitutes appear only in the separately labelled fixed-sample variant. The lineage's nominated series determine reproduction-data acquisition. Additional datasets collected for controversies have their own data map and do not silently enter the reproductions.

## Samples, periods and transformations

### Samples

The historical country sample is the verified membership of the released international dataset, currently identified as 23 countries. The historical state sample is 50 states, with the District of Columbia excluded unless primary evidence establishes otherwise. Each individual comparison uses the members with the required observations.

The primary current analysis keeps the historical master sample. A parallel analysis refreshes country eligibility using the rule the authors state in their 2010 response to Peter Saunders: start with the 50 richest countries, retain those with a population above 3 million, and require comparable income-distribution data.

The specification identifies the ranking measure and vintage, population period and income-distribution source. A consequential ambiguity about non-sovereign economies or ties is resolved before sample selection is finalised. The historical eligibility check is performed only if the required historical vintage can be obtained. An unavailable vintage is reported as a barrier, not replaced silently.

The refreshed state sample equals the fixed state sample unless the documented original rule establishes otherwise, so identical results are reported once.

Outcome values and availability never determine master-sample eligibility. Missing observations affect only the comparison that requires them. Every result identifies the master sample, included units, missing units and final sample size.

### Periods and variables

For each variable, the specification identifies the series, reference period, target population, unit, conversion, transformation and direction coding. Direction is specified per measure; different measures of the same concept need not point in the same direction.

Publication year, retrieval date and observation period are distinguished. Current means the frozen release obtained within the declared acquisition window. The current specification fixes the period-selection rule, treatment of multi-year measures and temporal alignment between predictor and outcomes, preserving the documented historical timing where possible. A necessary departure is disclosed. Sources and periods are not selected according to the resulting correlation.

### Parallel sources

Parallel sources are compared before combination. The specification identifies the primary source, the purpose of any secondary source and the conditions under which it may fill a gap. Definitions, populations, periods and units must be sufficiently compatible; unit conversion alone does not establish compatibility. Incompatible sources remain separate.

For reproduction of an available released file, that file supplies the primary values. Filling its gaps from another source is reconstruction and is labelled accordingly. Values are never averaged to improve agreement, every combined observation retains its source, and differing values are published in a comparison table. The combination rule is fixed before correlation is calculated.

## Index, missing values and statistics

The calculation follows the documented historical procedure for standardisation, its reference population and denominator, direction coding, weights and index construction. The numerical settings are held in the analysis specification, with their evidence or assumption status in the method rationale.

Missing components are treated by the authors' rule where it can be established. Otherwise the necessary operational choice is approved before index calculation and identified as an assumption. No new minimum-component threshold is introduced without a stated basis and approval. Missing values are not imputed and outliers are not deleted.

Every index result shows its component set, component availability per unit and differences from the historical index. A reduced or substituted component set is reported as a changed index, not simply the historical index with newer observations.

The project calculates the documented comparison statistic, Pearson correlation and its p-value where those are the reported calculation, and always discloses the number of observations. Figures show exactly the observations entering the calculation. New models and a general sensitivity-analysis programme are outside scope.

## Result variants and interpretation

Each catalogue comparison has a historical result or documented barrier and the following current counterparts where possible.

| Variant | Sample | Series | Role |
|---|---|---|---|
| Historical reproduction or reconstruction | Historical | Historical sources | Check the available historical calculation against the cited result |
| Fixed-sample current reproduction | Historical membership | Exact and conceptual successors | Primary current result |
| Eligibility-refreshed current reproduction | Refreshed eligibility | Exact and conceptual successors | Parallel result |
| Fixed-sample result with substitutes | Historical membership | Also permits declared substitutes | Parallel result |

A component with no current counterpart remains missing. A substitute-only component is missing from the primary index under its missing-component rule and is added only in the substitute variant. A comparison with no admissible predictor or outcome is not produced and has a specific reason. The refreshed country result is not possible if comparable current inequality data cannot support its eligibility rule. No additional sample, outcome, measure or model is introduced without a scope decision.

Each specification assigns each variant a stable identifier so its observations and figures remain distinct. A catalogue comparison keeps the same identity across its variants.

Results record separately:

- data provenance and the historical dataset's access label;
- master and actual sample membership;
- series comparability;
- method deviations and material uncertainty; and
- replay state: computed, retained from an earlier run or not produced.

A conceptual successor is not presented as an unchanged measurement merely because it enters the primary variant. A current result is a comparison under its declared data and method, not proof that a relationship persisted under identical conditions.

## Prospective decisions, corrections and validation

Current specifications and the catalogue they implement are fixed before any current association in the catalogue, including average-income comparisons, is computed or inspected. The reproduction lock identifies the specifications and their versions. Prior knowledge of published historical or 2024 correlations is disclosed; the blinding is procedural.

Unanticipated consequential choices are recorded before the affected calculation proceeds. A substantive change after the lock is a dated amendment with a new specification version; affected results remain available under both versions.

Documented extraction, transcription, unit, source-version or coding errors may be corrected after results have been seen. The correction records its evidence, reason and affected results and retains the earlier version in history. A software correction is distinguished from a change in research method. Neither is justified solely by closer agreement with a published number.

Validation establishes that the declared files, versions, sample and transformations were used and that the calculation can be independently regenerated. Numerical correctness is checked against independent test cases; comparison with the authors' values is a research result. Discrepancies are reported whether they increase, decrease or leave an association unchanged. An unresolved cause remains unresolved.

Acquisition is separate from replay. Reproduction uses stored inputs rather than changing live services. Restricted inputs are identified. A result kept because its input was unavailable in a replay is described as retained, not recomputed. The technical implementation of these checks and records is specified in the implementation plan.

## Source packages and controversy data

Supporting and controversy sources follow one search and screening protocol.

- The topics are inequality and health or social outcomes across rich countries and U.S. states, the authors' data and analyses, and identified criticisms and responses.
- Searches use OpenAlex, Crossref and PubMed, the Equality Trust site and cited sources.
- One search cut-off is recorded in the worklist and package READMEs.
- Citation chaining follows one step backward and one step forward from the declared author and controversy seed works.
- Inclusion requires an identifiable author, a citable record and relevant argument or evidence. Whether a source supports or challenges the findings does not determine its inclusion.

Searches and screening decisions are logged with their dates and reasons. Academic, non-academic, author, response and mixed roles remain visible. A source with several roles is acquired once and linked to each relevant package or controversy.

The supporting search explicitly seeks independent peer-reviewed evidence. Completion depends on carrying out the declared search and documenting what it found, not obtaining a predetermined number of favourable sources. If independent support is not identified under that procedure, this and the search limitations are reported. The packages need not contain equal numbers of sources and do not claim exhaustive coverage.

Every included text that can lawfully be obtained is downloaded. Redistribution requires permission under the terms of the exact version; public access alone is insufficient. Other texts remain local where lawful, with public bibliographic, version and acquisition information. Detailed folder and record layouts are defined in the implementation plan.

Each controversy has an identified author, title, year, stable identifier and, for a book, edition. Criticisms of the general hypothesis are distinguished from criticisms of a particular reproduced result, with their mapping explained. The register records the argument and available responses without adopting either as the project's conclusion.

Before controversy-related data are acquired, the map specifies the smallest justified package: variables, units, geography and periods. Shared datasets are obtained once. Each package ends as acquired, partially acquired or barrier documented. Coverage obtained is distinguished from what a later investigation would require. No controversy test or verdict is calculated here.

## Reporting and completion

For every target comparison the research release presents the cited statistic, historical result, primary current result and available parallel results, with observations, sample sizes, periods, sources, comparability and deviations. An unavailable calculation remains visible with its barrier. The release of goals 1–5 includes the headline table and a short deviation summary and does not wait for the website or a complete state reconstruction.

The first website presents those results with figures, underlying tables and downloadable plotted observations where publication is permitted. It links the supporting and controversy records, source documentation and code. Restrictions are stated where observations cannot be distributed. Interactive controls are optional later enhancements and do not gate the first release.

The report may state that a calculation was reproduced, did not match, remained uncertain or used a materially different variable. Such statements do not establish an overall causal, policy or controversy verdict. Author and critic claims are attributed accurately and kept separate from the project's calculations.

The research deliverables are complete when every target result has a computed result, reconstruction or documented barrier; each in-scope variable has a current counterpart or a documented absence or access status; both source packages have completed the declared search with known gaps; and each testable controversy has its defined data package or documented partial acquisition or barrier. Published observations and calculations must be traceable to sources, specifications and run records.

Website publication is the separate sixth goal. Its completion requires the declared minimum presentation and working access to the research release, rather than new analyses or an overall judgement.
