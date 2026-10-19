# Implementation plan

This plan sets how the project is implemented and in which order the work is done. [INTENT.md](INTENT.md) sets the goals and the scope. [RESEARCH-METHOD.md](RESEARCH-METHOD.md) is the research method, and this plan does not restate it. The exact choices of each computation are in the analysis specifications in `config/specs/`. Part A is the technical architecture and Part B the work organisation. The plan does not depend on a date. The schedule, the approved assumptions and the decisions of the current run are in [docs/worklist.md](docs/worklist.md).

## Goals and priorities

The project has six goals, in this order of priority. They come from the original project specification.

| Priority | Goal | Owner | Output path | Acceptance test | Blocking dependencies | Milestone | Human decision |
|---|---|---|---|---|---|---|---|
| 1 | Download the current version of every dataset Wilkinson and Pickett used | Source lineage, with original access, inequality data and outcome data | `data/00_original_released/`, `docs/source_lineage.csv`, `data/01_raw_current/` | Every original variable has a lineage row with a comparability class and either its current file with a matching file record or a documented absence, verification or acquisition barrier; a NOT_YET_VERIFIED row has a logged verification attempt and its reason, and lack of access alone never determines comparability | Scaffold | 1 | Accept the terms of use of sources that require it |
| 2 | Reproduce their findings | Updated reproduction, with historical reproduction and reproduction lock | `config/results_catalogue.csv`, `outputs/tables/historical_*`, `outputs/tables/updated_*`, `outputs/tables/headline_results.csv`, `outputs/diagnostics/discrepancy_summary.md` | Every catalogue row has a historical result and the three current results, or a documented reason why it could not be produced, every deviation from a published value is logged with its likely cause, every current result names its locked specification and version, and a partial U.S. state reconstruction is documented as partial | Goal 1 | 1 and 2 | Approve the assumptions before the run |
| 3 | Download a package of sources supporting their findings, academic and non-academic | Supporting sources, with original access for the authors' own works | `sources/supporting/` | The search protocol in the research method has been carried out and logged, independent peer-reviewed evidence has been sought and its findings or absence reported, every legally obtainable included text is downloaded or has a recorded reason, and the README states the known gaps; no favourable-source quota determines completion | Scaffold | 2 | None |
| 4 | Download a package of sources setting out controversies about their findings | Controversy sources and register | `sources/controversies/`, `docs/controversy_register.csv` | The same protocol has been carried out and logged, every register row has an identifiable source, its argument in neutral words, its target and any reply, and every legally obtainable text is downloaded or has a recorded reason | Scaffold | 2 | None |
| 5 | Download datasets that may support those controversies | Controversy test data | `data/04_controversy_test_data/`, `docs/controversy_data_map.csv` | Every register row with a testable statement has a map row with its variables, coverage and years defined before acquisition, and a final state of `acquired`, `partially_acquired` or `barrier_documented` | Goal 4 register freeze | 2 | None |
| 6 | Publish the results on a GitHub Pages site | Report | `site/`, `.github/workflows/pages.yml` | The results-v1 tag publishes a page for every catalogue result showing every specified variant and its state; computed or retained results show their available figure, observations, sample, sources, comparability and deviations, downloads contain exactly the plotted observations where publication is permitted, and not_produced variants show their barrier without requiring a figure, observation table or download | Goals 1 to 5 | 3 | Approve the `results-v1` tag |

The same table is kept in machine-readable form in `docs/goal_traceability.csv`. `make check-contracts` fails if any goal lacks an owner, an output path, an acceptance test or a milestone, if an output path is not owned by one of the goal's threads, or if a goal in milestone 1 or 2 depends on a thread outside milestones 1 and 2.

The project keeps one addition beyond the goals. The author claims register records and classifies what Wilkinson and Pickett claim. It never delays a goal or gates a tag.

Milestone 2 ends with `deliverables-v1`, a release that can be read on its own. It holds the data, the result catalogue and result tables, the headline table, the discrepancy summary, the two source packages and the registers. It needs neither the site nor a complete U.S. state reconstruction. Milestone 3 delivers goal 6.

# Part A. Technical architecture

## Stack

Python handles acquisition, reading, preparation, computation, checks and the report. It uses pandas and pyarrow for data, requests and tenacity for downloads, sdmx1 for OECD SDMX queries, wbgapi for World Bank WDI, openpyxl and xlrd for spreadsheets, PyYAML for specifications and records, scipy for correlations, matplotlib for figures, pandera for schemas and pytest for tests. Pixi manages the environment from conda-forge, with PyPI only for packages conda-forge lacks, and its lockfile `pixi.lock` pins every package for macOS on Apple silicon and for Linux. `environment.yml` and `requirements.txt` are exported from pixi, and CI fails if either is out of date. Ruff runs through pre-commit. GNU Make is the only entry point, and each target calls `pixi run`. The project builds no workflow system, no plugin framework and no web application of its own. Bibliography work uses Crossref, PubMed E-utilities, the PMC ID converter, Unpaywall and OpenAlex.

## Code layout

| Path | Contents |
|---|---|
| `code/NN_*.py` | Thin command-line scripts. Each parses its arguments, loads a specification or a record, calls the library, writes its outputs and adds its step to the run record. A script holds no method rule and no source-specific parsing. |
| `code/lib/readers/` | One module per source family, such as the Equality Trust release, World Bank WDI, OECD, UNDP, Census, CDC WONDER or NAEP. A reader turns a stored file into long-form observations and does nothing else. Readers are plain modules listed in one dictionary in `code/lib/readers/__init__.py`. |
| `code/lib/transform.py` | Shared transformations: unit conversion, direction coding, period selection, sample selection and the combination of parallel data. |
| `code/lib/compute.py` | The computation core: standardisation, the index with its component report, the correlations and the observation table of each comparison. It works on any unit type and never assumes that a unit key is a country code. |
| `code/lib/spec.py` | Loads and validates analysis specifications and the result catalogue. |
| `code/lib/schemas.py` | The pandera schemas of every interface table, defined once. |
| `code/lib/records.py` | Reads and validates data source and acquisition records and builds the generated views. |
| `code/lib/runs.py` | Writes and reads run records. |
| `code/lib/download.py`, `code/lib/paths.py` | The recorded download helper, which refuses the network when `OFFLINE=1`, and path resolution relative to the project root. |

Historical and updated reproduction run the same scripts and the same core with different specifications. The acquisition scripts are `01_ingest_original.py`, `01c_download_reconstruction_sources.py`, `02a_download_inequality.py`, `02b_download_outcomes.py` and `02d_download_controversy_test_data.py`. The replay scripts are `02e_extract.py` for extracts, `02f_build_outcome_coverage.py` for the coverage table, `03_prepare.py`, `03a_eligibility.py` and `04_reproduce.py` for the reproductions, `06_build_headline.py` for the headline table and the discrepancy summary, and `07_build_report.py` for the report and the site. Source-independent coverage and summary scripts take their declared canonical records; calculation scripts take `--spec` or `--source` and writes only to the paths the specification, the catalogue or the record names.

## Result catalogue and analysis specifications

**Result catalogue.** A missing published numeric benchmark is permitted with a reason in notes; the calculation can be reproduced without claiming numerical agreement with an unpublished statistic. Values estimated from a figure are identified as estimates with their precision. `config/results_catalogue.csv` lists every comparison the research method includes, with one row per comparison and the canonical columns in `templates/results_catalogue.csv`: `result_id`, `dataset`, `indicator_or_index` as a lineage `variable_id` or `index`, `predictor`, `sample`, `reported_statistic`, `reported_value`, `source_reference`, `historical_reproduction_required`, `current_reproduction_required` and `notes`. It is the only list of what is computed and reported. Its variables refer to the lineage, and its samples to the sample names in the specifications. Lineage rows hold no reported values.

**Analysis specifications.** A specification is a YAML file `config/specs/<spec_id>.yaml`, validated against the schema in `code/lib/spec.py`, with the fields shown in `templates/analysis_spec.yaml`. It holds `spec_id`, `version` as an integer raised on every change, `dataset`, `unit_type`, its named samples, the eligibility details where a sample uses the rule, each variable with its lineage `variable_id`, data sources in priority order, period, unit, conversion, transformation and direction, the missing-component rule, the evidence or assumption status of each choice using the values in templates/analysis_spec.yaml, the standardisation reference, the index definition, the check against published values for a reconstruction, and the current result variants it produces, each with a unique `variant_id`. It selects the catalogue rows of its dataset and never copies them. Each choice the original material leaves open names its section in `docs/method_rationale.md`.

There are four specifications: `historical_international`, `historical_us_states`, `updated_international` and `updated_us_states`. A specification is identified in every result and run record by its ID, its version and the SHA-256 of its file. The reproduction lock lists the same three values for the updated specifications, together with the SHA-256 of the catalogue, the lineage and the refreshed eligibility table. `make check-contracts` fails if a locked specification changes without a new version and a lock amendment.

## Data model

The project keeps five concepts apart. Each has one place where it is maintained, and every other view is generated from it by ID.

| Concept | Meaning | Maintained in | Key |
|---|---|---|---|
| Data source | A provider's specific series or package and what it means | `data/metadata/sources/<source_id>.yaml` | `source_id` |
| Acquisition | One exact request, when it was made and what came back | `data/metadata/acquisitions/<acquisition_id>.yaml` | `acquisition_id` |
| File | A stored raw file: path, size, SHA-256, storage and the data sources it holds | Inside its acquisition record | `path` |
| Analysis specification | Samples, transformations and computation rules | `config/specs/<spec_id>.yaml` | `spec_id` and `version` |
| Run | Code, environment, specifications, inputs, outputs and the state of each step | `outputs/runs/<run_id>.json` | `run_id` |

Three tables connect the concepts to the research. `docs/source_lineage.csv` maps each variable to its original and current data sources and holds no technical details of acquisitions or files. `config/results_catalogue.csv` lists the comparisons. The unit registries `config/units/countries.csv` and `config/units/us_states.csv` list every valid unit with its key, name and aliases. `make manifests` generates the flat views `build/metadata/sources.csv`, `acquisitions.csv`, `files.csv` and `file_sources.csv` from the records. The views are not committed and never edited.

**Identifiers.** `source_id` is the provider and series in lower case, such as `worldbank-wdi-sp.dyn.le00.in`. `acquisition_id` is `acq-` followed by the UTC time of the request and a short slug. A file is identified by its repository path, which is never reused for a raw file. `run_id` is the UTC start time followed by the short commit hash. `variable_id` and `result_id` are readable slugs, such as `life_expectancy` and `intl-inequality-index`. `variant_id` is `historical` for historical results and `updated`, `refreshed` or `with_substitutes` for current results. A result row is uniquely identified by `(spec_id, spec_version, result_id, variant_id)`. Every current specification declares its variants in `current_results`; a historical specification uses `historical`. No identifier contains a thread ID or depends on which session did the work.

**Relations.** One data source has many acquisitions. One acquisition has one or more raw files. A raw file holds one or more data sources, and a data source may be spread over several files. One acquisition may serve several analyses. A lineage row refers to exactly one original data source and at most one current data source. A catalogue row refers to two lineage variables or to one variable and the index. A specification refers to lineage rows and selects catalogue rows. A run refers to its specifications, input files and output files.

**Observations.** Readers produce long-form observations with `dataset`, `unit_type` as country or us_state, `unit_id` as an ISO 3166-1 alpha-3 code or a two-digit state FIPS code, `variable_id`, `period`, `value`, `unit`, `source_id`, `file_path` and `provenance` as released, reconstructed or current. Before combination the key is `dataset`, `unit_id`, `variable_id`, `period` and `source_id`. After combination the key is the same without `source_id`.

**Join rules.** Every join states its expected cardinality and is checked. Observations to the unit registry are many to one, and an unknown unit is an error. Observations to the lineage are many to one. Combining parallel data takes at most one value per source for each key and returns exactly one or none. A comparison takes one value per unit for each of its two variables. A join that multiplies rows unexpectedly, a key that is not unique, two units for one variable after conversion, or a unit missing from the registry stops the run with an error.

## Immutability and corrections

**Raw files are never modified.** Raw files live in `data/00_original_released/`, `data/00_original_reconstruction/`, `data/01_raw_current/` and `data/04_controversy_test_data/`. Only an acquisition script adds files there. A correction is a new file in a new acquisition whose record names the corrected acquisition or file in `corrects`. The path, size and SHA-256 in a file entry never change either. CI compares raw files and these fields with the base branch.

**Derived files are rebuilt in place.** Extracts in `data/02_extracts/`, analysis tables in `data/03_analysis_ready/` and everything in `outputs/` except `outputs/runs/` may be regenerated at the same path. Git keeps their earlier versions, and the run record of each new computation identifies its code, specification and inputs.

**Metadata may be corrected.** A data source description, an acquisition status, a lineage row, a catalogue row or a note may be corrected in a pull request, with the reason in the commit message or in the record's `notes`. A correction that would change a locked specification needs a lock amendment.

**Removal.** A file that contains credentials or personal data, breaks a licence, is subject to a takedown request or is malicious is removed in a pull request that a maintainer approves. The removal and its reason are recorded in `docs/removals.md`, and its file entry is kept with status `removed`.

## Storage

Git is the default store. Each stored file stays within 50 MiB, and an extract that would exceed it is split, for example by indicator or country. Bulk archives, such as the complete World Bank WDI or WID.world downloads, are never acquired. On 18 October 2026 those archives measured 283,089,754 and 886,945,845 bytes. Git LFS is not used.

An acquisition stores the provider's response as it was received, in the raw folder. A replay step, `code/02e_extract.py`, reads the stored response with its reader and writes the relevant observations to `data/02_extracts/<source_id>.csv`, and the run record links the extract to the response by path and SHA-256. When the response may not be published and is held only locally, the extraction step is a restricted target and the committed extract is retained.

`make storage-report` sums the sizes in the file entries and reports the size of the repository's packed history. If the data folders exceed 500 MiB or the packed repository exceeds 1 GiB, the integrator opens an issue that proposes how to store the data, and the maintainer decides. A later change of storage must not change the computation, which always reads the declared local paths.

## Licensing

1. Material whose terms allow publishing, data files and texts alike, is published in the repository as it was obtained, under its own terms.
2. Material whose terms do not allow publishing is handled locally and never committed or released. The repository records it as a data source or a package record with its link. Data may be extracted from it only below the threshold of originality, such as individual values and facts, never a copied table layout, text or figure, and never a substantial part of a database. An output that would cross either limit stays in the gitignored `outputs/local/` folder.
3. The project's own data collection, assembled from such extracts and from values the project derives, is published under CC BY 4.0. It covers `data/02_extracts/`, `data/03_analysis_ready/`, `outputs/observations/` and the tables in `outputs/tables/`. Data fetched from elsewhere are published as they are, under their own terms, and are never relicensed.

The licence and terms of each data source are in its record, and whether each file may be published is in its file entry. Credentials and registration-protected files are never committed. A file obtained by hand is listed in the owning thread's file in `data/local_data_required/` with its expected path, required version, acquisition page, acceptance steps and checksum, and its path is ignored in the `.gitignore` of its raw folder.

## Acquisition, replay and Make

`make acquire` is the only target that contacts live sources. It downloads, verifies and records, and its new files and records reach the repository through a pull request. `make all` replays every computation offline from stored files. The download helper refuses the network when `OFFLINE=1`, which `make all` sets.

Each thread declares its steps as Make targets in `make/<thread-id>.mk`, which the main `Makefile` includes. Every output is a target whose prerequisites are its script, its specification, the catalogue or its record, and its input files. Make builds every prerequisite a target needs, whichever list the target is in, so two rules keep acquisition and missing restricted steps out of a replay. First, every acquire rule sits in a block that is read only when `MODE=acquire`, and `make all` sets `MODE=replay`. Second, a target that needs a restricted input is listed in `RESTRICTED_TARGETS`, and its real rule is defined only when that input is present locally. Otherwise the target gets a stand-in rule with no prerequisites, which retains the committed output. A downstream target therefore always finds a rule that needs neither the network nor the missing input. `make check-contracts` runs `make -n all` without the restricted inputs and fails if any acquire recipe or real restricted recipe would run.

Every table published in `outputs/` is built by a replay step from stored files and records, never by a download script. A fresh clone does not keep file timestamps, so a clean replay rebuilds every replay target unconditionally, and data integrity is checked by hashes in `make verify-data`. `make clean-env` makes a fresh clone in a temporary folder, installs the environment from `pixi.lock`, runs `make verify-data` and runs `make all`.

## Run records and result states

Every `make all` and every acquisition writes a run record, `outputs/runs/<run_id>.json`, with the fields shown in `templates/run_record.json`: the start and end time, the commit and whether the tree was clean, the SHA-256 of `pixi.lock`, the mode, the specifications with ID, version and SHA-256, and one entry per step with its target, state, inputs and outputs. The record of the run that produced committed outputs is committed with them and never edited. Times and other run metadata appear only in run records, so the result tables are deterministic.

| State | Meaning |
|---|---|
| `computed` | The output was computed in this run from inputs whose files were verified against their checksums. |
| `retained` | A required input was not held locally, so the earlier committed output was kept. Only the input checksums recorded with it were compared with the file entries. |
| `not_produced` | The output could not be produced and no earlier output exists, with the reason. |

A retained output keeps its original producer run, code commit and specification ID, version and hash. It is never relabelled as computed by the current code or specification. Retention is allowed only when the requested specification and input hashes match the recorded producer and no relevant computation change invalidates the output; otherwise the new request is not_produced and the earlier result remains available under its original version. A matching input checksum alone does not establish compatibility.

Each input check is recorded as `file_verified` or `record_matched`. Skipped steps and missing inputs are listed. `RESTRICTED INPUT` is the `input_access` value of a result that depends on an input under use restrictions, and it says nothing about whether the result was recomputed. Result tables carry the other result properties of the research method in separate columns, and the replay state is joined from the run record wherever results are reported.

## Validation

`make check-contracts` runs in one of two modes.

- **metadata** runs in CI. It validates the schemas of specifications, the catalogue, records, lineage, registers and run records, the uniqueness of identifiers, every reference between them, file ownership on pull requests, that no raw file or immutable file entry field differs from the base branch except a removal recorded in `docs/removals.md`, that locked specifications match the lock, the `make -n all` check and the goal traceability rules. It reads no data file.
- **full** runs locally and in `make verify-data`. It also hashes every stored file and compares it with its file entry. A missing published file is an error. A restricted file that is not held locally is listed, not failed.

Acquisition statuses are `acquired`, `user_supplied`, `awaiting_user`, `access_failed`, `not_downloaded_restricted` and `removed`. Only `acquired` and `user_supplied` require a file and a checksum. `make check-data` runs the integrity tests on the data present.

## Testing plan

Tests are organised by function, not by thread. Ordinary tests never call an external service.

| Level | Path | Owner | Depends on | Accepted when |
|---|---|---|---|---|
| Computation unit tests | `tests/compute/` | Scaffold | `code/lib/transform.py`, `code/lib/compute.py` | Hand-checkable examples pass for direction coding, standardisation, missing components and the component report, index weights, the pairs entering a correlation and the sample size, and each expected value is calculated by hand and written into the test |
| Reader tests | `tests/readers/<reader>/` with fixtures in `tests/fixtures/readers/<reader>/` | The thread that owns the reader | The reader module | Each reader turns its small stored example file into the expected observations, including units, periods and unit keys, without network access |
| Data integrity | `tests/integrity/`, run by `make check-data` | Scaffold | Schemas, records, registries, catalogue | Schemas, key uniqueness, units, allowed values, references, checksums and join row counts pass on the data present |
| End to end | `tests/e2e/` with `tests/fixtures/synthetic/` | Scaffold, then each replay-step owner | Initially the reader, preparation, computation and result-table core; later replay scripts as implemented | A synthetic dataset of countries and states runs all three current variants without duplicate row keys or overwritten observation and figure paths; each available result matches the independent expected values, and a missing-input case remains visible as not_produced with its reason |
| Public data replay | `tests/replay/`, run by the CI replay job | Scaffold | Public data and replay steps on `main` | Once public data and replay steps exist, a CI replay from public inputs reproduces the committed outputs within the tolerances below |
| Release check | Run by `make clean-env` | Integrator | Everything on `main` | Before `deliverables-v1` and `results-v1`, a fresh clone in the locked environment verifies all data and replays, and a separate replay on a machine holding the restricted inputs records which restricted steps were computed |
| Eligibility | `tests/eligibility/` | Reproduction lock | `code/03a_eligibility.py` | The three conditions, the order of exclusion and the tie rule give the expected eligibility table on a constructed example |
| Report and site | `tests/report/` | Report | `code/07_build_report.py` | Every catalogue result has a page showing each specified variant and its state; computed and retained variants show available outputs with permitted downloads equal to the plotted observations, while not_produced variants show their barrier without requiring nonexistent outputs; a restricted-data fixture offers no forbidden download |

The tests cover these edge cases: a constant variable, which must give a defined error or missing value rather than a number, a missing component, a duplicated observation key, a conflicting unit, an unknown unit, and a shuffled row order, which must not change any result. Pandera checks structure and value constraints, and correctness is tested against independently derived expected values. In replay tests, identifiers including `variant_id`, samples and missing units must match exactly, z-scores, index values and correlations within an absolute tolerance of 1e-10, and p-values within a relative tolerance of 1e-8. These tolerances allow for floating-point differences between macOS and Linux on samples of at most 50 units and lie far below the two decimals of the published correlations. For computed or retained results, figures are checked against their plotted data when publication is permitted; not_produced results instead require a recorded reason and no fabricated figure or observations. A difference from a published value is never a test failure. The plan sets no coverage percentage, browser automation, load tests or tests of every helper.

## Continuous integration

`ci.yml` runs on every pull request and on every push to `main`. It installs the locked environment, runs ruff, runs the computation, reader and end-to-end tests, checks the exported environment files, and runs `make check-contracts` in `metadata` mode. On a push the ownership check is skipped. Once public data and replay steps exist, a replay job in the same workflow runs `make verify-data`, `make check-data`, `make all` on the public inputs and the replay tests. In milestone 3 the report thread adds `pages.yml`, which runs only when a tag matching `results-*` is pushed and publishes the committed `site/` folder. Third-party actions are pinned to commit hashes, and workflows get the minimum permissions they need.

## Result outputs

`code/04_reproduce.py` writes, for each specification, one result table `outputs/tables/<spec_id>_results.csv` and one index component report `outputs/tables/<spec_id>_components.csv`, both including `variant_id`. Each catalogue comparison and specified variant has a result row, and the run record states whether it was computed, retained or not_produced with its reason. A `not_produced` row keeps its identifiers and metadata, leaves unavailable statistics empty, and never invents observations or a figure. For each available variant, its observation table is `outputs/observations/<spec_id>/<variant_id>/<result_id>.csv` and its figure is `outputs/figures/<spec_id>/<variant_id>/<result_id>.png`, drawn from that table and nothing else. These paths must be unique across variants; restricted outputs follow the licensing rule. `code/06_build_headline.py` builds `outputs/tables/headline_results.csv` and the short discrepancy summary `outputs/diagnostics/discrepancy_summary.md` from the result tables, the catalogue and the discrepancy logs. Both belong to milestone 2.

## Report and site

`code/07_build_report.py` writes the report as Markdown from the prose in `report/` and from the outputs, run records and registers, so no number is typed in by hand. It writes `docs/replication_report.md` and the site into `site/`: an index page with the headline table, and one page per catalogue result showing the historical and all specified current variants with their states. For a computed or retained variant the page shows its available figure and observation table, sample, missing units, sources, comparability and deviations; a retained output is identified as retained. A not_produced variant shows its reason and available metadata instead of a required figure or observation table. A download is offered only where the licensing rules allow publishing the observations and contains exactly those plotted; otherwise the restriction is stated. GitHub Pages publishes `site/` with its standard Markdown build. The first version has no interactive features, which may come later without a new framework. The site links to the `deliverables-v1` release and to the repository and states the release tag, the lock commit, the commit it was built from and the date.

## Reference tables

**Result catalogue.** See above and `templates/results_catalogue.csv`.

**Data source record.** `source_id`, `provider`, `series_code`, `title`, `definition`, `unit`, `geography`, `licence`, `terms_url`, `redistributable` and `notes`. See `templates/data_source.yaml`.

**Acquisition record.** `acquisition_id`, `source_ids`, `method`, `request`, `requested_utc`, `response_status`, `dataset_version`, `status`, `corrects`, `retrieval_log`, `notes`, and `files`, each with `path`, `size_bytes`, `sha256`, `storage` as git or local, `redistributable` and `source_ids`. See `templates/acquisition.yaml`.

**Source lineage.** The canonical header is in `docs/source_lineage.csv`, with `dataset` as international or us_states, `role` as inequality, mean_income, index_component, extra_measure or eligibility, and `historical_source` and `current_source` as data source IDs. See `docs/source_lineage.csv`.

**Result tables.** `result_id`, `variant_id`, `spec_id`, `spec_version`, `spec_sha256`, `data_basis` as historical or current, `data_provenance` as released, reconstructed, combined or current, `access_label`, `sample` as historical, fixed or refreshed, `series_set` as original, successors or successors_and_substitutes, `comparability`, `method_deviations`, `r`, `p`, `n`, `missing_units`, `components_used`, `components_missing` and `input_access`, `state` and `reason`. Row state describes whether the numeric result was produced; the execution state still comes from the run record, so a retained table is not presented as newly computed. Display labels such as the access label or "Updated reproduction, refreshed sample" are derived from these columns. See `templates/result_table.csv`.

**Component report.** One row per variant, unit and index component, with `result_id`, `variant_id`, `spec_id`, `unit_id`, `component`, `available` and `used`. See `templates/component_report.csv`.

**Headline table.** One row per catalogue result: `result_id`, `dataset`, `indicator_or_index`, `predictor`, `reported_value`, `historical_r`, `historical_n`, `updated_r`, `updated_n`, `comparability`, `components_changed` and `deviation_summary`. The historical columns select `variant_id=historical` and the primary current columns select `variant_id=updated`; the other current variants remain separately available. See `templates/headline_results.csv`.

**Eligibility tables.** `outputs/tables/historical_country_eligibility.csv` and `outputs/tables/refreshed_country_eligibility.csv`, with the canonical header in `templates/eligibility_table.csv` and `exclusion_reason` as not_ranked, not_top_50, population_below_3m, no_comparable_inequality_data or empty. See `templates/eligibility_table.csv`. Comparison tables of parallel data follow `templates/source_comparison.csv`.

**Package records.** Each package subfolder has a `records.csv` for texts, and each package a `search_log.csv` and a `screening_log.csv`. See `templates/package_records.csv`, `templates/search_log.csv` and `templates/screening_log.csv`.

**Controversy register.** `docs/controversy_register.csv` with `controversy_id`, `claim_or_result_affected`, `target_level` as original, current, both or general_hypothesis, `mapping_rationale`, `source_role` as critic or independent, `source_author`, `source_title`, `publication_year`, `publication_date_type`, `source_type`, `peer_review_status`, `exact_controversy_in_neutral_words`, `testable_statement`, `wilkinson_pickett_response_available`, `response_source_id`, `local_path`, `citation_url` and `notes`. A controversy ID is its category followed by a number, such as `inequality-measure-002`. The categories are `country-selection` for country selection and sample definition, `inequality-measure` for the inequality measure, `index-construction` for composite-index construction, `outliers` for outliers and influential units, `temporal-persistence` for persistence in later data and in national time series, `mechanism` for the psychosocial account and alternative explanations, and `data-comparability` for data availability and comparability.

**Controversy data map.** `docs/controversy_data_map.csv` with `controversy_id`, `source_id`, `testable_statement`, `target_level`, `required_variables`, `required_geographies`, `required_years`, `candidate_sources`, `chosen_source`, `access_route`, `licence_status`, `redistributable`, `acquisition_status` as acquired, partially_acquired or barrier_documented, `local_paths`, `coverage_obtained`, `possible_use` and `barrier`, with one row per controversy and dataset.

**Claims register.** `docs/claims_register.csv` with `claim_id`, `author`, `source_work`, `source_locator`, `publication_year`, `stable_identifier`, `wording`, `wording_type`, `claim_class`, `verification_status`, `verification_log_ref` and `notes`.

**Report sections.** Scope and terminology. Headline results. Goals and deliverables. Historical reproduction. Updated reproduction, with the refreshed sample and the substitute variant as parallel results. Each reproduction section reports the countries and the U.S. states separately. Supporting sources. Controversies. Author claims, as the register stands at the `results-v1` tag. Limitations, covering the absence of the book and the assumptions that stand in for it, any partial state reconstruction, the small sample, cross-national comparability, temporal misalignment, missing data, measurement changes, series that ended or changed definition, and that the project tests neither the controversies nor causality. Reproducibility.

# Part B. Work organisation

## Threads

Each thread is a separate Claude session that owns a fixed set of paths, works on its own branch and hands over through the research method and Part A. No two threads write the same file.

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
| Report and site | `report` | 6 |

**Ownership.** The paths each thread owns are listed in `docs/ownership/<thread-id>.csv`, one pattern per row, under git's wildmatch rules, so `*` never crosses a `/`. Each thread owns its own ownership file and adds a row for every file whose name it creates, such as a data source or acquisition record, an extract or a run record. The ownership check fails if two threads claim the same path, or if a pull request from a branch `<thread-id>/<description>` changes a path its thread does not own.

**Integrator.** The integrator is a separate Claude session. It creates the milestone tags after the maintainer's approval, makes changes to the files the scaffold thread owns on branches named `scaffold/<description>`, makes a change another thread needs in a reader whose owner has finished, keeps the worklist and runs the release check. Whether the integrator later becomes an automated agent is left for consideration.

## Execution order

| Wave | Thread | Starts when | Milestone |
|---|---|---|---|
| 0 | Scaffold | Planning documents merged | 1 |
| 1A | Original access | Scaffold merged | 1 |
| 1A | Supporting sources, controversy sources and register | Scaffold merged | 2 |
| 1A | Claims register | Scaffold merged. It never gates a tag | None |
| 1B | Source lineage | Original access merged | 1 |
| 1B.1 | Historical reproduction | Source lineage merged | 1 |
| 1C | Inequality data, outcome data | Source lineage merged | 1 |
| 1D | Reproduction lock | Historical reproduction, inequality data and outcome data merged | 1 |
| 1E | Lock gate | Milestone 1 reviewed and tagged | 1 to 2 |
| 2A | Updated reproduction | Lock gate passed | 2 |
| 2B | Controversy test data | Frozen controversy register merged | 2 |
| 3 | Report | `deliverables-v1` tagged | 3 |

A thread reads another thread's output only from `main` after that thread has merged. The inequality data, outcome data and controversy test data threads mainly download and catalogue and can use a cheaper model.

## Milestones and repository

The project lives in https://github.com/open-reanalysis/how-economic-inequality-harms-societies, and the site is published at https://open-reanalysis.github.io/how-economic-inequality-harms-societies/.

| Milestone | Tag | Threads | What the maintainer reviews first |
|---|---|---|---|
| 1. Data and historical reproduction | `milestone-1` | Scaffold, original access, source lineage, historical reproduction, inequality data, outcome data, reproduction lock | The lineage, the result catalogue, the method rationale and historical specifications, the historical results with their access labels, and the lock |
| 2. Updated reproduction and source packages | `deliverables-v1` | Updated reproduction, supporting sources, controversy sources and register, controversy test data | The headline table and the discrepancy summary, the updated results, the two source packages with their logs and READMEs, the frozen controversy register and the controversy test data |
| 3. Site | `results-v1` | Report | The report and the site |

The tags `milestone-1`, `deliverables-v1` and `results-v1` were created on the planning commit `1a26437` at the maintainer's request, before any milestone work. When a milestone is approved, the integrator asks the maintainer whether to move its tag to the approved commit or to tag that commit with a new name.

Each thread works on a branch `<thread-id>/<description>` from `main` and opens a pull request into `main`. The pull request description is the merge package. A thread pull request auto-merges with a merge commit once every required check passes, and it opens only when the thread's start conditions are met. `main` accepts changes only through pull requests with passing checks and blocks force pushes. Tags matching `milestone-*`, `deliverables-*` and `results-*` are protected so that only organisation owners create them. History is never rewritten. Squash, rebase, amend and force push follow the rule in CONTRIBUTING.md.

**Merge package.** The commit hash, the changed files, the thread's completion checklist, the `full` validation output, the tests run by level with their exit status, the run record of any committed outputs, known access failures, licence status, and confirmation that only owned paths changed.

**Milestone review.** When every thread a milestone lists has merged, the integrator sends the maintainer the files to read first, the thread pull requests with their merge packages and the latest check results. Before `deliverables-v1` and `results-v1` it also runs the release check and reports its run records.

**Deliverables release.** After the maintainer approves milestone 2, the integrator publishes a GitHub release from `deliverables-v1`. Its notes are generated from the acceptance tests of goals 1 to 5, the headline table, the discrepancy summary and the package READMEs, and list every lineage row still not verified and every catalogue row not reproduced, with the reason. It needs no data assets, because every stored file is in the repository.

## New artefacts

| Artefact | Path | Owner | Depends on | Done when |
|---|---|---|---|---|
| Library skeleton and computation core | `code/lib/` except reader modules | Scaffold | This plan | Computation unit tests and a synthetic read–prepare–compute–result-table test pass; later replay scripts are integrated when their owning steps are implemented |
| Schemas | `code/lib/schemas.py`, `code/lib/spec.py` | Scaffold | Reference tables | Every interface table, specification, catalogue, record and run record validates against one schema |
| Unit registries | `config/units/` | Scaffold | ISO 3166-1 and Census FIPS lists | Every unit in the released data and the lineage resolves to exactly one entry |
| Templates | `templates/` | Scaffold | Reference tables | Each template validates against its schema |
| Ownership files | `docs/ownership/<thread-id>.csv` | Each thread its own | This plan | The ownership check finds no overlap |
| Result catalogue | `config/results_catalogue.csv` | Historical reproduction | Source lineage, the notes | Every included comparison has a verified locator; a published numeric benchmark is recorded where available, otherwise its absence and any figure-only evidence are explicit |
| Historical specifications and method rationale | `config/specs/historical_*.yaml`, `docs/method_rationale.md` | Historical reproduction | Lineage, catalogue, approved assumptions | The maintainer approves them in the milestone 1 review |
| Updated specifications and lock | `config/specs/updated_*.yaml`, `docs/reproduction_lock.md` | Reproduction lock | Historical specifications, lineage, catalogue, coverage and eligibility tables | The lock lists every updated specification with version and SHA-256, and the contract check passes |
| Readers | `code/lib/readers/<family>.py` with tests and fixtures | The thread that acquires the source family | Data source and acquisition records | The reader tests pass on stored example files |
| Headline table and discrepancy summary | `outputs/tables/headline_results.csv`, `outputs/diagnostics/discrepancy_summary.md`, `code/06_build_headline.py` | Updated reproduction | Historical and updated result tables, catalogue | Every catalogue row appears once, with its deviations summarised |
| Run records | `outputs/runs/` | The thread whose run produced committed outputs | `code/lib/runs.py` | Each committed output version (path and SHA-256) has an identified producer run; later verification or retention records refer back to that producer rather than claiming to produce it |
| Storage report | `make storage-report` | Scaffold | File entries | It reports both sizes against the thresholds |
| Site | `site/`, `code/07_build_report.py`, `.github/workflows/pages.yml` | Report | `deliverables-v1` | The goal 6 acceptance test passes |
| Worklist | `docs/worklist.md` | Integrator, on scaffold branches | This plan | It names the current run's date, order, assumptions and decisions |

## Steps that need the maintainer

Access requirements are verified when a source is acquired and recorded in its acquisition record. When a source needs registration or acceptance of terms, the thread stops at the access page, adds an entry to its own file in `data/local_data_required/` and says what to do. Creating accounts and accepting terms is the maintainer's. The maintainer approves the assumptions in the worklist before the run, decides any point they do not cover before the computation that depends on it, approves the method rationale with the historical specifications in the milestone 1 review, checks a source's licence where a thread could not establish it, decides on a storage proposal if the storage report exceeds its thresholds, decides whether to register research use of *The Spirit Level at 15* with the Equality Trust, and reviews the three milestones and approves their tags.

Code and tests are under MIT, in `LICENSE`. Documents, the report, the site, figures and the project's own data collection are under CC BY 4.0, in `LICENSE-docs`. Data and texts obtained elsewhere keep their own terms. Branch protection does not require an approving review while the maintainer is the only human contributor, and the milestone review is the human review.

## Thread briefs

A thread's brief is its section below, the research method, Part A and INTENT.md. Owned paths are in its ownership file.

### Scaffold

Configures the repository: the rulesets, auto-merge, the pull request template, `ci.yml`, the pixi workspace with its lockfile and exported files, pre-commit, the `Makefile` with `make/scaffold.mk`, the library skeleton and computation core, schemas, unit registries, templates, the contract checks, the storage report, the integrity, computation, end-to-end and replay tests, and the template for the files in `data/local_data_required/`. The root `.gitignore` holds only general rules, such as every `local/` folder, `build/` and temporary folders. The planning pull request before the scaffold thread is exempt from the ownership check, which does not exist yet.

### Original access and sample recovery

Decides the access status separately for the international and the U.S. state data and downloads and preserves the original material without modifying it. Obtains the authors' own works into `sources/supporting/original-authors/`: *The Spirit Level at 15* with its technical appendix, Pickett and Wilkinson's "Income inequality and health: a causal review", DOI 10.1016/j.socscimed.2014.12.031, and the Equality Trust's material on the book. *The Spirit Level*, Allen Lane 2009, ISBN 978-1-84614-039-6, gets a record marked not obtained.

*The Spirit Level at 15*, DOI 10.15124/yao-de9s-7k93, may be used freely for research with acknowledgement but needs permission for re-use in other publications, so it is handled locally and recorded with its link. The copy supplied on 18 October 2026 has SHA-256 `c14eb8832b6aea4f7d02817e535125a7a34f0e630a271238db73175febdb2aea` and 39 pages. The released international data downloaded on 18 October 2026 have SHA-256 `1897f2bbe503d35df3aea5f3d25a1b719660e1f4761f5913464b6a3b35c6c661`. The released U.S. state data could not be downloaded, because the archived page's download button has no link, and the file is listed in `data/local_data_required/original-access.md`.

Writes the Equality Trust reader with its tests, `outputs/tables/original_sample_recovery.csv` with unit membership, outcome availability flags and source references but no outcome values, and its source-verification log, including what the appendix says about the original method.

### Source lineage

Builds `docs/source_lineage.csv` for the inequality measure, average income, the index components, the extra measures and the eligibility series of both datasets, and the data source records of the original series. Reads no outcome values.

### Historical reproduction

Builds the result catalogue from the notes and the released data, including the comparisons with average income. Writes the historical specifications and the method rationale from the approved assumptions, puts to the maintainer any point they do not cover, and logs every verified fact. Writes the readers and acquisition script for reconstruction material in `data/00_original_reconstruction/`, including the April 2004 WDI vintage if it can be obtained and the historical U.S. state series. Runs the historical reproduction for both datasets, checks the eligibility rule against the released 23 countries, publishes the parallel data comparison, and logs every difference from a published value in `outputs/diagnostics/historical_reproduction_discrepancies.md`. A partial U.S. state rebuild is completed as far as the inputs allow and documented as the research method requires.

### Current inequality data and current outcome data

Download the current release of each series the lineage names, create their data source and acquisition records, and write their readers with tests. The inequality thread takes the inequality series and the U.S. state average income series, which come from the Census family. The outcome thread takes the outcome series and every World Bank series, including average income for the countries and the income and population series for eligibility, into `data/01_raw_current/outcomes/` and `data/01_raw_current/eligibility/`. A rolling or API source has its request and response pinned. For PISA the outcome thread records participation and sampling-standard flags per country and cycle. The outcome thread publishes `outputs/tables/outcome_source_coverage.csv` with coverage and years but no outcome values. Neither thread relates inequality or income to outcomes.

### Reproduction lock

Writes the updated specifications and the lock once historical reproduction, inequality data and outcome data have merged, reading no current outcome values. Builds the refreshed sample with `code/03a_eligibility.py` into `outputs/tables/refreshed_country_eligibility.csv` from the income, population and inequality files only, with the eligibility tests.

### Updated reproduction

Runs the updated specifications for both datasets, writes the updated result tables, component reports, observation tables and figures, the parallel data comparison for current data and `outputs/diagnostics/updated_reproduction_discrepancies.md`. Then builds the headline table and the discrepancy summary for milestone 2.

### Supporting sources

Builds the supporting package in `sources/supporting/academic/`, `non-academic/` and `responses/` with its `manifest.csv`, `README.md`, `search_log.csv` and `screening_log.csv`, under the search protocol in the research method.

### Controversy sources and register

Builds the controversy package in `sources/controversies/academic/`, `books/`, `reports/` and `responses/` under the same protocol, and the register `docs/controversy_register.csv`. The seed list includes Greener in the International Journal of Comparative Sociology, DOI 10.1177/00207152241245620, Judge 1995, Gravelle 1998, the Equality Trust author response, Fischer in the Boston Review, Saunders's "Beware False Prophets" for Policy Exchange, Snowdon's *The Spirit Level Delusion*, Sanandaji, Malm and Sanandaji's "The Spirit Illusion" for the Taxpayers' Alliance, Sanandaji and others in the Wall Street Journal in 2010, Goldthorpe's "Analysing Social Inequality" in the European Sociological Review 2010, DOI 10.1093/esr/jcp046, Rowlingson's 2011 review for the Joseph Rowntree Foundation, Nettle's 2017 essay on the psychosocial account, and the TUC summary of criticisms and replies. The controversy responses folder holds the authors' 2010 responses to Snowdon, the Taxpayers' Alliance and Policy Exchange, Hugh Noble's "The Spirit Level Revisited" and the authors' response to the Rowntree review. The thread records whether each date is the online-first or the issue date. The register is frozen by a commit that records the search cut-off date and the search log, and a criticism found later goes in a dated amendment.

### Controversy test data

Starts once the frozen register has merged. Defines each map row's variables, coverage and years, then acquires the smallest justified package. A dataset several controversies need is stored once in `data/04_controversy_test_data/shared/`, and every other package in `data/04_controversy_test_data/by_controversy/<controversy_id>/` with a README naming its controversies. Coverage is taken from non-missing flags only, and no analysis is run.

### Author claims register

Builds `docs/claims_register.csv` from the authors' published material: the notes, the frequently asked questions, the 2010 responses, *The Spirit Level at 15* and its appendix, the 2015 causal review, Wilkinson's 2011 TED talk and the authors' replies to criticism. A book page that such material cites is recorded as cited, not as checked. No quotation, page or identifier is entered without checking it. The register never attributes a causal inference to a correlation the authors reported without one, nor omits a causal claim they made. Claim classes are descriptive_correlation, proposed_mechanism, causal_claim and policy_prediction, and `claim_class` stays empty while an entry is to_be_verified. It is frozen by a commit that records its cut-off date.

### Report and site

Builds the report and the site from the outputs of milestone 2, adds `pages.yml`, writes the report tests, runs the release check before `results-v1` and checks the completion criteria, reporting each of the six goals first.

## Milestone 1 integration run

The maintainer requested implementation of milestone 1 in one new pull request after the planning merge. For this run the integrator may implement the milestone-1 threads on scaffold/milestone-one, using the same source, method and ownership boundaries but integrating dependent outputs on that branch in the order above. This is an explicit exception to separate thread pull requests and reading dependent outputs only after their main-branch merge. It does not waive tests, provenance, source terms, prospective decisions or the gate against current-data associations.

Begin with one historical international comparison through a stored source, reader, specification, calculation, result table and run record. Expand only after that path passes. The scaffold acceptance test uses synthetic inputs and does not depend on the site, headline builder or future eligibility script. Source-specific access and comparability are assessed individually; failed acquisitions and unresolved method choices remain explicit. Milestone 1 is ready for review only after its catalogue, lineage, historical results or barriers, current acquisition/coverage records and prospective lock can all be inspected. A pull request or passing scaffold tests alone do not complete the milestone.

The milestone-1 implementation currently preserves the original workbook locally because redistribution permission has not been established. Historical result tables can be produced from that file and conservatively retained by a public clone only with a matching code/specification/input producer record. Current sources and the prospective lock are explicitly unfinished until the remaining verification and method decisions have been resolved. See docs/milestone-1-status.md; this status does not redefine milestone acceptance.
