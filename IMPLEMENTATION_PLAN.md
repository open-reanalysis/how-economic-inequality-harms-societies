# Implementation plan

This plan turns [INTENT.md](INTENT.md) into work that separate Claude sessions can run in parallel. It has three parts. Part A is the research method, which says what is computed. Part B is the technical architecture, which says how the code, the data and the checks are built. Part C is the work organisation, which says who does what and in which order. The plan does not depend on a date. The schedule and the decisions of the current run are in [docs/worklist.md](docs/worklist.md).

## Goals and priorities

The project has six goals, in this order of priority. They come from the original project specification.

| Priority | Goal | Threads | Output path | Acceptance test | Blocking dependencies | Milestone | Human decision |
|---|---|---|---|---|---|---|---|
| 1 | Download the current version of every dataset Wilkinson and Pickett used | Original access, source lineage, inequality data, outcome data | `data/00_original_released/`, `docs/source_lineage.csv`, `data/01_raw_current/` | Every original variable has a lineage row with a comparability class, every row not marked `NO_CURRENT_EQUIVALENT` or `NOT_YET_VERIFIED` has its current file with a matching file record, and a `NOT_YET_VERIFIED` row passes only with a logged verification attempt and its reason | Scaffold | 1 | Accept the terms of use of sources that require it |
| 2 | Reproduce their findings | Historical reproduction, reproduction lock, updated reproduction | `outputs/tables/historical_*`, `outputs/tables/updated_*`, with their discrepancy logs | The historical reproduction and the fixed-sample current reproduction exist for every dataset whose inputs are available, every deviation from the reported values is logged with a cause, and every current result names its locked specification and version | Goal 1 | 1 and 2 | Approve the assumptions before the run |
| 3 | Download a package of sources supporting their findings, academic and non-academic | Original access for the authors' own works, supporting sources for the rest | `sources/supporting/` | The package has at least one peer-reviewed study by other authors, every record follows the screening protocol, and every legally obtainable text is downloaded or has a recorded reason | Scaffold | 2 | None |
| 4 | Download a package of sources setting out controversies about their findings | Controversy sources and register | `sources/controversies/`, `docs/controversy_register.csv` | Every register row has an identifiable source, its argument in neutral words, its target and any reply, and every legally obtainable text is downloaded or has a recorded reason | Scaffold | 2 | None |
| 5 | Download datasets that may support those controversies | Controversy test data | `data/04_controversy_test_data/`, `docs/controversy_data_map.csv` | Every register row with a testable statement has a map row whose datasets are acquired with provenance, or whose barrier is documented | Goal 4 register freeze | 2 | None |
| 6 | Publish the results on a GitHub Pages site | Report | `site/`, `.github/workflows/pages.yml` | The `results-v1` tag publishes the report with the headline table and links to the `deliverables-v1` release and the repository | Goals 1 to 5 | 3 | Approve the `results-v1` tag |

The same table is kept in machine-readable form in `docs/goal_traceability.csv`. `make check-contracts` fails if any goal lacks a thread, an output path, an acceptance test or a milestone, if an output path is not owned by one of the goal's threads, or if a goal in milestone 1 or 2 depends on a thread outside milestones 1 and 2.

The project keeps one addition beyond the goals. The author claims register records and classifies what Wilkinson and Pickett claim. It never delays a goal or gates a tag.

Milestone 2 ends with an independent release of goals 1 to 5, tagged `deliverables-v1`. It is complete even if the report and the website are not yet built. Milestone 3 delivers goal 6. Milestone 1 holds only the path to goals 1 and 2, so nothing from goals 3 to 5 gates the reproductions.

The original material contains an analysis of the U.S. states, as the authors' notes on sources and methods show. It is a second dataset for the same hypothesis within goals 1 and 2, reproduced from the original data and updated wherever a current release of the same series exists. It is always reported separately from the country analysis and never pooled with it.

The project runs no analysis beyond the two reproductions. It does not test the controversies and does not assess causality. The controversy register and the claims register document the debate, and the controversy test data make later tests possible.

# Part A. Research method

The research method covers the sample, the variables, their years, unit conversions, direction coding, missing values, standardisation, the index, the combination of parallel data and the statistics reported. Every rule of the method that the computation uses is written once, in a machine-readable analysis specification under `config/specs/`. The method rationale, `docs/method_rationale.md`, explains the source and the reason for each rule and refers to the specification by key. It never restates a value, so the two cannot drift apart. The structure of the specification is described in Part B.

## Original material

The book itself is not used. The project relies on what the authors and the Equality Trust published about the book's data and methods: the released international data with its sources sheet and errata, the notes on statistical sources and methods, the frequently asked questions and the authors' 2010 responses to their critics. *The Spirit Level at 15* and its technical appendix are used only for what they say about the original method, its timing and the meaning of 80:20. The project does not compare its results with the 2024 update.

The assumptions that fill the points this material leaves open are listed in [docs/worklist.md](docs/worklist.md) and approved by you before the run. The historical reproduction thread writes them into the specifications and their reasons into the method rationale. Only a point those assumptions do not cover is put to you during the run. The report states the absence of the book as a limitation. Every verified fact is logged in `docs/source_verification/` with the passage, table or file it came from before a rule uses it.

## Access labels

The original access thread assigns one of four access statuses, and the status fixes the label that every historical reproduction result carries.

| Status | Definition | Label |
|---|---|---|
| `verified_release` | Files download and hash, contain usable original data, and carry enough documentation to identify variables and units. | `DIRECT REPRODUCTION` |
| `incomplete_release` | Some files download, but required sheets, metadata, source notes or formulas are missing. | `PARTIAL REPRODUCTION` |
| `archived_copy` | A credible archive or third party supplies historical files, but provenance to the original release cannot be fully verified. | `ARCHIVE-BASED RECONSTRUCTION` |
| `unavailable` | No usable original package is accessible. | `INDEPENDENT RECONSTRUCTION` |

The status is decided only by the acquisition records of the retrieval attempts. A 2017 Equality Trust post saying the data could be downloaded establishes nothing about today.

## Source lineage and comparability

`docs/source_lineage.csv` records, for each variable and dataset, what the variable means, the series the authors used and the current series that corresponds to it. It takes the original series from the released data file's sources sheet and from the notes on sources and methods, never from a later summary. Where the two disagree, the data file comes first, because it describes the values in the file, and both are recorded. Each row gets one comparability class.

- `EXACT_SUCCESSOR`. The same series from the same provider, with the same definition, unit and population.
- `CONCEPTUAL_SUCCESSOR`. A series that measures the same concept for the same population, but whose provider, survey or method has changed.
- `SUBSTITUTE`. A different measure of a related concept, such as self-reported obesity in place of obesity corrected for self-report bias, or a Gini coefficient in place of an income ratio.
- `NO_CURRENT_EQUIVALENT`. No current series measures the concept for the original units.
- `NOT_YET_VERIFIED`. The original or the current series has not been confirmed. A row stays in this class only with a logged verification attempt and its reason.

The data threads download only what the lineage names, so "the data Wilkinson used" never becomes "comparable data" without a recorded reason. A source is never chosen by the strength of the correlation it produces.

## Samples and eligibility

**Countries.** The fixed sample is the 23 countries in the released international data. The refreshed sample applies the authors' eligibility rule, stated in their 2010 response to Peter Saunders's report for Policy Exchange, published by the Equality Trust. A country is eligible when it meets three conditions, applied in this order.

1. It is among the 50 richest countries in the world.
2. Its population is more than 3 million.
3. It has comparable income distribution data.

The specification fixes only the details that change which countries are eligible: the income measure and data vintage that rank the 50 richest, the year in which income and population are measured, the source that counts as comparable income distribution data, whether economies that are not sovereign states are ranked, and how a tie at rank 50 is broken. The historical check ranks by the vintage in the approved assumptions and compares the result with the released 23 countries. If that vintage cannot be obtained, the check is not made and the reason is recorded. The refreshed sample uses the current release of the same income series and the inequality series of the updated reproduction. Market democracy is not a condition, because the authors give it as the reason for the rule, not as part of it.

**U.S. states.** The sample is the 50 states. The District of Columbia is excluded unless the original material shows otherwise. The refreshed state sample therefore equals the fixed one, and that result is reported once with this note.

**Independence from outcomes.** Outcome data never decide eligibility. Neither the availability of an outcome nor its value, a correlation, an outlier or significance adds or removes a unit. A unit without a value for one outcome stays in the sample and is left out of that analysis only, and the result lists it among the missing units.

## Variables, years and transformations

For each variable the specification states the series from the lineage, the reference year or period, the unit, any unit conversion, any transformation and the direction coding, which is fixed per measure rather than per concept. The original timing is taken from the notes on sources and methods and checked against the appendix's description of an inequality measure averaged from values reported in 2003 to 2006 and measured in 1992 to 2001, with outcomes from 1999 to 2004. The inequality measure is the ratio of the incomes of the richest and the poorest fifths, averaged from the UN Human Development Reports of 2003 to 2006, as the notes describe it.

**Parallel data.** Where two sources give values for the same variable and unit, the values are compared, and every differing value is published in a comparison table. They are then combined into the project's own series. The source that the specification ranks first is primary, the other fills only its gaps, units are harmonised first, and values are never averaged. Every value keeps its source ID. In historical data the released file is primary, and a value filled from another source is flagged reconstructed, so the access label shows it. Three disagreements between the released file and the notes are already known. Infant mortality is World Bank 2000 in the notes and OECD 2005 in the file. Homicides are a rate per 100,000 for 1990 to 2000 in the notes and per million for 1999 to 2000 in the file. The education score is PISA 2000 in the notes and PISA 2003 in the file.

## Missing values, standardisation and the index

The specification states how components are standardised, including the reference population of the z-scores, how the index combines them, including weights, and how a unit with missing components is handled, as the authors' documented procedure handled it. The reproductions use no imputation and delete no outliers.

## Statistics

The reported statistics are those the original study used: the Pearson correlation between inequality and each outcome or the index, its p-value and the number of units. The project adds no statistics of its own. Figures follow the original graphic conventions.

Agreement with a published correlation is a research result, not a software test. A difference is logged in the discrepancy log with its likely cause. A difference alone does not mean a software error, and the published value is never used to tune the computation.

## Results

**Analyses.** For each dataset, the analyses are the correlations the authors reported: income inequality with the Index of Health and Social Problems and with each measure for which the notes on sources and methods give a correlation and p-value. The lineage rows with `reported_r` filled are this list, and every result type runs over the same list. No separate analysis register is kept.

Goal 2 has four result types, kept separate in every table and sentence.

| Result | Data | Sample | Label |
|---|---|---|---|
| Historical reproduction | Original data | Original sample | The access label |
| Fixed-sample current reproduction | Current releases with class `EXACT_SUCCESSOR` or `CONCEPTUAL_SUCCESSOR` | Fixed sample | `UPDATED REPRODUCTION, FIXED SAMPLE` |
| Fixed sample with substitutes | As above, plus `SUBSTITUTE` series | Fixed sample | `UPDATED REPRODUCTION, FIXED SAMPLE, WITH SUBSTITUTES` |
| Eligibility-refreshed current reproduction | As the fixed-sample result | Refreshed sample | `UPDATED REPRODUCTION, ELIGIBILITY REFRESHED` |

In the updated reproduction without substitutes a component whose only current series is a substitute is treated like a missing component under the original index rule, and the omission is logged. A component with `NO_CURRENT_EQUIVALENT` is left out of all current results. If the original inequality measure has no exact or conceptual successor, the eligibility rule's third condition cannot be applied, and the refreshed result is reported as not possible with that reason. Any expanded sample, changed outcome, changed inequality measure or changed model is a modern extension and is outside this project.

## Reproduction lock

The specifications of the updated reproduction are fixed before anyone computes, views or infers an association between current inequality data and current outcome data. The reproduction lock, `docs/reproduction_lock.md`, identifies them. It lists the ID, the version number and the SHA-256 of each locked specification, the SHA-256 of the lineage file and of the refreshed eligibility table it relies on, and which published correlations its author had seen, since the blinding is procedural only. The commit that merges the lock is the lock commit. Updated reproduction starts only after you have reviewed milestone 1 and it is tagged. A later change to a locked specification is a new specification version, recorded as a dated amendment in the lock, and affected results are reported under both versions. A later correction of the lineage or of the eligibility table that would change a locked specification needs the same amendment. Downloading data, reading metadata and checking coverage before the lock are allowed.

## U.S. state sources

The original source of each state variable comes from the notes on sources and methods. The candidate current series are starting points for source lineage, which confirms each one and assigns its class.

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

The notes list nine index components for the states but say that 40 states have all eight measures. The specification uses all nine until the released file settles which is right. The notes report trust as missing for Alaska, Delaware, Hawaii, Idaho, Maine, Nebraska, New Mexico, Nevada and South Dakota, and homicides as missing for Wyoming. The released U.S. state file is the primary source for the historical state data when it is held. Without it, the historical state data are rebuilt from the vintages the notes name, from the agencies' archives and the two articles' state tables, with every value flagged reconstructed. The historical state specification, with its sources, years and transformations, and the tolerance of the check are committed before any state correlation is computed, and are not changed in response to it. The rebuild's correlations are then compared with those the notes report, such as r = 0.59 for the index. A match within the tolerance confirms the rebuild. A mismatch is logged in the discrepancy log with its likely cause, and the rebuild is not adjusted to close it.

# Part B. Technical architecture

## Stack

Python handles acquisition, reading, preparation, computation, checks and the report. It uses pandas and pyarrow for data, requests and tenacity for downloads, sdmx1 for OECD SDMX queries, wbgapi for World Bank WDI, openpyxl and xlrd for spreadsheets, PyYAML for specifications and records, scipy for correlations, pandera for schemas and pytest for tests. Pixi manages the environment from conda-forge, with PyPI only for packages conda-forge lacks, and its lockfile `pixi.lock` pins every package for macOS on Apple silicon and for Linux. `environment.yml` and `requirements.txt` are exported from pixi, and CI fails if either is out of date. Ruff runs through pre-commit. GNU Make is the only entry point, and each target calls `pixi run`. The project builds no workflow system and no plugin framework of its own. Bibliography work uses Crossref, PubMed E-utilities, the PMC ID converter, Unpaywall and OpenAlex.

## Code layout

| Path | Contents |
|---|---|
| `code/NN_*.py` | Thin command-line scripts. Each parses its arguments, loads a specification or a record, calls the library, writes its outputs and adds its step to the run record. A script holds no method rule and no source-specific parsing. |
| `code/lib/readers/` | One module per source family, such as the Equality Trust release, World Bank WDI, OECD, UNDP, CDC WONDER or NAEP. A reader turns a stored file into long-form observations and does nothing else. Readers are plain modules listed in one dictionary in `code/lib/readers/__init__.py`. |
| `code/lib/transform.py` | Shared transformations: unit conversion, direction coding, period selection, sample selection and the combination of parallel data. |
| `code/lib/compute.py` | The computation core: standardisation, the index and the correlations. It works on any unit type and never assumes that a unit key is a country code. |
| `code/lib/spec.py` | Loads and validates analysis specifications. |
| `code/lib/schemas.py` | The pandera schemas of every interface table, defined once. |
| `code/lib/records.py` | Reads and validates data source and acquisition records and builds the generated views. |
| `code/lib/runs.py` | Writes and reads run records. |
| `code/lib/download.py`, `code/lib/paths.py` | The recorded download helper, which refuses the network when `OFFLINE=1`, and path resolution relative to the project root. |

Historical and updated reproduction run the same scripts and the same core with different specifications. The numbered scripts are `01_ingest_original.py`, `01c_download_reconstruction_sources.py`, `02a_download_inequality.py`, `02b_download_outcomes.py` and `02d_download_controversy_test_data.py` for acquisition, `02e_extract.py` for extracts, `02f_build_outcome_coverage.py` for the coverage table, `03_prepare.py`, `03a_eligibility.py` and `04_reproduce.py` for the reproductions, and `06_build_headline.py` and `07_build_report.py` for the report. Every replay script takes `--spec` or `--source` and writes only to the paths the specification or record names.

## Analysis specifications

A specification is a YAML file `config/specs/<spec_id>.yaml`, validated against the schema in `code/lib/spec.py`, with the fields shown in `templates/analysis_spec.yaml`. It holds `spec_id`, `version` as an integer raised on every change, `dataset`, `unit_type`, the sample or a reference to an eligibility table, each variable with its lineage `variable_id`, source IDs in priority order, period, unit, conversion, transformation and direction, the missing-value rule, the standardisation reference, the index definition, the statistics, and the result types it produces with their series classes. Each choice that the original material leaves open carries a `rationale` key naming its section in `docs/method_rationale.md`.

There are four specifications: `historical_international`, `historical_us_states`, `updated_international` and `updated_us_states`. A specification is identified in every result and run record by its ID, its version and the SHA-256 of its file. The reproduction lock lists the same three values for the updated specifications, and `make check-contracts` fails if a locked specification changes without a new version and a lock amendment.

## Data model

The project keeps five concepts apart. Each has one place where it is maintained, and every other view is generated from it by ID.

| Concept | Meaning | Maintained in | Key |
|---|---|---|---|
| Data source | A provider's specific series or package and what it means | `data/metadata/sources/<source_id>.yaml` | `source_id` |
| Acquisition | One exact request, when it was made and what came back | `data/metadata/acquisitions/<acquisition_id>.yaml` | `acquisition_id` |
| File | A stored raw file: path, size, SHA-256, storage and the sources it holds | Inside its acquisition record | `path` |
| Analysis specification | Sample, transformations and computation rules | `config/specs/<spec_id>.yaml` | `spec_id` and `version` |
| Run | Code, environment, specifications, inputs, outputs and the state of each step | `outputs/runs/<run_id>.json` | `run_id` |

Two tables connect the concepts to the research. `docs/source_lineage.csv` maps each variable to its original and current data sources and holds no technical details of acquisitions or files. The unit registries `config/units/countries.csv` and `config/units/us_states.csv` list every valid unit with its key, name and aliases. `make manifests` generates the flat views `build/metadata/sources.csv`, `acquisitions.csv`, `files.csv` and `file_sources.csv` from the records. The views are not committed and never edited.

**Identifiers.** `source_id` is the provider and series in lower case, such as `worldbank-wdi-sp.dyn.le00.in` or `equalitytrust-international-inequality`. `acquisition_id` is `acq-` followed by the UTC time of the request and a short slug, such as `acq-20261019t101500z-wdi-life-expectancy`. A file is identified by its repository path, which is never reused for a raw file. `run_id` is the UTC start time followed by the short commit hash. `variable_id` is a readable slug such as `life_expectancy`. No identifier contains a thread ID or depends on which session did the work. Ownership is recorded separately, as described in Part C.

**Relations.** One data source has many acquisitions, one per version or retrieval. One acquisition has one or more raw files. A raw file holds one or more data sources, and a data source may be spread over several files. One acquisition may serve several analyses. A lineage row refers to exactly one original data source and at most one current data source. A specification refers to lineage rows by `variable_id`. A run refers to its specifications, input files and output files.

**Observations.** Readers produce long-form observations with `dataset`, `unit_type` as country or us_state, `unit_id` as an ISO 3166-1 alpha-3 code or a two-digit state FIPS code, `variable_id`, `period`, `value`, `unit`, `source_id`, `file_path` and `provenance` as released, reconstructed or current. Before combination the key is `dataset`, `unit_id`, `variable_id`, `period` and `source_id`. After combination the key is the same without `source_id`. A wide analysis table has one row per unit and one column per variable.

**Join rules.** Every join states its expected cardinality and is checked. Observations to the unit registry are many to one, and an unknown unit is an error. Observations to the lineage are many to one. Combining parallel data takes at most one value per source for each key and returns exactly one or none. Pivoting to the wide table is one to one per unit and variable. A join that multiplies rows unexpectedly, a key that is not unique, two units for one variable after conversion, or a unit missing from the registry stops the run with an error.

## Immutability and corrections

**Raw files are never modified.** Raw files live in `data/00_original_released/`, `data/00_original_reconstruction/`, `data/01_raw_current/` and `data/04_controversy_test_data/`. Only an acquisition script adds files there. A correction is a new file in a new acquisition whose record names the corrected acquisition or file in `corrects`. The path, size and SHA-256 in a file entry describe an immutable file, so they never change either. CI compares raw files and these fields with the base branch.

**Derived files are rebuilt in place.** Extracts in `data/02_extracts/`, analysis tables in `data/03_analysis_ready/` and everything in `outputs/` may be regenerated at the same path. Git keeps their earlier versions, and the run record of each new computation identifies its code, specification and inputs. No check compares a derived file with its earlier checksums.

**Metadata may be corrected.** A data source description, an acquisition status, a lineage row or a note may be corrected in a pull request, with the reason in the commit message or in the record's `notes`. Git history keeps every earlier version.

**Removal.** A file that contains credentials or personal data, breaks a licence, is subject to a takedown request or is malicious is removed in a pull request that a maintainer approves. The removal and its reason are recorded in `docs/removals.md`, and its file entry is kept with status `removed`.

## Storage

Git is the default store. Each stored file stays within 50 MiB, and an extract that would exceed it is split, for example by indicator or country. Bulk archives, such as the complete World Bank WDI or WID.world downloads, are never acquired. On 18 October 2026 those archives measured 283,089,754 and 886,945,845 bytes. Git LFS is not used.

An acquisition stores the provider's response as it was received, in the raw folder. An extract is a derived file: a replay step, `code/02e_extract.py`, reads the stored response with its reader and writes the relevant observations to `data/02_extracts/<source_id>.csv`. The run record links the extract to the response by path and SHA-256. When the response itself may not be published and is held only locally, the extraction step is a restricted target and the committed extract is retained as described under replay.

`make storage-report` sums the sizes in the file entries and reports the size of the repository's packed history. If the data folders exceed 500 MiB or the packed repository exceeds 1 GiB, the integrator opens an issue that proposes how to store the data, and you decide. A later change of storage must not change the computation. The code always reads the declared local paths, so another store only has to place the same files at the same paths and pass `make verify-data`.

## Licensing

Three rules decide what the repository publishes.

1. Material whose terms allow publishing, data files and texts alike, is published in the repository as it was obtained, under its own terms.
2. Material whose terms do not allow publishing is handled locally and never committed or released. The repository records it as a data source or a package record with its link. Data may be extracted from it only as long as the extract stays below the threshold of originality, such as individual values and facts, and never a copied table layout, text or figure. No substantial part of a database is taken either. An output that would cross either limit stays in the gitignored `outputs/local/` folder.
3. The project's own data collection, assembled from such extracts and from values the project derives, is published under CC BY 4.0. It covers `data/02_extracts/`, `data/03_analysis_ready/` and the tables in `outputs/tables/`. Every value names its data source through `source_id` and its file through the run record. Data fetched from elsewhere are published as they are, under their own terms, and are never relicensed.

Credentials and registration-protected files are never committed. A file you obtain by hand is listed in the owning thread's file in `data/local_data_required/` with its expected path, required version, acquisition page, acceptance steps and checksum, and its path is ignored in the `.gitignore` of its raw folder.

## Acquisition, replay and Make

`make acquire` is the only target that contacts live sources. It downloads, verifies and records, and its new files and records reach the repository through a pull request. `make all` replays every computation offline from stored files. The download helper refuses the network when `OFFLINE=1`, which `make all` sets.

Each thread declares its steps as Make targets in `make/<thread-id>.mk`, which the main `Makefile` includes. Every output is a target whose prerequisites are its script, its specification or record and its input files. Make builds every prerequisite a target needs, whichever list the target is in, so two rules keep acquisition and missing restricted steps out of a replay. First, every acquire rule sits in a block that is read only when `MODE=acquire`, and `make all` sets `MODE=replay`, so a replay has no recipe that downloads and an acquired file is an ordinary existing file to Make. Second, a target that needs a restricted input is listed in `RESTRICTED_TARGETS`, and its real rule is defined only when that input is present locally. Otherwise the target gets a stand-in rule with no prerequisites, which retains the committed output as described below. A downstream target such as the report therefore always finds a rule that needs neither the network nor the missing input. `make check-contracts` runs `make -n all` without the restricted inputs and fails if any acquire recipe or real restricted recipe would run.

Every table published in `outputs/` is built by a replay step from stored files and records, never by a download script, so emptying `outputs/` loses nothing that replay cannot rebuild, apart from `outputs/runs/` and the local files in `outputs/local/`.

A fresh clone does not keep file timestamps, so a clean replay rebuilds every replay target unconditionally, and data integrity is checked by hashes in `make verify-data`. `make clean-env` makes a fresh clone in a temporary folder, installs the environment from `pixi.lock`, runs `make verify-data` and runs `make all`.

## Run records and result states

Every `make all` and every acquisition writes a run record, `outputs/runs/<run_id>.json`, with the fields shown in `templates/run_record.json`. It holds the start and end time, the commit and whether the tree was clean, the SHA-256 of `pixi.lock`, the mode, the specifications with ID, version and SHA-256, and one entry per step. A step entry gives the target, its state, its inputs and its outputs with their SHA-256, and for each input how it was checked. The record of the run that produced committed outputs is committed with them. Run records are never edited. Times and other run metadata appear only in run records, never in result tables, so the result tables are deterministic.

Each step ends in one of three states.

| State | Meaning |
|---|---|
| `computed` | The output was computed in this run from inputs whose files were verified against their checksums. |
| `retained` | A required input was not held locally, so the earlier committed output was kept. Only the input IDs and checksums recorded with that output were compared with the file entries, because the missing file itself cannot be checked. |
| `not_produced` | The output could not be produced and no earlier output exists, with the reason. |

Each input check is recorded as `file_verified`, when the file's content was hashed in this run, or `record_matched`, when only the recorded checksum was compared with the file entry. Steps skipped and inputs missing are listed in the run record. `RESTRICTED INPUT` is separate from these states. It is the `input_access` value of a result that depends on an input under use restrictions, and it says nothing about whether the result was recomputed. The report shows for every result its state, how its inputs were checked and whether it carries `RESTRICTED INPUT`.

## Validation

`make check-contracts` runs in one of two modes.

- **metadata** runs in CI. It validates the schemas of specifications, records, lineage, registers and run records, the uniqueness of identifiers, every reference between them, file ownership on pull requests, that no raw file or immutable file entry field differs from the base branch, except a removal recorded in `docs/removals.md` and approved by a maintainer, that locked specifications match the lock, the `make -n all` check and the goal traceability rules. It reads no data file.
- **full** runs locally and in `make verify-data`. It does everything `metadata` does, then hashes every stored file and compares it with its file entry. A missing published file is an error. A restricted file that is not held locally is listed, not failed.

Acquisition statuses are `acquired`, `user_supplied`, `awaiting_user`, `access_failed`, `not_downloaded_restricted` and `removed`. Only `acquired` and `user_supplied` require a file and a checksum. The other statuses require their retrieval record or listing instead.

`make check-data` runs the integrity tests on the data present: schemas, key uniqueness, units, allowed values, references, checksums and the row counts of joins.

## Testing plan

Tests are organised by function, not by thread. The table gives each level its path, owner, dependencies and acceptance criterion. Ordinary tests never call an external service.

| Level | Path | Owner | Depends on | Accepted when |
|---|---|---|---|---|
| Computation unit tests | `tests/compute/` | Scaffold | `code/lib/transform.py`, `code/lib/compute.py` | Hand-checkable examples pass for direction coding, standardisation, missing components, index weights, the pairs entering a correlation and the sample size, and each expected value is written in the test from a hand calculation, not from the code |
| Reader tests | `tests/readers/<reader>/` with fixtures in `tests/fixtures/readers/<reader>/` | The thread that owns the reader | The reader module | Each reader turns its small stored example file into the expected observations, including units, periods and unit keys, without network access |
| Data integrity | `tests/integrity/`, run by `make check-data` | Scaffold | Schemas, records, registries | Schemas, key uniqueness, units, allowed values, references, checksums and join row counts pass on the data present |
| End to end | `tests/e2e/` with `tests/fixtures/synthetic/` | Scaffold, with the report thread adding the report assertions | All library modules and replay scripts | A synthetic dataset of a few countries and states runs offline from preparation to result tables, headline table and report, and every number matches the expected values in the fixture |
| Public data replay | `tests/replay/`, run by the CI replay job | Scaffold | Public data and replay steps on `main` | Once public data and replay steps exist, a CI replay from public inputs reproduces the committed outputs within the tolerances below |
| Release check | Run by `make clean-env` | Integrator | Everything on `main` | Before `deliverables-v1` and `results-v1`, a fresh clone in the locked environment verifies all data and replays, and a separate replay on a machine holding the restricted inputs records which restricted steps were computed |
| Eligibility | `tests/eligibility/` | Reproduction lock | `code/03a_eligibility.py` | The rule's three conditions, the order of exclusion and the handling of ties give the expected eligibility table on a constructed example |
| Report | `tests/report/` | Report | `code/06_build_headline.py`, `code/07_build_report.py` | The headline table and the report contain every result with its state and labels, and every figure file is produced and holds the expected series |

The tests cover these edge cases: a constant variable, whose standardisation and correlation must give a defined error or missing value rather than a number, a missing component, a duplicated observation key, a conflicting unit, an unknown unit, and a shuffled row order, which must not change any result.

Pandera checks structure and value constraints. Correctness of the computation is tested against expected values derived independently of the code.

In replay tests, identifiers, samples and missing units must match exactly. Floating-point values must match within an absolute tolerance of 1e-10 for z-scores, index values and correlations, and a relative tolerance of 1e-8 for p-values. The pinned environment should give identical results on one platform. The tolerances allow for differences in floating-point libraries between macOS and Linux on samples of at most 50 units, and they are far below the two decimals at which the authors published correlations. Figures are checked for being produced and for the data they plot.

A difference from a published value is never a test failure. It goes to the discrepancy log as a research result.

The plan sets no coverage percentage, browser automation, load tests or tests of every helper.

## Continuous integration

`ci.yml` runs on every pull request and on every push to `main`. It installs the locked environment, runs ruff, runs the computation, reader and end-to-end tests, checks that the exported environment files match `pixi.lock`, and runs `make check-contracts` in `metadata` mode. On a push there is no pull request, so the ownership check is skipped there. Once public data and replay steps exist, a replay job in the same workflow runs `make all` on the public inputs and the replay tests, so restricted steps are retained and reported as such. In milestone 3 the report thread adds `pages.yml`, which runs only when a tag matching `results-*` is pushed and publishes the committed `site/` folder. Third-party actions are pinned to commit hashes, and workflows get the minimum permissions they need.

## Report and site

`code/06_build_headline.py` builds `outputs/tables/headline_results.csv` from the result tables. `code/07_build_report.py` writes the report as Markdown from the prose in `report/` and the result tables, run records and registers, so no number is typed in by hand. It writes `docs/replication_report.md` and the same page as `site/index.md`, and copies the figures it uses into `site/`. GitHub Pages publishes `site/` with its standard Markdown build. The site is the report with links to the `deliverables-v1` release and to the repository, and it states the release tag, the lock commit, the commit it was built from and the date.

## Reference tables

**Data source record.** `source_id`, `provider`, `series_code`, `title`, `definition`, `unit`, `geography`, `licence`, `terms_url`, `redistributable` and `notes`. See `templates/data_source.yaml`.

**Acquisition record.** `acquisition_id`, `source_ids`, `method` as download, api, manual or archive, `request` as the exact URL or query with its parameters, `requested_utc`, `response_status`, `dataset_version`, `status` as one of the acquisition statuses, `corrects`, `retrieval_log`, `notes`, and a list of `files`, each with `path`, `size_bytes`, `sha256`, `storage` as git or local, `redistributable` and `source_ids`. See `templates/acquisition.yaml`.

**Source lineage.** `variable_id`, `dataset` as international or us_states, `role` as inequality, index_component, extra_measure or eligibility, `meaning`, `original_source_id`, `original_locator` as the released file's sources sheet, the notes page or another document, `original_reference_period`, `current_source_id`, `comparability`, `deviation_reason`, `reported_r` and `reported_p` as the authors published them, `verification_status`, `verification_log_ref` and `notes`.

**Result tables.** `spec_id`, `spec_version`, `spec_sha256`, `result_type` as historical_reproduction, current_fixed_sample, current_fixed_sample_with_substitutes or current_eligibility_refreshed, `dataset`, `variable_id`, `r`, `p`, `n`, `missing_units`, `access_label` and `input_access`. Comparison tables of parallel data have `dataset`, `unit_id`, `variable_id`, `period`, the two source IDs, both values and the difference.

**Headline table.** `indicator`, `dataset`, `reported_r`, `historical_r`, `historical_n`, `updated_r` and `updated_n` from the fixed-sample result, `comparability` and `deviation_reason`.

**Eligibility tables.** `outputs/tables/historical_country_eligibility.csv` and `outputs/tables/refreshed_country_eligibility.csv`, with one row per country considered and `unit_id`, `income_rank`, `population`, `inequality_data_available`, `eligible` and `exclusion_reason` as not_top_50, population_below_3m, no_comparable_inequality_data or empty.

**Package records.** Each source package subfolder has a `records.csv` for texts, with `citation_key`, `authors`, `year`, `title`, `edition`, `journal_or_publisher`, `doi`, `pmid`, `pmcid`, `isbn`, `stable_url`, `archive_url`, `access_date`, `peer_review_status`, `roles`, `claim_or_controversy_ids`, `open_access`, `licence`, `download_status` as published, local or record_only, `record_only_reason`, `local_path`, `sha256` and `notes`. See `templates/package_records.csv` and `templates/screening_log.csv`.

**Controversy register.** `docs/controversy_register.csv` with `controversy_id`, `claim_or_result_affected`, `target_level` as original, current, both or general_hypothesis, `mapping_rationale`, `source_role` as critic or independent, `source_author`, `source_title`, `publication_year`, `publication_date_type`, `source_type`, `peer_review_status`, `exact_controversy_in_neutral_words`, `testable_statement`, `wilkinson_pickett_response_available`, `response_source_id`, `local_path`, `citation_url` and `notes`. A controversy ID is its category followed by a number, such as `inequality-measure-002`.

**Controversy data map.** `docs/controversy_data_map.csv` with `controversy_id`, `source_id`, `testable_statement`, `target_level`, `required_variables`, `required_geographies`, `required_years`, `candidate_sources`, `chosen_source`, `access_route`, `licence_status`, `redistributable`, `acquisition_status`, `local_paths`, `country_coverage`, `year_coverage` and `reason_not_obtained`, with one row per controversy and dataset.

**Claims register.** `docs/claims_register.csv` with `claim_id` such as `claim-007`, `author`, `source_work`, `source_locator`, `publication_year`, `stable_identifier`, `wording`, `wording_type` as verbatim or paraphrase, `claim_class` as descriptive_correlation, proposed_mechanism, causal_claim or policy_prediction, `verification_status` as verified or to_be_verified, `verification_log_ref` and `notes`. `claim_class` stays empty while the status is to_be_verified.

**Controversy categories.** `country-selection` covers country selection and sample definition. `inequality-measure` covers the inequality measure, including the 80:20 ratio against Gini, market against disposable income, and survey comparability and timing. `index-construction` covers composite-index construction, including weighting, component choice and reverse coding. `outliers` covers outliers and influential countries. `temporal-persistence` covers persistence in later data and in national time series. `mechanism` covers the psychosocial account and alternatives such as material conditions, public services, institutions and social cohesion. `data-comparability` covers data availability and comparability. A criticism that predates *The Spirit Level* or addresses the hypothesis in general, such as Judge 1995 or Gravelle 1998, has `target_level` set to `general_hypothesis`, and its `mapping_rationale` names the result it bears on.

**Report sections.** Scope and terminology. Headline results. Goals and deliverables, reporting each of the six goals. Historical reproduction. Fixed-sample current reproduction, with its substitute variant. Eligibility-refreshed current reproduction, or the reason it is not possible. Each reproduction section reports the countries and the U.S. states separately and gives each result's state, input checks and labels. Supporting sources. Controversies, where each entry states the source's claim, cites it, names its category, lists the datasets downloaded for it and links any published response by Wilkinson and Pickett. Author claims, as the register stands at the `results-v1` tag. Limitations, covering the absence of the book and the assumptions that stand in for it, the small sample, cross-national comparability, temporal misalignment, missing data, measurement changes, series that ended or changed definition, and that the project tests neither the controversies nor causality. Reproducibility, with commands, environment, specification versions, the lock commit, data-access limits and links to the release and the repository.

# Part C. Work organisation

## Threads

Each thread is a separate Claude session that owns a fixed set of paths, works on its own branch and hands over through Part A and Part B. No two threads write the same file. Each thread has a name used in prose and an ID used by tools.

| Thread | ID | Goal |
|---|---|---|
| Scaffold | `scaffold` | All |
| Original access and sample recovery | `original-access` | 1, 2 |
| Source lineage | `source-lineage` | 1 |
| Historical reproduction | `historical-reproduction` | 2 |
| Current inequality data | `inequality-data` | 1 |
| Current outcome data | `outcome-data` | 1 |
| Reproduction lock | `reproduction-lock` | 2 |
| Updated reproduction | `updated-reproduction` | 2 |
| Supporting sources | `supporting-sources` | 3 |
| Controversy sources and register | `controversy-register` | 4 |
| Controversy test data | `controversy-test-data` | 5 |
| Author claims register | `claims-register` | Addition |
| Report and clean offline run | `report` | 6 |

**Ownership.** The paths each thread owns are listed in `docs/ownership/<thread-id>.csv`, one pattern per row. Each thread owns its own ownership file and adds a row for every record file it creates, such as a data source or acquisition record. The ownership check reads all of these files, fails if two threads claim the same path, and fails if a pull request from a branch `<thread-id>/<description>` changes a path its thread does not own.

**Integrator.** The integrator is a separate Claude session. It creates the milestone tags after your approval, makes changes to the files the scaffold thread owns on branches named `scaffold/<description>`, and runs the release check. A reader module is owned by the thread that creates it. When another thread needs a change to it after the owner has finished, it asks in its merge package, and the integrator makes the change. Whether the integrator later becomes an automated agent is left for consideration.

## Execution order

Work runs in waves. A thread starts only when every gate it depends on has passed. Wave numbers give the order, and the milestone says which tag requires the thread.

| Wave | Thread | Starts when | Milestone |
|---|---|---|---|
| 0 | Scaffold | Planning documents merged | 1 |
| 1A | Original access | Scaffold merged | 1 |
| 1A | Supporting sources, controversy sources and register | Scaffold merged | 2 |
| 1A | Claims register | Scaffold merged. It never gates a tag | None |
| 1B | Source lineage, historical reproduction | Original access merged | 1 |
| 1C | Inequality data, outcome data | Source lineage merged | 1 |
| 1D | Reproduction lock | Historical reproduction, inequality data and outcome data merged | 1 |
| 1E | Lock gate | Milestone 1 reviewed and tagged | 1 to 2 |
| 2A | Updated reproduction | Lock gate passed | 2 |
| 2B | Controversy test data | Frozen controversy register merged | 2 |
| 3 | Report | `deliverables-v1` tagged | 3 |

A thread reads another thread's output only from `main` after that thread has merged. The inequality data, outcome data and controversy test data threads mainly download and catalogue and can use a cheaper model. All other threads involve judgement and use the default model.

## Milestones and repository

The project lives in https://github.com/open-reanalysis/how-economic-inequality-harms-societies, and the site is published at https://open-reanalysis.github.io/how-economic-inequality-harms-societies/.

| Milestone | Tag | Threads | What you review first |
|---|---|---|---|
| 1. Data and historical reproduction | `milestone-1` | Scaffold, original access, source lineage, historical reproduction, inequality data, outcome data, reproduction lock | The source lineage, the method rationale and the historical specifications, the historical results with their access label, and the reproduction lock |
| 2. Updated reproduction and source packages | `deliverables-v1` | Updated reproduction, supporting sources, controversy sources and register, controversy test data | The updated results with their discrepancy log, the two source packages with their READMEs, the frozen controversy register and the controversy test data |
| 3. Report and publication | `results-v1` | Report | The report and the site |

Each thread works on a branch `<thread-id>/<description>` from `main` and opens a pull request into `main`. The pull request description is the merge package. A thread pull request auto-merges with a merge commit once every required check passes, and it opens only when the thread's start conditions are met. `main` accepts changes only through pull requests with passing checks and blocks force pushes. Tags matching `milestone-*`, `deliverables-*` and `results-*` are protected so that only organisation owners create them, and the integrator creates them with an owner account after your approval. History is never rewritten. Squash, rebase, amend and force push follow the rule in CONTRIBUTING.md.

**Merge package.** The commit hash, the changed files, the thread's completion checklist, the `full` validation output, the tests run by level with their exit status, the run record of any committed outputs, known access failures, licence and redistribution status, and confirmation that only owned paths changed.

**Milestone review.** When every thread a milestone lists has merged, the integrator sends you the files to read first, the thread pull requests with their merge packages and the latest check results. Before `deliverables-v1` it also runs the release check and reports its run records. You review `main` at that commit. When you approve, the integrator tags it, and the tag message lists the pull requests it covers.

**Deliverables release.** After you approve milestone 2, the integrator publishes a GitHub release from the `deliverables-v1` tag. Its notes are generated from the acceptance tests of goals 1 to 5 and the package READMEs and list every lineage row still marked not yet verified with its reason. It needs no data assets, because every stored file is in the repository.

## Steps that need you

Access requirements are verified when a source is acquired and recorded in its acquisition record. When a source needs registration or acceptance of terms, the thread stops at the access page, adds an entry to its own file in `data/local_data_required/` and tells you what to do. Creating accounts and accepting terms is yours. You check a source's licence where a thread could not establish it. You approve the assumptions in `docs/worklist.md` before the run, decide any point they do not cover, and approve the method rationale with the historical specifications in the milestone 1 review. You decide whether to register research use of *The Spirit Level at 15* with the Equality Trust. You review the three milestones and approve their tags. You decide on the storage proposal if the storage report exceeds its thresholds. The decisions taken for the current run are in [docs/worklist.md](docs/worklist.md).

Code and tests are under MIT, in `LICENSE`. Documents, the report, the site, figures and the project's own data collection are under CC BY 4.0, in `LICENSE-docs`. Data and texts obtained elsewhere keep their own terms.

Branch protection does not require an approving review while you are the only human contributor. Your milestone review is the human review. Once a second person contributes, one approving review becomes required.

## New artefacts

| Artefact | Path | Owner | Depends on | Done when |
|---|---|---|---|---|
| Library skeleton and computation core | `code/lib/` except `code/lib/readers/<family>.py` | Scaffold | This plan | The computation unit tests and the end-to-end test pass |
| Schemas | `code/lib/schemas.py`, `code/lib/spec.py` | Scaffold | Reference tables in this plan | Every interface table, specification, record and run record validates against one schema |
| Unit registries | `config/units/countries.csv`, `config/units/us_states.csv` | Scaffold | ISO 3166-1 and Census FIPS lists | Every unit in the released data and the lineage resolves to exactly one entry |
| Templates | `templates/` | Scaffold | Reference tables | Each template validates against its schema |
| Ownership files | `docs/ownership/<thread-id>.csv` | Each thread its own | This plan | The ownership check finds no overlap |
| Historical specifications and method rationale | `config/specs/historical_*.yaml`, `docs/method_rationale.md` | Historical reproduction | Source lineage, source-verification logs | You approve them in the milestone 1 review |
| Updated specifications and lock | `config/specs/updated_*.yaml`, `docs/reproduction_lock.md` | Reproduction lock | Historical specifications, lineage, coverage and eligibility tables | The lock lists every updated specification with version and SHA-256, and the contract check passes |
| Readers | `code/lib/readers/<family>.py` with tests and fixtures | The thread that acquires the source family | Data source and acquisition records | The reader tests pass on stored example files |
| Run records | `outputs/runs/` | The thread whose run produced committed outputs | `code/lib/runs.py` | Every committed output appears in exactly one committed run record |
| Storage report | `make storage-report` | Scaffold | File entries | It reports both sizes against the thresholds |
| Worklist | `docs/worklist.md` | Integrator | This plan | It names the current run's date, order and decisions |

## Thread briefs

A thread's brief is its section below plus Parts A and B and INTENT.md. Owned paths are in its ownership file.

### Scaffold

Configures the repository: the rulesets, auto-merge, the pull request template, `ci.yml`, the pixi workspace with its lockfile and exported files, pre-commit, the `Makefile` with `make/scaffold.mk`, the library skeleton and computation core, schemas, unit registries, templates, the contract checks, the storage report, the integrity, computation, end-to-end and replay tests, and the template for the files in `data/local_data_required/`. The root `.gitignore` holds only general rules, such as every `local/` folder, `build/` and temporary folders. Each data thread keeps the ignore rules for its own raw folder in that folder. The planning pull request before the scaffold thread is exempt from the ownership check, which does not exist yet.

### Original access and sample recovery

Decides the access gate and downloads and preserves the original material without modifying it. Obtains the authors' own works that milestone 1 depends on into `sources/supporting/original-authors/`: *The Spirit Level at 15* with its technical appendix, Pickett and Wilkinson's "Income inequality and health: a causal review", DOI 10.1016/j.socscimed.2014.12.031, and the Equality Trust's material on the book. *The Spirit Level*, Allen Lane 2009, ISBN 978-1-84614-039-6, gets a record marked not obtained.

*The Spirit Level at 15*, DOI 10.15124/yao-de9s-7k93, may be used freely for research with acknowledgement but needs permission for re-use in other publications, so it is handled locally and recorded with its link. The copy you supplied on 18 October 2026 has SHA-256 `c14eb8832b6aea4f7d02817e535125a7a34f0e630a271238db73175febdb2aea` and 39 pages. Its figures carry no correlation coefficients.

The released international data, `international-inequality.xls`, holds the 23 countries, the inequality measure, the ten index components, the index and further measures, with sheets of sources and errata. A copy downloaded on 18 October 2026 has SHA-256 `1897f2bbe503d35df3aea5f3d25a1b719660e1f4761f5913464b6a3b35c6c661`. It was last saved in 2011 and its errata say some series were revised after the book. The notes on statistical sources and methods are read through the Internet Archive copy of 7 January 2017. The released U.S. state data could not be downloaded, because the archived page's download button has no link, and the file is listed in `data/local_data_required/original-access.md`.

Writes the Equality Trust reader with its tests, `outputs/tables/original_sample_recovery.csv` with unit membership, outcome availability flags and source references but no outcome values, and its source-verification log, including what the appendix says about the original method.

### Source lineage

Builds `docs/source_lineage.csv` for the ten indicators, the inequality measure, every U.S. state series and the income and population series the eligibility rule needs, and the data source records of the original series. Reads no outcome values.

### Historical reproduction

Writes the historical specifications and the method rationale from the approved assumptions, puts to you only a point they do not cover, and logs every verified fact. Writes the readers and acquisition script for reconstruction material in `data/00_original_reconstruction/`, including the April 2004 WDI vintage if it can be obtained and the historical U.S. state series. Runs the historical reproduction for both datasets under the access label, checks the eligibility rule against the released 23 countries in `outputs/tables/historical_country_eligibility.csv`, publishes the parallel data comparison, and logs every difference from the reported values in `outputs/diagnostics/historical_reproduction_discrepancies.md`.

### Current inequality data and current outcome data

Download the current release of each series the lineage names, create their data source and acquisition records, and write their readers with tests. The inequality thread takes the inequality series. The outcome thread takes the outcome series and the income and population series for eligibility, which come from the same World Bank source family, into `data/01_raw_current/eligibility/`. A rolling or API source has its request and response pinned. For PISA the outcome thread records participation and sampling-standard flags per country and cycle. The outcome thread publishes `outputs/tables/outcome_source_coverage.csv` with coverage and years but no outcome values. Neither thread relates inequality to outcomes.

### Reproduction lock

Writes the updated specifications and the lock once historical reproduction, inequality data and outcome data have merged, reading no current outcome values. Builds the refreshed sample with `code/03a_eligibility.py` into `outputs/tables/refreshed_country_eligibility.csv` from the income, population and inequality files only, with the eligibility tests.

### Updated reproduction

Runs the updated specifications for both datasets, writes `outputs/tables/updated_*` and `outputs/figures/updated_*`, the parallel data comparison for current data, and the discrepancy log `outputs/diagnostics/updated_reproduction_discrepancies.md`, which compares each value with the one the authors reported.

### Supporting sources

Builds the supporting package in `sources/supporting/academic/` and `sources/supporting/non-academic/` with its `manifest.csv`, `README.md` and `screening_log.csv`, under the shared search and screening protocol below. The package needs at least one peer-reviewed study by authors other than Wilkinson and Pickett. The README, generated from the manifest, counts the texts published, the texts kept locally and the records without a text, with the reason for each.

### Controversy sources and register

Builds the controversy package in `sources/controversies/academic/`, `non-academic/` and `responses/`, and the register `docs/controversy_register.csv`. A row enters the register only with the author's name, exact title, year and a stable DOI, PMID, PMCID, ISBN or URL, checked against its record, and a book also needs its edition. The seed list includes Greener in the International Journal of Comparative Sociology, DOI 10.1177/00207152241245620, Judge 1995, Gravelle 1998, the Equality Trust author response, Fischer in the Boston Review, Saunders's "Beware False Prophets" for Policy Exchange, Snowdon's *The Spirit Level Delusion*, Sanandaji, Malm and Sanandaji's "The Spirit Illusion" for the Taxpayers' Alliance, Sanandaji and others in the Wall Street Journal in 2010, Goldthorpe's "Analysing Social Inequality" in the European Sociological Review 2010, DOI 10.1093/esr/jcp046, Rowlingson's 2011 review for the Joseph Rowntree Foundation, Nettle's 2017 essay on the psychosocial account, and the TUC summary of criticisms and replies. The responses folder holds the authors' 2010 responses to Snowdon, the Taxpayers' Alliance and Policy Exchange, Hugh Noble's "The Spirit Level Revisited" and the authors' response to the Rowntree review. The thread records whether each date is the online-first or the issue date. The register is frozen by a commit that records the search cut-off date and the search log, and a criticism found later goes in a dated amendment.

### Controversy test data

Starts once the frozen register has merged. Writes `docs/controversy_data_map.csv` and downloads the data for every register row with a testable statement. A dataset several rows need is stored once in `data/04_controversy_test_data/shared/`, and every other package in `data/04_controversy_test_data/by_controversy/<controversy_id>/` with a README naming its controversies. Coverage is taken from non-missing flags only, and no analysis is run. A dataset that cannot be obtained gets its barrier in its map row.

### Author claims register

Builds `docs/claims_register.csv` from the authors' published material: the notes on sources and methods, the frequently asked questions, the 2010 responses, *The Spirit Level at 15* and its appendix, the 2015 causal review, Wilkinson's 2011 TED talk and the authors' replies to criticism. A book page that such material cites is recorded as cited, not as checked. No quotation, page or identifier is entered without checking it. The register never attributes a causal inference to a correlation the authors reported without one, nor omits a causal claim they made. It is frozen by a commit that records its cut-off date.

### Report and clean offline run

Builds the headline table and the report, adds `pages.yml`, writes the report tests, runs the release check before `results-v1` and checks the completion criteria, reporting each of the six goals first.

## Shared search and screening protocol

Both source packages are searched and screened the same way, so the inclusion standard is not stricter for one side. Both use OpenAlex, Crossref and PubMed, the Equality Trust site and the sources the authors and their critics cite, search backward and forward from the same starting works, and record the search date. A source is included when it has an identifiable author, a citable record and an argument or evidence about Wilkinson and Pickett's findings or the hypothesis behind them. Whether it supports or criticises the findings never decides inclusion. Every screened source gets a row in the package's `screening_log.csv`. A source with several roles is downloaded once, into the folder of its main role, and listed in both manifests. Every legally obtainable text is downloaded. A text whose terms allow publishing is committed to its folder. Any other text is kept in the gitignored `local/` folder of its subfolder and recorded with its link, an archived landing page where it has no DOI, and the SHA-256 of the file read.
