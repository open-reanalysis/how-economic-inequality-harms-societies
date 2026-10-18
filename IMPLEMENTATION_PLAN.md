# Implementation plan

This plan turns [INTENT.md](INTENT.md) into work that separate Claude sessions can run in parallel. Each session is called a thread here. A thread owns a fixed set of files, works on its own branch, and hands over through the shared contracts at the end of this document. No two threads write the same file.

## Goals and priorities

The project has six goals, in this order of priority. They come from the original project specification.

| Priority | Goal | Threads | Output path | Acceptance test | Blocking dependencies | Milestone | Human decision |
|---|---|---|---|---|---|---|---|
| 1 | Download the current version of every dataset Wilkinson and Pickett used | Original access, source lineage, inequality data, outcome data | `data/00_original_released/`, `docs/source_lineage.csv`, `data/01_raw_current/` | Every original variable has a lineage row with a comparability class, every row not marked `NO_CURRENT_EQUIVALENT` or `NOT_YET_VERIFIED` has its current file with a matching manifest hash, and a `NOT_YET_VERIFIED` row passes only with a logged verification attempt and its reason | Scaffold | 1 | Accept the CDC WONDER terms of use |
| 2 | Reproduce their findings | Historical reproduction, reproduction lock, updated reproduction | `outputs/tables/historical_*`, `outputs/tables/updated_reproduction_*`, with their discrepancy logs | The historical reproduction and the fixed-sample current reproduction exist for every dataset whose inputs are available, every deviation from the reported values is logged with a cause, and every current result cites the reproduction lock commit | Goal 1 | 1 and 2 | None |
| 3 | Download a package of sources supporting their findings, academic and non-academic | Original access for the authors' own works, supporting sources for the rest | `sources/supporting/` | The package has at least one peer-reviewed study by other authors, every record follows the screening protocol, and every legally obtainable text is downloaded or has a recorded reason | Scaffold | 2 | None |
| 4 | Download a package of sources setting out controversies about their findings | Controversy sources and register | `sources/controversies/`, `docs/controversy_register.csv` | Every register row has an identifiable source, its argument in neutral words, its target and any reply, and every legally obtainable text is downloaded or has a recorded reason | Scaffold | 2 | None |
| 5 | Download datasets that may support those controversies | Controversy test data | `data/04_controversy_test_data/`, `docs/controversy_data_map.csv` | Every register row with a testable statement has a map row whose datasets are acquired with provenance, or whose barrier is documented | Goal 4 register freeze | 2 | None |
| 6 | Publish the results on a GitHub Pages site | Report | `site/`, `.github/workflows/pages.yml` | The `results-v1` tag publishes the report with the headline table and links to the `deliverables-v1` release and the repository | Goals 1 to 5 | 3 | Approve the `results-v1` tag |

The same table is kept in machine-readable form in `docs/goal_traceability.csv`. `make check-contracts` fails if any goal lacks a thread, an output path, an acceptance test or a milestone, if an output path is not owned by one of the goal's threads, or if a goal in milestone 1 or 2 depends on a thread outside milestones 1 and 2.

The project keeps one addition beyond the goals. The author claims register records and classifies what Wilkinson and Pickett claim. It never delays a goal.

Milestone 2 ends with an independent release of goals 1 to 5, tagged `deliverables-v1`. It holds those five deliverables and is complete even if the report and the website are not yet built. Milestone 3 delivers goal 6, the site that publishes the results.

Milestone 1 holds only the path to goals 1 and 2, so nothing from goals 3 to 5 gates the reproductions. The threads for goals 3 to 5 may start as soon as the scaffold has merged and merge into `main` whenever their work is done, but only milestone 2 requires them. The claims register may start at the same time. It is an addition and never gates a tag, and the report publishes it as it stands.

The book itself is not used. The project relies on what the authors and the Equality Trust published about the book's data and methods, as described under the original access thread. Where that material leaves a point of the original method open, the historical reproduction thread proposes a choice with its reasons, you agree it, and it is recorded in the original method specification, `docs/original_method_spec.md`.

The original material contains an analysis of the U.S. states, as the notes on sources and methods show. That analysis is part of goals 1 and 2. It is a second dataset for the same hypothesis, reproduced from the released data and updated wherever a current release of the same series exists. It is always reported separately from the country analysis and never pooled with it.

The project runs no analysis beyond the two reproductions. It does not test the controversies and does not assess causality. The controversy register and the claims register document the debate, and the controversy test data make later tests possible.

## Execution order

The implementation runs in one day, 19 October 2026. No step waits for material that cannot be obtained that day. Work runs in waves. A thread starts only when every gate it depends on has passed.

| Wave | Thread | Starts when | Milestone |
|---|---|---|---|
| 0 | Scaffold | Now | 1 |
| 1A | Original access | Scaffold merged | 1 |
| 1A | Supporting sources, controversy sources and register | Scaffold merged. They work alongside milestone 1 | 2 |
| 1A | Claims register | Scaffold merged. It never gates a tag | None |
| 1B | Source lineage, historical reproduction | Original access merged | 1 |
| 1C | Inequality data, outcome data | Source lineage merged | 1 |
| 1D | Reproduction lock | Historical reproduction, inequality data and outcome data merged | 1 |
| 1E | Reproduction lock gate | Milestone 1 reviewed and tagged | 1 to 2 |
| 2A | Updated reproduction | Reproduction lock gate passed | 2 |
| 2B | Controversy test data | Frozen controversy register merged | 2 |
| 3 | Report | `deliverables-v1` tagged | 3 |

Each thread has a name used in prose and an ID used by tools. The ID names the thread's branches, its Make file, its test folder, its manifest and its source-verification log, and it prefixes its source IDs. Wave numbers and milestone numbers stay numeric because they give the order of execution. The wave says when a thread starts, and the milestone says which tag requires it.

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

A thread reads another thread's output only from `main` after that thread has merged into it. No thread reads from an unmerged thread branch.

## Gates

**Access gate.** The original access thread assigns one of four access statuses, and the status fixes the label that every historical reproduction output carries.

| Status | Definition | Label on outputs |
|---|---|---|
| `verified_release` | Files download and hash, contain usable original data, and carry enough documentation to identify variables and country cases. | `DIRECT REPRODUCTION` |
| `incomplete_release` | Some files download, but required sheets, metadata, source notes or formulas are missing. | `PARTIAL REPRODUCTION` |
| `archived_copy` | A credible archive or third party supplies historical files, but provenance to the original release cannot be fully verified. | `ARCHIVE-BASED RECONSTRUCTION` |
| `unavailable` | No usable original package is accessible. | `INDEPENDENT RECONSTRUCTION` |

For every retrieval attempt the original access thread records the HTTP status, redirect chain, response headers where available, UTC timestamp, SHA-256, file size, MIME type and whether the file is machine-readable. A 2017 Equality Trust post says the data could be downloaded. That establishes nothing about today, so the gate is decided only by these records.

**Reproduction lock gate.** The reproduction lock thread commits `docs/reproduction_lock.md` before any thread computes, views or infers an association between current inequality data and current outcome data. The lock fixes, for current data, only what the original method leaves open. It names the series for each indicator from `docs/source_lineage.csv` and the successor rule where a series has ended. It fixes the reference years and the lag that keep the original timing. The fixed sample is the 23 countries in the released international data. The refreshed sample is the result of the country eligibility rule under shared contracts, applied to the declared current data, and the lock freezes it together with its open choices. For the U.S. states the lock fixes the state series, reference years and state inclusion rule in the same way. It also fixes the original index procedure, measure, statistic and graphic conventions, as the original method specification states them. It also fixes the definition of each reproduction result described under updated reproduction. Anything the original study did not document is fixed as the one choice the specification records. Downloading data, reading metadata and checking country coverage before the lock are allowed.

The lock is a file merged into `main`. The reproduction lock pull request merges `docs/reproduction_lock.md`, and the commit that merges it is the lock commit. Updated reproduction starts only after you have reviewed milestone 1 and the integrator has tagged it, so you see the lock before any current association is computed. Every current result and the report cite the lock commit hash. Historical results do not, because the lock does not cover them. A later change to the lock is a dated amendment in the same file, and affected results are reported under both versions.

The blinding is procedural only, and the lock says so. The original correlations are published, and so are the 2024 update's correlations for 22 countries using recent data. The lock lists which of them its author had seen.

**Completion gate.** Every criterion in INTENT.md is met and `make clean-env` succeeds.

## Tech stack

**Python** handles acquisition, provenance, preparation, index construction, the reproduction statistics and the contract checks. It uses pandas and pyarrow for data, requests and tenacity for downloads, sdmx1 for OECD SDMX queries, wbgapi for World Bank WDI, openpyxl and xlrd for spreadsheets, country_converter for ISO codes, scipy for correlations, pandera for schemas and pytest for tests. The project needs no second language. Another language is added only when a method needs a reference implementation that Python lacks, and the pull request that adds it says why.

**Shared schemas.** Every interface file has one pandera schema, defined once in `code/lib/schemas.py`. Scripts that write or read the file validate it against that schema, and no other copy of a schema exists.

**Environment.** Pixi manages the environment from conda-forge, with PyPI only for packages conda-forge lacks. Its single lockfile, `pixi.lock`, pins every package for macOS on Apple silicon and for Linux, so local runs and GitHub Actions resolve to the same builds. `environment.yml` and `requirements.txt`, which the original project specification requires, are exported from pixi, and CI fails if either is out of date.

**Code quality.** Ruff, run by pre-commit before every commit.

**Build.** GNU Make remains the entry point, and each target calls `pixi run`. The download helper refuses network access when `OFFLINE=1`, which `make all` sets, so offline replay is enforced in code rather than by convention.

**Report and site.** A Python script, `code/07_build_report.py`, writes the report as Markdown. It takes the prose from the report thread's section files and inserts every table, figure and number from the output tables, so no number is typed in by hand. It writes `docs/replication_report.md`, which is never edited by hand, and the same page as `site/index.md`, and it copies the figures the report uses into `site/`. GitHub Pages publishes `site/` with its standard Markdown build, so the project needs no site generator of its own.

**Bibliography tooling.** Crossref for DOIs, PubMed E-utilities for PMIDs, the PMC ID converter for PMCIDs, Unpaywall for legally open full texts and OpenAlex for citation chaining.

## GitHub repository and workflow

The project lives in the public GitHub repository https://github.com/open-reanalysis/how-economic-inequality-harms-societies under the `open-reanalysis` organisation. The site is published at https://open-reanalysis.github.io/how-economic-inequality-harms-societies/. Thread pull requests merge directly into `main`. Three milestones mark the points where you review what has merged, and each ends in a tag.

| Milestone | Tag | Threads | What you review first |
|---|---|---|---|
| 1. Data and historical reproduction | `milestone-1` | Scaffold, original access, source lineage, historical reproduction, inequality data, outcome data, reproduction lock | The source lineage, the authors' own works in `sources/supporting/original-authors/`, the historical reproduction results with their access label, and the reproduction lock |
| 2. Updated reproduction and source packages | `deliverables-v1` | Updated reproduction, supporting sources, controversy sources and register, controversy test data | The updated reproduction results with their discrepancy log, the two source packages with their READMEs, the frozen controversy register and the controversy test data |
| 3. Report and publication | `results-v1` | Report | The report and the site |

Each thread works on a branch named after it, such as `original-access/first-download`, branched from `main`, and opens a pull request into `main` when its work is done. The pull request description is the merge package, using a template that lists every item the merge protocol requires. A thread pull request has no human review. It auto-merges with a merge commit once every required check passes, and it opens only when the thread's start conditions in the wave table are met.

When every thread a milestone lists has merged, the integrator tells you, and you review `main` as it stands. When you approve, the integrator tags that commit with the milestone's tag. Updated reproduction does not start before the `milestone-1` tag, and the report thread does not start before `deliverables-v1`.

`main` is protected by a ruleset. Changes arrive only through pull requests, the checks must pass, force pushes are blocked, and auto-merge is allowed. Tags matching `milestone-*`, `deliverables-*` and `results-*` are protected by a tag ruleset that lets only organisation owners create, move or delete them. Owners are on the ruleset's bypass list, and the integrator creates these tags with an owner account after your approval. Workflows cannot create them. Every pull request is merged with a merge commit, so every commit stays in the history of `main` exactly as it was made. History is never rewritten. Squash, rebase, amend and force push follow the rule in CONTRIBUTING.md, which allows squash or rebase only with its own stated reason and its own permission from a maintainer.

**Data storage serves the deliverables.** For each source the thread acquires the smallest official, legally redistributable input that holds every observation and all the metadata the deliverable needs, not a whole database because it is available. Bulk archives, such as the complete World Bank WDI or WID.world downloads, are never acquired. The thread extracts the relevant series through the provider's API or its per-indicator download and stores that extract. The thread chooses one storage method per source and records it in the manifest's `storage_method`.

- `git`. An ordinary committed file, for files up to 50 MiB.
- `api_extract`. A reproducible extract from an official API, with the exact request and the SHA-256 of the response. The response itself is stored with `git`, so the extract is never fetched again from the live API.
- `user_supplied`. A restricted file you obtain by hand, kept locally and listed in the owning thread's file in `data/local_data_required/`, with its local path in the `.gitignore` of its raw folder.

Every stored data file is in git and arrives with a clone, and its hash is checked against the manifest. User-supplied files are placed by you. A clone and the documented verification procedure therefore rebuild every package. Restricted or non-redistributable material is never committed or released.

GitHub warns at 50 MiB and rejects a normal git object above 100 MiB. Git LFS on GitHub Free accepts files up to 2 GiB, but its storage and bandwidth count against the organisation's quota, so the project does not use LFS. An extract above 50 MiB is split, for example by indicator or country, so every stored file stays within 50 MiB. On 18 October 2026 the World Bank WDI bulk CSV archive measured 283,089,754 bytes and the WID.world bulk archive 886,945,845 bytes. Neither is needed, because only the relevant series are extracted from them.

Documents are downloaded as part of the source packages of goals 3 and 4. Every text in either package that can be obtained legally is downloaded, whether or not anyone has read it yet. Every text whose terms allow publishing, typically an open-access article under CC BY, is committed to its package folder in the repository and listed in its source record with SHA-256 and URL. A text whose terms do not allow publishing, such as the book and most journal articles, is never committed or released. It is recorded as a source with its link, and the downloaded file is kept locally, in a gitignored `local/` folder inside its `sources/` folder, with its path in the record. Its record holds the stable identifier, an archived copy of its landing page in the Internet Archive where it has no DOI, and the SHA-256 of the downloaded file, so a later reader can confirm they hold the same version. Each source also has a bibliographic record a person can open through its link.

Immutability is checked against the base branch. A pull request may add data files but may not modify or delete an existing one, with one exception. A file that contains credentials or personal data, breaks a licence, is subject to a takedown request or is malicious is removed at once in a pull request that a maintainer approves. The removal and its reason are recorded in `docs/removals.md`, and the manifest row is kept with `acquisition_status` set to `removed`. CI fails if a pull request changes or deletes an existing data file or an existing manifest row, which git shows without reading the files. A correction is a new dated file whose manifest row names the file it corrects in `corrects_source_id`, never an overwrite. Every stored file is checked against its manifest checksum and size locally in `full` mode, and the thread reports the result in its merge package.

**Replay.** Results are replayed locally with `make all`. A step that needs a restricted input runs only where that input is held, and its aggregated outputs are committed together with the checksums of the inputs they used. Every result that depends on a restricted input carries the output label `RESTRICTED INPUT` and lists what a person must obtain locally to reproduce it.

Each thread declares its steps as Make targets in its own file `make/<thread>.mk`, which the main `Makefile` includes. Every output file is a target whose prerequisites are its script and its input files. The thread adds each target to `ACQUIRE_TARGETS` if it downloads or records assets, or to `REPLAY_TARGETS` if it works only from files already present. `make acquire` builds the acquire targets and `make all` the replay targets, so Make runs the steps in dependency order without a runner of the project's own.

Make builds every prerequisite a target needs, whichever list the target is in, so the lists alone cannot keep a step out of a replay. Two rules do that. First, every acquire rule sits in a block of `make/<thread>.mk` that is read only when `MODE=acquire`, and `make all` sets `MODE=replay`. A replay therefore has no recipe that downloads, and an acquired file is an ordinary existing file to Make. Second, a replay target that needs a restricted input is listed in `RESTRICTED_TARGETS`, and its real rule is defined only when that input is present locally. When the input is missing, the target gets a stand-in rule with no prerequisites. Its recipe checks the input checksums recorded with the committed outputs, marks them `RESTRICTED INPUT` and lists what to obtain. A downstream target such as the report always finds a rule that needs neither the missing input nor the network. `make check-contracts` runs `make -n all` without the restricted inputs and fails if any acquire recipe or real restricted recipe would run.

Make decides what is stale by file timestamps, which a fresh clone does not preserve, so a clean replay builds every replay target unconditionally, and data integrity is checked by hashes in `make verify-data`.

## GitHub Actions

The repository has one workflow until milestone 3. `ci.yml` runs on every pull request and on every push to `main`, so the contract checks also run after every merge. It installs the locked environment, runs ruff and pytest, checks that the exported environment files match `pixi.lock`, and runs `make check-contracts` in `metadata` mode. On a push there is no pull request, so `make check-contracts` skips the ownership check there and runs the other `metadata` checks on the pushed tree. The ownership check reads the thread from the branch name and fails if the pull request changes files outside that thread's owned paths. Pull requests from forks are not merged. A person outside the project proposes a change in an issue, and a thread or the integrator makes it.

In milestone 3 the report thread adds `pages.yml`. It runs only when a tag matching `results-*` is pushed, so unfinished results never appear on the public site. It publishes the committed `site/` folder to GitHub Pages.

Third-party actions are pinned to commit hashes, and workflows get the minimum permissions they need.

## Deliverables release

When you have approved milestone 2, the integrator tags that commit of `main` `deliverables-v1` and publishes a GitHub release from it. Its notes are generated from the acceptance tests of goals 1 to 5 and the package READMEs and list every lineage row still marked not yet verified with its reason. It needs no data assets, because every stored file is in the repository. This release completes goals 1 to 5. If the repository is connected to Zenodo, every release is archived with a DOI.

## Results website

The GitHub Pages site is the rendered report, with links to the `deliverables-v1` release and to the repository. Everything else, the data, the registers, the source packages and the logs, is reached through those links. Each published version states the release tag, the reproduction lock commit, the commit it was built from and the date.

## Threads

### Scaffold

Runs in this session. Configures the GitHub repository with the rulesets for `main` and the protected tags, auto-merge enabled at repository level, the pull request template, the `ci.yml` workflow, the pixi workspace with its lockfile and the exported `environment.yml` and `requirements.txt`, the pre-commit configuration, the licence files, the `Makefile` targets described under shared contracts, a `code/lib/` package with shared helpers, the manifest schema, `.gitignore` rules for user-supplied files, a template for the per-thread files in `data/local_data_required/`. The shared helpers cover recorded downloads, manifest rows, path resolution, country-code mapping, logging, and z-scoring and index construction, so every thread computes them the same way. Z-scoring and index construction live in `code/lib/index.py`. The scaffold pull request is the first thread pull request into `main`, and its CI runs on that pull request itself.

Owns `README.md`, `CONTRIBUTING.md`, `LICENSE`, `LICENSE-docs`, `CITATION.cff`, `pixi.toml`, `pixi.lock`, `environment.yml`, `requirements.txt`, `Makefile`, `.gitignore`, `.pre-commit-config.yaml`, `.github/` except `.github/workflows/pages.yml`, `code/lib/`, `code/check_contracts.py`, `make/scaffold.mk`, `docs/goal_traceability.csv`, `docs/removals.md`, `.gitattributes` and `tests/scaffold/`. Each data thread owns the `.gitattributes` and `.gitignore` files inside its own raw folder, which mark the paths of its user-supplied files, so no thread edits another's patterns. The root `.gitignore` holds only general rules, such as every `local/` folder and the temporary folders.

This pull request, which adds the planning documents before the scaffold thread, is exempt from the ownership check, which does not exist yet either. It already adds `README.md`, `CONTRIBUTING.md`, the licences, the GitHub templates and the folder skeleton. The scaffold thread keeps them and changes them only where its own setup requires, for example to add real commands to the README.

After the scaffold thread merges, a thread that needs a change in a file the scaffold thread owns asks for it in its merge package. The integrator makes the change on a branch named `scaffold/<description>`, which the ownership check treats as the scaffold thread, and opens a pull request into `main`, where it auto-merges like any thread pull request. The thread then merges `main` into its own branch.

### Original access and sample recovery

Serves goals 1 and 2. Decides the access gate. Downloads and preserves whatever original material is available without modifying it.

Also obtains the authors' own works that milestone 1 depends on, because source lineage, historical reproduction and the reproduction lock read them. These are *The Spirit Level at 15* with its technical appendix, Pickett and Wilkinson's "Income inequality and health: a causal review", DOI 10.1016/j.socscimed.2014.12.031, and the Equality Trust's published material on the book. They form `sources/supporting/original-authors/`, with its `records.csv`, which is the first part of the goal 3 package. *The Spirit Level* itself, Allen Lane 2009, ISBN 978-1-84614-039-6, is not used. It gets a record marked not obtained, and the material below stands in for it.

*The Spirit Level at 15*, DOI 10.15124/yao-de9s-7k93, is copyright of the Equality Trust and the authors. Its terms allow free use for research with full acknowledgement but require permission for re-use in other publications, so under the licensing rule it is handled locally and recorded as a source with its link. The copy you supplied on 18 October 2026 has SHA-256 `c14eb8832b6aea4f7d02817e535125a7a34f0e630a271238db73175febdb2aea` and 39 pages. Its figures carry no correlation coefficients, which are in the technical appendix.

The stand-in material is the following, each kept with its URL, its Internet Archive copy where the live page is not reachable, the access date and its SHA-256.

- **The released international data.** `international-inequality.xls`, from the Equality Trust's data page. It holds the 23 countries, the inequality measure, the ten index components, the index and further measures, with a sheet of sources and a sheet of errata. A copy downloaded on 18 October 2026 has SHA-256 `1897f2bbe503d35df3aea5f3d25a1b719660e1f4761f5913464b6a3b35c6c661`. The file was last saved in 2011 and its errata say some series were revised after the book, so it may not be identical to the data behind the book.
- **The notes on statistical sources and methods.** The Equality Trust page "Notes on Statistical Sources and Methods", read through its Internet Archive copy of 7 January 2017. It gives the inequality measure, the source and year of every index component for the countries and the U.S. states, how the index was built, which countries lack which components, and the correlation and p-value the book reported for each measure.
- **The authors' answers to questions.** The Equality Trust's frequently asked questions on *The Spirit Level* and the authors' 2010 responses to their critics.

The released U.S. state data could not be downloaded, because the archived page's download button has no link. A request to the Equality Trust cannot be answered within the one-day run, so the historical reproduction thread rebuilds the state data from the original sources, as described under that thread. The released file is listed in `data/local_data_required/original-access.md` as a later addition.

Where the data file's sources sheet and the notes page disagree, both are logged, and the values are compared and combined under the rule for parallel data in the shared contracts. Three such disagreements are already known: infant mortality is World Bank 2000 in the notes and OECD 2005 in the file, homicides are a rate per 100,000 for 1990 to 2000 in the notes and per million for 1999 to 2000 in the file, and the education score is PISA 2000 in the notes and PISA 2003 in the file. The access gate takes these into account.

Extracts from the technical appendix only what it says about the original method, its description of the original timing and its use of the term 80:20, and records them in its source-verification log. Nothing else from the appendix is used, because the project does not compare its results with the 2024 update.

Publishes `outputs/tables/original_sample_recovery.csv` as early as possible. The file contains country membership, outcome availability flags, source references and documented inclusion notes. It contains no outcome values, correlations or figures, because the reproduction lock thread reads it.

Preserves any U.S. state material in the original package like every other file and records in `original_sample_recovery.csv` which states and outcomes it covers, so that historical reproduction and source lineage can treat it as a second dataset.

Records every verified fact about the original study, with the passage, table or file it came from, in its part of the source-verification log.

Owns `data/00_original_released/`, `sources/supporting/original-authors/`, `code/01_ingest_original.py`, `data/metadata/manifests/original-access.csv`, `outputs/tables/original_sample_recovery.csv`, `outputs/diagnostics/original_access_record.md` and `docs/source_verification/original-access.md`.

### Source lineage

Serves goal 1. Starts once original access has merged, so it can read the released data. Builds `docs/source_lineage.csv`, which records for each of the ten indicators, for the inequality measure and for any U.S. state series the source Wilkinson and Pickett actually used. It also names the gross national income per capita and population series that the country eligibility rule needs, in the original vintage and the current release. Each row takes the source from the released data file's sources sheet and from the Equality Trust's notes on sources and methods, never from a later summary. Where the two disagree, the data file comes first, because it describes the values in the file, and both are recorded. A row that the available material cannot settle is settled in the original method specification. It records the original series and its years, and the newest release of that same series. Where the series has ended or changed definition, it names the closest successor and the reason. Each row gets one comparability class:

- `EXACT_SUCCESSOR`. The same series from the same provider, with the same definition, unit and population.
- `CONCEPTUAL_SUCCESSOR`. A series that measures the same concept for the same population, but whose provider, survey or method has changed, such as the American Community Survey replacing the census income question.
- `SUBSTITUTE`. A different measure of a related concept, such as self-reported obesity in place of obesity corrected for self-report bias, or a Gini coefficient in place of an income ratio.
- `NO_CURRENT_EQUIVALENT`. No current series measures the concept for the original units.
- `NOT_YET_VERIFIED`. The original source or the current series has not been confirmed.

The inequality and outcome data threads download only what this table names, so "the data Wilkinson used" never becomes "comparable data" without a recorded reason.

Each row carries a verification status and a log reference. A row whose original source could not be confirmed is marked to be verified, and its current series is not chosen until it is confirmed. Reads the original material and the stand-in sources, and reads no outcome values.

Owns `docs/source_lineage.csv` and `docs/source_verification/source-lineage.md`.

### Historical reproduction

Serves goal 2. Answers the historical reproduction question under the label the access gate assigned. Verifies from the released files and the notes on sources and methods the inequality measure and year, the direction of each index component and the handling of missing components. None of these are assumed. Writes the original method specification, `docs/original_method_spec.md`, which states the sample, the eligibility rule, every measure and year, the direction coding, the handling of missing components, the index construction and the rule for combining parallel data, each with its source or, where the material leaves it open, the choice agreed with you. You approve it in the milestone 1 review. Checks the country eligibility rule under shared contracts against the released 23 countries. It applies the rule to the World Bank data vintage the authors used, if that vintage can be obtained from the World Bank's archives and stored in `data/00_original_reconstruction/`, writes the outcome to `outputs/tables/historical_country_eligibility.csv`, and logs every country the rule and the released data disagree on. If the vintage cannot be obtained, it records why, and the check is not made. Undocumented choices are settled in the original method specification.

Outputs use only the statistic, country cases, transformations and graphic conventions documented in the original study, including the authors' documented composite-index procedure as it actually handled countries with incomplete components. The project adds no statistics of its own.

Compares each computed value with the one reported in the notes on sources and methods, which lists the correlation and p-value of every measure, and logs every difference. Records each verified fact about the original method, with the passage, table or file it came from, in its own part of the source-verification log.

The historical reproduction thread is the only thread that prepares the original release dataset. `code/01b_prepare_original.py` writes it to `data/03_analysis_ready/original/` and `code/04_reproduce_original.py` analyses it.

Under the status `archived_copy` or `unavailable`, the historical reproduction thread rebuilds the original analysis from published tables, the notes on sources and methods and independently sourced historical data. Under `incomplete_release` it takes a hybrid path. It uses the released files for everything they contain and reconstructs only the missing sheets, formulas or source notes by the same route. Every value carries a provenance flag, released or reconstructed, and a component-provenance table accompanies every historical reproduction output, so the partial-reproduction label shows exactly which parts were reconstructed. `code/01c_download_reconstruction_sources.py` stores that material as downloaded in `data/00_original_reconstruction/`, separate from the original access thread's released files.

Reproduces the U.S. state analysis as a separate dataset with its own outputs, following the U.S. state data model under shared contracts. The released U.S. file is not available in the one-day run, so the thread rebuilds the state data from the historical sources listed there into `data/00_original_reconstruction/us_states/`, with every value flagged as reconstructed. The rebuild is accepted when its correlations match the ones the notes on sources and methods report, such as r = 0.59 for the index, within a tolerance that the thread records in its source-verification log before it computes any state correlation. Every mismatch is logged with its likely cause. When the released file arrives, it replaces the rebuild, and the two are compared.

Writes a data dictionary and a source-year matrix for the original release dataset and records every raw and derived file it creates in its own manifests.

Owns `code/01b_prepare_original.py`, `code/01c_download_reconstruction_sources.py`, `data/00_original_reconstruction/`, `data/03_analysis_ready/original/`, `data/metadata/manifests/historical-reproduction.csv`, `docs/data_dictionary_original.md`, `docs/original_method_spec.md`, `outputs/tables/historical_variable_year_matrix.csv`, `code/04_reproduce_original.py`, `outputs/tables/historical_*`, `outputs/figures/historical_*`, `outputs/diagnostics/historical_reproduction_discrepancies.md` and `docs/source_verification/historical-reproduction.md`.

### Current inequality data

Serves goal 1. Downloads the current release of the inequality series that `docs/source_lineage.csv` names, and the named successor where a series has ended, including any U.S. state series. Also downloads the current gross national income per capita and population series that the country eligibility rule needs, as source lineage names them. Downloads nothing else. Records for each series the income concept, tax and transfer treatment, equivalisation, unit, price basis, survey year, coverage and known series breaks. A source revised on a rolling basis or served through an API, such as the OECD database through SDMX, has its endpoint, query parameters, response hash and any version identifier pinned. Does not merge inequality with outcomes.

Owns `data/01_raw_current/inequality/`, `code/02a_download_inequality.py`, `data/metadata/manifests/inequality-data.csv` and `docs/source_verification/inequality-data.md`.

### Current outcome data

Serves goal 1. Downloads the current release of each outcome series that `docs/source_lineage.csv` names, and the named successor where a series has ended, including any U.S. state series, with metadata and methodology notes. Downloads nothing else.

For PISA it records participation status and sampling-standard flags per country and cycle. OECD flagged several countries in PISA 2022 for not meeting sampling standards. Source lineage decides which cycle is the current release of the original series.

Records the actual reference year for every country-value pair and the comparability of each series with the original. Publishes `outputs/tables/outcome_source_coverage.csv`, built by a replay step `code/02f_build_outcome_coverage.py` from the downloaded files and metadata so a clean offline run regenerates it, with source, coverage, years and comparability notes but no outcome values, which the reproduction lock thread may read. Never inspects any outcome against inequality.

Owns `data/01_raw_current/outcomes/`, `code/02b_download_outcomes.py`, `code/02f_build_outcome_coverage.py`, `data/metadata/manifests/outcome-data.csv` and `outputs/tables/outcome_source_coverage.csv`.

### Reproduction lock

Serves goal 2. Writes `docs/reproduction_lock.md` once historical reproduction, inequality data and outcome data have merged, as described under the reproduction lock gate. Reads the historical reproduction thread's verified method, the source lineage, `original_sample_recovery.csv` and the coverage table, and reads no current outcome values. Writes the prior-knowledge section.

Builds the refreshed sample with `code/03a_country_eligibility.py`, which applies the country eligibility rule to the current income, population and inequality files and writes `outputs/tables/refreshed_country_eligibility.csv`. The script reads no outcome file. The lock cites the table and its hash.

Owns `docs/reproduction_lock.md`, `code/03a_country_eligibility.py`, `outputs/tables/refreshed_country_eligibility.csv` and `tests/reproduction-lock/`.

### Updated reproduction

Serves goal 2. Applies the original method, as fixed in the reproduction lock, unchanged to the current release of the same data, with the same inequality measure, the same index procedure and the same statistic and graphic conventions. Goal 2 keeps its results separate, so a changed sample is never presented as a data update.

- **Historical reproduction.** The original data, sample and method. The historical reproduction thread produces it, labelled with the access status.
- **Fixed-sample current reproduction.** Current releases of the variables for the verified historical sample, with the original method unchanged and only unavoidable missing-data deviations. This thread produces it as `UPDATED REPRODUCTION, FIXED SAMPLE`. It is the project's answer to whether the findings hold in current data.
- **Eligibility-refreshed current reproduction.** Current releases for the refreshed sample that the reproduction lock froze, with the original method unchanged. This thread produces it as `UPDATED REPRODUCTION, ELIGIBILITY REFRESHED`. If source lineage finds no exact or conceptual successor for the original inequality measure, the rule's third condition cannot be applied, and the result is reported as not possible with that reason. For the U.S. states the rule is all 50 states, so the result equals the fixed-sample one and is reported once with that note.

Any expanded sample, changed outcome, changed inequality measure or changed model is a modern extension, not a reproduction, and is outside this project.

The fixed-sample and eligibility-refreshed results use only series whose lineage class is `EXACT_SUCCESSOR` or `CONCEPTUAL_SUCCESSOR`. A component whose only current series is a `SUBSTITUTE` is left out of the strict result and treated like a missing component under the original index rule, and the omission is logged. A further result for the fixed sample, labelled `UPDATED REPRODUCTION, FIXED SAMPLE, WITH SUBSTITUTES`, adds the substitute series, so the effect of each substitution is visible. A component with `NO_CURRENT_EQUIVALENT` is left out of both. A substitute never replaces the original measure in the strict result.

Prepares its analysis file with `code/03c_prepare_updated_reproduction.py` into `data/03_analysis_ready/updated_reproduction/`, using the shared index helpers in `code/lib/index.py`. Analyses it with `code/05c_updated_reproduction.py`. Writes the results, each with the provenance fields every result row carries and the reproduction lock commit, and a discrepancy log that compares each value with the one the authors reported. Like historical reproduction it adds no statistics of its own. Reproduces the U.S. state analysis the same way where source lineage found a current release of its series.

Owns `code/03c_prepare_updated_reproduction.py`, `code/05c_updated_reproduction.py`, `data/03_analysis_ready/updated_reproduction/`, `data/metadata/manifests/updated-reproduction.csv`, `docs/data_dictionary_updated_reproduction.md`, `outputs/tables/updated_reproduction_*`, `outputs/figures/updated_reproduction_*`, `outputs/diagnostics/updated_reproduction_discrepancies.md` and `docs/source_verification/updated-reproduction.md`.

### Supporting sources

Serves goal 3. Builds the rest of the package of sources supporting Wilkinson and Pickett's findings in `sources/supporting/academic/` and `sources/supporting/non-academic/`, and the package's `manifest.csv`, `README.md` and `screening_log.csv`. The authors' own works are already in `sources/supporting/original-authors/`, from the original access thread. The supporting folders hold independent academic studies and non-academic material, such as policy reports and Equality Trust publications, that support the findings. Searches and screens under the shared protocol in the shared contracts, so the standard is the same as for the controversy package. The package is not complete without at least one peer-reviewed study by authors other than Wilkinson and Pickett.

Downloads every text in the package that can be obtained legally, as described under the repository workflow. Each subfolder has a `records.csv`. The package `README.md`, generated from the manifest, counts the texts published in the repository, the texts kept locally and the records without a text, with the reason for each record without one.

Owns `sources/supporting/` except `sources/supporting/original-authors/`, `code/00_fetch_supporting_sources.py` and `docs/source_verification/supporting-sources.md`.

### Controversy sources and register

Serves goal 4. Builds the package of sources setting out controversies in `sources/controversies/academic/`, `sources/controversies/non-academic/` and `sources/controversies/responses/`, with a `records.csv` in each subfolder and the package's `manifest.csv`, `README.md` and `screening_log.csv`, as for the supporting package. The responses folder holds the replies by Wilkinson and Pickett and the relevant independent responses. Downloads every text in the package that can be obtained legally. Searches and screens under the shared protocol.

Writes the controversy register, which holds every named controversy about Wilkinson and Pickett's findings. A row enters it only with the author's name, exact title, year and a stable DOI, PMID, PMCID, ISBN or URL, checked against PubMed, the DOI record, the publisher page or, for a book, the publisher's or a library's record together with the edition. Each row records `source_role` as critic or independent researcher. Each row belongs to one of the controversy categories in the shared contracts, which is the prefix of its controversy ID. The data that would support or test a controversy are recorded in the controversy data map, which the controversy test data thread builds. The project does not run any tests. Wilkinson and Pickett's published responses are linked to the criticisms they answer.

Each row also records the testable statement, or that it has none. The seed list includes Greener's reproduction and update in the International Journal of Comparative Sociology, DOI 10.1177/00207152241245620, Judge 1995, Gravelle 1998, the Equality Trust author response, Fischer in the Boston Review, Saunders's "Beware False Prophets" for Policy Exchange, Snowdon's *The Spirit Level Delusion*, Sanandaji, Malm and Sanandaji's "The Spirit Illusion" for the Taxpayers' Alliance, Sanandaji and others in the Wall Street Journal in 2010, Goldthorpe's "Analysing Social Inequality" in the European Sociological Review 2010, DOI 10.1093/esr/jcp046, Rowlingson's 2011 review for the Joseph Rowntree Foundation, Nettle's 2017 essay on the psychosocial account, and the TUC summary of criticisms and replies. The replies folder holds the authors' 2010 responses to Snowdon, the Taxpayers' Alliance and Policy Exchange, Hugh Noble's "The Spirit Level Revisited" and the authors' response to the Rowntree review. Wikipedia's article on the book served only as a pointer to these and is not cited. The thread records for every entry the exact publication date and whether it is the online-first or the issue date, in `publication_date_type`, and cites it the same way everywhere. Greener's DOI carries a 2024 suffix while the issue is dated 2025, so the distinction matters there.

Only texts whose terms allow publishing are committed, as the licensing rule under shared contracts says. The source-verification log cites the section or page, quotes at most a short phrase, and records which version was read by access date, version or DOI, and file hash.

The register is frozen by a commit that records the search cut-off date and the search log, and the frozen register merges first so that the controversy test data thread can start. The rest of the package may follow in a second pull request, after the thread merges `main` into its own branch. Later threads read only a frozen version. A named criticism found after the freeze is added in a dated register amendment, and its data are downloaded as a dated addition.

Owns `sources/controversies/`, `code/00_fetch_controversy_sources.py`, `docs/controversy_register.csv` and `docs/source_verification/controversy-register.md`.

### Controversy test data

Serves goal 5. Starts once the frozen controversy register has merged. Writes `docs/controversy_data_map.csv`, with one row for every register row that has a testable statement, using the columns in the shared contracts. For every dataset a map row names, the map records candidate sources, country and year coverage, licence, redistributability and access route, and the thread downloads the data. A dataset that several rows need, such as GDP per capita, poverty or social expenditure, is downloaded once into `data/04_controversy_test_data/shared/` and linked to every row that needs it. Every other package goes into `data/04_controversy_test_data/by_controversy/<controversy_id>/`. No package is downloaded without at least one `controversy_id`, and each package has a README naming the controversies it serves. Downloading needs no lock, because the lock restricts only associations between inequality and outcomes. Coverage is taken from the downloaded files' non-missing flags only, and no analysis is run. A dataset that cannot be obtained gets the specific access, licence or availability barrier in its map row. The datasets may turn out to support the criticism, weaken it, support the original finding or leave the question open, and the map describes them in those neutral terms.

Owns `data/04_controversy_test_data/`, `docs/controversy_data_map.csv`, `code/02d_download_controversy_test_data.py` and `data/metadata/manifests/controversy-test-data.csv`.

### Author claims register

Builds `docs/claims_register.csv`, which records and classifies statements by Wilkinson and Pickett. The claims are taken as stated in the authors' own published material on the Equality Trust site, with the page's URL or archived copy as the locator. A book page that such a page cites, such as page 80 in the answer on medical spending, is recorded as cited by that page, not as checked. The sources are the Equality Trust's notes on sources and methods, its frequently asked questions and the authors' 2010 responses, *The Spirit Level at 15* and its technical appendix, Pickett and Wilkinson's "Income inequality and health: a causal review" in Social Science & Medicine 128, 316 to 326, 2015, DOI 10.1016/j.socscimed.2014.12.031, Wilkinson's 2011 TED talk, and the authors' published replies to criticism. The thread reads them from their publishers or from local copies and adds no files under `sources/`.

Each entry carries the four fields the controversy register requires, which are author, exact work, year and stable identifier, together with the page or chapter. For a book the identifier may be an ISBN, and the edition and year are checked against the publisher's or a library's record. For a web page the identifier is its URL with an Internet Archive copy. Its wording is a short verbatim quotation or a concise paraphrase marked as such, kept short enough to respect copyright. Each entry is classified as a descriptive correlation, a proposed mechanism, a causal claim or a policy prediction. The classification is documentation. The project does not test the claims.

An entry whose source the thread could not check is kept with `verification_status` set to to_be_verified and is left unclassified. No quotation, page number or identifier is entered without checking it against the source. The register never attributes a causal inference to a correlation the authors reported without one, nor omits a causal claim they did advance.

The register is frozen by a commit that records its cut-off date. A statement added after the freeze goes in a dated amendment.

Owns `docs/claims_register.csv`, `docs/claims_register_method.md` and `docs/source_verification/claims-register.md`.

### Report and clean offline run

Builds `outputs/tables/headline_results.csv`, the project's one headline table, from the historical and updated reproduction tables. It has one row per indicator and dataset, with the reported r, the historical r and n, the updated r and n, the comparability class and the deviation reason. Writes the prose of the report sections listed under shared contracts in `report/`, and `code/07_build_report.py` assembles the report from them and the output tables, as described under the tech stack. Runs `make clean-env` and checks the completion criteria, listing anything unmet and reporting each of the six goals first. When you approve, the integrator tags the release as `results-v1` with an owner account, which publishes the site.

Adds `pages.yml`, so the site exists only from milestone 3. Owns `code/07_build_report.py`, `report/`, `.github/workflows/pages.yml`, `site/`, the generated `docs/replication_report.md`, `tests/report/`, `outputs/tables/headline_results.csv`, `outputs/figures/` except files starting with `historical_` or `updated_reproduction_`, and `outputs/logs/`.

## How the threads run as sessions

The integrator is a separate Claude session. It creates the milestone tags after your approval, makes the changes to files the scaffold thread owns, and runs `make clean-env` before `deliverables-v1`. Whether the integrator later becomes an automated LLM agent is left for consideration.

The scaffold thread runs here. Every other thread runs as its own Claude session in its own git worktree, branched from `main` when its wave opens. A thread's brief is its section of this plan plus INTENT.md. A thread finishes by pushing its branch, opening a pull request into `main` whose description is the merge package described below, and enabling auto-merge. A thread session never creates a tag.

The inequality data, outcome data and controversy test data threads mainly download and catalogue and can use a cheaper model. All other threads involve judgement and use the default model. The two source-package threads are among them because they decide what counts as supporting evidence and as a valid criticism, and source lineage because it decides which series the authors used.

## Merge protocol

Before a thread pull request can merge into `main`, its thread provides in the pull request description the commit hash, the list of changed files, its completion checklist, the manifest validation output, the tests run with exit status, known access failures, licence and redistribution status, and confirmation that it wrote nothing outside its owned files.

`make check-contracts` runs in CI on every pull request and again after every merge. In CI it runs in `metadata` mode and validates file ownership on pull requests, manifest schemas, source-ID uniqueness, country-code integrity, unchanged manifest rows for raw files, and that every controversy test data package links to a register row. None of these needs data files. Whether the thread's declared commands reproduce its outputs needs data, so the thread checks it locally in `full` mode and reports the result in the merge package. A thread pull request merges automatically once every required check passes. It needs no human approval, and it opens only when the thread's start conditions in the wave table are met.

**Milestone review.** When every thread a milestone lists has merged, the integrator sends you the files to read first, links every thread pull request with its merge package, and reports the latest contract-check results and the local `full` replay result. Before the `deliverables-v1` tag the integrator also runs `make clean-env`, which fetches and verifies the stored data and replays every result offline from a fresh clone, and reports its result. The report thread runs it again before `results-v1`. You review `main` at that commit. When you approve, the integrator tags it, and the tag message lists the thread pull requests it covers.

## Steps that need you

Access requirements are verified at run time and recorded per source. Nothing is assumed from earlier descriptions. The WVS site describes the joint EVS and WVS 2017 to 2022 release as free without registration, while the EVS route through GESIS requires sign-in and acceptance of GESIS terms. The access path, licence and version can differ between WVS, EVS and historical trend files. Every other source that the source lineage or the controversy data map names is checked at run time in the same way, including the General Social Survey's restricted state identifiers.

When a source needs registration or acceptance of terms, the thread stops at the access page, adds an entry to its own file in `data/local_data_required/`, and tells you what to download and where to put it. Creating accounts and accepting terms is yours to do.

The licences are decided. Code and tests are under MIT, in `LICENSE`. Documents, the report, the site, figures and the project's own data collection are under CC BY 4.0, in `LICENSE-docs`. Data and texts obtained elsewhere keep their own terms, recorded in their manifest rows or source records, and neither repository licence covers them. What may be committed is decided by the licensing rule under shared contracts.

Branch protection does not require an approving review while you are the only human contributor, since GitHub does not let an author approve their own pull request. Your milestone review is the human review. Once a second person contributes, one approving review becomes required. Most commits so far are co-authored by an AI model, so a human pass over the gates in this plan before the scaffold thread starts is worth doing.

You check each source's licence where a thread could not establish it, which decides whether its files may be committed. Git LFS is not used. Connecting the repository to Zenodo is left for later. You accept the CDC WONDER terms of use. Obtaining the released U.S. state data from the Equality Trust is a later addition. The book is not used. You agree the open points of the original method specification with the historical reproduction thread and approve the specification in the milestone 1 review. The copyright holder of *The Spirit Level at 15* asks that research use be registered with the Equality Trust for impact assessment, and whether to do so is your decision.

You also review the three milestones and approve their tags, `milestone-1`, `deliverables-v1` and `results-v1`, the last of which publishes the site.

## Shared contracts

**Two manifests.** Each thread writes only its own files in `data/metadata/manifests/`, `<thread>.csv` for the data files it acquires and `<thread>-derived.csv` for the data files it derives. `make manifests` merges them deterministically into `data/metadata/manifest.csv` and `data/metadata/derived_manifest.csv`. Sources are not in the data manifests. Their records live in `sources/`. Validation runs in one of two modes, chosen by where it runs.

Every row carries `acquisition_status`. `acquired` means the file was obtained and must exist with a matching checksum. `user_supplied` means you obtained a restricted file by hand, and it is treated like `acquired` once present. `awaiting_user` means the source needs registration or acceptance of terms and is listed in the owning thread's file in `data/local_data_required/`. `access_failed` records an attempt that did not produce a usable file, with the retrieval record that shows why. `not_downloaded_restricted` records a source catalogued for metadata only. `removed` records a file taken out under the exception to immutability. Only `acquired` and `user_supplied` rows require a file and a checksum. The other statuses require their retrieval record or listing instead, and a validation mode never treats them as missing files.

- **metadata** runs in CI on every pull request. It validates schemas, source-ID uniqueness, cross-references, and that no existing raw or acquired row's checksum, path or retrieval record has changed. Derived rows are never edited either. A regenerated derived file, after a bug fix or a lock amendment, gets a new versioned `derived_id`, and the old row is kept with `superseded_by` pointing to it. It touches no data files.
- **full** runs locally, before a thread opens its pull request and in `make verify-data`. It does everything `metadata` does, then verifies every stored data file against its manifest checksum and size. It fails on a hash mismatch or a missing redistributable file. A restricted `acquired` or `user_supplied` file that is not held locally is listed, not failed, so results that need it carry `RESTRICTED INPUT`, and a thread that owns such a file must hold it before opening its pull request. It lists `awaiting_user` rows so the gap stays visible. The thread reports the `full` result in its merge package.

`make manifests` and `make check-contracts` take the mode as a parameter and default to `full` locally.

**Manifest columns.** `source_id`, `request` as the download URL or the exact API query, `retrieval_date` as a UTC timestamp, `dataset_version`, `sha256`, `size_bytes`, `licence`, `redistributable`, `storage_method`, `acquisition_status`, `local_path`, `corrects_source_id` and `notes`. `redistributable` is set from the source's terms and decides whether the file may be committed. A dataset with no formal version gets `dataset_version` set to `unversioned`. What each series measures, its unit and its years are recorded in the source lineage, not in the manifest.

**Licensing.** Three rules decide what the repository publishes.

1. Material whose terms allow publishing, data files and texts alike, is published in the repository as it was obtained, under its own terms, by the storage method recorded for each source.
2. Material whose terms do not allow publishing is handled locally and never committed or released. The repository records it as a source with its link. Data may be extracted from it as long as the extract stays below the threshold of originality, such as individual values and facts, and never a copied table layout, text or figure. No substantial part of a database is taken either. The project does not copy a database whole or in large part, but builds its own collection from the values each analysis needs. An output that would cross either limit stays in the gitignored `outputs/local/` folder.
3. The project's own data collection is published under CC BY 4.0. It is assembled from such extracts and from values the project derives, and it covers `data/03_analysis_ready/` and the tables in `outputs/tables/`. Every extracted value names its source through the derived manifest. Data fetched from elsewhere are published as they are, under their own terms, and are never relicensed.

Credentials and registration-protected files are never committed or released. For restricted material the repository holds the manifest row, the retrieval record, retrieval instructions, the expected checksum once you have supplied the file locally, and a rule for its path in the `.gitignore` of its raw folder. The owning thread's file in `data/local_data_required/` lists every user-supplied file with its expected path, required version, acquisition page, acceptance steps and checksum verification.

**Data immutability.** Raw files are never edited. The raw folders are `data/00_original_released/`, `data/00_original_reconstruction/`, `data/01_raw_current/` and `data/04_controversy_test_data/`. The raw folders hold the data files themselves, whether committed or placed by you. Only the acquisition script that owns a raw folder may add files to it, and it never overwrites or deletes an existing file, which CI enforces against the base branch, except under the removal exception above. No script numbered 04 or higher may write to any raw folder or to `data/03_analysis_ready/`. Analysis scripts write only to `outputs/` and to gitignored temporary folders. Any derived dataset comes from a numbered preparation script with a derived manifest row and a data dictionary entry.

**Build modes.** `make acquire` is the only target that contacts live sources. It builds only the targets in `ACQUIRE_TARGETS`, downloads, verifies and records assets, and its new files reach the repository through a pull request. `make verify-data` checks every stored data file against the manifest in `full` mode. `make all` builds every target in `REPLAY_TARGETS`, fully offline. A step whose restricted input is missing locally is not run. Its committed outputs are kept after their recorded input checksums are checked, they carry `RESTRICTED INPUT`, and `make all` lists what to obtain. `make all` never runs an acquire step. Every table an acquisition thread publishes in `outputs/` is built by a replay step from stored data and metadata, never by the download script itself, so emptying `outputs/` loses nothing that replay cannot rebuild, apart from the locally kept files in `outputs/local/`. `make clean-env` makes a fresh clone in a temporary folder, installs the environment from `pixi.lock`, runs `make verify-data`, and runs `make all` with `OFFLINE=1`. `make check-contracts` runs the merge checks.

**Source-verification log.** Each thread that verifies a fact writes only its own file in `docs/source_verification/`. A fact is usable in a rule only once it is logged with the passage, table or file it was verified from.

**Source IDs.** Prefixed by the thread ID, for example `original-access-001`, `inequality-data-oecd-idd-gini` or `outcome-data-wdi-sp.dyn.le00.in`. IDs never change once written.

**Parallel data.** Where two sources give values for the same variable, the values are compared, and every differing value is published in `outputs/tables/historical_source_comparison.csv` or the updated reproduction's own comparison table. They are then combined into the project's own series. The source that source lineage ranks first is primary, the other fills only its gaps, units are harmonised, and values are never averaged. Every value keeps its source ID. In historical data the released file is primary, and a value filled from another source is flagged reconstructed, so the access label shows it. The combining rule is recorded in the original method specification before any correlation is computed, and the combined series belong to the project's own data collection.

**Country codes.** ISO 3166-1 alpha-3 throughout. Name variants map through one table in `code/lib/`.

**Country eligibility rule.** The authors state the rule in their 2010 response to Peter Saunders's report for Policy Exchange, published by the Equality Trust. A country is eligible when it meets three conditions, applied in this order.

1. It is among the 50 richest countries in the world.
2. Its population is more than 3 million.
3. It has comparable income distribution data.

The authors do not state two details, the measure and data vintage used to rank the 50 richest, and the source that counted as comparable income distribution data. The original method specification settles both. For the ranking, the candidate is gross national income per capita by the World Bank's Atlas method from the April 2004 World Development Indicators, used only in the historical check. If that vintage cannot be obtained on the day of the run, the check is not made and the reason is recorded. The refreshed sample ranks countries by the current release of the same series. For comparable income distribution data, the candidate is the inequality measure source lineage records for the original data. In the refreshed sample, the third condition uses the inequality series of the strict updated reproduction.

Outcome data never decide eligibility. Neither the availability of an outcome nor its value, a correlation, an outlier or significance adds or removes a country. A country without a value for one outcome stays in the sample and is left out of that analysis only, and the result row lists it in `missing_units`. Choices the rule leaves open, such as economies that are not sovereign states, the year in which population and income are measured, and ties at rank 50, are fixed in the reproduction lock as named choices. A country type such as market democracy is not a condition, because the authors give it as the reason for the rule, not as a part of it.

Both eligibility tables have one row per country considered, with `iso3`, `income_rank`, `population`, `inequality_data_available`, `eligible` and `exclusion_reason` as not_top_50, population_below_3m, no_comparable_inequality_data or empty.

**Controversy IDs.** The category ID listed at the end of this section followed by a number, for example `inequality-measure-002`. The controversy register thread assigns them.

**Code ownership.** Each thread also owns its manifests `data/metadata/manifests/<thread>.csv` and `data/metadata/manifests/<thread>-derived.csv`, `make/<thread>.mk` for its Make targets, `tests/<thread>/` for its tests and `data/local_data_required/<thread>.md` for the files you must obtain for it. This applies to every thread, whether or not its own section repeats these paths, and the ownership check derives them from the thread ID. Shared test utilities live in `tests/scaffold/` and change only through the integrator.

**Criticisms of the general hypothesis.** Some named criticisms predate *The Spirit Level* or address the income inequality and health hypothesis in general rather than the book's analyses. Judge 1995 and Gravelle 1998 are examples. Such a row has `target_level` set to `general_hypothesis`, while other rows use `original`, `current` or `both`. Its `mapping_rationale` states which book or current result the criticism bears on and why, and its `claim_or_result_affected` names that result.

**Result rows.** Every row of a reproduction table carries `result_type` as historical_reproduction, current_fixed_sample, current_fixed_sample_with_substitutes or current_eligibility_refreshed, `input_access`, which is `RESTRICTED INPUT` when any input is restricted and empty otherwise, with the restricted source IDs listed, `n`, `missing_units` listing the sample's countries or states without a value for that analysis, and for current results `reproduction_lock_commit`. The headline table that the report thread builds from these tables has one row per indicator and dataset, with `indicator`, `dataset`, `reported_r`, `historical_r`, `historical_n`, `updated_r` and `updated_n` from the fixed-sample result, `comparability` and `deviation_reason`.

**U.S. state data model.** The state data are stored in long form in three tables, so every value traces to its source. Z-scores and the index are never stored. They are computed from these tables with the same shared functions as for the countries.

- `us_states` has one row per state. Its columns are `state_fips` as the key, `state_abbr`, `state_name`, `in_original_sample`, which is true for the 50 states and false for the District of Columbia until verified otherwise, and `missing_in_original`, which lists the components the notes report as missing. Those are trust for Alaska, Delaware, Hawaii, Idaho, Maine, Nebraska, New Mexico, Nevada and South Dakota, and homicides for Wyoming.
- `us_state_variables` holds the state rows of the source lineage, with the columns listed above.
- `us_state_observations` has one row per state, variable and dataset. Its columns are `state_fips`, `variable_id`, `dataset` as et_release, historical_reconstruction or current, `reference_period`, `value`, `unit`, `source_id`, `source_sha256` and `provenance` as released, reconstructed or current.

The notes on sources and methods list nine index components for the states but say that 40 states have all eight measures. The rebuild uses all nine until the released file settles which is right.

**U.S. state sources.** The original source of each state variable comes from the notes on sources and methods. The candidate current series below are starting points for source lineage, which confirms each one and assigns its comparability class.

| Variable | Original definition, period and source | Candidate current series | Expected class |
|---|---|---|---|
| Income inequality | Gini coefficient by state, 1999, US Census Bureau table S4 | American Community Survey table B19083 | `CONCEPTUAL_SUCCESSOR` |
| Trust | Share agreeing that most people can be trusted, 1999, General Social Survey, reverse coded | General Social Survey by state, whose state identifier is restricted and would need a data agreement with NORC that the one-day run cannot obtain | `NO_CURRENT_EQUIVALENT` |
| Life expectancy | At birth, men and women, 2000, Census Population Division interim projections, reverse coded | NCHS U.S. State Life Tables | `EXACT_SUCCESSOR` or `CONCEPTUAL_SUCCESSOR` |
| Infant mortality | Deaths in the first year per 1000 live births, 2002, NCHS | CDC WONDER linked birth and infant death data | `EXACT_SUCCESSOR` |
| Obesity | BMI above 30, men and women averaged, 1999 to 2002, corrected for self-report bias by Ezzati and others, J R Soc Med 2006, PMID 16672759, PMC1457748 | Behavioral Risk Factor Surveillance System, self-reported | `SUBSTITUTE` |
| Mental health | Days in the past month when mental health was not good, 1993 to 2001, BRFSS, as published by Zahran and others, MMWR Surveillance Summaries 2005, PMID 16251867 | BRFSS health-related quality of life, mentally unhealthy days | `EXACT_SUCCESSOR` |
| Education | Grade 8 maths and reading scores combined, 2003, NAEP, reverse coded | NAEP, latest grade 8 maths and reading | `EXACT_SUCCESSOR` |
| Teenage births | Births per 1000 women aged 15 to 19, 2000, National Vital Statistics | CDC WONDER natality | `EXACT_SUCCESSOR` |
| Homicides | Homicides per 100,000, 1999, FBI Crime in the United States | CDC WONDER mortality by homicide, because the FBI series has gaps from the 2021 change to NIBRS | `CONCEPTUAL_SUCCESSOR` |
| Imprisonment | Prisoners per 100,000, 1997 to 1998, Bureau of Justice Statistics, not log transformed | BJS Prisoners series | `EXACT_SUCCESSOR` |

The historical rebuild takes the same series in the vintage the notes name, from the agencies' archives and the two articles' state tables. The released U.S. file is a later addition, and when it arrives it replaces the rebuild. For the one-day run the restricted General Social Survey state data are not applied for, and the current homicide source is CDC WONDER, whose terms of use you accept.

**Paths in code.** Relative to the project root, resolved through one helper in `code/lib/`.

**Derived manifest columns.** `derived_id`, `local_path`, `sha256`, `producing_script`, `code_version` as the commit the run used, `input_source_ids`, `input_sha256s`, `data_dictionary_ref`, `reproduction_lock_commit`, which is empty for the original release dataset, `superseded_by` and `notes`. No commit is rewritten, so that commit stays in the history of `main`. `make manifests` fails if any input ID is missing from the manifest, if an input hash does not match, or if the data dictionary reference does not resolve.

**Source packages.** Both packages have the same layout. `sources/supporting/` holds `original-authors/`, `academic/` and `non-academic/`. `sources/controversies/` holds `academic/`, `non-academic/` and `responses/`. Each subfolder has a `records.csv` and a gitignored `local/` folder for texts that may not be redistributed. Each package has a `manifest.csv`, a `README.md` and a `screening_log.csv`. A source with more than one role, such as a study that both supports and criticises, is downloaded once, into the folder of its main role, and listed in both manifests with all its roles in `roles`.

**Shared search and screening protocol.** Both packages are searched and screened the same way, so the inclusion standard is not stricter for one side. Both use the same databases, which are OpenAlex, Crossref and PubMed, plus the Equality Trust site and the sources the authors and their critics cite. Both search backward and forward from the same starting works and record the search date. A source is included when it has an identifiable author, a citable record and an argument or evidence about Wilkinson and Pickett's findings or the hypothesis behind them. Whether it supports or criticises the findings never decides inclusion. Every screened source gets a row in the package's `screening_log.csv` with the decision and its reason.

**Controversy data map columns.** `controversy_id`, `source_id`, `testable_statement`, `target_level`, `required_variables`, `required_geographies`, `required_years`, `candidate_sources`, `chosen_source`, `access_route`, `licence_status`, `redistributable`, `acquisition_status`, `local_paths`, `country_coverage`, `year_coverage` and `reason_not_obtained`. One map row per controversy and dataset, so a dataset that several controversies need appears in each of their rows.

**Source record columns.** `citation_key`, `authors`, `year`, `title`, `edition`, `journal_or_publisher`, `doi`, `pmid`, `pmcid`, `isbn`, `stable_url`, `archive_url`, `access_date`, `peer_review_status`, `roles`, `claim_or_controversy_ids`, `open_access` as yes, no or unknown, `licence`, `download_status` as published, local or record_only, `record_only_reason`, `local_path`, `sha256` and `notes`. `peer_review_status` stays because the supporting package's acceptance test needs it.

**Controversy register columns.** `controversy_id`, `claim_or_result_affected`, `target_level`, `mapping_rationale`, `source_role` as critic or independent, `source_author`, `source_title`, `publication_year`, `publication_date_type`, `source_type`, `peer_review_status`, `exact_controversy_in_neutral_words`, which also summarises the argument, `testable_statement`, `wilkinson_pickett_response_available`, `response_source_id`, `local_path`, `citation_url` and `notes`.

**Source lineage columns.** `variable_id`, `dataset` as international or us_states, `role` as inequality, index_component, extra_measure or eligibility, `original_definition`, `original_source`, `original_series`, `original_locator` as the released file's sources sheet, the notes page or a book page, `original_reference_period`, `original_population`, `original_geographic_unit`, `original_unit`, `original_transformation`, `direction` as as_is or reverse_coded, `reported_r` and `reported_p` where the authors published them, `current_provider`, `current_series_id`, `current_vintage`, `retrieval_date`, `request` as the exact download URL or API query, `comparability` from the classes under the source lineage thread, `deviation_reason`, `licence`, `local_path`, `sha256`, `current_source_id`, `verification_status`, `verification_log_ref` and `notes`.

**Claims register columns.** `claim_id`, `author`, `source_work`, `source_locator` as page or chapter, `publication_year`, `stable_identifier`, `wording`, `wording_type` as verbatim or paraphrase, `claim_class` as descriptive_correlation, proposed_mechanism, causal_claim or policy_prediction, `verification_status` as verified or to_be_verified, `verification_log_ref` and `notes`. Claim IDs are `claim-` followed by a number, for example `claim-007`. `claim_class` stays empty while `verification_status` is to_be_verified.

**Controversy categories.** `country-selection` covers country selection and sample definition. `inequality-measure` covers the inequality measure, including the 80:20 ratio against Gini, market against disposable income, and survey comparability and timing. `index-construction` covers composite-index construction, including weighting, component choice and reverse coding. `outliers` covers outliers and influential countries. `temporal-persistence` covers persistence in later data and in national time series. `mechanism` covers the psychosocial account and alternatives such as material conditions, public services, institutions and social cohesion. `data-comparability` covers data availability and comparability.

**Report sections.** The report has these sections in this order. Scope and terminology. Headline results, the headline table with one line on how to read it. Goals and deliverables, which reports each of the six goals with its deliverable and lists what each source package and dataset folder holds. Historical reproduction. Fixed-sample current reproduction, with its substitute variant. Eligibility-refreshed current reproduction, or the reason it is not possible. Each reproduction section reports the countries and the U.S. states separately. Supporting sources. Controversies, where each entry states the source's claim, cites it, names its category, lists the datasets downloaded for it and links any published Wilkinson and Pickett response. Author claims, which presents the claims register by class as it stands at the `results-v1` tag. Limitations, covering the small country sample, cross-national comparability, temporal misalignment, missing data, measurement changes, series that ended or changed definition, and the fact that the project tests neither the controversies nor causality. Reproducibility, with exact commands, environment versions, the reproduction lock commit and data-access limits, and links to the `deliverables-v1` release and the repository.
