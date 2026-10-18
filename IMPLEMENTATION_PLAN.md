# Implementation plan

This plan turns [INTENT.md](INTENT.md) into work that separate Claude sessions can run in parallel. Each session is called a thread here. A thread owns a fixed set of files, works on its own branch, and hands over through the shared contracts at the end of this document. No two threads write the same file.

## Execution order

Work runs in waves. A thread starts only when every gate it depends on has passed.

| Wave | Threads | Starts when |
|---|---|---|
| 0 | T0 Scaffold | Now |
| 1A | T1a Original access and sample recovery, T2 Sources, T3 Inequality data, T4 Outcome data, T5a Core test data, T6a Design lock | T0 merged |
| 1B | T1b Original reproduction | T1a merged |
| 1B | T6b Sample amendment and lock | T1a merged, and T2 merged with its register frozen and its appendix verification logged |
| 2 | T7 Primary harmonisation | T3, T4 and T6b merged, gate G2 passed |
| 2B | T5b Register-specific test data | T2 merged with its register frozen |
| 3 | T8a Current replication | T7 merged |
| 3 | T7b Controversy harmonisation | T7, T5a and T5b merged |
| 3 | T8b Sensitivity and controversy tests | T8a, T7b and T1b merged |
| 4 | T9 Report and clean offline run | T1b and T8b merged |

The answer to question B never waits for controversy-specific downloads. T7 builds the primary datasets and T8a analyses them while T5b and T7b are still working on named criticisms.

The lock waits for T2's frozen register so that every criticism-driven covariate, sample rule and panel test is declared before harmonisation, rather than added afterwards as an amendment. This makes T2 the critical path of wave 1A.

A thread reads another thread's output only from the main line after that thread has merged. No thread reads from an unmerged branch.

## Gates

**G1. Original data access.** T1a assigns one of four statuses, and the status fixes the label that every question A output carries.

| Status | Definition | Label on outputs |
|---|---|---|
| G1-A verified original release | Files download and hash, contain usable original data, and carry enough documentation to identify variables and country cases. | Direct reproduction from released data |
| G1-B accessible but incomplete | Some files download, but required sheets, metadata, source notes or formulas are missing. | Partial released-data reproduction |
| G1-C archived copy only | A credible archive or third party supplies historical files, but provenance to the original release cannot be fully verified. | Archive-based reconstruction |
| G1-D unavailable | No usable original package is accessible. | Independent reconstruction |

For every retrieval attempt T1a records the HTTP status, redirect chain, response headers where available, UTC timestamp, SHA-256, file size, MIME type and whether the file is machine-readable. A 2017 Equality Trust post says the data could be downloaded. That establishes nothing about today, so the gate is decided only by these records.

**G2. Analysis lock.** T6 commits the analysis lock before any thread computes, views or infers an association between current inequality data and current outcome data. The gate does not cover T1b, because the original data and the authors' correlations are already published and reproducing them reveals nothing new about the current analysis. Downloading sources, reading metadata and checking country coverage before the lock are allowed. The lock consists of `docs/analysis_lock.md`, `docs/inclusion_rules.md` and `docs/dag.md`, and its commit hash goes into `docs/analysis_lock_hash.txt` and the report.

The blinding is procedural only, and the lock says so in a section on prior knowledge. The original correlations are published, and table 1 of the 2024 technical appendix publishes correlations for 22 countries using recent data. Anyone writing the lock may know these results. The lock lists which published results its author had seen.

A git commit is an internal analysis lock, not a preregistration, even in a public repository, because commits and tags can be rewritten. The documents are called preregistration only if the lock commit is archived before T7 starts in an immutable public record such as OSF, Zenodo or Software Heritage. Archiving is your decision. Later changes to the lock are dated amendments with a stated reason, and affected results are reported under both the original and the amended rule.

**G3. Harmonised data validated.** T7's validation passes. Every analysis-ready column traces to a raw source variable, a formula, a direction, a missing-data rule, a reference year and a source ID.

**G4. Completion.** Every criterion in INTENT.md is met and `make clean-env` succeeds.

## Tech stack

The project mixes Python and R. Each language does what it does best, and the boundary between them is files, never in-process calls.

**Python** handles acquisition, provenance, harmonisation, index construction, the cross-sectional statistics and the contract checks. It uses pandas and pyarrow for data, requests and tenacity for downloads, sdmx1 for OECD SDMX queries, wbgapi for World Bank WDI, openpyxl and xlrd for spreadsheets, country_converter for ISO codes, scipy and statsmodels for correlations, OLS, robust regression, Theil–Sen and influence diagnostics, scikit-learn for the exploratory principal-component index, pandera for schemas and pytest for tests.

**R** handles the models where its packages are the reference implementations. These are the panel models with fixest, the small-cluster inference method the lock selects, the DAG with dagitty, and qualitative comparative analysis with the QCA package if a register row requires re-running Greener's QCA. R code is tested with testthat and linted with lintr.

**The language boundary.** Every script is in one language. Scripts exchange data only through Parquet and CSV files under the paths the contracts define, read with arrow in R and pyarrow in Python. Z-scoring and index construction exist once, in Python, and R reads the computed indices instead of reimplementing them. Where both languages can compute the same statistic, a cross-language test computes the primary OLS and Pearson results in both and fails on any difference beyond numerical tolerance.

**Environment.** pixi manages one environment for both languages from conda-forge, with PyPI only for packages conda-forge lacks. Its single lockfile, `pixi.lock`, pins every Python and R package for macOS on Apple silicon and for Linux, so local runs and GitHub Actions resolve to the same builds. This was chosen for result quality. A separate Python lock and R lock, such as uv with renv, can drift apart and cannot pin the shared system libraries, while pixi pins the whole stack in one file. `environment.yml` and `requirements.txt`, which the original project specification requires, are exported from pixi and CI fails if they are out of date. R packages that exist only on GitHub are not used, because they cannot be locked.

**Code quality.** ruff for Python, lintr and styler for R, and pre-commit to run them before every commit.

**Build.** GNU Make remains the entry point, and each target calls `pixi run`. The download helper refuses network access when `OFFLINE=1`, which `make all` sets, so offline replay is enforced in code rather than by convention.

**Report and site.** Quarto renders the report and the results website. The report source is `site/replication_report.qmd`. Quarto renders it both into the site and into `docs/replication_report.md` as GitHub-flavoured Markdown, so the Markdown report is a generated file, never edited by hand. It runs Python and R code chunks in the same document, so every number in the report is computed from the output tables at render time rather than typed in.

**Bibliography tooling.** Crossref for DOIs, PubMed E-utilities for PMIDs, the PMC ID converter for PMCIDs, Unpaywall for legally open full texts and OpenAlex for citation chaining.

## GitHub repository and workflow

The project lives in the public GitHub repository https://github.com/open-reanalysis/how-economic-inequality-harms-societies under the `open-reanalysis` organisation. The site is published at https://open-reanalysis.github.io/how-economic-inequality-harms-societies/. Each thread works on a branch named after it, such as `t1a-original-access`, and opens a pull request into `main` when its stage is done. The pull request description is the merge package, using a template that lists every item the merge protocol requires. Merging still happens only when you say so.

`main` is protected. Pull requests need the contract checks to pass and cannot be force-pushed. The analysis lock commit gets the tag `analysis-lock-v1`, and amendments get `analysis-lock-v1.1` and so on. Tags matching `analysis-lock-*` and `results-*` are protected.

**Raw data are not stored in git.** This applies to every raw folder and to downloaded full texts under `sources/`, whatever their licence. Several sources are far larger than GitHub's file limits, and many cannot be redistributed. Git holds manifests, metadata, code and generated outputs. `make acquire` builds a data snapshot, a set of archives whose checksums are recorded in the manifest. Redistributable assets are published as a GitHub release asset named after the snapshot, such as `data-snapshot-2026-11`. Non-redistributable assets stay on your machine and are listed in `data/LOCAL_DATA_REQUIRED.md`. Offline replay downloads the frozen snapshot and verifies every checksum before running. Fetching a frozen snapshot is not the same as redownloading live data, so this is compatible with the offline rule.

Because raw files do not appear in pull requests, the immutability check works on manifests and checksums instead. A pull request may add manifest rows but may not change the checksum, path or retrieval record of an existing row. CI verifies every redistributable file in the snapshot against its manifest checksum, and the thread verifies non-redistributable files locally and reports the result in its merge package.

**What CI can and cannot replay.** CI replays every step that depends only on redistributable assets. Steps that need non-redistributable data run locally, and their aggregated outputs are committed together with the checksums of the inputs they used. The report marks which results CI reproduced and which were reproduced locally.

## GitHub Actions

`ci.yml` runs on every pull request. It installs the locked environment, runs ruff, lintr, pytest and testthat, checks that the exported environment files match `pixi.lock`, and runs `make check-contracts`. The ownership check reads the thread from the branch name and fails if the pull request changes files outside that thread's owned paths. It also builds the Quarto site as a check and uploads it as a workflow artifact without deploying it.

`replay.yml` runs on every push to `main`. It fetches the current data snapshot, verifies checksums, runs `make all` with `OFFLINE=1` and uploads the outputs as a workflow artifact. It fails if any committed output that CI can reproduce differs from the replayed one.

`acquire.yml` runs only on manual dispatch. It runs `make acquire` for the open sources and drafts a new snapshot release for you to review. It never publishes a snapshot by itself.

`pages.yml` runs only when a tag matching `results-*` is pushed. No test deployment exists. Rendering is verified by `ci.yml` without publishing anything. It replays the analysis, renders the Quarto site and deploys it to GitHub Pages. Unfinished results therefore never appear on the public site.

Third-party actions are pinned to commit hashes, and workflows get the minimum permissions they need.

## Results website

The GitHub Pages site is the public face of the project. It is built entirely from repository outputs and contains the replication report, all figures, every result table as a downloadable CSV, the controversy register with each test result, the analysis lock with its amendments and tag, the data dictionary, the manifests, the source-verification logs and instructions for reproducing everything. It contains no raw data.

Each published version states the release tag, the analysis-lock tag, the data snapshot and the date. The site uses the neutral terminology of INTENT.md throughout, and every controversy page shows the critic's claim, its source, the test, the result and any published response by Wilkinson and Pickett.

If the repository is connected to Zenodo, every release is archived with a DOI. A release made at the analysis-lock tag then serves as the immutable public record that allows the lock to be called a preregistration.

## Threads

### T0 Scaffold

Runs in this session. Configures the GitHub repository with branch protection, the pull request template, the four workflows, the pixi workspace with its lockfile and the exported `environment.yml` and `requirements.txt`, the pre-commit configuration, a minimal Quarto site that `ci.yml` renders but does not deploy, the licence files, the `Makefile` targets described under shared contracts, a `code/lib/` package with shared helpers, the manifest schema, `.gitignore` rules for user-supplied files, `data/LOCAL_DATA_REQUIRED.md` as a template and `LICENSES_AND_ACCESS.md` as a template. The shared helpers cover recorded downloads, manifest rows, path resolution, country-code mapping, logging, and z-scoring and index construction, so every thread computes them the same way. T0's commit is the base of every other branch.

Owns `README.md`, `LICENSE`, `LICENSE-docs`, `CITATION.cff`, `LICENSES_AND_ACCESS.md`, `pixi.toml`, `pixi.lock`, `environment.yml`, `requirements.txt`, `Makefile`, `.gitignore`, `.pre-commit-config.yaml`, `.github/`, `_quarto.yml`, `code/lib/` except `code/lib/harmonise.py`, `code/check_contracts.py`, `data/metadata/schemas/`, `data/LOCAL_DATA_REQUIRED.md` and `tests/t0/`.

The README already on `main` was written before the plan settled. T0 keeps its framing and rewrites the parts that describe layout, labels, commands and logs so they match this plan.

After T0 merges, a thread that needs a change in a T0 file asks for it in its merge package. The integrator makes the change as a separate commit on the main line, and the thread rebases onto it.

### T1a Original access and sample recovery

Decides gate G1. Downloads and preserves whatever original material is available without modifying it.

Publishes `outputs/tables/original_sample_recovery.csv` as early as possible. The file contains country membership, outcome availability flags, source references and documented inclusion notes. It contains no outcome values, correlations or figures, because T6b reads it.

If the package contains U.S. state material, T1a records its existence, file names and provenance in the manifest and does nothing else with it.

Records every verified fact about the original study, with the passage, table or file it came from, in its part of the source-verification log.

Owns `data/00_original_released/`, `code/01_ingest_original.py`, `data/metadata/manifests/t1_original.csv`, `outputs/tables/original_sample_recovery.csv`, `outputs/diagnostics/g1_access_record.md` and `docs/source_verification/t1_original.md`.

### T1b Original reproduction

Answers question A under the label G1 assigned. Verifies from the files and the original book's notes the inequality measure and year, the direction of each index component and the handling of missing components. None of these are assumed. Undocumented choices are implemented as labelled alternatives.

Outputs are split into two kinds. Exact reproduction outputs use only the statistic, country cases, transformations and graphic conventions documented in the original study, including the authors' documented composite-index procedure as it actually handled countries with incomplete components. Supplementary diagnostics are labelled as modern additions and never presented as original-study outputs. These are confidence intervals, Spearman correlations, robust methods, influence diagnostics and alternative specifications.

Compares each computed value with the reported one and logs every difference. Records each verified fact about the original method, with the passage, table or file it came from, in its own part of the source-verification log.

T1b is the only thread that prepares the original release dataset. `code/01b_prepare_original.py` writes it to `data/03_analysis_ready/original/` and `code/04_reproduce_original.py` analyses it.

Under status G1-C or G1-D, T1b rebuilds the original analysis from published tables, the book's notes and independently sourced historical data. `code/01c_download_reconstruction_sources.py` stores that material as downloaded in `data/00_original_reconstruction/`, separate from T1a's released files.

Writes a data dictionary and a source-year matrix for the original release dataset and records every raw and derived file it creates in its own manifest.

Owns `code/01b_prepare_original.py`, `code/01c_download_reconstruction_sources.py`, `data/00_original_reconstruction/`, `data/03_analysis_ready/original/`, `data/metadata/manifests/t1b_original_derived.csv`, `docs/data_dictionary_original.md`, `outputs/tables/original_variable_year_matrix.csv`, `code/04_reproduce_original.py`, `outputs/tables/original_*` except the sample recovery file, `outputs/figures/original_*`, `outputs/diagnostics/original_reproduction_discrepancies.md` and `docs/source_verification/t1b_original_method.md`.

### T2 Sources and controversy register

Builds the literature package in the five `sources/` folders, keeping primary author material, supporting academic work, academic criticism, non-academic criticism and author replies apart. Expands the seed list by backward and forward citation searching.

Writes the controversy register. A row enters it only with the critic's name, exact title, year and a stable DOI, PMID, PMCID or URL, checked against PubMed, the DOI record or the publisher page. Rows are classified by target, which is data selection, measurement, index construction, robustness, mechanism, causal interpretation or policy inference. Each row names the data T5b must supply and the test T8b must run, or marks `empirical_test_possible` as no with the reason. Wilkinson and Pickett's published responses are linked to the criticisms they answer.

The seed list includes Greener 2025, Judge 1995, Gravelle 1998, the Equality Trust author response, Fischer in the Boston Review, Saunders, Snowdon, the TUC summary of criticisms and replies, and the 2024 technical appendix.

Full texts are never committed to git. They are stored locally under `sources/` and enter the public data snapshot only where the licence allows redistribution. The repository holds the bibliographic record, retrieval instructions and a gitignored local path for each.

Extracts from the 2024 technical appendix the passages, table definitions, country list, reference-year statements, index construction and direction coding, and records them in its part of the source-verification log as update-method documentation. This includes the appendix's description of the original timing, its use of the term 80:20 and its use of PISA 2018 instead of PISA 2022. T6a uses these only after they are logged.

The appendix verification and the register freeze are both prerequisites for the lock, so T2 does them before expanding the supporting literature.

Owns `sources/`, `code/00_download_sources.py`, `docs/controversy_register.md`, `data/metadata/manifests/t2_sources.csv` and `docs/source_verification/t2_sources.md`.

Runs backward and forward citation searching over the criticism literature and the author replies before the freeze. Expanding the supporting literature can continue afterwards.

Done when the register is frozen by a commit that records the search cut-off date and the search log. Later threads read only a frozen version. A named criticism found after the freeze is added in a dated register amendment and a matching dated lock amendment. Its test is reported separately as a post-lock analysis, and the report states that it was not declared before the data were examined.

### T3 Current inequality data

Downloads raw copies, metadata and codebooks from the OECD Income Distribution Database, the World Bank Poverty and Inequality Platform, UNU-WIDER WIID and WID.world. Records for each measure the income concept, tax and transfer treatment, equivalisation, unit, price basis, survey year, coverage and known series breaks. The OECD database is revised on a rolling basis and served through an SDMX API, so the endpoint, query parameters, response hash and any version identifier are pinned.

Builds the inequality measure crosswalk. Does not merge inequality with outcomes.

Owns `data/01_raw_current/inequality/`, `code/02a_download_inequality.py`, `data/metadata/manifests/t3_inequality.csv` and `outputs/tables/inequality_measure_crosswalk.csv`.

### T4 Current outcome data

Downloads the ten outcome series with metadata and methodology notes. These cover trust from WVS, EVS and ESS, life expectancy, infant mortality and adolescent births from WDI, WHO and OECD, adult obesity from WHO and OECD, mental illness from GBD and OECD, educational performance from PISA, homicide from UNODC, imprisonment from World Prison Brief and SPACE, and intergenerational mobility from OECD and the World Bank GDIM.

For PISA it records participation status and sampling-standard flags per country and cycle. OECD flagged several countries in PISA 2022 for not meeting sampling standards, and the 2024 update used PISA 2018 for that reason.

Rates comparability per outcome and records the actual reference year for every country-value pair. Downloads the preferred source and the plausible fallbacks for each outcome, so that the hierarchy in the lock can be applied without a second acquisition. Publishes `outputs/tables/outcome_source_coverage.csv` with source, coverage, years and comparability notes but no outcome values, which T6a may read. Never inspects any outcome against inequality.

Owns `data/01_raw_current/outcomes/`, `code/02b_download_outcomes.py`, `data/metadata/manifests/t4_outcomes.csv` and `outputs/tables/outcome_source_coverage.csv`.

### T5a Core controversy-test data

Downloads the packages that many criticisms share, chosen before the register is frozen. These are country universe and population, OECD membership history, World Bank income classification and GNI, democracy indicators from V-Dem or Freedom House, the OECD Social Expenditure Database, GDP per capita, poverty, unemployment, the Worldwide Governance Indicators, the Quality of Government dataset and health expenditure. Panel versions are pinned the same way as T3.

Owns `data/04_controversy_test_data/core/`, `code/02c_download_core_test_data.py` and `data/metadata/manifests/t5a_core.csv`.

### T5b Register-specific test data

Starts after T2 freezes the register. Downloads only data that a named register row requires, such as alternative outcome components proposed by a critic, and records the controversy ID before each download. Each package gets a README naming the controversy it tests.

Owns `data/04_controversy_test_data/by_controversy/`, `code/02d_download_register_test_data.py` and `data/metadata/manifests/t5b_register.csv`.

### T6a Design lock

Writes the analysis plan without reading any outcome values. Fixes the primary inequality measure, the year alignment rule and lag windows, the index formulas and the robustness methods.

Fixes the index direction per measure, not per concept. A measure where a higher value means more of a problem keeps its sign, and every other measure is reversed. For mobility this matters, because an intergenerational elasticity and a mobility index point in opposite directions.

Defines the expanded sample rule with population threshold, income threshold and its source, democracy criterion and the treatment of contested countries including Germany, Israel, Singapore, South Korea and Czechia. Fixes the multiverse dimensions and the reproducibility seed. Every alternative country rule, every multiverse dimension and the panel protocol cites either a register row or a sensitivity rationale stated in the lock, in line with question C of INTENT.md.

Fixes the source hierarchy for every indicator. Each entry names the preferred source, permitted fallbacks, the minimum comparability conditions and the circumstances that justify a fallback. T6a may read T4's coverage table and T3's crosswalk but no outcome values.

Admits a macro-level covariate only where a named criticism, a cited alternative explanation or a stated sensitivity rationale identifies it, and records which one.

Names every domain index and its component membership. If a component cannot be harmonised, the domain is reported with fewer components and the change appears in the component-availability table.

Fixes the panel protocol. This covers the panel unit, a minimum number of countries and within-country observations per outcome below which no model is fitted, country and year fixed effects, whether country trends enter, the lag structure, serial-correlation handling, the standard-error method for a small number of countries and the missing-data treatment.

Draws the DAG used for covariate selection, separating possible confounders from possible mediators. The DAG is written in dagitty syntax, and an R script derives the adjustment sets from it so the covariate choice is computed rather than asserted.

Owns `docs/analysis_lock.md`, `docs/inclusion_rules.md`, `docs/dag.md`, `docs/dag.dagitty`, `code/00b_dag_adjustment_sets.R` and `tests/t6/`.

### T6b Sample amendment

Starts from the main line after T1a and T2 have merged. Reads `original_sample_recovery.csv` and nothing else from T1. Inserts the recovered historical country list and its source reference into `docs/inclusion_rules.md`. Adds the covariates, sample rules and panel tests that named register rows require. Writes the prior-knowledge section. Then commits the lock and writes `docs/analysis_lock_hash.txt`, which passes gate G2. T6b is a second stage of the same thread, not a separate session. If T6a has already merged, the thread rebases onto the current main line before starting T6b and merges again afterwards.

### T7 Primary harmonisation

Applies the locked rules to T3 and T4 raw data. Produces `country_year_analysis_panel.parquet`, `cross_section_primary.csv` and the three current datasets, which are the current primary, the current alternative inequality and the current high-comparability core. The original release dataset belongs to T1b. Writes the data dictionary, the variable-year matrix, the missingness report and the country sample flow. Uses no T5 data.

Applies the source hierarchy before any join and writes `outputs/tables/source_selection_log.csv`, which records for every indicator the source used, its tier and the lock condition that triggered any fallback. An indicator whose required source is missing and has no permitted fallback is omitted and labelled as not tested.

Records every derived file in its own manifest.

Owns `data/02_harmonised/primary/`, `data/03_analysis_ready/primary/`, `data/metadata/manifests/t7_primary_derived.csv`, `code/03_harmonise.py`, `code/lib/harmonise.py`, `docs/data_dictionary.md`, `outputs/tables/variable_year_matrix.csv`, `outputs/tables/country_sample_flow.csv`, `outputs/tables/source_selection_log.csv` and `outputs/diagnostics/missingness_report.csv`.

Passes gate G3.

### T7b Controversy harmonisation

Uses the functions in `code/lib/harmonise.py` without modifying them to turn T5a and T5b material into one analysis file per controversy under `data/03_analysis_ready/controversies/<controversy_id>/`, each with a manifest entry, a data dictionary entry and a source-year matrix. Never modifies T7's primary outputs.

Owns `data/02_harmonised/controversies/`, `data/03_analysis_ready/controversies/`, `data/metadata/manifests/t7b_controversy_derived.csv`, `code/03b_harmonise_controversy_data.py` and `docs/data_dictionary_controversies.md`.

### T8a Current replication

Answers question B on the three current datasets from T7. Writes only to `outputs/`.

For each dataset and outcome it computes Pearson and Spearman correlations, the OLS slope with 95 percent interval, robust regression, Theil–Sen, the leave-one-country-out range, Cook's distance, leverage and DFBETAs.

The equal-weighted, direction-aligned z-score index is the primary index. The domain indices defined in the lock are secondary.

Every result row carries its dataset version, country sample, outcome-year range, inequality-year range, source IDs, component availability and the analysis-lock commit hash.

Also owns the cross-language test, which computes the primary OLS and Pearson results in both Python and R and fails on any difference beyond numerical tolerance.

Owns `code/05_current_replication.py`, `tests/t8a/`, `outputs/tables/current_replication_results.csv` and `outputs/diagnostics/influence_diagnostics.csv`.

### T8b Sensitivity and controversy tests

Answers question C for both the original and the current result. A second stage of the same thread as T8a, which rebases onto the main line once T7b and T1b have merged.

A register row whose `claim_or_result_affected` names the original result is tested on T1b's original release dataset in `data/03_analysis_ready/original/`. This covers, for example, criticisms of the original country selection or the original index. A row that names the current result is tested on T7 and T7b data, and a row that names both is tested on both. T8b only reads T1b's data. T1b's own alternative specifications remain labelled diagnostics and are not counted as controversy tests. Writes only to `outputs/`, and every result row carries the same provenance fields as in T8a.

Runs the multiverse over the locked country rules and inequality measures. A principal-component index is an exploratory sensitivity analysis only. It reports loadings, explained variance, sign choice, country sample and missing-data treatment, and it is never described as a reproduction or used in place of the primary index.

Panel analyses run in a separate module. Before fitting any model, it reports for each outcome the number of countries, years, country-year observations and within-country variation. No model is fitted below the minimum set in the lock. Results are described as within-country associations, not causal estimates.

Each controversy in the frozen register gets one result, labelled with one of five outcomes. Consistent, partly consistent or inconsistent with the critic's stated concern. Indeterminate when coverage, comparability or precision is insufficient to assess it. Not testable in this design when the register marks `empirical_test_possible` as no, as with a mechanism or causal claim that country-level correlations cannot address. Rows of the last kind get no test table. They are listed in a separate table with the reason, and the report discusses them under the matching heading of the terminology in INTENT.md.

If a register row requires re-running Greener's qualitative comparative analysis, it runs in R with the QCA package.

Owns `code/06_robustness_and_controversy_tests.py`, `code/06b_panel_models.R`, `code/06c_qca.R`, `tests/t8b/`, `outputs/tables/sensitivity_results.csv`, `outputs/tables/controversy_test_results.csv` and `outputs/tables/controversies_not_testable.csv`.

### T9 Report and clean offline run

Generates all figures and tables from code and builds the Quarto site, including `outputs/tables/all_model_results.csv` as the combination of T1b, T8a and T8b results, writes `site/replication_report.qmd` with the report sections listed under shared contracts and renders it to `docs/replication_report.md`, runs `make clean-env`, and checks the completion criteria, listing anything unmet. When you approve, T9 tags the release as `results-v1`, which publishes the site.

Owns `code/07_make_tables_figures.py`, `site/` including `site/replication_report.qmd`, the generated `docs/replication_report.md`, `tests/t9/`, `outputs/tables/all_model_results.csv`, `outputs/figures/` except files starting with `original_`, and `outputs/logs/`.

## How the threads run as sessions

T0 runs here. Every other thread runs as its own Claude session in its own git worktree, branched from the current main line when its wave opens. A thread's brief is its section of this plan plus INTENT.md. A thread finishes by pushing its branch and opening a pull request whose description is the merge package described below.

T2, T3, T4, T5a and T5b mainly download and catalogue and can use a cheaper model. T1a, T1b, T6, T7, T7b and T8 in both stages involve method judgement and use the default model.

## Merge protocol

Before a branch is merged, its thread provides in the pull request description the commit hash, the list of changed files, its completion checklist, the manifest validation output, the tests run with exit status, known access failures, licence and redistribution status, and confirmation that it wrote nothing outside its owned files.

`make check-contracts` runs in CI on every pull request and again after every merge. It validates file ownership, manifest schemas, source-ID uniqueness, country-code integrity, the absence of modified raw files and the reproducibility of the thread's declared commands.

Merges happen in wave order and only when you say so. Within wave 1, T6a can merge at any time, but T6b's lock commit must precede T7's branch point. A thread with two stages, which applies to T6 and T8, rebases onto the main line before its second stage and merges again.

## Steps that need you

Access requirements are verified at run time and recorded per source. Nothing is assumed from earlier descriptions. The WVS site describes the joint EVS and WVS 2017 to 2022 release as free without registration, while the EVS route through GESIS requires sign-in and acceptance of GESIS terms. The access path, licence and version can differ between WVS, EVS and historical trend files. IHME Global Burden of Disease, PISA microdata if published aggregates prove insufficient, WIID and World Prison Brief are also checked at run time.

When a source needs registration or acceptance of terms, the thread stops at the access page, adds an entry to `data/LOCAL_DATA_REQUIRED.md`, and tells you what to download and where to put it. Creating accounts and accepting terms is yours to do.

You choose the licences before T0 merges. The recommendation is MIT for code, because it is the simplest permissive licence and fits both Python and R reuse, and CC BY 4.0 for documents, figures and result tables, because it requires attribution and is the norm for open research outputs. Each data source keeps its own licence, recorded in its manifest row, and the repository licence never covers raw data.

You also decide whether to archive the analysis lock publicly, you approve every merge, you review each data snapshot before it is published, and you approve the `results-*` tag that publishes the site.

## Shared contracts

**One manifest.** Each thread writes only its own file in `data/metadata/manifests/`, and every thread that creates a raw or derived data file has one. `make manifests` merges them deterministically into `data/metadata/all_assets_manifest.csv` and writes filtered views named `original_release_manifest.csv`, `inequality_manifest.csv`, `outcome_manifest.csv`, `controversy_test_manifest.csv`, `sources_manifest.csv` and `derived_manifest.csv`. The merge fails on duplicate source IDs, missing local files or hash mismatches.

**Manifest fields.** Every row carries the columns listed for its asset type at the end of this section. Every API, rolling database or periodically revised file also carries `retrieval_method`, `api_endpoint_or_landing_page`, `request_parameters`, `dataset_version`, `release_date`, `last_modified_header`, `etag`, `content_length_bytes`, `mime_type`, `archive_url`, `raw_file_sha256` and `code_version`. A dataset with no formal version gets `dataset_version` set to `unversioned` and keeps its raw response, retrieval timestamp and hash.

**Licensing.** No raw data or full text is committed to git. A source's licence decides only whether it may enter the public data snapshot. Restricted datasets, credentials, registration-protected files and copyrighted full texts never enter the snapshot. For such material the repository holds the bibliographic record, the manifest row, retrieval instructions, the expected checksum once you have supplied the file locally, and a `.gitignore` rule for its path. `data/LOCAL_DATA_REQUIRED.md` lists every user-supplied file with its expected path, required version, acquisition page, acceptance steps and checksum verification.

**Data immutability.** Raw files are never edited. The raw folders are `data/00_original_released/`, `data/00_original_reconstruction/`, `data/01_raw_current/` and `data/04_controversy_test_data/`. Only the acquisition script that owns a raw folder may add files to it, and it never overwrites an existing file. No script numbered 04 or higher may write to any raw folder, `data/02_harmonised/` or `data/03_analysis_ready/`. Analysis scripts write only to `outputs/` and to gitignored temporary folders. Any derived dataset comes from a numbered harmonisation script with a manifest row, a data dictionary entry and a source-year matrix.

**Build modes.** `make acquire` is the only target that contacts live sources. It downloads, verifies and records assets. `make fetch-snapshot` downloads a frozen, published snapshot and verifies its checksums. It is the only other target that uses the network, and it never contacts a live source. `make all` runs fully offline from files already present. `make clean-env` creates a disposable environment from `pixi.lock`, empties `outputs/`, runs `make fetch-snapshot` and then runs `make all`. `make check-contracts` runs the merge checks.

**Source-verification log.** Each thread that verifies a fact writes only its own file in `docs/source_verification/`. A fact is usable in a rule only once it is logged with the passage, table or file it was verified from.

**Source IDs.** Prefixed by thread, for example `T1-ORIG-001`, `T3-OECD-IDD-GINI` or `T4-WDI-SP.DYN.LE00.IN`. IDs never change once written.

**Country codes.** ISO 3166-1 alpha-3 throughout. Name variants map through one table in `code/lib/`.

**Controversy IDs.** `C-` followed by the category letter listed at the end of this section and a number, for example `C-B-002`. T2 assigns them.

**Code ownership.** An owned script path covers that script in either language. Each thread also owns `tests/<thread>/` for its pytest and testthat tests. Shared test utilities live in `tests/t0/` and change only through the integrator.

**Criticisms of the general hypothesis.** Some named criticisms predate *The Spirit Level* or address the income inequality and health hypothesis in general rather than the book's analyses. Judge 1995 and Gravelle 1998 are examples. Such a row has `target_level` set to `general_hypothesis`, while other rows use `original`, `current` or `both`. Its `mapping_rationale` states which book or current result the criticism bears on and why, and its `claim_or_result_affected` names that result. A general criticism whose testable implication requires individual-level data is classified as not testable in this design. Gravelle's artefact argument, which concerns a concave individual relationship between income and health, is an example where the country-level test can only be partial, and the register says so.

**Paths in code.** Relative to the project root, resolved through one helper in `code/lib/`.

**Original release manifest columns.** `source_id`, `title`, `organisation`, `url`, `publication_or_access_date`, `download_utc`, `local_path`, `sha256`, `file_format`, `licence_or_terms`, `notes` and `access_status`.

**Outcome manifest columns.** `source_id`, `outcome`, `source_organisation`, `dataset_title`, `url`, `indicator_code`, `indicator_definition`, `unit`, `population`, `geography`, `reference_year`, `publication_or_release_year`, `download_utc`, `local_path`, `sha256`, `licence`, `comparability_rating`, `transformation_needed` and `notes`. The inequality and controversy-test manifests use the same columns, with `outcome` holding the measure or variable name.

**Derived data manifest columns.** `derived_id`, `local_path`, `sha256`, `created_utc`, `producing_script`, `code_version` as the git commit, `input_source_ids`, `input_sha256s`, `transformation_summary`, `data_dictionary_ref`, `source_year_matrix_ref`, `analysis_lock_hash`, which is empty for T1b's original release dataset, and `notes`. `make manifests` fails if any input ID is missing from the manifest, if an input hash does not match, or if the data dictionary or source-year matrix reference does not resolve.

**Source bibliography columns.** `citation_key`, `authors`, `year`, `title`, `journal_or_publisher`, `doi`, `landing_url`, `direct_pdf_url`, `source_type`, `peer_review_status`, `research_design`, `geography`, `outcome`, `inequality_measure`, `main_finding_verbatim_short`, `methodological_limitations_verbatim_short`, `local_path`, `access_status` and `notes`. Quoted fields stay short enough to respect copyright.

**Controversy register columns.** `controversy_id`, `claim_or_result_affected`, `target_level`, `mapping_rationale`, `critic_name`, `source_title`, `publication_year`, `source_type`, `peer_review_status`, `exact_controversy_in_neutral_words`, `critic_argument_summary`, `data_or_method_the_critic_targets`, `empirical_test_possible`, `test_plan`, `wilkinson_pickett_response_available`, `response_source_id`, `local_path`, `citation_url` and `notes`.

**Controversy categories.** A is country selection and sample definition. B is the inequality measure, including the 80:20 ratio against Gini, market against disposable income, and survey comparability and timing. C is composite-index construction, including weighting, component choice and reverse coding. D is outliers and influential countries. E is temporal persistence, in later data and in national time series. F is mechanism, including the psychosocial account and alternatives such as material conditions, public services, institutions and social cohesion. G is data availability and comparability.

**Report sections.** The report has these sections in this order. Scope and terminology. Original analysis. Current update. Findings. Controversies, where each entry states the critic's claim, cites it, describes the test, shows the result, names its category and links any published Wilkinson and Pickett response. Limitations, covering the small country sample, cross-national comparability, temporal misalignment, missing data, measurement changes, dependence among outcomes and the limits of observational designs. Reproducibility, with exact commands, environment versions, checksums and data-access limits.
