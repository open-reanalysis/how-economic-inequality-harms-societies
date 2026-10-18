# Contributing

This project re-examines Wilkinson and Pickett's *The Spirit Level* in the open. Contributions come from people and from Claude sessions working as threads of the [implementation plan](IMPLEMENTATION_PLAN.md). This file says how to work. The reasons behind the rules are in [INTENT.md](INTENT.md) and the plan, and this file links to them instead of repeating them.

Issues and pull requests are welcome at any time.

## Rules that are never broken

No one computes, views or infers an association between current inequality data and current outcome data before the analysis lock is tagged. Downloading data, reading metadata and checking country coverage are fine.

Acquired data files are committed exactly as acquired, with their manifest rows. No restricted data and no full texts are committed. A pull request may add data files but never modifies or deletes an existing one.

An alternative enters the register only with a named author, an exact title, a publication year and a stable DOI, PMID, PMCID, ISBN or URL, and a book also needs its edition. Whether the source is a critic, the original authors or an independent researcher never decides whether the alternative is tested.

Results are described in neutral language. The words debunk, toxic, cherry-picking, proves and disproves appear only inside attributed quotations, in code and comments as well as in prose.

## Environment

Install everything with `pixi install` and run everything through `pixi run` or `make`. The single lockfile `pixi.lock` pins both Python and R.

Do not install packages with `pip install` or `install.packages()`. To add a dependency, add it to `pixi.toml` from conda-forge, or from PyPI only if conda-forge lacks it, and commit the updated `pixi.lock`, `environment.yml` and `requirements.txt` together. R packages that are published only on GitHub are not used, because they cannot be locked.

## Python and R

The project uses both languages on purpose. Each does the work where it is strongest, and they meet only through files.

### Which language to use

Python is the default. Acquisition, provenance, harmonisation, z-scoring and index construction, cross-sectional statistics, contract checks and the report are written in Python.

R is used where its package is the reference implementation of the method. That covers panel models with fixest, the small-cluster inference method the lock selects, DAG adjustment sets with dagitty, and qualitative comparative analysis with QCA. A pull request that introduces R for anything else explains which reference implementation makes R the better choice.

### The boundary between them

Every script is written in one language. Scripts exchange data only through Parquet and CSV files at the paths the plan defines. rpy2 and reticulate are not used anywhere, including the report.

Logic that has one canonical implementation exists once. Z-scores and the composite index are computed in Python, and R reads them from file instead of recomputing them.

### Interface files

Every file that crosses the boundary follows a schema in `data/metadata/schemas/`, written once as a Frictionless Table Schema JSON file. Python validates against it through a pandera schema generated from the JSON, and R validates against it through a small base R and jsonlite validator that testthat calls. Neither language defines a schema in code.

Column names are snake_case. Countries are ISO 3166-1 alpha-3 codes. Dates are ISO 8601. A missing value is a null, never an empty string or the text NA. Neither R factors nor pandas indexes are written to file.

### Naming and ownership

Scripts are numbered by pipeline stage, and the number does not depend on the language. `code/06b_panel_models.R` belongs to the same thread that would own `code/06b_panel_models.py`. Tests go in `tests/<thread>/`, with pytest and testthat tests side by side. Each script is declared as a pipeline step in `code/pipeline/<thread>.toml` with its phase, inputs and outputs. The phase is `acquire` for a script that downloads or records assets and `replay` for a script that works only from files already present. `make acquire` runs acquire steps, while `make all` and `make replay-ci` run only replay steps, and CI uses the inputs to tell replay steps it can run from those that need restricted data.

### Agreement between the languages

Current replication's cross-language test computes the primary OLS and Pearson results in both Python and R and fails beyond the tolerance written in the test. Stochastic results are not compared across languages, because the random number generators differ. Each language records its own seed, taken from the lock.

### Style

Python follows ruff. R is written in base R with arrow for file input and output, linted with lintr and formatted with styler. Keep R dependencies to what the method needs. A new R package is justified in the pull request in the same way as a new R use.

### The report

Quarto pages contain Python chunks only and render through the Jupyter engine. Results computed in R reach the report through the files the R scripts wrote.

## Commenting code

Comments are in English. A comment says why the code does something, not what it does. Self-explanatory lines get no comment.

Every script starts with the same header.

```python
# SPDX-License-Identifier: MIT
# Purpose: <one sentence>
# Thread: <thread id>
# Reads: <paths>
# Writes: <paths>
# Network: none | live sources
```

R scripts use the same fields.

Code that applies a rule from the analysis lock cites the section of the lock. Code that tests a criticism cites the register row, for example `inequality-measure-002`. Code that reproduces the original method cites the source-verification log entry it relies on. A labelled alternative implementation says in its comment that it is an alternative and what it is an alternative to.

The data dictionary is the canonical description of every transformation. A comment points to its entry instead of copying the formula, so the two cannot drift apart.

Code that writes or reads an interface file names the schema the file follows.

Python functions have Google-style docstrings that state parameters, return value, units and assumptions. R functions have roxygen-style `#'` comments with the same content, even though the code is not a package.

Comments contain no commented-out code, no TODO without an issue reference, and no interpretation of results.

## Threads, branches and ownership

Work reaches `main` in three milestones, and each has an integration branch: `milestone/1-lock`, `milestone/2-analysis` and `milestone/3-report`. Thread pull requests go into the current integration branch. Only the three milestone pull requests go into `main`, and a maintainer reviews and merges each of them. The plan lists which thread belongs to which milestone.

A thread's branch is named `<thread-id>/<short-description>`, for example `original-access/first-download`. A thread changes only the files it owns, and `make check-contracts` enforces this. A thread reads another thread's output only from its milestone's integration branch after that thread has merged into it. A change to a file owned by the scaffold thread is requested in the pull request and made by the integrator.

A pull request from a fork has no thread branch. A maintainer gives it a label such as `thread:controversy-register`, and the ownership check runs against that thread's paths. Until the label is set, the check waits. While the ownership check is a required status, a pending check blocks the merge, so a fork pull request cannot be merged until a maintainer has labelled it. A fork pull request targets the current integration branch and never auto-merges. A maintainer reviews and merges it.

## Data and sources

Every download goes through the shared download helper, which writes the manifest row with checksum, size, licence and `redistributable` flag. A file up to 50 MiB is committed normally. A larger file goes through Git LFS, marked with `lfs` in the manifest and in the `.gitattributes` file of its raw folder. Prefer a source's per-indicator or per-country download to a bulk archive where one exists. A correction is a new dated file with `corrects_source_id`, never an overwrite.

Sources are bibliographic records in `sources/`, with links, not full texts. Every text whose licence permits redistribution is attached to a release and listed in its record. For any other text, keep the file you read locally in the gitignored `local/` folder of its `sources/` folder, and record its local path, an archived landing-page URL where there is no DOI and the SHA-256 of the file. The source-verification log cites the section or page, quotes at most a short phrase and records which version was read. A source that needs registration or acceptance of terms is recorded in `data/LOCAL_DATA_REQUIRED.md`, and a person obtains it. Paywalls and access controls are never bypassed.

Manifest checks run in three modes. `metadata` runs in CI on every pull request and checks schemas, identifiers and references without touching data files. `available` runs in CI replay and in `make verify-data` and verifies every committed data file. `full` runs locally and also checks the restricted files you hold. A manifest row whose `acquisition_status` records a failed attempt, a source awaiting you or a metadata-only source needs its retrieval record instead of a file. Run `make check-contracts` in `full` mode before opening a pull request and report the result in it.

## The analysis lock

Before the lock gate, work that touches current outcome data is limited to downloading it, reading its metadata and checking coverage. After the lock is tagged, its files are covered by content hashes. That includes the DAG and the script that derives adjustment sets from it. A change to any of them is made as a dated amendment with a new tag, and results are reported under both the original and the amended rule.

## Proposing a criticism or an alternative

The register takes any named alternative, from a critic, from Wilkinson and Pickett themselves or from an independent researcher. Open an issue with the criticism proposal template. It asks for the fields the register requires and for the result the criticism bears on.

A proposal made before the register is frozen is considered for the register. A proposal made after the freeze is added in a dated amendment, and its test is reported separately as a post-lock analysis, because it was not declared before the data were examined. Either way it is welcome.

## Writing about results

Use the terminology in INTENT.md. A correlation is described as a correlation, and a correlation that Wilkinson and Pickett reported without a causal interpretation is never presented as their causal inference. Causal readings and mechanisms appear as claims attributed to their source in the claims register or the controversy register, or as results of a causal design declared in the analysis lock, stated with its identifying assumptions and what it cannot rule out. Every result carries its evidence tier. Results in tiers 1 to 3 use the neutral association vocabulary. The words "causes" and "does not cause" appear only next to a verdict that the locked verdict rules produced, together with its assumptions sentence, and a verdict is written in the same form whether it agrees or disagrees with the original authors. The full specification curve is reported, and significance is never used to choose what to report. Controversy tests use the six outcome labels in the plan.

## Tests and checks

Install the hooks once with `pixi run pre-commit install`. Before opening a pull request, run the linters, `pytest`, `testthat` and `make check-contracts` locally. CI runs the same checks.

## Commits and pull requests

Write commit messages in the imperative, with a short subject line and a body that says why. Commits written with an AI assistant carry a `Co-Authored-By` line naming it.

The pull request template is the merge package the plan requires. Fill in every item. A thread pull request from a branch in this repository auto-merges by squash into its integration branch once every required check passes. A milestone pull request into `main` is opened by the integrator, reviewed by a maintainer and merged with a merge commit only by that maintainer's decision. A Claude session never merges into `main`. The ownership check does not apply one thread's paths to a milestone pull request. It runs in milestone mode instead and accepts the pull request only if every commit on the integration branch is the squash commit of a thread pull request that passed its own ownership check. An approving review becomes mandatory once more than one person contributes.

## Licences

By contributing you agree that your contribution is published under the project's licences. Code and tests are under the [MIT License](LICENSE). Documents, the report, the website, figures and result tables are under [CC BY 4.0](LICENSE-docs). Raw data and third-party full texts are covered by neither, and derived outputs follow a source's stricter terms where they apply.
