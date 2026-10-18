# Implementation plan

This plan turns [INTENT.md](INTENT.md) into work that separate Claude sessions can run in parallel. Each session is called a thread here. A thread owns a fixed set of files, works on its own branch, and hands over through the shared contracts at the end of this document. No two threads write the same file.

## Execution order

Work runs in waves. A thread starts only when every gate it depends on has passed.

| Wave | Thread or stage | Starts when | Milestone |
|---|---|---|---|
| 0 | Scaffold | Now | 1 |
| 1A | Original access, register freeze, inequality data, outcome data, core test data, lock design, claims register | Scaffold merged | 1 |
| 1B | Original reproduction | Original access merged | 1 |
| 1B | Availability inventory | Register freeze and analysis types merged | 1 |
| 1B | Analysis types | Lock design, claims register and register freeze merged | 1 |
| 1B | Lock completion | Lock design, original access, inequality data, outcome data, core test data, claims register, analysis types, register freeze with the appendix logged, and availability inventory merged | 1 |
| 1C | Lock gate sequence | Milestone 1 reviewed and merged into `main`, then tagged. The hash and archive decision merge into milestone 2 | 1 to 2 |
| 2 | Primary harmonisation | Lock gate passed | 2 |
| 2 | Literature expansion | Milestone 2 branch exists | 2 |
| 2B | Register test downloads | Milestone 2 branch exists | 2 |
| 3 | Current replication | Primary harmonisation merged | 2 |
| 3 | Controversy harmonisation | Primary harmonisation and register test downloads merged | 2 |
| 3 | Sensitivity tests | Current replication and controversy harmonisation merged | 2 |
| 3 | Causal assessment | Current replication and controversy harmonisation merged | 2 |
| 2 | Multilevel feasibility | Milestone 2 branch exists | 2 |
| 4 | Report | Milestone 2 reviewed and merged into `main` | 3 |

Each thread has a name used in prose and an ID used by tools. The ID names the thread's branches, its pipeline file, its test folder, its manifest and its source-verification log, and it prefixes its source IDs. Four threads run in two stages, each with its own name. Wave numbers and milestone numbers stay numeric because they give the order of execution.

| Thread | ID | Stages |
|---|---|---|
| Scaffold | `scaffold` | |
| Original access and sample recovery | `original-access` | |
| Original reproduction | `original-reproduction` | |
| Sources and controversy register | `controversy-register` | Register freeze, then literature expansion |
| Current inequality data | `inequality-data` | |
| Current outcome data | `outcome-data` | |
| Core controversy-test data | `core-test-data` | |
| Register-specific test data | `register-test-data` | Availability inventory, then register test downloads |
| Analysis lock | `lock` | Lock design, then lock completion |
| Author claims register | `claims-register` | |
| Analysis-type declaration | `analysis-types` | |
| Primary harmonisation | `harmonisation` | |
| Controversy harmonisation | `controversy-harmonisation` | |
| Analysis | `analysis` | Current replication, then sensitivity tests |
| Causal assessment | `causal-assessment` | |
| Multilevel feasibility | `multilevel-feasibility` | |
| Report and clean offline run | `report` | |

The answer to the current replication question never waits for controversy-specific downloads. Primary harmonisation builds the primary datasets and current replication analyses them while the register test data thread and controversy harmonisation are still working on named criticisms.

The lock waits for the controversy register thread's frozen register so that every criticism-driven covariate, sample rule and panel test is declared before harmonisation, rather than added afterwards as an amendment. This makes the controversy register thread the critical path of wave 1A. For the same reason the lock waits for the claims register thread's frozen claims register and for the analysis-type thread's declaration of each analysis as a sensitivity analysis or part of a causal assessment. The lock also waits for the core test data thread and for the register test data thread's availability inventory, so it is known before the lock which covariates and alternative components have an obtainable source. A covariate the register requires is declared in the lock whether or not a source exists. If the inventory found none, the lock says so in advance, and the result is reported as not tested for lack of data rather than discovered as a gap later.

A thread reads another thread's output only from its milestone's integration branch after that thread has merged into it. An integration branch always contains everything already on `main`. No thread reads from an unmerged thread branch.

## Gates

**Access gate.** The original access thread assigns one of four access statuses, and the status fixes the label that every original reproduction output carries.

| Status | Definition | Label on outputs |
|---|---|---|
| `verified_release` | Files download and hash, contain usable original data, and carry enough documentation to identify variables and country cases. | `DIRECT REPRODUCTION` |
| `incomplete_release` | Some files download, but required sheets, metadata, source notes or formulas are missing. | `PARTIAL REPRODUCTION` |
| `archived_copy` | A credible archive or third party supplies historical files, but provenance to the original release cannot be fully verified. | `ARCHIVE-BASED RECONSTRUCTION` |
| `unavailable` | No usable original package is accessible. | `INDEPENDENT RECONSTRUCTION` |

For every retrieval attempt the original access thread records the HTTP status, redirect chain, response headers where available, UTC timestamp, SHA-256, file size, MIME type and whether the file is machine-readable. A 2017 Equality Trust post says the data could be downloaded. That establishes nothing about today, so the gate is decided only by these records.

**Lock gate.** The lock thread commits the analysis lock before any thread computes, views or infers an association between current inequality data and current outcome data. The gate does not cover the original reproduction thread, because the original data and the authors' correlations are already published and reproducing them reveals nothing new about the current analysis. Downloading sources, reading metadata and checking country coverage before the lock are allowed. The lock files are `docs/analysis_lock.md`, `docs/source_hierarchy.md`, `docs/inclusion_rules.md`, `docs/analysis_types.md`, `docs/dag.md`, the executable DAG `docs/dag.dagitty`, the script `code/00b_dag_adjustment_sets.R` that derives adjustment sets from it, the adjustment sets it produced in `docs/dag_adjustment_sets.csv`, the causal standard `docs/causal_standard.md`, the machine-readable verdict rules `docs/verdict_rules.toml`, and the power simulation script `code/00c_power_simulation.py` with its output `docs/power_simulation.csv`. The commit that contains them is the lock commit.

`docs/analysis_lock_hash.txt` is not a lock file. It records the hashes and cannot contain its own. The lock is defined on `main`, after your review. Lock completion's pull request squash-merges the lock files into the milestone 1 integration branch. When you have reviewed and merged milestone 1 into `main`, its merge commit on `main` is the lock commit, and the integrator tags that commit `analysis-lock-v1`. The first pull request into the milestone 2 integration branch then adds `docs/analysis_lock_hash.txt` with the tag, the lock commit hash on `main` and a SHA-256 of each lock file's contents. Every result and the report cite the tag and the lock commit hash.

`make check-contracts` compares the lock files' contents with the most recent `analysis-lock-*` tag, so an amendment always has a defined reference. Before the first tag exists there is nothing to compare. Between the tag and the hash pull request, the check compares against the tag and reports the missing hash file as pending, not as a failure.

The lock gate passes in four steps, in this order. You review and merge milestone 1 into `main`. The integrator tags the merge commit and creates the milestone 2 integration branch from it. The hash pull request merges into milestone 2. You then decide whether to archive the lock publicly, and the decision is recorded in `docs/analysis_lock_archive.md`, either with the archive record and its DOI or with a statement that the lock remains internal. The decision merges into milestone 2 in its own small pull request. The lock thread owns both files, so the hash pull request and the decision pull request come from branches named `lock/<description>` and pass the ownership check as the lock thread. The lock gate has passed once both are on the milestone 2 integration branch, and only then does primary harmonisation branch.

The blinding is procedural only, and the lock says so in a section on prior knowledge. The original correlations are published, and table 1 of the 2024 technical appendix publishes correlations for 22 countries using recent data. Anyone writing the lock may know these results. The lock lists which published results its author had seen.

A git commit is an internal analysis lock, not a preregistration, even in a public repository, because commits and tags can be rewritten. The documents are called preregistration only if the lock commit is archived before primary harmonisation starts in an immutable public record such as OSF, Zenodo or Software Heritage. Archiving is your decision. Later changes to the lock are dated amendments with a stated reason, and affected results are reported under both the original and the amended rule.

**Harmonisation gate.** Primary harmonisation's validation passes. Every analysis-ready column traces to a raw source variable, a formula, a direction, a missing-data rule, a reference year and a source ID.

**Causal verdict gate.** The causal assessment thread may not change any threshold, criterion or rule in the lock. It computes the evidence for each of the nine criteria of the causal standard, writes it to `outputs/tables/causal_criteria.csv`, and derives every verdict mechanically from that table and `docs/verdict_rules.toml` with `code/06g_apply_verdict_rules.py`. Each verdict row records the hash of `verdict_rules.toml` and the analysis-lock tag. `make check-contracts` recomputes every verdict from the committed criteria table and the locked rules, which needs no data files, and fails if any verdict differs or any hash does not match. The gate passes when this check passes on the milestone 2 integration branch. A deviation from the locked rules is a dated lock amendment, and affected verdicts are reported under both the original and the amended rules.

**Completion gate.** Every criterion in INTENT.md is met and `make clean-env` succeeds.

## Tech stack

The project mixes Python and R. Each language does what it does best, and the boundary between them is files, never in-process calls.

**Python** Handles acquisition, provenance, harmonisation, index construction, the cross-sectional statistics and the contract checks. It uses pandas and pyarrow for data, requests and tenacity for downloads, sdmx1 for OECD SDMX queries, wbgapi for World Bank WDI, openpyxl and xlrd for spreadsheets, country_converter for ISO codes, scipy and statsmodels for correlations, OLS, robust regression, Theil–Sen and influence diagnostics, scikit-learn for the exploratory principal-component index, pandera for schemas and pytest for tests.

**Shared schemas.** Interface-file schemas are written once, in a language-neutral format, as Frictionless Table Schema JSON files in `data/metadata/schemas/`. A helper in `code/lib/` converts each into a pandera schema for Python. A small R validator in `code/lib/`, written in base R with jsonlite, checks the same names, types, required fields and allowed values, and testthat calls it. Neither language defines a schema in code.

**R** Handles the models where its packages are the reference implementations. These are the panel models and event studies with fixest, synthetic control with a package available on conda-forge, the small-cluster inference method the lock selects, the DAG with dagitty, and qualitative comparative analysis with the QCA package if a register row requires re-running Greener's QCA. R code is tested with testthat and linted with lintr.

**The language boundary.** Every script is in one language. Scripts exchange data only through Parquet and CSV files under the paths the contracts define, read with arrow in R and pyarrow in Python. Z-scoring and index construction exist once, in Python, and R reads the computed indices instead of reimplementing them. Where both languages can compute the same statistic, a cross-language test computes the primary OLS and Pearson results in both and fails on any difference beyond numerical tolerance.

**Environment.** Pixi manages one environment for both languages from conda-forge, with PyPI only for packages conda-forge lacks. Its single lockfile, `pixi.lock`, pins every Python and R package for macOS on Apple silicon and for Linux, so local runs and GitHub Actions resolve to the same builds. This was chosen for result quality. A separate Python lock and R lock, such as uv with renv, can drift apart and cannot pin the shared system libraries, while pixi pins the whole stack in one file. `environment.yml` and `requirements.txt`, which the original project specification requires, are exported from pixi. `environment.yml` covers the whole environment, while `requirements.txt` covers only the Python packages installable from PyPI, because R packages from conda-forge cannot appear there. CI fails if either export is out of date for what it covers. R packages that exist only on GitHub are not used, because they cannot be locked.

**Code quality.** Ruff for Python, lintr and styler for R, and pre-commit to run them before every commit.

**Build.** GNU Make remains the entry point, and each target calls `pixi run`. The download helper refuses network access when `OFFLINE=1`, which `make all` sets, so offline replay is enforced in code rather than by convention.

**Report and site.** Quarto renders the report and the results website. The report source is `site/replication_report.qmd`. Quarto renders it both into the site and into `docs/replication_report.md` as GitHub-flavoured Markdown, so the Markdown report is a generated file, never edited by hand. The report and site pages contain Python code chunks only and render through the Jupyter engine. R results reach the report as files that R scripts wrote beforehand, so the language boundary holds and no knitr or reticulate bridge is needed. Every number in the report is computed from the output tables at render time rather than typed in.

**Bibliography tooling.** Crossref for DOIs, PubMed E-utilities for PMIDs, the PMC ID converter for PMCIDs, Unpaywall for legally open full texts and OpenAlex for citation chaining.

## GitHub repository and workflow

The project lives in the public GitHub repository https://github.com/open-reanalysis/how-economic-inequality-harms-societies under the `open-reanalysis` organisation. The site is published at https://open-reanalysis.github.io/how-economic-inequality-harms-societies/. Work reaches `main` through three milestone pull requests, and you review each of them.

| Milestone | Integration branch | Threads | What you review first |
|---|---|---|---|
| 1. Foundations, original reproduction and lock | `milestone/1-lock` | Scaffold, original access, original reproduction, register freeze, inequality data, outcome data, core test data, availability inventory, lock design, lock completion, claims register, analysis types | The lock files, the source hierarchy, the inclusion rules, the analysis-type declaration, the frozen controversy and claims registers, and the original reproduction results with their access label |
| 2. Analysis | `milestone/2-analysis` | Lock hash and archive decision, literature expansion, register test downloads, primary harmonisation, controversy harmonisation, current replication, sensitivity tests, causal assessment, multilevel feasibility | The current replication and sensitivity results, the source-selection log, the specification curve, the controversy tests, and the evidence tier and causal verdict of every outcome with its criteria table |
| 3. Report and publication | `milestone/3-report` | Report | The report and site, before you approve the `results-v1` tag |

Each thread works on a branch named after it, such as `original-access/first-download`, and opens a pull request into its milestone's integration branch when its stage is done. The pull request description is the merge package, using a template that lists every item the merge protocol requires. A thread pull request has no human review. It auto-merges by squash once every required check passes. Your review happens at the milestone pull request, which merges into `main` only when you say so.

The integration branch for milestone 1 is created from `main` when the scaffold thread starts. Each later one is created from `main` right after the previous milestone merges.

`main` is protected by a ruleset. Changes arrive only through pull requests from a `milestone/*` branch, the checks must pass, force pushes are blocked, and only organisation owners may merge. Claude sessions push and open pull requests with your GitHub account, which is an owner, so for them the rule that they never merge into `main` is procedural, written into every brief and into CONTRIBUTING.md. It becomes technical if you give the sessions a separate machine account or GitHub App with write access but no owner role. The `milestone/*` branches are protected too. They accept only pull requests, require the checks and allow auto-merge. The lock commit gets the tag `analysis-lock-v1`, as described under the lock gate, and amendments get `analysis-lock-v1.1` and so on. Tags matching `analysis-lock-*` and `results-*` are protected by a tag ruleset that lets only organisation owners create, move or delete them. Owners are on the ruleset's bypass list, and the integrator creates these tags with an owner account. Workflows cannot create them. Thread pull requests are squash-merged into their integration branch, so each thread stage becomes one commit with a descriptive message. Milestone pull requests are merged into `main` with a merge commit, so those thread commits stay visible in the history of `main`.

**Data are committed to git.** Every acquired data file is committed exactly as acquired, so that `git clone`, `make verify-data` and an offline `make all` reproduce every result that rests on redistributable data. No data package, archive or release asset is needed to reproduce. Restricted or non-redistributable material is the one exception. It is never committed or released, and it gets a manifest row, a retrieval record and an entry in `data/LOCAL_DATA_REQUIRED.md`, with its local path in `.gitignore`.

GitHub warns at 50 MiB and rejects a normal git object above 100 MiB. A data file up to 50 MiB is committed as an ordinary file. A larger one is stored with Git LFS, which on GitHub Free accepts files up to 2 GiB, and its manifest row sets `lfs` to true. A file that cannot go to LFS may be published as a release asset, recorded in the manifest with its SHA-256, size and URL and with `release_asset` set to true. LFS storage and bandwidth count against the organisation's quota, and every CI checkout with LFS objects uses bandwidth, so CI caches LFS objects and data threads prefer documented per-indicator or per-country downloads over bulk archives where the source offers them, which keeps files small. The measured sizes behind these rules are in `outputs/logs/data_size_survey.csv`, produced by `code/measure_data_sizes.py`. On 18 October 2026 the World Bank WDI bulk CSV archive measured 283,089,754 bytes and the WID.world bulk archive 886,945,845 bytes, so either would need LFS if acquired whole.

Documents are kept as GitHub release attachments. Every text whose licence permits redistribution, typically an open-access article under CC BY, is attached to a GitHub release, listed in its source record with SHA-256 and URL, and mirrored on Zenodo, because a release can be deleted. A text whose licence does not permit redistribution, such as the book and most journal articles, is never committed or released. The file that was read is still kept locally, in a gitignored `local/` folder inside its `sources/` folder, with its path in the record. Its record holds the stable identifier, an archived copy of its landing page in the Internet Archive where it has no DOI, and the SHA-256 of the file that was read, so a later reader can confirm they hold the same version. What to do with these local copies later is an open decision for you. Each source also has a bibliographic record a person can open through its link.

Immutability is checked against the base branch. A pull request may add data files but may not modify or delete an existing one. CI compares the checksum of every committed data file with the base branch and fails on any change or deletion. A correction is a new dated file whose manifest row names the file it corrects in `corrects_source_id`, never an overwrite. CI also verifies every committed data file against its manifest checksum and size, and the thread verifies restricted files locally and reports the result in its merge package.

**What CI can and cannot replay.** CI replays every step whose inputs are committed. Steps that need restricted inputs run locally, and their aggregated outputs are committed together with the checksums of the inputs they used. Every result that depends on a restricted input carries the output label `RESTRICTED INPUT` and lists what a person must obtain locally to reproduce it. The report marks which results CI reproduced and which were reproduced locally.

Each thread declares its pipeline steps in its own file `code/pipeline/<thread>.toml`. A step entry names its script, its phase, its input source IDs and derived IDs, and its outputs. The phase is either `acquire`, for steps that download or record assets, or `replay`, for steps that work only from files already present. A small runner in `code/lib/` merges these files into one ordered pipeline and marks a replay step as CI-reproducible when every input traces back, through the manifests, to redistributable acquired assets. Every other replay step is local-only. Acquire steps are never CI-reproducible and never run in replay.

`make replay-ci` runs only the CI-reproducible replay steps. For every local-only step it leaves the committed outputs untouched and checks that the input checksums recorded with those outputs still match the manifest. If they do not match, the outputs are stale and the replay fails. A CI-reproducible step that depends on a local-only output is reported as an error in the pipeline declaration, because it could never be replayed in CI.

## GitHub Actions

`ci.yml` runs on every pull request. It installs the locked environment, runs ruff, lintr, pytest and testthat, checks that the exported environment files match `pixi.lock`, and runs `make check-contracts` in `metadata` mode. For a thread pull request the ownership check reads the thread from the branch name and fails if the pull request changes files outside that thread's owned paths. A milestone pull request has no thread and is validated in milestone mode instead, as described under the merge protocol. A pull request from a fork has no thread branch, so a maintainer gives it a label such as `thread:controversy-register` and the check runs against that thread's paths. Until the label is set, the check stays pending. A fork pull request targets the current integration branch and never auto-merges. A maintainer reviews and merges it, because code from outside the repository should not reach an integration branch without a person reading it. It also builds the Quarto site as a check and uploads it as a workflow artifact without deploying it.

`replay.yml` runs on every push to `main` or to a `milestone/*` branch. It checks out the repository with its LFS objects, runs `make verify-data`, runs `make replay-ci` with `OFFLINE=1` and uploads the outputs as a workflow artifact. It fails if any committed output that CI can reproduce differs from the replayed one.

`acquire.yml` runs only on manual dispatch, for one thread ID given as input. It runs that thread's acquire steps for open sources and opens a pull request from a branch named `<thread-id>/acquire-<date>` into the current integration branch that adds the new data files and manifest rows. The pull request passes the same checks as any thread pull request. Restricted sources are never acquired by a workflow.

`pages.yml` runs only when a tag matching `results-*` is pushed, so unfinished results never appear on the public site. No test deployment exists, and rendering is verified by `ci.yml` without publishing anything. The site is built from the committed outputs. Before rendering, the workflow checks out the data with LFS, runs `make verify-data`, replays the steps CI can reproduce and fails if their outputs differ from the committed ones. The site shows a reproduction-status table, generated from the manifests, that marks each result as reproduced in CI or reproduced locally from non-redistributable inputs.

Third-party actions are pinned to commit hashes, and workflows get the minimum permissions they need.

## Results website

The GitHub Pages site is the public face of the project. It is built entirely from repository outputs and contains the replication report, all figures, every result table as a downloadable CSV, the controversy register with each test result, the evidence tier and causal verdict of every outcome with its criteria table, the power simulation and the negative-control results, the analysis lock with its amendments and tag, the data dictionary, the manifests, the source-verification logs and instructions for reproducing everything. It does not host the data, which are in the repository, and links to them.

Each published version states the release tag, the analysis-lock tag, the commit it was built from and the date. The site uses the neutral terminology of INTENT.md throughout, and every controversy page shows the critic's claim, its source, the test, the result and any published response by Wilkinson and Pickett.

If the repository is connected to Zenodo, every release is archived with a DOI. A release made at the analysis-lock tag then serves as the immutable public record that allows the lock to be called a preregistration.

## Threads

### Scaffold

Runs in this session. Creates the `milestone/1-lock` integration branch and configures the GitHub repository with the rulesets for `main`, `milestone/*` and the protected tags, auto-merge enabled at repository level, the pull request template, the four workflows, the pixi workspace with its lockfile and the exported `environment.yml` and `requirements.txt`, the pre-commit configuration, a minimal Quarto site that `ci.yml` renders but does not deploy, the licence files, the `Makefile` targets described under shared contracts, a `code/lib/` package with shared helpers, the manifest schema, `.gitignore` rules for user-supplied files, `data/LOCAL_DATA_REQUIRED.md` as a template, `LICENSES_AND_ACCESS.md` as a template, the Git LFS configuration and the file size survey. The shared helpers cover recorded downloads, manifest rows, path resolution, country-code mapping, logging, the pipeline runner, and z-scoring and index construction, so every thread computes them the same way. Z-scoring and index construction live in `code/lib/index.py`, which the scaffold thread owns, so original reproduction can use them in wave 1B before primary harmonisation exists. `code/lib/harmonise.py`, owned by the harmonisation thread, contains harmonisation helpers only. The scaffold pull request is the first into `milestone/1-lock`, and its CI runs on that pull request itself. Its squash commit is the base of every other thread branch in milestone 1.

Owns `README.md`, `CONTRIBUTING.md`, `LICENSE`, `LICENSE-docs`, `CITATION.cff`, `LICENSES_AND_ACCESS.md`, `pixi.toml`, `pixi.lock`, `environment.yml`, `requirements.txt`, `Makefile`, `.gitignore`, `.pre-commit-config.yaml`, `.github/`, `_quarto.yml`, `code/lib/` except `code/lib/harmonise.py`, `code/check_contracts.py`, `code/pipeline/scaffold.toml`, `data/metadata/schemas/`, `data/LOCAL_DATA_REQUIRED.md`, `.gitattributes`, `code/measure_data_sizes.py`, `outputs/logs/data_size_survey.csv` and `tests/scaffold/`. Each data thread owns the `.gitattributes` file inside its own raw folder, which marks its LFS files, so no thread edits another's LFS patterns.

This pull request, which adds the planning documents before the scaffold thread, merges directly into `main` because no milestone branch exists yet. It is exempt from the ownership check, which does not exist yet either. It already adds `README.md`, `CONTRIBUTING.md`, the licences and the GitHub templates. The scaffold thread keeps them and changes them only where its own setup requires, for example to add real commands to the README.

After the scaffold thread merges, a thread that needs a change in a file the scaffold thread owns asks for it in its merge package. The integrator makes the change on a branch named `scaffold/<description>`, which the ownership check treats as the scaffold thread, and opens a pull request into the current integration branch, where it auto-merges like any thread pull request. The thread then rebases onto the integration branch.

### Original access and sample recovery

Decides the access gate. Downloads and preserves whatever original material is available without modifying it.

Publishes `outputs/tables/original_sample_recovery.csv` as early as possible. The file contains country membership, outcome availability flags, source references and documented inclusion notes. It contains no outcome values, correlations or figures, because lock completion reads it.

If the package contains U.S. state material, the original access thread records its existence, file names and provenance in the manifest and does nothing else with it.

Records every verified fact about the original study, with the passage, table or file it came from, in its part of the source-verification log.

Owns `data/00_original_released/`, `code/01_ingest_original.py`, `data/metadata/manifests/original-access.csv`, `outputs/tables/original_sample_recovery.csv`, `outputs/diagnostics/original_access_record.md` and `docs/source_verification/original-access.md`.

### Original reproduction

Answers the original reproduction question under the label the access gate assigned. Verifies from the files and the original book's notes the inequality measure and year, the direction of each index component and the handling of missing components. None of these are assumed. Undocumented choices are implemented as labelled alternatives.

Outputs are split into two kinds. Exact reproduction outputs use only the statistic, country cases, transformations and graphic conventions documented in the original study, including the authors' documented composite-index procedure as it actually handled countries with incomplete components. Supplementary diagnostics are labelled as modern additions and never presented as original-study outputs. These are confidence intervals, Spearman correlations, robust methods, influence diagnostics and alternative specifications.

Compares each computed value with the reported one and logs every difference. Records each verified fact about the original method, with the passage, table or file it came from, in its own part of the source-verification log.

The original reproduction thread is the only thread that prepares the original release dataset. `code/01b_prepare_original.py` writes it to `data/03_analysis_ready/original/` and `code/04_reproduce_original.py` analyses it.

Under the status `archived_copy` or `unavailable`, the original reproduction thread rebuilds the original analysis from published tables, the book's notes and independently sourced historical data. Under `incomplete_release` it takes a hybrid path. It uses the released files for everything they contain and reconstructs only the missing sheets, formulas or source notes by the same route. Every value carries a provenance flag, released or reconstructed, and a component-provenance table accompanies every original reproduction output, so the partial-reproduction label shows exactly which parts were reconstructed. `code/01c_download_reconstruction_sources.py` stores that material as downloaded in `data/00_original_reconstruction/`, separate from the original access thread's released files.

Writes a data dictionary and a source-year matrix for the original release dataset and records every raw and derived file it creates in its own manifest.

Owns `code/01b_prepare_original.py`, `code/01c_download_reconstruction_sources.py`, `data/00_original_reconstruction/`, `data/03_analysis_ready/original/`, `data/metadata/manifests/original-reproduction.csv`, `docs/data_dictionary_original.md`, `outputs/tables/original_variable_year_matrix.csv`, `code/04_reproduce_original.py`, `outputs/tables/original_*` except the sample recovery file, `outputs/figures/original_*`, `outputs/diagnostics/original_reproduction_discrepancies.md` and `docs/source_verification/original-reproduction.md`.

### Sources and controversy register

Builds the literature package as records in the five `sources/` folders, one `records.csv` per folder, keeping primary author material, supporting academic work, academic criticism, non-academic criticism and author replies apart. A record holds author, exact title, year, a DOI, PMID, PMCID, ISBN or stable URL, the access date, `open_access` as yes, no or unknown, the licence if known, and `fulltext_asset`, which is empty or names a release asset with its SHA-256. Expands the seed list by backward and forward citation searching.

Writes the controversy register, which holds every named alternative the project tests. A row enters it only with the author's name, exact title, year and a stable DOI, PMID, PMCID, ISBN or URL, checked against PubMed, the DOI record, the publisher page or, for a book, the publisher's or a library's record together with the edition. Each row records `source_role` as critic, original author or independent researcher. The role never decides whether a row is tested. Each row also records `locked_direction`, which states before analysis whether the alternative, if it holds, would weaken or strengthen the original result, so the report can show the balance of the tests. Rows are classified by target, which is data selection, measurement, index construction, robustness, mechanism, causal interpretation or policy inference. Each row names the data the register test data thread must supply and the test that the sensitivity tests or the causal assessment must run, or sets `empirical_test_possible` to `needs_other_design` with the design named, or to `no` with the reason when no empirical design could address it. Wilkinson and Pickett's published responses are linked to the criticisms they answer.

The seed list includes Greener's reproduction and update in the International Journal of Comparative Sociology, DOI 10.1177/00207152241245620, Judge 1995, Gravelle 1998, the population-weighted life-expectancy correlation that the 2024 technical appendix reports as the authors' own robustness test, the Equality Trust author response, Fischer in the Boston Review, Saunders, Snowdon, the TUC summary of criticisms and replies, and the 2024 technical appendix. The controversy register thread records for every entry the exact publication date and whether it is the online-first or the issue date, in `publication_date_type`, and cites it the same way everywhere. Greener's DOI carries a 2024 suffix while the issue is dated 2025, so the distinction matters there.

Full texts are never committed to git. Every text whose licence permits redistribution is attached to a GitHub release and listed in its record. For every other text the file that was read is kept locally in the gitignored `local/` folder of its `sources/` folder, and the record holds its local path, an archived landing-page URL where there is no DOI, and the SHA-256 of the file read. The source-verification log cites the section or page, quotes at most a short phrase, and records which version was read by access date, version or DOI, and file hash.

Extracts from the 2024 technical appendix the passages, table definitions, country list, reference-year statements, index construction and direction coding, and records them in its part of the source-verification log as update-method documentation. This includes the appendix's description of the original timing, its use of the term 80:20 and its use of PISA 2018 instead of PISA 2022. Lock completion uses these only after they are logged. The log covers methods, definitions, samples and years only. It excludes correlation coefficients and other result values, table 1 included, so lock completion does not see current-data results through it. Anyone working on the lock who has seen such values lists them in the lock's prior-knowledge section.

The appendix verification and the register freeze are both prerequisites for the lock, so the controversy register thread does them before expanding the supporting literature.

Owns `sources/`, `code/00_fetch_source_records.py`, `docs/controversy_register.md` and `docs/source_verification/controversy-register.md`.

Runs backward and forward citation searching over the criticism literature and the author replies before the freeze. Expanding the supporting literature can continue afterwards.

The controversy register thread merges twice. The register freeze ends when the register is frozen and the appendix is logged, and its merge unblocks the availability inventory and lock completion. The literature expansion expands the supporting literature and merges separately before the report. Both stages are the same thread. The register freeze targets milestone 1 and the literature expansion targets milestone 2, so the thread rebases onto the milestone 2 integration branch before the literature expansion.

The register freeze is done when the register is frozen by a commit that records the search cut-off date and the search log. Later threads read only a frozen version. A named criticism found after the freeze is added in a dated register amendment and a matching dated lock amendment. Its test is reported separately as a post-lock analysis, and the report states that it was not declared before the data were examined.

### Current inequality data

Downloads raw copies, metadata and codebooks from the OECD Income Distribution Database, the World Bank Poverty and Inequality Platform, UNU-WIDER WIID and WID.world. Records for each measure the income concept, tax and transfer treatment, equivalisation, unit, price basis, survey year, coverage and known series breaks. The OECD database is revised on a rolling basis and served through an SDMX API, so the endpoint, query parameters, response hash and any version identifier are pinned.

Records documented tax-transfer reforms that could serve as events for event studies or synthetic control in `docs/tax_transfer_reforms.csv`. Each row gives the country, the reform, its date, its documented size and a stable source, and is logged in the thread's source-verification log. The file holds no outcome values.

Builds the inequality measure crosswalk in a replay step, `code/02e_build_inequality_crosswalk.py`, from the downloaded files and metadata, so a clean offline run regenerates it. Does not merge inequality with outcomes.

Owns `data/01_raw_current/inequality/`, `code/02a_download_inequality.py`, `code/02e_build_inequality_crosswalk.py`, `data/metadata/manifests/inequality-data.csv`, `outputs/tables/inequality_measure_crosswalk.csv`, `docs/tax_transfer_reforms.csv` and `docs/source_verification/inequality-data.md`.

### Current outcome data

Downloads the ten outcome series with metadata and methodology notes. These cover trust from WVS, EVS and ESS, life expectancy, infant mortality and adolescent births from WDI, WHO and OECD, adult obesity from WHO and OECD, mental illness from GBD and OECD, educational performance from PISA, homicide from UNODC, imprisonment from World Prison Brief and SPACE, and intergenerational mobility from OECD and the World Bank GDIM.

For PISA it records participation status and sampling-standard flags per country and cycle. OECD flagged several countries in PISA 2022 for not meeting sampling standards, and the 2024 update used PISA 2018 for that reason.

Also downloads, as a separate secondary set, the five environmental indicators that the 2024 technical appendix adds to form its fifteen-indicator index, once the controversy register thread has logged their definitions and sources from the appendix. They are kept apart from the ten original outcomes in every file.

Rates comparability per outcome and records the actual reference year for every country-value pair. Downloads the preferred source and the plausible fallbacks for each outcome, so that the hierarchy in the lock can be applied without a second acquisition. Publishes `outputs/tables/outcome_source_coverage.csv`, built by a replay step `code/02f_build_outcome_coverage.py` from the downloaded files and metadata so a clean offline run regenerates it, with source, coverage, years and comparability notes but no outcome values, which lock completion may read. Never inspects any outcome against inequality.

Owns `data/01_raw_current/outcomes/`, `code/02b_download_outcomes.py`, `code/02f_build_outcome_coverage.py`, `data/metadata/manifests/outcome-data.csv` and `outputs/tables/outcome_source_coverage.csv`.

### Core controversy-test data

Downloads the packages that many criticisms share, chosen before the register is frozen. These are country universe and population, OECD membership history, World Bank income classification and GNI, democracy indicators from V-Dem or Freedom House, the OECD Social Expenditure Database, GDP per capita, poverty, unemployment, the Worldwide Governance Indicators, the Quality of Government dataset and health expenditure. Panel versions are pinned the same way as inequality data.

Owns `data/04_controversy_test_data/core/`, `code/02c_download_core_test_data.py` and `data/metadata/manifests/core-test-data.csv`.

### Register-specific test data

Runs in two stages. The availability inventory starts after the register freeze and the analysis-type declaration have merged.

The availability inventory is the stage that the lock depends on. For every covariate and alternative component a register row requires, and for every negative control and every treated or donor country panel that the analysis-type declaration names, it records candidate sources, country and year coverage, licence, redistributability and access route in `outputs/tables/test_data_availability.csv`. Coverage usually needs the data files, and the lock restricts only associations between inequality and outcomes, so the inventory may download covariate values. It computes coverage from non-missing flags only and runs no analysis. The table is built by a replay step, `code/02g_build_test_data_availability.py`, so a clean offline run regenerates it.

The register test downloads run after the inventory merges and download only data that a named register row or a declared causal design requires, such as alternative outcome components proposed by a critic, negative controls, or treated and donor panels around documented reforms, and record the controversy ID or claim ID before each download. Each package gets a README naming the controversy it tests.

Owns `data/04_controversy_test_data/by_controversy/`, `code/02d_download_register_test_data.py`, `code/02g_build_test_data_availability.py`, `outputs/tables/test_data_availability.csv` and `data/metadata/manifests/register-test-data.csv`.

### Lock design

Writes the parts of the analysis plan that need no other thread's output, without reading any outcome values. Fixes the primary inequality measure, the year alignment rule and lag windows, the index formulas and the robustness methods.

Fixes the index direction per measure, not per concept. A measure where a higher value means more of a problem keeps its sign, and every other measure is reversed. For mobility this matters, because an intergenerational elasticity and a mobility index point in opposite directions.

Defines the expanded sample rule with population threshold, income threshold and its source, democracy criterion and the treatment of contested countries including Germany, Israel, Singapore, South Korea and Czechia. Fixes the multiverse dimensions and the reproducibility seed. Every alternative country rule, every multiverse dimension and the panel protocol cites a controversy-register row, a claims-register row or a sensitivity rationale stated in the lock, in line with the sensitivity and causal questions of INTENT.md.

Admits a macro-level covariate only where a named criticism, a cited alternative explanation, a causal claim in the claims register or a stated sensitivity rationale identifies it, and records which one. Whether a covariate model is a sensitivity analysis or part of a causal assessment is declared by the analysis-type thread. A locked covariate for which neither test data thread obtained a usable source is reported as not tested, with the reason, and is never silently dropped from the model.

Fixes the missing-component rule for the index. A mean of the available z-scores is itself a missing-data rule, even though no value is imputed, so the lock states it as one. It fixes the minimum number of components a country needs to receive an index value, reports the number of components behind every country's value, and adds a complete-case index over countries with every component as a declared sensitivity analysis. "No imputation" means that no missing value is filled in. It does not mean that the available-case mean is free of assumptions.

Fixes the reference population for z-scores. By default the components are standardised within each analysed sample, so the index is recomputed for every country rule in the multiverse and for every leave-one-country-out run. Standardising on a fixed reference set, the historical country sample, is a declared sensitivity analysis. The original reproduction thread verifies separately how the original study standardised.

Fixes how the many comparisons are reported. Every specification in the multiverse is reported as a specification curve, with none omitted. Effect sizes with confidence intervals are the primary result. Statistical significance is never used to select which specifications, outcomes or samples are reported. The ten outcomes are always reported together. P-values are shown unadjusted, alongside Holm-adjusted p-values across the ten outcomes as a declared secondary view.

Keeps the ten-indicator index primary. Declares the 2024 update's fifteen-indicator index as a separate extended index, built by the same rule from the ten original indicators and the five environmental ones, and reports the update's further dimensions separately from both. Declares population weighting, which the 2024 appendix reports as the authors' own robustness test, as a named variant for every outcome.

Names every domain index and its component membership. If a component cannot be harmonised, the domain is reported with fewer components and the change appears in the component-availability table.

Fixes the panel protocol. This covers the panel unit, a minimum number of countries and within-country observations per outcome below which no model is fitted, country and year fixed effects, whether country trends enter, the lag structure, serial-correlation handling, the standard-error method for a small number of countries and the missing-data treatment. Whether each panel model is a sensitivity analysis or part of a causal assessment is declared by the analysis-type thread.

Writes `docs/causal_standard.md` and `docs/verdict_rules.toml`. The standard operationalises the nine criteria in INTENT.md with a numerical threshold for each. It includes a table that maps each criterion to the criteria in Pickett and Wilkinson's 2015 causal review, once the claims register thread has logged that review, and adds any criterion of theirs the nine do not cover or explains why not. The standard applies to every outcome series the lock declares, including the population-weighted variants and the extended index. These cover the lag window and how the reverse lag is compared, the compatibility of within-country and cross-sectional estimates, the minimum E-value or an equivalent bound on unmeasured confounding, the negative-control rule, the number and kind of agreeing designs, the dose-response and cross-source consistency test, the mediator test, the rule for when a rival explanation blocks a causal conclusion, and the share of multiverse specifications that must agree. A negative control fails when its estimate falls outside the locked equivalence bounds, not when it reaches a significance threshold, so that significance is never used as a selector. The verdict rules state, in a form code can apply, which combination of criterion results yields each of the four verdicts, the equivalence bounds for not supported, and the rule that an underpowered null is undetermined.

Draws the DAG used for covariate selection, separating possible confounders from possible mediators. The DAG is written in dagitty syntax, and an R script derives the adjustment sets from it so the covariate choice is computed rather than asserted.

Owns the lock files listed under the lock gate except `docs/analysis_types.md`, which the analysis-type thread owns, together with `docs/analysis_lock_hash.txt`, `docs/analysis_lock_archive.md` and `tests/lock/`. The lock files are covered by the content hashes, so a change to any of them after the lock, the DAG and its script included, fails `make check-contracts` unless it comes as a dated amendment with a new tag. The hash file and the archive record are not hashed.

### Lock completion

Starts from the milestone 1 integration branch once its wave-table conditions are met.

Fixes the source hierarchy for every indicator in `docs/source_hierarchy.md`. Each entry names the preferred source, permitted fallbacks, the minimum comparability conditions and the circumstances that justify a fallback. Lock completion may read the outcome data thread's coverage table, the inequality data thread's crosswalk, the controversy register thread's logged appendix passages, the core test data thread's manifest and the register test data thread's availability inventory, but no outcome values.

Reads `original_sample_recovery.csv` and nothing else from the original access and original reproduction threads. Inserts the recovered historical country list and its source reference into `docs/inclusion_rules.md`. Adds the covariates, sample rules and panel tests that named register rows require. It also adds to the DAG the covariates and adjustment sets that the analysis-type thread's causal designs require, and checks that every causal design in `docs/analysis_types.md` names an adjustment set the DAG produces. Adding covariates changes the DAG, so lock completion re-runs `code/00b_dag_adjustment_sets.R` and commits the regenerated `docs/dag_adjustment_sets.csv` before the lock commit. Lists in `docs/causal_standard.md`, after the availability inventory, which designs are feasible for each outcome. Runs the power simulation with `code/00c_power_simulation.py` and commits `docs/power_simulation.csv`, which gives the minimum detectable effect for each outcome and design. The simulation uses the country and year coverage from the coverage tables and the effect sizes and variance assumptions stated in the standard, and reads no outcome values. Writes the prior-knowledge section. Then opens the lock pull request into milestone 1. After you have merged milestone 1 into `main` and the integrator has tagged the merge commit, the thread opens the hash pull request with `docs/analysis_lock_hash.txt` into milestone 2. The thread never creates tags itself. The lock gate passes after your archive decision, as described under the lock gate. Lock completion is a second stage of the same thread, not a separate session. Lock design merges first, and the thread rebases onto the milestone 1 integration branch before starting lock completion.

### Primary harmonisation

Applies the locked rules to the raw inequality and outcome data. Produces `country_year_analysis_panel.parquet`, `cross_section_primary.csv` and the four current datasets, which are the current primary, the current alternative inequality, the current high-comparability core and the current extended index with the five environmental indicators. The original release dataset belongs to the original reproduction thread. Writes the data dictionary, the variable-year matrix, the missingness report and the country sample flow. Uses no data from the core or register test data threads.

Applies the source hierarchy before any join and writes `outputs/tables/source_selection_log.csv`, which records for every indicator the source used, its tier and the lock condition that triggered any fallback. An indicator whose required source is missing and has no permitted fallback is omitted and labelled as not tested.

Records every derived file in its own manifest.

Owns `data/02_harmonised/primary/`, `data/03_analysis_ready/primary/`, `data/metadata/manifests/harmonisation.csv`, `code/03_harmonise.py`, `code/lib/harmonise.py`, `docs/data_dictionary.md`, `outputs/tables/variable_year_matrix.csv`, `outputs/tables/country_sample_flow.csv`, `outputs/tables/source_selection_log.csv` and `outputs/diagnostics/missingness_report.csv`.

Passes the harmonisation gate.

### Controversy harmonisation

Uses the functions in `code/lib/harmonise.py` without modifying them to turn the core and register-specific test data into one analysis file per controversy under `data/03_analysis_ready/controversies/<controversy_id>/`, each with a manifest entry, a data dictionary entry and a source-year matrix. Never modifies the primary harmonisation outputs.

Owns `data/02_harmonised/controversies/`, `data/03_analysis_ready/controversies/`, `data/metadata/manifests/controversy-harmonisation.csv`, `code/03b_harmonise_controversy_data.py` and `docs/data_dictionary_controversies.md`.

### Current replication

Answers the current replication question on the four current datasets from primary harmonisation. The extended index is reported separately from the primary ten-indicator index and never replaces it. Writes only to `outputs/`.

For each dataset and outcome it computes Pearson and Spearman correlations, the OLS slope with 95 percent interval, robust regression, Theil–Sen, the leave-one-country-out range, Cook's distance, leverage and DFBETAs.

The equal-weighted, direction-aligned z-score index is the primary index. The domain indices defined in the lock are secondary.

Every result row carries its dataset version, country sample, outcome-year range, inequality-year range, source IDs, component availability and the analysis-lock commit hash.

Also owns the cross-language test, which computes the primary OLS and Pearson results in both Python and R and fails on any difference beyond numerical tolerance.

Owns `code/05_current_replication.py`, `code/05b_crosscheck.R`, `tests/analysis/`, `outputs/tables/current_replication_results.csv` and `outputs/diagnostics/influence_diagnostics.csv`.

### Sensitivity tests

Answers the sensitivity question for both the original and the current result. It is the second stage of the analysis thread, which rebases onto the milestone 2 integration branch once controversy harmonisation has merged.

A register row whose `claim_or_result_affected` names the original result is tested on the original reproduction thread's original release dataset in `data/03_analysis_ready/original/`. This covers, for example, criticisms of the original country selection or the original index. A row that names the current result is tested on primary harmonisation and controversy harmonisation data, and a row that names both is tested on both. This stage only reads the original reproduction thread's data. The original reproduction thread's own alternative specifications remain labelled diagnostics and are not counted as controversy tests. Writes only to `outputs/`, and every result row carries the same provenance fields as in current replication.

Runs the multiverse over the locked country rules and inequality measures and reports it as the full specification curve the lock defines. A principal-component index is an exploratory sensitivity analysis only. It reports loadings, explained variance, sign choice, country sample and missing-data treatment, and it is never described as a reproduction or used in place of the primary index.

Panel analyses run in a separate module. Before fitting any model, it reports for each outcome the number of countries, years, country-year observations and within-country variation. No model is fitted below the minimum set in the lock. A panel model that the analysis-type thread declared a sensitivity analysis is described as a within-country association. A panel model declared part of a causal assessment is run by the causal assessment thread instead. A model declared as both runs in both threads from the same locked specification.

Each row in the frozen register gets one result, labelled with one of six outcomes. Consistent, partly consistent or inconsistent with the source's stated concern. Indeterminate when coverage, comparability or precision is insufficient to assess it. Needs another design when the register sets `empirical_test_possible` to `needs_other_design`, as with a claim about individuals that country-level data cannot address, and the named design is listed with it. Not testable when the register sets it to `no`. Rows of the last two kinds get no test table. They are listed in a separate table with the reason, and the report discusses them under the matching heading of the terminology in INTENT.md.

If a register row requires re-running Greener's qualitative comparative analysis, it runs in R with the QCA package.

Owns `code/06_robustness_and_controversy_tests.py`, `code/06b_panel_models.R`, `code/06c_qca.R`, `outputs/tables/sensitivity_results.csv`, `outputs/tables/controversy_test_results.csv` and `outputs/tables/controversies_not_testable.csv`.

### Report and clean offline run

Generates all figures and tables from code and builds the Quarto site, including `outputs/tables/all_model_results.csv` as the combination of the original reproduction, current replication, sensitivity and causal assessment results, with a mandatory `result_type` column, writes `site/replication_report.qmd` with the report sections listed under shared contracts and renders it to `docs/replication_report.md`, runs `make clean-env`, and checks the completion criteria, listing anything unmet. When you approve, the report thread tags the release as `results-v1`, which publishes the site.

Owns `code/07_make_tables_figures.py`, `outputs/LICENSE_EXCEPTIONS.md`, `site/` including `site/replication_report.qmd`, the generated `docs/replication_report.md`, `tests/report/`, `outputs/tables/all_model_results.csv`, `outputs/figures/` except files starting with `original_` or `causal_`, and `outputs/logs/` except `outputs/logs/data_size_survey.csv`.

### Author claims register

Builds `docs/claims_register.csv`, which records statements by Wilkinson and Pickett that the project assesses. The sources are *The Spirit Level*, *The Spirit Level at 15* and its technical appendix, Pickett and Wilkinson's "Income inequality and health: a causal review" in Social Science & Medicine 128, 316 to 326, 2015, DOI 10.1016/j.socscimed.2014.12.031, Wilkinson's 2011 TED talk, and the authors' published replies to criticism. The causal review states the authors' own causal argument, so its criteria are logged first, before the lock design maps the causal standard to them. The claims register thread reads them from their publishers or from local copies and adds no files under `sources/`.

Each entry carries the four fields the controversy register requires, which are author, exact work, year and stable identifier, together with the page or chapter. For a book the identifier may be an ISBN, and the edition and year are checked against the publisher's or a library's record. Its wording is a short verbatim quotation or a concise paraphrase marked as such, kept short enough to respect copyright. Each entry is classified as a descriptive correlation, a proposed mechanism or a causal claim, and as testable with country-level data, needing another design with that design named, or not testable. A policy prediction is recorded as a causal claim with a note marking it as a policy prediction, because it asserts that an intervention would change an outcome. It is assessed under the policy-inference rule in INTENT.md, which needs a stated counterfactual, population and effect size beyond a causal verdict.

An entry whose source the claims register thread could not check is kept with `verification_status` set to to_be_verified and is left unclassified. No quotation, page number or identifier is entered without checking it against the source. The register never attributes a causal inference to a correlation they reported without one, nor omits a causal claim they did advance.

The register is frozen by a commit that records its cut-off date before the analysis-type thread starts. A statement added after the freeze goes in a dated amendment, and its assessment is reported as a post-lock analysis.

Owns `docs/claims_register.csv`, `docs/claims_register_method.md` and `docs/source_verification/claims-register.md`.

### Analysis-type declaration

Writes `docs/analysis_types.md`, a lock file that separates causal assessments from sensitivity analyses before any result is examined. Every analysis named in the lock and in the frozen controversy register is listed with its type, which is sensitivity analysis, causal assessment or both. For each causal design it states which criteria of the causal standard the design feeds. It also names the negative-control outcomes and exposures that theory says should be unaffected, and the documented reforms from `docs/tax_transfer_reforms.csv` that any event study or synthetic control uses. A sensitivity analysis tests the robustness of a descriptive correlation and names the controversy-register row or lock rationale behind it. A causal assessment tests a causal claim from the claims register and names the claim ID, the design, the estimand, the identifying assumptions, what the design cannot rule out and the DAG adjustment set it relies on.

Panel models, covariate adjustment such as for poverty, and critic-named alternatives may appear under either type, and the same model may appear twice if it serves both purposes. Lock completion then adds any covariates the causal designs need to the DAG.

Owns `docs/analysis_types.md`.

### Causal assessment

Answers the causal question. Starts from the milestone 2 integration branch once current replication and controversy harmonisation have merged, and writes only to `outputs/`.

Runs every causal design declared in `docs/analysis_types.md` among those the lock lists as feasible for each outcome. These can include lagged and reverse-lagged panel models, first-difference and long-difference models with country and year fixed effects, adjustment by the locked DAG sets with E-values, negative-control tests, event studies and synthetic control around documented reforms, and leave-one-country-out runs. It reports, for each outcome, the evidence for each of the nine criteria in `outputs/tables/causal_criteria.csv`, and the tier and verdict derived from them by the locked rules in `outputs/tables/causal_verdicts.csv`, as described under the causal verdict gate. Every verdict row carries the assumptions sentence, the untestable assumptions, the power result from `docs/power_simulation.csv`, the claim ID it addresses and the same provenance fields as current replication.

A causal claim that the claims register thread marked not testable in this design gets no model and is listed with its reason. The thread may not change any locked threshold or rule.

Owns `code/06d_causal_designs.py`, `code/06e_causal_panel.R`, `code/06f_event_studies.R`, `code/06g_apply_verdict_rules.py`, `outputs/tables/causal_*`, `outputs/figures/causal_*` and `docs/source_verification/causal-assessment.md`.

### Multilevel feasibility

Assesses before the first release whether a multilevel design, with individuals nested in countries, could test the alternatives the register marks as needing another design, such as Gravelle's artefact argument. Starts once the milestone 2 branch exists and runs no analysis of outcomes.

Checks the European Social Survey documentation for a self-rated health item, a household income measure on the same respondent, and the rounds and countries that carry both, and records what it finds in its source-verification log. Notes that the ESS covers European countries only, so it cannot cover the full country sample, and that self-rated health is not the mortality outcome Gravelle analysed, so the test would be partial. Looks for other surveys that would cover the non-European countries.

Writes `docs/multilevel_feasibility.md`, a proposal with the design, the data, the coverage, what it could and could not test, and what it would cost in work. It is a scope proposal, not part of the lock. You decide whether it becomes a dated scope amendment before `results-v1`.

Owns `docs/multilevel_feasibility.md`.

## How the threads run as sessions

The scaffold thread runs here. Every other thread runs as its own Claude session in its own git worktree, branched from its milestone's integration branch when its wave opens. A thread's brief is its section of this plan plus INTENT.md. A thread finishes by pushing its branch, opening a pull request into its integration branch whose description is the merge package described below, and enabling auto-merge. A thread session never merges into `main` and never opens a milestone pull request.

The inequality data, outcome data, core test data and register test data threads mainly download and catalogue and can use a cheaper model. All other threads involve judgement and use the default model. The controversy register thread is among them because its register freeze decides what counts as a valid criticism, and it is on the critical path.

## Merge protocol

**Thread pull requests.** Before a thread pull request can merge into its integration branch, its thread provides in the pull request description the commit hash, the list of changed files, its completion checklist, the manifest validation output, the tests run with exit status, known access failures, licence and redistribution status, and confirmation that it wrote nothing outside its owned files.

`make check-contracts` runs in CI on every pull request and again after every merge. In CI it runs in `metadata` mode and validates file ownership, manifest schemas, source-ID uniqueness, country-code integrity, unchanged manifest rows for raw files, the lock content hashes, that `docs/dag_adjustment_sets.csv` matches a fresh run of its script, and that every verdict in `outputs/tables/causal_verdicts.csv` follows from the committed criteria table and the locked verdict rules. None of these needs data files. Whether the thread's declared commands reproduce its outputs needs data, so the thread checks it locally in `full` mode and reports the result in the merge package, and `make replay-ci` checks it again on the integration branch and on `main` for the CI-reproducible steps. A thread pull request merges automatically once every required check passes. It needs no human approval, and it opens only when the thread's start conditions in the wave table are met.

**Milestone pull requests.** The integrator opens each milestone pull request from its integration branch into `main` once every thread in that milestone has merged. Its description lists the gate files to read first, links every thread pull request with its merge package, and reports the latest replay and contract-check results. You review it and merge it with a merge commit. Nothing else merges into `main`.

**Milestone validation.** A milestone pull request combines many threads, so no single thread's ownership scope applies to it. `make check-contracts` recognises a pull request from a `milestone/*` branch into `main` and runs the ownership part in milestone mode. It lists every commit on the integration branch that is not on `main` and accepts each one only if it is the squash commit of a merged pull request into that integration branch. That pull request must come from a thread branch, a `scaffold/` or `lock/` branch as described above, or a labelled fork pull request. Its ownership check must have passed on its final head commit, its thread must belong to this milestone in the milestone table, and its squash commit must change exactly the files that pull request changed. Any other commit fails the check. This catches a direct push, a change made after a thread's check ran and a merge commit. A merge commit is never needed, because only milestone pull requests reach `main` and each integration branch starts from `main` after the previous milestone has merged. The check also fails if a thread or stage that the milestone table lists has no merged pull request. It reports every constituent pull request with its head commit and check result, and the integrator copies that report into the milestone description. The other contract checks run on the combined tree in `metadata` mode as on any pull request.

Thread pull requests merge in wave order, because each opens only when its conditions are met. A thread with two stages, which applies to the controversy register, register test data, lock and analysis threads, rebases onto its integration branch before its second stage and merges again.

## Steps that need you

Access requirements are verified at run time and recorded per source. Nothing is assumed from earlier descriptions. The WVS site describes the joint EVS and WVS 2017 to 2022 release as free without registration, while the EVS route through GESIS requires sign-in and acceptance of GESIS terms. The access path, licence and version can differ between WVS, EVS and historical trend files. IHME Global Burden of Disease, PISA microdata if published aggregates prove insufficient, WIID and World Prison Brief are also checked at run time.

When a source needs registration or acceptance of terms, the thread stops at the access page, adds an entry to `data/LOCAL_DATA_REQUIRED.md`, and tells you what to download and where to put it. Creating accounts and accepting terms is yours to do.

The licences are decided. Code and tests are under MIT, in `LICENSE`. Documents, the report, the site, figures and result tables are under CC BY 4.0, in `LICENSE-docs`. Each data source keeps its own licence, recorded in its manifest row, and neither repository licence covers raw data or third-party full texts. A derived table or figure that contains values from a source follows that source's terms where they are stricter than CC BY 4.0. Each output's manifest row names the source terms it inherits, the report thread generates `outputs/LICENSE_EXCEPTIONS.md` from those rows, and an output whose source terms forbid publication is not put on the site.

Branch protection does not require an approving review while you are the only human contributor, since GitHub does not let an author approve their own pull request. Your decision to merge a milestone pull request is the human review. Once a second person contributes, one approving review becomes required. Most commits so far are co-authored by an AI model, so a human pass over the gates in this plan before the scaffold thread starts is worth doing.

You check each source's licence where a thread could not establish it, which decides whether its files may be committed. You decide whether to accept Git LFS and its quota for files above 50 MiB, or to require threads to acquire smaller per-indicator files instead. You connect the repository to Zenodo so that tagged releases are mirrored. You decide later what to do with the locally kept copies of texts that may not be redistributed.

You also decide whether to archive the analysis lock publicly, you review and merge the three milestone pull requests, and you approve the `results-*` tag that publishes the site.

## Shared contracts

**One manifest.** Each thread writes only its own file in `data/metadata/manifests/`, and every thread that creates a raw or derived data file has one. `make manifests` merges them deterministically into `data/metadata/all_assets_manifest.csv` and writes filtered views named `original_release_manifest.csv`, `inequality_manifest.csv`, `outcome_manifest.csv`, `controversy_test_manifest.csv` and `derived_manifest.csv`. Sources are not in the data manifests. Their records live in `sources/`. Validation runs in one of three modes, chosen by where it runs.

Every row carries `acquisition_status`. `acquired` means the file was obtained and must exist with a matching checksum. `user_supplied` means you obtained a restricted file by hand, and it is treated like `acquired` once present. `awaiting_user` means the source needs registration or acceptance of terms and is listed in `data/LOCAL_DATA_REQUIRED.md`. `access_failed` records an attempt that did not produce a usable file, with the retrieval record that shows why. `not_downloaded_restricted` records a source catalogued for metadata only. Only `acquired` and `user_supplied` rows require a file and a checksum. The other statuses require their retrieval record or listing instead, and a validation mode never treats them as missing files.

- **metadata** runs in CI on every pull request. It validates schemas, source-ID uniqueness, cross-references, and that no existing raw or acquired row's checksum, path or retrieval record has changed. Derived rows are never edited either. A regenerated derived file, after a bug fix or a lock amendment, gets a new versioned `derived_id`, and the old row is kept with `superseded_by` pointing to it. It touches no data files.
- **available** runs in CI replay and in `make verify-data`. It does everything `metadata` does, then verifies every committed data file against its manifest checksum and size, LFS files included. Restricted rows are listed as skipped, never as passed.
- **full** runs locally before a thread opens its pull request. It does everything `available` does and additionally requires every restricted `acquired` and `user_supplied` file held locally, and fails on any missing file or hash mismatch. It lists `awaiting_user` rows so the gap stays visible. The thread reports the `full` result in its merge package.

`make manifests` and `make check-contracts` take the mode as a parameter and default to `full` locally.

**Manifest fields.** Every row carries the columns listed for its asset type at the end of this section. Every row also carries the common columns `source_id`, `local_path`, `sha256`, `size_bytes`, `licence`, `redistributable`, `source_url`, `retrieval_date` as a UTC timestamp, `acquisition_status`, `lfs`, `release_asset`, `release_asset_url` and `corrects_source_id`. `redistributable` is set from the source's terms and decides whether the file may be committed. Every API, rolling database or periodically revised file also carries `retrieval_method`, `api_endpoint_or_landing_page`, `request_parameters`, `dataset_version`, `release_date`, `last_modified_header`, `etag`, `content_length_bytes`, `mime_type`, `archive_url`, `raw_file_sha256` and `code_version`. A dataset with no formal version gets `dataset_version` set to `unversioned` and keeps its raw response, retrieval timestamp and hash.

**Licensing.** Redistributable data files are committed. Restricted datasets, credentials and registration-protected files are never committed or released. Full texts are never committed to git, and only those whose licence permits redistribution are attached to a release. For restricted material the repository holds the manifest row, the retrieval record, retrieval instructions, the expected checksum once you have supplied the file locally, and a `.gitignore` rule for its path. `data/LOCAL_DATA_REQUIRED.md` lists every user-supplied file with its expected path, required version, acquisition page, acceptance steps and checksum verification.

**Data immutability.** Raw files are never edited. The raw folders are `data/00_original_released/`, `data/00_original_reconstruction/`, `data/01_raw_current/` and `data/04_controversy_test_data/`. The raw folders hold the committed data files themselves. Only the acquisition script that owns a raw folder may add files to it, and it never overwrites or deletes an existing file, which CI enforces against the base branch. No script numbered 04 or higher may write to any raw folder, `data/02_harmonised/` or `data/03_analysis_ready/`. Analysis scripts write only to `outputs/` and to gitignored temporary folders. Any derived dataset comes from a numbered harmonisation script with a manifest row, a data dictionary entry and a source-year matrix.

**Build modes.** `make acquire` is the only target that uses the network. It runs only steps whose phase is `acquire`, downloads, verifies and records assets, and its new files reach the repository through a pull request. `make verify-data` checks every committed data file against the manifest in `available` mode. `make all` runs every step whose phase is `replay`, fully offline. A step whose restricted input is missing locally is not run. Its committed outputs are kept after their recorded input checksums are checked, they carry `RESTRICTED INPUT`, and `make all` lists what to obtain. `make replay-ci` runs only the CI-reproducible replay steps and fails if any committed output they produce differs. Neither `make all` nor `make replay-ci` ever runs an acquire step. Every table an acquisition thread publishes in `outputs/` is built by a replay step from committed data and metadata, never by the download script itself, so emptying `outputs/` loses nothing that replay cannot rebuild. `make clean-env` makes a fresh clone in a temporary folder, installs the environment from `pixi.lock`, runs `make verify-data`, and runs `make all` with `OFFLINE=1`. `make check-contracts` runs the merge checks.

**Source-verification log.** Each thread that verifies a fact writes only its own file in `docs/source_verification/`. A fact is usable in a rule only once it is logged with the passage, table or file it was verified from.

**Source IDs.** Prefixed by the thread ID, for example `original-access-001`, `inequality-data-oecd-idd-gini` or `outcome-data-wdi-sp.dyn.le00.in`. IDs never change once written.

**Country codes.** ISO 3166-1 alpha-3 throughout. Name variants map through one table in `code/lib/`.

**Controversy IDs.** The category ID listed at the end of this section followed by a number, for example `inequality-measure-002`. The controversy register thread assigns them.

**Code ownership.** An owned script path covers that script in either language. Each thread also owns `code/pipeline/<thread>.toml` for its pipeline steps and `tests/<thread>/` for its pytest and testthat tests. This applies to every thread, whether or not its own section repeats these paths, and the ownership check derives them from the thread ID. Shared test utilities live in `tests/scaffold/` and change only through the integrator.

**Criticisms of the general hypothesis.** Some named criticisms predate *The Spirit Level* or address the income inequality and health hypothesis in general rather than the book's analyses. Judge 1995 and Gravelle 1998 are examples. Such a row has `target_level` set to `general_hypothesis`, while other rows use `original`, `current` or `both`. Its `mapping_rationale` states which book or current result the criticism bears on and why, and its `claim_or_result_affected` names that result. A general criticism whose testable implication requires individual-level data is classified as needing another design, with that design named. Gravelle's artefact argument, which concerns a concave individual relationship between income and health, is an example. The named design is a multilevel analysis with income and a health measure from the same respondent, and the country-level test can only be partial. The register says both.

**Result rows.** Every result row carries `input_access`, which is `RESTRICTED INPUT` when any input is restricted and empty otherwise, with the restricted source IDs listed. Every result row in every output table carries `evidence_tier`, from 1 for a descriptive association to 4 for a causal conclusion, assigned per outcome and per design as INTENT.md defines. Original reproduction outputs are tier 1. Only `outputs/tables/causal_verdicts.csv` may carry tier 4.

**Paths in code.** Relative to the project root, resolved through one helper in `code/lib/`.

**Original release manifest columns.** The common columns, plus `title`, `organisation`, `publication_or_access_date`, `file_format` and `notes`.

**Outcome manifest columns.** The common columns, plus `outcome`, `source_organisation`, `dataset_title`, `indicator_code`, `indicator_definition`, `unit`, `population`, `geography`, `reference_year`, `publication_or_release_year`, `comparability_rating`, `transformation_needed` and `notes`. The inequality and controversy-test manifests use the same columns, with `outcome` holding the measure or variable name.

**Derived data manifest columns.** `derived_id`, `local_path`, `sha256`, `created_utc`, `producing_script`, `code_version` as the git tree hash of `code/` together with the blob hash of the producing script, `base_commit` as the integration-branch commit the run started from, `input_source_ids`, `input_sha256s`, `transformation_summary`, `data_dictionary_ref`, `source_year_matrix_ref`, `analysis_lock_hash`, which is empty for the original reproduction thread's original release dataset, `superseded_by` and `notes`. A tree hash is the same before and after a squash merge and a milestone merge when the code is unchanged, so it identifies the code even though the thread's branch commit disappears. The same two fields identify code in every result row. `make manifests` fails if any input ID is missing from the manifest, if an input hash does not match, or if the data dictionary or source-year matrix reference does not resolve.

**Source record columns.** `citation_key`, `authors`, `year`, `title`, `edition`, `journal_or_publisher`, `doi`, `pmid`, `pmcid`, `isbn`, `stable_url`, `access_date`, `open_access` as yes, no or unknown, `licence`, `fulltext_asset`, `fulltext_asset_sha256`, `read_file_sha256`, `local_path`, `archive_url`, `source_type`, `peer_review_status`, `research_design`, `geography`, `outcome`, `inequality_measure`, `main_finding_verbatim_short`, `methodological_limitations_verbatim_short` and `notes`. Quoted fields stay short enough to respect copyright.

**Controversy register columns.** `controversy_id`, `claim_or_result_affected`, `target_level`, `mapping_rationale`, `source_role` as critic, original_author or independent, `locked_direction` as weakens_original, strengthens_original or neutral, `critic_name` holding the source's author, `source_title`, `publication_year`, `publication_date_type`, `source_type`, `peer_review_status`, `exact_controversy_in_neutral_words`, `critic_argument_summary`, `data_or_method_the_critic_targets`, `empirical_test_possible`, `test_plan`, `wilkinson_pickett_response_available`, `response_source_id`, `local_path`, `citation_url` and `notes`.

**Claims register columns.** `claim_id`, `author`, `source_work`, `source_locator` as page or chapter, `publication_year`, `stable_identifier`, `wording`, `wording_type` as verbatim or paraphrase, `claim_class` as descriptive_correlation, proposed_mechanism or causal_claim, `testability` as testable_country_level, needs_other_design or not_testable, `verification_status` as verified or to_be_verified, `verification_log_ref` and `notes`. Claim IDs are `claim-` followed by a number, for example `claim-007`. `claim_class` and `testability` stay empty while `verification_status` is to_be_verified.

**Controversy categories.** `country-selection` covers country selection and sample definition. `inequality-measure` covers the inequality measure, including the 80:20 ratio against Gini, market against disposable income, and survey comparability and timing. `index-construction` covers composite-index construction, including weighting, component choice and reverse coding. `outliers` covers outliers and influential countries. `temporal-persistence` covers persistence in later data and in national time series. `mechanism` covers the psychosocial account and alternatives such as material conditions, public services, institutions and social cohesion. `data-comparability` covers data availability and comparability.

**Report sections.** The report has these sections in this order. Scope and terminology. Original analysis. Current update. Findings. Controversies, which opens with a table of how many tests had each `locked_direction` and each `source_role`, and where each entry states the source's claim, cites it, describes the test, shows the result, names its category and links any published Wilkinson and Pickett response. Causal assessment, which leads each outcome with its evidence tier and verdict, then shows the evidence for each criterion of the causal standard, the designs used, the power result and the negative controls, then states the assumptions sentence and what the designs cannot rule out. Each causal claim names its source and class, or the reason it is not testable in this design. Limitations, covering the small country sample, cross-national comparability, temporal misalignment, missing data, measurement changes, dependence among outcomes and the limits of observational designs. Reproducibility, with exact commands, environment versions, checksums and data-access limits.
