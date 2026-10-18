# Implementation plan

This plan turns [INTENT.md](INTENT.md) into work that separate Claude sessions can run in parallel. Each session is called a thread here. A thread owns a fixed set of files, works on its own branch, and hands over through the shared contracts at the end of this document. No two threads write the same file.

## Execution order

Work runs in waves. A thread starts only when every gate it depends on has passed.

| Wave | Threads | Starts when | Milestone |
|---|---|---|---|
| 0 | T0 Scaffold | Now | 1 |
| 1A | T1a Original access and sample recovery, T2 stage 1 Register and appendix log, T3 Inequality data, T4 Outcome data, T5a Core test data, T6a Design lock | T0 merged | 1 |
| 1B | T1b Original reproduction | T1a merged | 1 |
| 1B | T5b stage 1 Test-data availability inventory | T2 stage 1 merged with the register frozen | 1 |
| 1B | T6b Lock completion | T6a, T1a, T3, T4 and T5a merged, T2 stage 1 merged with the register frozen and the appendix logged, and T5b stage 1 merged | 1 |
| 1C | Gate G2 sequence | Milestone 1 reviewed and merged into `main`, then tagged. The hash and archive decision merge into milestone 2 | 1 to 2 |
| 2 | T7 Primary harmonisation | Gate G2 passed | 2 |
| 2 | T2 stage 2 Supporting literature | Milestone 2 branch exists | 2 |
| 2B | T5b stage 2 Register-specific downloads | Milestone 2 branch exists | 2 |
| 3 | T8a Current replication | T7 merged | 2 |
| 3 | T7b Controversy harmonisation | T7 and T5b stage 2 merged | 2 |
| 3 | T8b Sensitivity and controversy tests | T8a and T7b merged | 2 |
| 4 | T9 Report and clean offline run | Milestone 2 reviewed and merged into `main` | 3 |

The answer to question B never waits for controversy-specific downloads. T7 builds the primary datasets and T8a analyses them while T5b and T7b are still working on named criticisms.

The lock waits for T2's frozen register so that every criticism-driven covariate, sample rule and panel test is declared before harmonisation, rather than added afterwards as an amendment. This makes T2 the critical path of wave 1A. The lock also waits for T5a and for T5b's availability inventory, so it is known before the lock which covariates and alternative components have an obtainable source. A covariate the register requires is declared in the lock whether or not a source exists. If the inventory found none, the lock says so in advance, and the result is reported as not tested for lack of data rather than discovered as a gap later.

A thread reads another thread's output only from its milestone's integration branch after that thread has merged into it. An integration branch always contains everything already on `main`. No thread reads from an unmerged thread branch.

## Gates

**G1. Original data access.** T1a assigns one of four statuses, and the status fixes the label that every question A output carries.

| Status | Definition | Label on outputs |
|---|---|---|
| G1-A verified original release | Files download and hash, contain usable original data, and carry enough documentation to identify variables and country cases. | Direct reproduction from released data |
| G1-B accessible but incomplete | Some files download, but required sheets, metadata, source notes or formulas are missing. | Partial released-data reproduction |
| G1-C archived copy only | A credible archive or third party supplies historical files, but provenance to the original release cannot be fully verified. | Archive-based reconstruction |
| G1-D unavailable | No usable original package is accessible. | Independent reconstruction |

For every retrieval attempt T1a records the HTTP status, redirect chain, response headers where available, UTC timestamp, SHA-256, file size, MIME type and whether the file is machine-readable. A 2017 Equality Trust post says the data could be downloaded. That establishes nothing about today, so the gate is decided only by these records.

**G2. Analysis lock.** T6 commits the analysis lock before any thread computes, views or infers an association between current inequality data and current outcome data. The gate does not cover T1b, because the original data and the authors' correlations are already published and reproducing them reveals nothing new about the current analysis. Downloading sources, reading metadata and checking country coverage before the lock are allowed. The lock files are `docs/analysis_lock.md`, `docs/source_hierarchy.md`, `docs/inclusion_rules.md`, `docs/dag.md`, the executable DAG `docs/dag.dagitty`, the script `code/00b_dag_adjustment_sets.R` that derives adjustment sets from it, and the adjustment sets it produced in `docs/dag_adjustment_sets.csv`. The commit that contains them is the lock commit.

`docs/analysis_lock_hash.txt` is not a lock file. It records the hashes and cannot contain its own. The lock is defined on `main`, after your review. T6b's pull request squash-merges the lock files into the milestone 1 integration branch. When you have reviewed and merged milestone 1 into `main`, its merge commit on `main` is the lock commit, and the integrator tags that commit `analysis-lock-v1`. The first pull request into the milestone 2 integration branch then adds `docs/analysis_lock_hash.txt` with the tag, the lock commit hash on `main` and a SHA-256 of each lock file's contents. Every result and the report cite the tag and the lock commit hash.

`make check-contracts` compares the lock files' contents with the most recent `analysis-lock-*` tag, so an amendment always has a defined reference. Before the first tag exists there is nothing to compare. Between the tag and the hash pull request, the check compares against the tag and reports the missing hash file as pending, not as a failure.

G2 passes in four steps, in this order. You review and merge milestone 1 into `main`. The integrator tags the merge commit and creates the milestone 2 integration branch from it. The hash pull request merges into milestone 2. You then decide whether to archive the lock publicly, and the decision is recorded in `docs/analysis_lock_archive.md`, either with the archive record and its DOI or with a statement that the lock remains internal. The decision merges into milestone 2 in its own small pull request. G2 has passed once both are on the milestone 2 integration branch, and only then does T7 branch.

The blinding is procedural only, and the lock says so in a section on prior knowledge. The original correlations are published, and table 1 of the 2024 technical appendix publishes correlations for 22 countries using recent data. Anyone writing the lock may know these results. The lock lists which published results its author had seen.

A git commit is an internal analysis lock, not a preregistration, even in a public repository, because commits and tags can be rewritten. The documents are called preregistration only if the lock commit is archived before T7 starts in an immutable public record such as OSF, Zenodo or Software Heritage. Archiving is your decision. Later changes to the lock are dated amendments with a stated reason, and affected results are reported under both the original and the amended rule.

**G3. Harmonised data validated.** T7's validation passes. Every analysis-ready column traces to a raw source variable, a formula, a direction, a missing-data rule, a reference year and a source ID.

**G4. Completion.** Every criterion in INTENT.md is met and `make clean-env` succeeds.

## Tech stack

The project mixes Python and R. Each language does what it does best, and the boundary between them is files, never in-process calls.

**Python** handles acquisition, provenance, harmonisation, index construction, the cross-sectional statistics and the contract checks. It uses pandas and pyarrow for data, requests and tenacity for downloads, sdmx1 for OECD SDMX queries, wbgapi for World Bank WDI, openpyxl and xlrd for spreadsheets, country_converter for ISO codes, scipy and statsmodels for correlations, OLS, robust regression, Theil–Sen and influence diagnostics, scikit-learn for the exploratory principal-component index, pandera for schemas and pytest for tests.

**Shared schemas.** Interface-file schemas are written once, in a language-neutral format, as Frictionless Table Schema JSON files in `data/metadata/schemas/`. A helper in `code/lib/` converts each into a pandera schema for Python. A small R validator in `code/lib/`, written in base R with jsonlite, checks the same names, types, required fields and allowed values, and testthat calls it. Neither language defines a schema in code.

**R** handles the models where its packages are the reference implementations. These are the panel models with fixest, the small-cluster inference method the lock selects, the DAG with dagitty, and qualitative comparative analysis with the QCA package if a register row requires re-running Greener's QCA. R code is tested with testthat and linted with lintr.

**The language boundary.** Every script is in one language. Scripts exchange data only through Parquet and CSV files under the paths the contracts define, read with arrow in R and pyarrow in Python. Z-scoring and index construction exist once, in Python, and R reads the computed indices instead of reimplementing them. Where both languages can compute the same statistic, a cross-language test computes the primary OLS and Pearson results in both and fails on any difference beyond numerical tolerance.

**Environment.** pixi manages one environment for both languages from conda-forge, with PyPI only for packages conda-forge lacks. Its single lockfile, `pixi.lock`, pins every Python and R package for macOS on Apple silicon and for Linux, so local runs and GitHub Actions resolve to the same builds. This was chosen for result quality. A separate Python lock and R lock, such as uv with renv, can drift apart and cannot pin the shared system libraries, while pixi pins the whole stack in one file. `environment.yml` and `requirements.txt`, which the original project specification requires, are exported from pixi. `environment.yml` covers the whole environment, while `requirements.txt` covers only the Python packages installable from PyPI, because R packages from conda-forge cannot appear there. CI fails if either export is out of date for what it covers. R packages that exist only on GitHub are not used, because they cannot be locked.

**Code quality.** ruff for Python, lintr and styler for R, and pre-commit to run them before every commit.

**Build.** GNU Make remains the entry point, and each target calls `pixi run`. The download helper refuses network access when `OFFLINE=1`, which `make all` sets, so offline replay is enforced in code rather than by convention.

**Report and site.** Quarto renders the report and the results website. The report source is `site/replication_report.qmd`. Quarto renders it both into the site and into `docs/replication_report.md` as GitHub-flavoured Markdown, so the Markdown report is a generated file, never edited by hand. The report and site pages contain Python code chunks only and render through the Jupyter engine. R results reach the report as files that R scripts wrote beforehand, so the language boundary holds and no knitr or reticulate bridge is needed. Every number in the report is computed from the output tables at render time rather than typed in.

**Bibliography tooling.** Crossref for DOIs, PubMed E-utilities for PMIDs, the PMC ID converter for PMCIDs, Unpaywall for legally open full texts and OpenAlex for citation chaining.

## GitHub repository and workflow

The project lives in the public GitHub repository https://github.com/open-reanalysis/how-economic-inequality-harms-societies under the `open-reanalysis` organisation. The site is published at https://open-reanalysis.github.io/how-economic-inequality-harms-societies/. Work reaches `main` through three milestone pull requests, and you review each of them.

| Milestone | Integration branch | Threads | What you review first |
|---|---|---|---|
| 1. Foundations, original reproduction and lock | `milestone/1-lock` | T0, T1a, T1b, T2 stage 1, T3, T4, T5a, T5b stage 1, T6a, T6b | The lock files, the source hierarchy, the inclusion rules, the frozen register and the question A results with their access label |
| 2. Analysis | `milestone/2-analysis` | Lock hash and archive decision, T2 stage 2, T5b stage 2, T7, T7b, T8a, T8b | The question B and C results, the source-selection log, the specification curve and the controversy tests |
| 3. Report and publication | `milestone/3-report` | T9 | The report and site, before you approve the `results-v1` tag |

Each thread works on a branch named after it, such as `t1a-original-access`, and opens a pull request into its milestone's integration branch when its stage is done. The pull request description is the merge package, using a template that lists every item the merge protocol requires. A thread pull request has no human review. It auto-merges by squash once every required check passes. Your review happens at the milestone pull request, which merges into `main` only when you say so.

The integration branch for milestone 1 is created from `main` when T0 starts. Each later one is created from `main` right after the previous milestone merges.

`main` is protected by a ruleset. Changes arrive only through pull requests from a `milestone/*` branch, the checks must pass, force pushes are blocked, and only organisation owners may merge. Claude sessions push and open pull requests with your GitHub account, which is an owner, so for them the rule that they never merge into `main` is procedural, written into every brief and into CONTRIBUTING.md. It becomes technical if you give the sessions a separate machine account or GitHub App with write access but no owner role. The `milestone/*` branches are protected too. They accept only pull requests, require the checks and allow auto-merge. The lock commit gets the tag `analysis-lock-v1`, as described under gate G2, and amendments get `analysis-lock-v1.1` and so on. Tags matching `analysis-lock-*` and `results-*` are protected by a tag ruleset that lets only organisation owners create, move or delete them. Owners are on the ruleset's bypass list, and the integrator creates these tags with an owner account. Workflows cannot create them. Thread pull requests are squash-merged into their integration branch, so each thread stage becomes one commit with a descriptive message. Milestone pull requests are merged into `main` with a merge commit, so those thread commits stay visible in the history of `main`.

**Raw data are not stored in git.** This applies to every raw folder and to downloaded full texts under `sources/`, whatever their licence. Several sources are far larger than GitHub's file limits, and many cannot be redistributed. Git holds manifests, metadata, code and generated outputs. `make acquire` builds a data snapshot, a set of archives whose checksums are recorded in the manifest. Redistributable assets are published as a GitHub release asset named after the snapshot, such as `data-snapshot-2026-11`. Non-redistributable assets stay on your machine and are listed in `data/LOCAL_DATA_REQUIRED.md`. Offline replay downloads the frozen snapshot and verifies every checksum before running. Fetching a frozen snapshot is not the same as redownloading live data, so this is compatible with the offline rule.

Because raw files do not appear in pull requests, the immutability check works on manifests and checksums instead. A pull request may add manifest rows but may not change the checksum, path or retrieval record of an existing row. CI verifies every redistributable file in the snapshot against its manifest checksum, and the thread verifies non-redistributable files locally and reports the result in its merge package.

**What CI can and cannot replay.** CI replays every step that depends only on redistributable assets. Steps that need non-redistributable data run locally, and their aggregated outputs are committed together with the checksums of the inputs they used. The report marks which results CI reproduced and which were reproduced locally.

Each thread declares its pipeline steps in its own file `code/pipeline/<thread>.toml`. A step entry names its script, its phase, its input source IDs and derived IDs, and its outputs. The phase is either `acquire`, for steps that download or record assets, or `replay`, for steps that work only from files already present. A small runner in `code/lib/` merges these files into one ordered pipeline and marks a replay step as CI-reproducible when every input traces back, through the manifests, to redistributable acquired assets. Every other replay step is local-only. Acquire steps are never CI-reproducible and never run in replay.

`make replay-ci` runs only the CI-reproducible steps. For every local-only step it leaves the committed outputs untouched and checks that the input checksums recorded with those outputs still match the manifest. If they do not match, the outputs are stale and the replay fails. A CI-reproducible step that depends on a local-only output is reported as an error in the pipeline declaration, because it could never be replayed in CI.

## GitHub Actions

`ci.yml` runs on every pull request. It installs the locked environment, runs ruff, lintr, pytest and testthat, checks that the exported environment files match `pixi.lock`, and runs `make check-contracts` in `metadata` mode. The ownership check reads the thread from the branch name and fails if the pull request changes files outside that thread's owned paths. A pull request from a fork has no thread branch, so a maintainer gives it a label such as `thread:t2` and the check runs against that thread's paths. Until the label is set, the check stays pending. A fork pull request targets the current integration branch and never auto-merges. A maintainer reviews and merges it, because code from outside the repository should not reach an integration branch without a person reading it. It also builds the Quarto site as a check and uploads it as a workflow artifact without deploying it.

`replay.yml` runs on every push to `main` or to a `milestone/*` branch. The published snapshot in use is declared in `data/metadata/snapshot.toml`, which names the release tag and the checksum of every archive. Until that file names a published snapshot, the workflow reports that there is nothing to replay and passes. Once it does, the workflow fetches that snapshot, verifies checksums, runs `make replay-ci` with `OFFLINE=1` and uploads the outputs as a workflow artifact. It fails if any committed output that CI can reproduce differs from the replayed one.

`acquire.yml` runs only on manual dispatch. It runs `make acquire` for the open sources and drafts a new snapshot release for you to review. It never publishes a snapshot by itself.

`pages.yml` runs only when a tag matching `results-*` is pushed, so unfinished results never appear on the public site. No test deployment exists, and rendering is verified by `ci.yml` without publishing anything. The site is built from the committed outputs. The workflow reads `data/metadata/snapshot.toml` in the same way as `replay.yml` and fetches that snapshot. If no published snapshot is declared, it renders the committed outputs without replay, and the reproduction-status table says that nothing was replayed in CI. Otherwise, before rendering, the workflow replays the steps CI can reproduce and fails if their outputs differ from the committed ones. The site shows a reproduction-status table, generated from the manifests, that marks each result as reproduced in CI or reproduced locally from non-redistributable inputs.

Third-party actions are pinned to commit hashes, and workflows get the minimum permissions they need.

## Results website

The GitHub Pages site is the public face of the project. It is built entirely from repository outputs and contains the replication report, all figures, every result table as a downloadable CSV, the controversy register with each test result, the analysis lock with its amendments and tag, the data dictionary, the manifests, the source-verification logs and instructions for reproducing everything. It contains no raw data.

Each published version states the release tag, the analysis-lock tag, the data snapshot and the date. The site uses the neutral terminology of INTENT.md throughout, and every controversy page shows the critic's claim, its source, the test, the result and any published response by Wilkinson and Pickett.

If the repository is connected to Zenodo, every release is archived with a DOI. A release made at the analysis-lock tag then serves as the immutable public record that allows the lock to be called a preregistration.

## Threads

### T0 Scaffold

Runs in this session. Creates the `milestone/1-lock` integration branch and configures the GitHub repository with the rulesets for `main`, `milestone/*` and the protected tags, auto-merge enabled at repository level, the pull request template, the four workflows, the pixi workspace with its lockfile and the exported `environment.yml` and `requirements.txt`, the pre-commit configuration, a minimal Quarto site that `ci.yml` renders but does not deploy, the licence files, the `Makefile` targets described under shared contracts, a `code/lib/` package with shared helpers, the manifest schema, `.gitignore` rules for user-supplied files, `data/LOCAL_DATA_REQUIRED.md` as a template and `LICENSES_AND_ACCESS.md` as a template. The shared helpers cover recorded downloads, manifest rows, path resolution, country-code mapping, logging, the pipeline runner, and z-scoring and index construction, so every thread computes them the same way. Z-scoring and index construction live in `code/lib/index.py`, which T0 owns, so T1b can use them in wave 1B before T7 exists. `code/lib/harmonise.py`, owned by T7, contains harmonisation helpers only. T0 is the first pull request into `milestone/1-lock`, and its CI runs on that pull request itself. Its squash commit is the base of every other thread branch in milestone 1.

Owns `README.md`, `CONTRIBUTING.md`, `LICENSE`, `LICENSE-docs`, `CITATION.cff`, `LICENSES_AND_ACCESS.md`, `pixi.toml`, `pixi.lock`, `environment.yml`, `requirements.txt`, `Makefile`, `.gitignore`, `.pre-commit-config.yaml`, `.github/`, `_quarto.yml`, `code/lib/` except `code/lib/harmonise.py`, `code/check_contracts.py`, `code/pipeline/t0.toml`, `data/metadata/schemas/`, `data/LOCAL_DATA_REQUIRED.md`, `data/metadata/snapshot.toml` and `tests/t0/`. After T0, `snapshot.toml` changes only through the integrator, when you approve a snapshot release.

This pull request, which adds the planning documents before T0, merges directly into `main` because no milestone branch exists yet. It is exempt from the ownership check, which does not exist yet either. It already adds `README.md`, `CONTRIBUTING.md`, the licences and the GitHub templates. T0 keeps them and changes them only where its own setup requires, for example to add real commands to the README.

After T0 merges, a thread that needs a change in a T0 file asks for it in its merge package. The integrator makes the change on a branch named `t0-<description>`, which the ownership check treats as T0, and opens a pull request into the current integration branch, where it auto-merges like any thread pull request. Changes to `snapshot.toml` go the same way after you have approved the snapshot release. The thread then rebases onto the integration branch.

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

Under status G1-C or G1-D, T1b rebuilds the original analysis from published tables, the book's notes and independently sourced historical data. Under G1-B it takes a hybrid path. It uses the released files for everything they contain and reconstructs only the missing sheets, formulas or source notes by the same route. Every value carries a provenance flag, released or reconstructed, and a component-provenance table accompanies every question A output, so the partial-reproduction label shows exactly which parts were reconstructed. `code/01c_download_reconstruction_sources.py` stores that material as downloaded in `data/00_original_reconstruction/`, separate from T1a's released files.

Writes a data dictionary and a source-year matrix for the original release dataset and records every raw and derived file it creates in its own manifest.

Owns `code/01b_prepare_original.py`, `code/01c_download_reconstruction_sources.py`, `data/00_original_reconstruction/`, `data/03_analysis_ready/original/`, `data/metadata/manifests/t1b_original_derived.csv`, `docs/data_dictionary_original.md`, `outputs/tables/original_variable_year_matrix.csv`, `code/04_reproduce_original.py`, `outputs/tables/original_*` except the sample recovery file, `outputs/figures/original_*`, `outputs/diagnostics/original_reproduction_discrepancies.md` and `docs/source_verification/t1b_original_method.md`.

### T2 Sources and controversy register

Builds the literature package in the five `sources/` folders, keeping primary author material, supporting academic work, academic criticism, non-academic criticism and author replies apart. Expands the seed list by backward and forward citation searching.

Writes the controversy register. A row enters it only with the critic's name, exact title, year and a stable DOI, PMID, PMCID or URL, checked against PubMed, the DOI record or the publisher page. Rows are classified by target, which is data selection, measurement, index construction, robustness, mechanism, causal interpretation or policy inference. Each row names the data T5b must supply and the test T8b must run, or marks `empirical_test_possible` as no with the reason. Wilkinson and Pickett's published responses are linked to the criticisms they answer.

The seed list includes Greener's reproduction and update in the International Journal of Comparative Sociology, DOI 10.1177/00207152241245620, Judge 1995, Gravelle 1998, the Equality Trust author response, Fischer in the Boston Review, Saunders, Snowdon, the TUC summary of criticisms and replies, and the 2024 technical appendix. T2 records for every entry the exact publication date and whether it is the online-first or the issue date, in `publication_date_type`, and cites it the same way everywhere. Greener's DOI carries a 2024 suffix while the issue is dated 2025, so the distinction matters there.

Full texts are never committed to git. They are stored locally under `sources/` and enter the public data snapshot only where the licence allows redistribution. The repository holds the bibliographic record, retrieval instructions and a gitignored local path for each.

Extracts from the 2024 technical appendix the passages, table definitions, country list, reference-year statements, index construction and direction coding, and records them in its part of the source-verification log as update-method documentation. This includes the appendix's description of the original timing, its use of the term 80:20 and its use of PISA 2018 instead of PISA 2022. T6b uses these only after they are logged. The log covers methods, definitions, samples and years only. It excludes correlation coefficients and other result values, table 1 included, so T6b does not see current-data results through it. Anyone working on the lock who has seen such values lists them in the lock's prior-knowledge section.

The appendix verification and the register freeze are both prerequisites for the lock, so T2 does them before expanding the supporting literature.

Owns `sources/`, `code/00_download_sources.py`, `docs/controversy_register.md`, `data/metadata/manifests/t2_sources.csv` and `docs/source_verification/t2_sources.md`.

Runs backward and forward citation searching over the criticism literature and the author replies before the freeze. Expanding the supporting literature can continue afterwards.

T2 merges twice. Stage 1 ends when the register is frozen and the appendix is logged, and its merge unblocks T5b and T6b. Stage 2 expands the supporting literature and merges separately before T9. Both stages are the same thread. Stage 1 targets milestone 1 and stage 2 targets milestone 2, so the thread rebases onto the milestone 2 integration branch before stage 2.

Stage 1 is done when the register is frozen by a commit that records the search cut-off date and the search log. Later threads read only a frozen version. A named criticism found after the freeze is added in a dated register amendment and a matching dated lock amendment. Its test is reported separately as a post-lock analysis, and the report states that it was not declared before the data were examined.

### T3 Current inequality data

Downloads raw copies, metadata and codebooks from the OECD Income Distribution Database, the World Bank Poverty and Inequality Platform, UNU-WIDER WIID and WID.world. Records for each measure the income concept, tax and transfer treatment, equivalisation, unit, price basis, survey year, coverage and known series breaks. The OECD database is revised on a rolling basis and served through an SDMX API, so the endpoint, query parameters, response hash and any version identifier are pinned.

Builds the inequality measure crosswalk in a replay step, `code/02e_build_inequality_crosswalk.py`, from the downloaded files and metadata, so a clean offline run regenerates it. Does not merge inequality with outcomes.

Owns `data/01_raw_current/inequality/`, `code/02a_download_inequality.py`, `code/02e_build_inequality_crosswalk.py`, `data/metadata/manifests/t3_inequality.csv` and `outputs/tables/inequality_measure_crosswalk.csv`.

### T4 Current outcome data

Downloads the ten outcome series with metadata and methodology notes. These cover trust from WVS, EVS and ESS, life expectancy, infant mortality and adolescent births from WDI, WHO and OECD, adult obesity from WHO and OECD, mental illness from GBD and OECD, educational performance from PISA, homicide from UNODC, imprisonment from World Prison Brief and SPACE, and intergenerational mobility from OECD and the World Bank GDIM.

For PISA it records participation status and sampling-standard flags per country and cycle. OECD flagged several countries in PISA 2022 for not meeting sampling standards, and the 2024 update used PISA 2018 for that reason.

Rates comparability per outcome and records the actual reference year for every country-value pair. Downloads the preferred source and the plausible fallbacks for each outcome, so that the hierarchy in the lock can be applied without a second acquisition. Publishes `outputs/tables/outcome_source_coverage.csv`, built by a replay step `code/02f_build_outcome_coverage.py` from the downloaded files and metadata so a clean offline run regenerates it, with source, coverage, years and comparability notes but no outcome values, which T6b may read. Never inspects any outcome against inequality.

Owns `data/01_raw_current/outcomes/`, `code/02b_download_outcomes.py`, `code/02f_build_outcome_coverage.py`, `data/metadata/manifests/t4_outcomes.csv` and `outputs/tables/outcome_source_coverage.csv`.

### T5a Core controversy-test data

Downloads the packages that many criticisms share, chosen before the register is frozen. These are country universe and population, OECD membership history, World Bank income classification and GNI, democracy indicators from V-Dem or Freedom House, the OECD Social Expenditure Database, GDP per capita, poverty, unemployment, the Worldwide Governance Indicators, the Quality of Government dataset and health expenditure. Panel versions are pinned the same way as T3.

Owns `data/04_controversy_test_data/core/`, `code/02c_download_core_test_data.py` and `data/metadata/manifests/t5a_core.csv`.

### T5b Register-specific test data

Runs in two stages, both after T2's stage 1 merge.

Stage 1 is an availability inventory that the lock depends on. For every covariate and alternative component a register row requires, it records candidate sources, country and year coverage, licence, redistributability and access route in `outputs/tables/test_data_availability.csv`. Coverage usually needs the data files, and the lock restricts only associations between inequality and outcomes, so stage 1 may download covariate values. It computes coverage from non-missing flags only and runs no analysis. The table is built by a replay step, `code/02g_build_test_data_availability.py`, so a clean offline run regenerates it.

Stage 2 runs after stage 1 merges and downloads only data that a named register row requires, such as alternative outcome components proposed by a critic, and records the controversy ID before each download. Each package gets a README naming the controversy it tests.

Owns `data/04_controversy_test_data/by_controversy/`, `code/02d_download_register_test_data.py`, `code/02g_build_test_data_availability.py`, `outputs/tables/test_data_availability.csv` and `data/metadata/manifests/t5b_register.csv`.

### T6a Design lock

Writes the parts of the analysis plan that need no other thread's output, without reading any outcome values. Fixes the primary inequality measure, the year alignment rule and lag windows, the index formulas and the robustness methods.

Fixes the index direction per measure, not per concept. A measure where a higher value means more of a problem keeps its sign, and every other measure is reversed. For mobility this matters, because an intergenerational elasticity and a mobility index point in opposite directions.

Defines the expanded sample rule with population threshold, income threshold and its source, democracy criterion and the treatment of contested countries including Germany, Israel, Singapore, South Korea and Czechia. Fixes the multiverse dimensions and the reproducibility seed. Every alternative country rule, every multiverse dimension and the panel protocol cites either a register row or a sensitivity rationale stated in the lock, in line with question C of INTENT.md.

Admits a macro-level covariate only where a named criticism, a cited alternative explanation or a stated sensitivity rationale identifies it, and records which one. A locked covariate for which no T5 thread obtained a usable source is reported as not tested, with the reason, and is never silently dropped from the model.

Fixes the missing-component rule for the index. A mean of the available z-scores is itself a missing-data rule, even though no value is imputed, so the lock states it as one. It fixes the minimum number of components a country needs to receive an index value, reports the number of components behind every country's value, and adds a complete-case index over countries with every component as a declared sensitivity analysis. "No imputation" means that no missing value is filled in. It does not mean that the available-case mean is free of assumptions.

Fixes the reference population for z-scores. By default the components are standardised within each analysed sample, so the index is recomputed for every country rule in the multiverse and for every leave-one-country-out run. Standardising on a fixed reference set, the historical country sample, is a declared sensitivity analysis. T1b verifies separately how the original study standardised.

Fixes how the many comparisons are reported. Every specification in the multiverse is reported as a specification curve, with none omitted. Effect sizes with confidence intervals are the primary result. Statistical significance is never used to select which specifications, outcomes or samples are reported. The ten outcomes are always reported together. P-values are shown unadjusted, alongside Holm-adjusted p-values across the ten outcomes as a declared secondary view.

Names every domain index and its component membership. If a component cannot be harmonised, the domain is reported with fewer components and the change appears in the component-availability table.

Fixes the panel protocol. This covers the panel unit, a minimum number of countries and within-country observations per outcome below which no model is fitted, country and year fixed effects, whether country trends enter, the lag structure, serial-correlation handling, the standard-error method for a small number of countries and the missing-data treatment.

Draws the DAG used for covariate selection, separating possible confounders from possible mediators. The DAG is written in dagitty syntax, and an R script derives the adjustment sets from it so the covariate choice is computed rather than asserted.

Owns the lock files listed under gate G2, together with `docs/analysis_lock_hash.txt`, `docs/analysis_lock_archive.md` and `tests/t6/`. The lock files are covered by the content hashes, so a change to any of them after the lock, the DAG and its script included, fails `make check-contracts` unless it comes as a dated amendment with a new tag. The hash file and the archive record are not hashed.

### T6b Lock completion

Starts from the milestone 1 integration branch once its wave-table conditions are met.

Fixes the source hierarchy for every indicator in `docs/source_hierarchy.md`. Each entry names the preferred source, permitted fallbacks, the minimum comparability conditions and the circumstances that justify a fallback. T6b may read T4's coverage table, T3's crosswalk, T2's logged appendix passages, T5a's manifest and T5b's availability inventory, but no outcome values.

Reads `original_sample_recovery.csv` and nothing else from T1. Inserts the recovered historical country list and its source reference into `docs/inclusion_rules.md`. Adds the covariates, sample rules and panel tests that named register rows require. Adding covariates changes the DAG, so T6b re-runs `code/00b_dag_adjustment_sets.R` and commits the regenerated `docs/dag_adjustment_sets.csv` before the lock commit. Writes the prior-knowledge section. Then opens the lock pull request into milestone 1. After you have merged milestone 1 into `main` and the integrator has tagged the merge commit, the thread opens the hash pull request with `docs/analysis_lock_hash.txt` into milestone 2. The thread never creates tags itself. Gate G2 passes after your archive decision, as described under G2. T6b is a second stage of the same thread, not a separate session. T6a merges first, and the thread rebases onto the milestone 1 integration branch before starting T6b.

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

Owns `code/05_current_replication.py`, `code/05b_crosscheck.R`, `tests/t8a/`, `outputs/tables/current_replication_results.csv` and `outputs/diagnostics/influence_diagnostics.csv`.

### T8b Sensitivity and controversy tests

Answers question C for both the original and the current result. A second stage of the same thread as T8a, which rebases onto the milestone 2 integration branch once T7b has merged.

A register row whose `claim_or_result_affected` names the original result is tested on T1b's original release dataset in `data/03_analysis_ready/original/`. This covers, for example, criticisms of the original country selection or the original index. A row that names the current result is tested on T7 and T7b data, and a row that names both is tested on both. T8b only reads T1b's data. T1b's own alternative specifications remain labelled diagnostics and are not counted as controversy tests. Writes only to `outputs/`, and every result row carries the same provenance fields as in T8a.

Runs the multiverse over the locked country rules and inequality measures and reports it as the full specification curve the lock defines. A principal-component index is an exploratory sensitivity analysis only. It reports loadings, explained variance, sign choice, country sample and missing-data treatment, and it is never described as a reproduction or used in place of the primary index.

Panel analyses run in a separate module. Before fitting any model, it reports for each outcome the number of countries, years, country-year observations and within-country variation. No model is fitted below the minimum set in the lock. Results are described as within-country associations, not causal estimates.

Each controversy in the frozen register gets one result, labelled with one of five outcomes. Consistent, partly consistent or inconsistent with the critic's stated concern. Indeterminate when coverage, comparability or precision is insufficient to assess it. Not testable in this design when the register marks `empirical_test_possible` as no, as with a mechanism or causal claim that country-level correlations cannot address. Rows of the last kind get no test table. They are listed in a separate table with the reason, and the report discusses them under the matching heading of the terminology in INTENT.md.

If a register row requires re-running Greener's qualitative comparative analysis, it runs in R with the QCA package.

Owns `code/06_robustness_and_controversy_tests.py`, `code/06b_panel_models.R`, `code/06c_qca.R`, `tests/t8b/`, `outputs/tables/sensitivity_results.csv`, `outputs/tables/controversy_test_results.csv` and `outputs/tables/controversies_not_testable.csv`.

### T9 Report and clean offline run

Generates all figures and tables from code and builds the Quarto site, including `outputs/tables/all_model_results.csv` as the combination of T1b, T8a and T8b results, writes `site/replication_report.qmd` with the report sections listed under shared contracts and renders it to `docs/replication_report.md`, runs `make clean-env`, and checks the completion criteria, listing anything unmet. When you approve, T9 tags the release as `results-v1`, which publishes the site.

Owns `code/07_make_tables_figures.py`, `outputs/LICENSE_EXCEPTIONS.md`, `site/` including `site/replication_report.qmd`, the generated `docs/replication_report.md`, `tests/t9/`, `outputs/tables/all_model_results.csv`, `outputs/figures/` except files starting with `original_`, and `outputs/logs/`.

## How the threads run as sessions

T0 runs here. Every other thread runs as its own Claude session in its own git worktree, branched from its milestone's integration branch when its wave opens. A thread's brief is its section of this plan plus INTENT.md. A thread finishes by pushing its branch, opening a pull request into its integration branch whose description is the merge package described below, and enabling auto-merge. A thread session never merges into `main` and never opens a milestone pull request.

T3, T4, T5a and T5b mainly download and catalogue and can use a cheaper model. T1a, T1b, T2, T6, T7, T7b and T8 in both stages involve judgement and use the default model. T2 is among them because its register freeze decides what counts as a valid criticism, and it is on the critical path.

## Merge protocol

**Thread pull requests.** Before a thread pull request can merge into its integration branch, its thread provides in the pull request description the commit hash, the list of changed files, its completion checklist, the manifest validation output, the tests run with exit status, known access failures, licence and redistribution status, and confirmation that it wrote nothing outside its owned files.

`make check-contracts` runs in CI on every pull request and again after every merge. In CI it runs in `metadata` mode and validates file ownership, manifest schemas, source-ID uniqueness, country-code integrity, unchanged manifest rows for raw files, the lock content hashes, and that `docs/dag_adjustment_sets.csv` matches a fresh run of its script, which needs no data files. Whether the thread's declared commands reproduce its outputs needs data, so the thread checks it locally in `full` mode and reports the result in the merge package, and `make replay-ci` checks it again on the integration branch and on `main` for the CI-reproducible steps. A thread pull request merges automatically once every required check passes. It needs no human approval, and it opens only when the thread's start conditions in the wave table are met.

**Milestone pull requests.** The integrator opens each milestone pull request from its integration branch into `main` once every thread in that milestone has merged. Its description lists the gate files to read first, links every thread pull request with its merge package, and reports the latest replay and contract-check results. You review it and merge it with a merge commit. Nothing else merges into `main`.

Thread pull requests merge in wave order, because each opens only when its conditions are met. A thread with two stages, which applies to T2, T5b, T6 and T8, rebases onto its integration branch before its second stage and merges again.

## Steps that need you

Access requirements are verified at run time and recorded per source. Nothing is assumed from earlier descriptions. The WVS site describes the joint EVS and WVS 2017 to 2022 release as free without registration, while the EVS route through GESIS requires sign-in and acceptance of GESIS terms. The access path, licence and version can differ between WVS, EVS and historical trend files. IHME Global Burden of Disease, PISA microdata if published aggregates prove insufficient, WIID and World Prison Brief are also checked at run time.

When a source needs registration or acceptance of terms, the thread stops at the access page, adds an entry to `data/LOCAL_DATA_REQUIRED.md`, and tells you what to download and where to put it. Creating accounts and accepting terms is yours to do.

The licences are decided. Code and tests are under MIT, in `LICENSE`. Documents, the report, the site, figures and result tables are under CC BY 4.0, in `LICENSE-docs`. Each data source keeps its own licence, recorded in its manifest row, and neither repository licence covers raw data or third-party full texts. A derived table or figure that contains values from a source follows that source's terms where they are stricter than CC BY 4.0. Each output's manifest row names the source terms it inherits, T9 generates `outputs/LICENSE_EXCEPTIONS.md` from those rows, and an output whose source terms forbid publication is not put on the site.

Branch protection does not require an approving review while you are the only human contributor, since GitHub does not let an author approve their own pull request. Your decision to merge a milestone pull request is the human review. Once a second person contributes, one approving review becomes required. Most commits so far are co-authored by an AI model, so a human pass over the gates in this plan before T0 starts is worth doing.

You also decide whether to archive the analysis lock publicly, you review and merge the three milestone pull requests, you review each data snapshot before it is published, and you approve the `results-*` tag that publishes the site.

## Shared contracts

**One manifest.** Each thread writes only its own file in `data/metadata/manifests/`, and every thread that creates a raw or derived data file has one. `make manifests` merges them deterministically into `data/metadata/all_assets_manifest.csv` and writes filtered views named `original_release_manifest.csv`, `inequality_manifest.csv`, `outcome_manifest.csv`, `controversy_test_manifest.csv`, `sources_manifest.csv` and `derived_manifest.csv`. Validation runs in one of three modes, chosen by where it runs.

Every row carries `acquisition_status`. `acquired` means the file was obtained and must exist with a matching checksum. `user_supplied` means you obtained a restricted file by hand, and it is treated like `acquired` once present. `awaiting_user` means the source needs registration or acceptance of terms and is listed in `data/LOCAL_DATA_REQUIRED.md`. `access_failed` records an attempt that did not produce a usable file, with the retrieval record that shows why. `not_downloaded_restricted` records a source catalogued for metadata only. Only `acquired` and `user_supplied` rows require a file and a checksum. The other statuses require their retrieval record or listing instead, and a validation mode never treats them as missing files.

- **metadata** runs in CI on every pull request. It validates schemas, source-ID uniqueness, cross-references, and that no existing raw or acquired row's checksum, path or retrieval record has changed. Derived rows are never edited either. A regenerated derived file, after a bug fix or a lock amendment, gets a new versioned `derived_id`, and the old row is kept with `superseded_by` pointing to it. It touches no data files.
- **available** runs in CI replay. It does everything `metadata` does, then requires every row marked `redistributable` to have its file present and its hash matching. Rows not marked `redistributable` are listed as skipped, never as passed.
- **full** runs locally before a thread opens its pull request and in `make clean-env`. It requires the file for every `acquired` and `user_supplied` row, restricted ones included, and fails on any missing file or hash mismatch. It lists `awaiting_user` rows so the gap stays visible. The thread reports the `full` result in its merge package.

`make manifests` and `make check-contracts` take the mode as a parameter and default to `full` locally.

**Manifest fields.** Every row carries the columns listed for its asset type at the end of this section. Every row also carries `redistributable`, set from the source's terms, which decides whether the asset enters the public snapshot and which validation mode checks its file. Every API, rolling database or periodically revised file also carries `retrieval_method`, `api_endpoint_or_landing_page`, `request_parameters`, `dataset_version`, `release_date`, `last_modified_header`, `etag`, `content_length_bytes`, `mime_type`, `archive_url`, `raw_file_sha256` and `code_version`. A dataset with no formal version gets `dataset_version` set to `unversioned` and keeps its raw response, retrieval timestamp and hash.

**Licensing.** No raw data or full text is committed to git. A source's licence decides only whether it may enter the public data snapshot. Restricted datasets, credentials, registration-protected files and copyrighted full texts never enter the snapshot. For such material the repository holds the bibliographic record, the manifest row, retrieval instructions, the expected checksum once you have supplied the file locally, and a `.gitignore` rule for its path. `data/LOCAL_DATA_REQUIRED.md` lists every user-supplied file with its expected path, required version, acquisition page, acceptance steps and checksum verification.

**Data immutability.** Raw files are never edited. The raw folders are `data/00_original_released/`, `data/00_original_reconstruction/`, `data/01_raw_current/` and `data/04_controversy_test_data/`. Only the acquisition script that owns a raw folder may add files to it, and it never overwrites an existing file. No script numbered 04 or higher may write to any raw folder, `data/02_harmonised/` or `data/03_analysis_ready/`. Analysis scripts write only to `outputs/` and to gitignored temporary folders. Any derived dataset comes from a numbered harmonisation script with a manifest row, a data dictionary entry and a source-year matrix.

**Build modes.** `make acquire` is the only target that contacts live sources. It downloads, verifies and records assets. `make fetch-snapshot` downloads a frozen, published snapshot and verifies its checksums. It is the only other target that uses the network, and it never contacts a live source. `make acquire` runs only steps whose phase is `acquire`. `make all` runs every step whose phase is `replay`, fully offline from files already present, which needs the restricted files too and therefore runs locally. `make replay-ci` runs only the CI-reproducible replay steps, as described under the GitHub repository section. Neither `make all` nor `make replay-ci` ever runs an acquire step. Every table an acquisition thread publishes in `outputs/` is built by a replay step from snapshot files and metadata, never by the download script itself, so emptying `outputs/` loses nothing that replay cannot rebuild. `make clean-env` creates a disposable environment from `pixi.lock`, empties `outputs/`, runs `make fetch-snapshot` and then runs `make all`. `make check-contracts` runs the merge checks.

**Source-verification log.** Each thread that verifies a fact writes only its own file in `docs/source_verification/`. A fact is usable in a rule only once it is logged with the passage, table or file it was verified from.

**Source IDs.** Prefixed by thread, for example `T1-ORIG-001`, `T3-OECD-IDD-GINI` or `T4-WDI-SP.DYN.LE00.IN`. IDs never change once written.

**Country codes.** ISO 3166-1 alpha-3 throughout. Name variants map through one table in `code/lib/`.

**Controversy IDs.** `C-` followed by the category letter listed at the end of this section and a number, for example `C-B-002`. T2 assigns them.

**Code ownership.** An owned script path covers that script in either language. Each thread also owns `code/pipeline/<thread>.toml` for its pipeline steps and `tests/<thread>/` for its pytest and testthat tests. This applies to every thread, whether or not its own section repeats these paths, and the ownership check derives them from the thread ID. Shared test utilities live in `tests/t0/` and change only through the integrator.

**Criticisms of the general hypothesis.** Some named criticisms predate *The Spirit Level* or address the income inequality and health hypothesis in general rather than the book's analyses. Judge 1995 and Gravelle 1998 are examples. Such a row has `target_level` set to `general_hypothesis`, while other rows use `original`, `current` or `both`. Its `mapping_rationale` states which book or current result the criticism bears on and why, and its `claim_or_result_affected` names that result. A general criticism whose testable implication requires individual-level data is classified as not testable in this design. Gravelle's artefact argument, which concerns a concave individual relationship between income and health, is an example where the country-level test can only be partial, and the register says so.

**Paths in code.** Relative to the project root, resolved through one helper in `code/lib/`.

**Original release manifest columns.** `source_id`, `title`, `organisation`, `url`, `publication_or_access_date`, `download_utc`, `local_path`, `sha256`, `file_format`, `licence_or_terms`, `notes` and `access_status`.

**Outcome manifest columns.** `source_id`, `outcome`, `source_organisation`, `dataset_title`, `url`, `indicator_code`, `indicator_definition`, `unit`, `population`, `geography`, `reference_year`, `publication_or_release_year`, `download_utc`, `local_path`, `sha256`, `licence`, `comparability_rating`, `transformation_needed` and `notes`. The inequality and controversy-test manifests use the same columns, with `outcome` holding the measure or variable name.

**Derived data manifest columns.** `derived_id`, `local_path`, `sha256`, `created_utc`, `producing_script`, `code_version` as the git tree hash of `code/` together with the blob hash of the producing script, `base_commit` as the integration-branch commit the run started from, `input_source_ids`, `input_sha256s`, `transformation_summary`, `data_dictionary_ref`, `source_year_matrix_ref`, `analysis_lock_hash`, which is empty for T1b's original release dataset, `superseded_by` and `notes`. A tree hash is the same before and after a squash merge and a milestone merge when the code is unchanged, so it identifies the code even though the thread's branch commit disappears. The same two fields identify code in every result row. `make manifests` fails if any input ID is missing from the manifest, if an input hash does not match, or if the data dictionary or source-year matrix reference does not resolve.

**Source bibliography columns.** `citation_key`, `authors`, `year`, `title`, `journal_or_publisher`, `doi`, `landing_url`, `direct_pdf_url`, `source_type`, `peer_review_status`, `research_design`, `geography`, `outcome`, `inequality_measure`, `main_finding_verbatim_short`, `methodological_limitations_verbatim_short`, `local_path`, `access_status` and `notes`. Quoted fields stay short enough to respect copyright.

**Controversy register columns.** `controversy_id`, `claim_or_result_affected`, `target_level`, `mapping_rationale`, `critic_name`, `source_title`, `publication_year`, `publication_date_type`, `source_type`, `peer_review_status`, `exact_controversy_in_neutral_words`, `critic_argument_summary`, `data_or_method_the_critic_targets`, `empirical_test_possible`, `test_plan`, `wilkinson_pickett_response_available`, `response_source_id`, `local_path`, `citation_url` and `notes`.

**Controversy categories.** A is country selection and sample definition. B is the inequality measure, including the 80:20 ratio against Gini, market against disposable income, and survey comparability and timing. C is composite-index construction, including weighting, component choice and reverse coding. D is outliers and influential countries. E is temporal persistence, in later data and in national time series. F is mechanism, including the psychosocial account and alternatives such as material conditions, public services, institutions and social cohesion. G is data availability and comparability.

**Report sections.** The report has these sections in this order. Scope and terminology. Original analysis. Current update. Findings. Controversies, where each entry states the critic's claim, cites it, describes the test, shows the result, names its category and links any published Wilkinson and Pickett response. Limitations, covering the small country sample, cross-national comparability, temporal misalignment, missing data, measurement changes, dependence among outcomes and the limits of observational designs. Reproducibility, with exact commands, environment versions, checksums and data-access limits.
