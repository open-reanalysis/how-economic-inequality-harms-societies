# Method rationale

## released-values

The source is the official international workbook linked by the Equality Trust's [2017 data page](https://equalitytrust.org.uk/news/blog/spirit-level-data-antidote-alternative-facts-0/), retrieved on 19 October 2026 local time. Its SHA-256 equals the hash in the approved planning documents. This verifies the downloaded release identity; it does not independently establish the version behind each book or TED figure.

Historical calculations use the workbook values without filling gaps, changing observations or reapplying transformations already present in the file. The natural logarithm of imprisonment is already supplied. The source record declares each column, unit and period. Variables labelled historical_release retain a period uncertainty rather than inventing an observation year.

The workbook has no average-income column. The three named average-income comparisons remain in the catalogue, with their TED timestamps and absent numeric benchmarks, but cannot yet be computed from this input. No replacement income series is silently inserted into the historical calculations.

## released-membership

The first worksheet contains 23 distinct named countries. The country registry maps UK to GBR and USA to USA. Every univariate calculation uses its available pairs within those 23 countries, with no deletion of observations on substantive grounds. The coverage table records presence flags, not values.

## supplied-index

The historical index comparison uses the index column supplied in the release. It does not claim an independent reconstruction of that column. The [authors' notes](https://equalitytrust.org.uk/notes-statistical-sources-and-methods/), inspected through the web connector on 19 October 2026 local time, describe ten international components, direction reversal for trust, life expectancy and education, logarithmic imprisonment, and averaging available component z-scores. They identify Israel and Singapore as excluded from the international index. The notes do not unambiguously fix every standardisation detail needed to rebuild it. The current-index specification therefore remains unresolved rather than inferring a recipe from whichever calculation best matches a published correlation.

## source-version-conflicts

The workbook and live source notes disagree in consequential details. The workbook describes infant mortality using 2005 OECD data; the live notes describe a 2000 World Bank measure. The workbook describes education as PISA 2003, while its bibliographic wording and the live notes mention other years. Homicides in the workbook are per million; the live notes table says per 100,000. These are disclosed as source/version differences and do not trigger changes to the available release.

The public-health-expenditure summary coefficient on the notes page conflicts with its Singapore erratum. The catalogue uses the explicitly corrected coefficient, with the erratum as its locator. The workbook Erratum sheet also needs to be distinguished from the present notes page when interpreting p-values or corrected data versions. The UNICEF index in the release is the authors' modified index, not an interchangeable unmodified UNICEF composite. A new UNICEF edition is not nominated as an unchanged successor.

## state-membership

The planned historical state sample contains the 50 states, excluding DC. State identifiers retain their leading zeros. The FIPS registry uses [Census state codes](https://www.census.gov/library/reference/code-lists/ansi.html). The source notes list nine index components but elsewhere say eight measures; that internal inconsistency is preserved as a verification question, not interpreted as permission to omit a component.

## state-access

The official data page displays a USA download label without a usable download link in its rendered content. No released state package has been obtained. The state specification currently produces explicit barriers for the 17 reported state comparisons; it does not claim that a numerical reconstruction has been completed. Historical source recovery remains work to do. State imprisonment is a rate, not the logged international variable.

## current-candidates

Current World Bank responses were acquired for coverage assessment only. Their immutable responses are not analysis-ready inputs. The request window is not a selected analysis year. Source correspondence, income/consumption definitions, measurement populations, periods and unit conversions still require verification before the updated specifications can be locked.

The Census candidate returned an HTML Missing Key page despite HTTP 200. The response is preserved as evidence of that attempt and is not counted as obtained state data. No registration or acceptance of terms was performed on the maintainer's behalf.

The World Values Survey's [documentation page](https://www.worldvaluessurvey.org/WVSContents.jsp?CMSID=Documentation) describes registration and non-redistribution terms. This is an access restriction, not evidence that a current trust series does not exist. The [OECD PISA database](https://www.oecd.org/en/data/datasets/pisa-2022-database.html) documents participation and sampling issues; those flags must accompany a nominated current education series. The [WHO obesity metadata](https://www.who.int/data/gho/data/indicators/indicator-details/GHO/prevalence-of-obesity-among-adults-bmi--30-%28age-standardized-estimate%29-%28-%29) identifies modelled, age-standardised estimates, which cannot silently replace a historically averaged adult measure. These checks identify leads and differences, not completed current-series validation.

## numeric-benchmarks

Reported correlations are transcribed as numeric facts from the source notes and explicitly applicable errata. Their published precision is kept separate from computational replay tolerances. A difference is a research finding, not a failed software test. No unavailable reported statistic is represented as zero, and a verbal statement that there is no relationship is not converted to a numeric r of zero.

## Prior published knowledge

The 2024 technical appendix was consulted for methodological context on 19 October 2026. Its published coefficient table was visible during that reading. Those published results were not used to select current series, periods, samples or transformations and are not comparison targets of this run. The appendix describes a changed mobility measure/direction and different PISA choices, which are not silently imported into the historical specifications.

The component report for the supplied historical index records available components. Its used flags are inferred from the declared component list, availability and the presence of the supplied index; they do not demonstrate independent reconstruction of the authors’ exact standardisation.

## state-historical-sources

Before any reconstructed state correlation was computed, historical_us_states version 2 nominated the Census [Table S4](https://www.census.gov/data/tables/time-series/dec/historical-income-states.html) household Gini for 1999 and FBI [Crime in the United States 1999, Table 5](https://ucr.fbi.gov/crime-in-the-u.s/1999) homicide rate. Raw files are stored unchanged with acquisition records. The missing author file is not presented as recovered; this remains an independent partial reconstruction. Source-hosted historical data may differ in revision or precision from the authors’ inputs.

## state-homicide-availability

The authors’ source notes explicitly identify Wyoming as lacking homicide data. The primary reconstructed comparison therefore uses the named historical_homicides sample of the other 49 states. All 50 source observations are preserved; exclusion is declared before computation and is not selected by its effect on the correlation. The book coefficient is not used to tune the sample.

## state-infant-source

Before computing this additional reconstructed comparison, historical_us_states version 3 nominates Statistical Abstract 2006 (125th edition), Table 105, total-race 2002 infant mortality rates per 1000 live births by state of residence. This is the table and period in the authors' index component table and reference 6. The downloaded file is the official linked .xlw Excel workbook; row 10 holds the years, column E the 2002 total rate, and rows 14–64 the states and DC. DC is excluded. No outcome was chosen based on its correlation with inequality. The source record holds zero-based parser coordinates.

## refreshed-membership

config/eligibility.yaml holds the maintainer-approved universe, ranking vintage, strict population boundary, survey window and tie policy. UN membership is verified against the UN Dag Hammarskjold Library Current UN Member States page (193 members), acquired 19 October 2026. config/units/un_members.csv records the ISO mapping; the existing general registry already contains these countries and its aliases are unchanged. This operational state definition is a project clarification supported by, but not identical to, the authors' rejection of Hong Kong as a non-nation-state.

Ranking precedes both population and inequality exclusions; it is never recomputed after those exclusions. All cutoff ties enter. Survey eligibility requires national observed income distributions, national coverage and matching survey/reporting year. S80/S20 is the sum of the richest two decile shares divided by the poorest two, using a single distribution. Missing, zero-denominator, interpolated, consumption and nonnational records cannot establish comparable income availability. Latest eligible survey year is retained for audit; no outcome or outcome-availability column enters the eligibility script. Cross-country equivalence-scale differences are disclosed as conceptual-succession limits. No average-income/outcome association is computed.
