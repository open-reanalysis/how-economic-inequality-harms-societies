# Prospective index counterpart review

Reviewed on 19 October 2026. This supplements the generated [candidate-presence assessment](../current-index-assessment.md). It records metadata and coverage only. It records proposed series correspondence in the lineage, subject to milestone review. It selects no analysis period and calculates no index or association.

## Acquired international candidates

The historical definitions are identified in the released-workbook source records and the authors' [component table](https://equalitytrust.org.uk/notes-statistical-sources-and-methods/), section “Sources of Data for the Index of Health and Social Problems”. The current definitions below were checked against the linked official indicator metadata. These checks support conceptual, rather than exact, succession for the four WDI targets. The lineage discloses the historical version conflicts and revised estimation.

| Component | Current metadata checked | Correspondence and remaining check |
|---|---|---|
| Life expectancy | [SP.DYN.LE00.IN](https://api.worldbank.org/v2/indicator/SP.DYN.LE00.IN?format=json): years a newborn would live under the period's mortality pattern; WDI names UN, national statistical offices and Eurostat inputs | The birth/total-sex concept matches the historical target. Establish the historical UNDP input lineage and current revision before distinguishing conceptual from exact succession. Both-sex life expectancy must not be replaced by an unweighted arithmetic mean of male/female values without evidence. |
| Infant mortality | [SP.DYN.IMRT.IN](https://api.worldbank.org/v2/indicator/SP.DYN.IMRT.IN?format=json): deaths before age one per thousand live births; current upstream provider is UN IGME | The event, age boundary and denominator match the declared target. Resolve the historical workbook's OECD source versus the notes' WDI source and document changes in estimation. A common indicator name does not establish an unchanged series. |
| Teenage births | [SP.ADO.TFRT](https://data.worldbank.org/indicator/SP.ADO.TFRT): births per thousand women aged 15–19; UN Population Division | The age group and denominator match the historical UNICEF target. Verify estimation and age conventions and trace the original input before classifying continuity. The metadata API route failed in this review; the official indicator page supplied the title and upstream attribution. |
| Homicides | [VC.IHR.PSRC.P5](https://api.worldbank.org/v2/indicator/VC.IHR.PSRC.P5?format=json): intentional unlawful deaths, per hundred thousand people; UNODC | The workbook is labelled per million, while the authors' notes use per hundred thousand. Any unit conversion belongs in a prospective specification after the historical unit is resolved. Verify offences/victims, exclusions and the original crime-survey definition; modern intentional homicide is not assumed identical solely because both involve homicide. |

The WDI indicator pages identify CC BY 4.0. The downloaded responses, their retrieval dates, hashes and provider notices remain the source of truth for this run; a live metadata page may later change. Additional acquisitions and their immutable records are described below.

## Timing and joint coverage

The following counts were derived only from `outputs/tables/outcome_source_coverage.csv`, filtering the four candidate source IDs above to `payload_status=parsed` and `available=True`, counting distinct original-sample country IDs within each period. “All four” is the intersection of those ID sets. Outcome magnitudes, inequality and income were not read or joined. This is a coverage diagnostic, not an analysis-period rule.

| Recorded period | Life expectancy | Infant mortality | Teenage births | Homicides | All four |
|---|---:|---:|---:|---:|---:|
| 2020 | 23 | 23 | 23 | 22 | 22 |
| 2021 | 23 | 23 | 23 | 23 | 23 |
| 2022 | 23 | 23 | 23 | 21 | 21 |
| 2023 | 23 | 23 | 23 | 18 | 18 |
| 2024 | 23 | 23 | 23 | 0 | 0 |
| 2025 | 0 | 0 | 0 | 0 | 0 |

The earlier “23 countries in at least one year” summary therefore cannot justify a common latest-year index. Zero means no nonmissing observation in this stored response, not that the provider has no series or will never revise it. The requested window included 2026, but the responses did not contain that period; do not fabricate 2026 rows. No final year, lag allowance or maximum observation age is selected from this table.

## Other dimensions and state-specific differences

| Dimension | Evidence and next verification |
|---|---|
| Trust | The WVS registration barrier is recorded. Verify question wording, response denominator, survey wave, country-year and weights before choosing a successor. State trust requires GSS state identifiers; national trust is not a state counterpart. |
| Obesity | [WHO indicator metadata](https://www.who.int/data/gho/data/indicators/indicator-details/GHO/prevalence-of-obesity-among-adults-bmi--30-(age-standardized-estimate)-(-)), Definition and Method of estimation, describes measured-input, model-based adult prevalence, age 18+, BMI at least 30, with age-standardized and crude estimates. The historical target's sex averaging and age conventions need checking. The acquired NCD_BMI_30A response uses SEX_BTSX and AGEGROUP_YEARS18-PLUS, with 23 original countries in each 2020–2024 year. Earlier BTSX-filtered responses were empty and remain preserved. The old sex code must not be interpreted as missing country data. The current age-standardised both-sex estimate is classified SUBSTITUTE while historical age and sex aggregation conventions remain unresolved. For states, raw self-reported BRFSS prevalence cannot silently replace the historically corrected estimates. |
| Mental health | International diagnostic prevalence and state mentally unhealthy days are distinct targets. A modern distress score, disability burden or service-use measure needs explicit treatment as a related measure; broad topic similarity is insufficient. No statistical candidate has been parsed. |
| Education | The [OECD PISA data and methodology page](https://www.oecd.org/en/about/programmes/pisa/pisa-data.html) provides cycle-specific data and manuals. Verify the actual release available at the cut-off, math/reading country estimates and sampling caveats; a page listing a cycle is insufficient evidence of usable data. State NAEP grade-eight scores are a separate target. Prefer official summary tables over unnecessary student microdata. |
| Imprisonment | Verify prisoners versus admissions, jurisdiction/custody, remand inclusion, population denominator and observation date in the nominated UNODC/BJS table. The international log transformation is distinct from the state rate. The acquired workbook is dated 30 September 2026. The declared filter selects Persons held / Total / Total / Total / Total / Rate per 100,000 population, excluding admissions and regional estimates. Among the original countries it covers 22 in at least one year; the UK has separate England/Wales, Northern Ireland and Scotland identifiers. Rates are not summed and England/Wales is not relabelled GBR. The workbook remains local because full redistribution permission is unverified. |
| Social mobility | The historical intergenerational income correlation is not a yearly administrative rate. Resolve cohort, parent/child definition, income age and estimator. A rank-based mobility measure cannot become an exact successor by rescaling. The June 2025 GDIM income file has code, IGE and source fields and 22 original countries. IGE is elasticity for 1980s–1990s birth cohorts, not a 2025 annual observation and not an income correlation. It is classified SUBSTITUTE. This component has no state-index counterpart. |

The nine-component state index needs its own source/definition/coverage assessment. International coverage cannot be transferred to states. CDC WONDER source-route failures and terms requirements are recorded separately; no current state outcome table has been parsed here.

## Consequences for the lock

1. Omitting all unacquired dimensions would produce a materially different construct. Candidate acquisition progress is not a scientific basis for choosing component weights or a minimum count.
2. Averaging the components present in each country can give countries different effective weights and meanings. Before approval, report each country's admissible component set for the proposed period, including the missingness pattern and whether omitted dimensions are systematic. This diagnostic needs no association calculation.
3. Complete-case restriction can change the sample; allowing different years can change temporal interpretation. Document the consequences of each proposed rule using coverage alone before selecting the rule.
4. Distinguish source continuity from observation availability. An available substitute may belong only in the specified parallel variant; an access barrier does not prove that no counterpart exists.
5. Keep the reproduction lock and updated specifications in draft until nominated data, version-specific correspondence, timing, eligibility and the missing-component decision can all be reviewed. The maintainer's deferral does not approve a four-component index or any numerical threshold.

## Additional acquisition evidence

WHO metadata: https://www.who.int/data/gho/indicator-metadata-registry/imr-details/2389 (Definition, Method of estimation). Maintainer terms acceptance: docs/worklist.md. The statistical query is pinned in the source and acquisition records, including the failed long filter and empty obsolete-sex-code response.

UNODC source: https://data.unodc.org/datareport/prison-held; downloadable workbook, data_cts_prisons_and_prisoners sheet, header row 3. Cohort mobility source: https://datacatalog.worldbank.org/search/dataset/0066878/global-database-on-intergenerational-income-mobility, June 2025 income release. Source-specific layout facts are stored in their YAML records.

PIP national income survey metadata and distributions were acquired using the official pip/v1/pip route with income, national, fill_gaps=false and 2020–2025 filters. Reporting years still require matching to survey years; one returned record differs and is excluded by the declared reader. Matched decile shares permit S80/S20 without joining potentially different WDI surveys. This is a conceptual successor, not evidence of identical welfare equivalence scales across countries. Source and API documentation: https://blogs.worldbank.org/en/opendata/how-use-pips-api.

The WMH contact route returned HTTP 503 in the stored acquisition attempt. The official contact documentation, read via the web service, requires coordinating-centre permission for non-US data. No message or access request was sent. This is an acquisition barrier, not NO_CURRENT_EQUIVALENT. The PISA current-method route returned HTTP 403; the official 2025 release exists, but a usable national aggregate table with sampling flags has not been obtained in this run.
