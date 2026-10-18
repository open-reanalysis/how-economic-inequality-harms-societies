# Contributing

This project re-examines Wilkinson and Pickett's *The Spirit Level* in the open. Contributions come from people and from Claude sessions working as threads of the [implementation plan](IMPLEMENTATION_PLAN.md). This file says how to work. The reasons behind the rules are in [INTENT.md](INTENT.md) and the plan, and this file links to them instead of repeating them.

Issues are welcome at any time.

## Rules that are never broken

No one computes, views or infers an association between current inequality data and current outcome data before the reproduction lock has merged and milestone 1 is tagged. Downloading data, reading metadata and checking country coverage are fine.

Acquired data files are stored exactly as acquired, by the storage method recorded for each source, with their manifest rows. Only data and texts whose terms allow publishing are committed. Anything else is handled locally and recorded as a source with its link, and data extracted from it stay below the threshold of originality and never take a substantial part of a database. A pull request may add data files but never modifies or deletes an existing one, except to remove credentials, personal data, licence breaches, files under a takedown request or malicious files, with a maintainer's approval and a record in `docs/removals.md`.

A controversy enters the register only with a named author, an exact title, a publication year and a stable DOI, PMID, PMCID, ISBN or URL, and a book also needs its edition.

Results are described in neutral language. The words debunk, toxic, cherry-picking, proves and disproves appear only inside attributed quotations, in code and comments as well as in prose.

## Environment

Install everything with `pixi install` and run everything through `pixi run` or `make`. The single lockfile `pixi.lock` pins every package.

Do not install packages with `pip install` or any other way outside pixi. To add a dependency, add it to `pixi.toml` from conda-forge, or from PyPI only if conda-forge lacks it, and commit the updated `pixi.lock`, `environment.yml` and `requirements.txt` together.

## Language and files

The project is written in Python. Another language is added only when a method needs a reference implementation that Python lacks, and the pull request that adds it says why.

Every file another script reads follows a pandera schema defined once in `code/lib/schemas.py`. A change to a schema is requested from the integrator, like any change to a scaffold file. Column names are snake_case. Countries are ISO 3166-1 alpha-3 codes. Dates are ISO 8601. A missing value is a null, never an empty string or the text NA. Pandas indexes are not written to file.

Scripts are numbered by pipeline stage. Tests go in `tests/<thread>/`. Each script is a Make target in your thread's `make/<thread>.mk`, with the script and its input files as prerequisites. Add the target to `ACQUIRE_TARGETS` if it downloads or records assets, or to `REPLAY_TARGETS` if it works only from files already present. `make acquire` builds acquire targets, and `make all` builds only replay targets. A replay target that needs a restricted input also goes in `RESTRICTED_TARGETS`, so `make all` skips it where the input is missing and keeps its committed outputs.

Python follows ruff.

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

Code that applies a rule from the reproduction lock cites the section of the lock. Code that downloads data for a controversy cites the register row, for example `inequality-measure-002`. Code that reproduces the original method cites the source-verification log entry it relies on. A labelled alternative implementation says in its comment that it is an alternative and what it is an alternative to.

The data dictionary is the canonical description of every transformation. A comment points to its entry instead of copying the formula, so the two cannot drift apart.

Code that writes or reads an interface file names the schema the file follows.

Python functions have Google-style docstrings that state parameters, return value, units and assumptions.

Comments contain no commented-out code, no TODO without an issue reference, and no interpretation of results.

## Threads, branches and ownership

Thread pull requests go directly into `main`. Three milestones mark the points where a maintainer reviews what has merged, and each ends in a tag: `milestone-1`, `deliverables-v1` and `results-v1`. The first two deliver the project's five goals. The plan lists which thread belongs to which milestone.

A thread's branch is named `<thread-id>/<short-description>`, for example `original-access/first-download`, and is branched from `main`. A thread changes only the files it owns, and `make check-contracts` enforces this. A thread reads another thread's output only from `main` after that thread has merged into it. A change to a file owned by the scaffold thread is requested in the pull request and made by the integrator.

Pull requests from forks are not merged. If you are outside the project, propose a change in an issue, and a thread or the integrator makes it.

## Data and sources

Every download goes through the shared download helper, which writes the manifest row with checksum, size, licence and `redistributable` flag. Acquire the smallest official input that holds what the deliverable needs, and record its storage method in the manifest. A file up to 50 MiB is committed normally. How larger files are stored is open until a maintainer decides on Git LFS, so ask before acquiring one. Never acquire a bulk archive, such as the complete WDI or WID.world download. Extract the relevant series through the provider's API or its per-indicator download. A correction is a new dated file with `corrects_source_id`, never an overwrite.

`sources/supporting/` and `sources/controversies/` are the two packages. Search and screen both under the shared protocol in the plan, and log every screening decision. Download every text in a package that can be obtained legally, whether or not you read it. Commit a text whose terms allow publishing to its package folder and list it in its record. Keep any other text in the gitignored `local/` folder of its `sources/` folder, and record its local path, an archived landing-page URL where there is no DOI and the SHA-256 of the file. The package `README.md`, generated from the manifest, says what the package holds and what it lacks. The source-verification log cites the section or page, quotes at most a short phrase and records which version was read. A source that needs registration or acceptance of terms is recorded in your thread's file in `data/local_data_required/`, and a person obtains it. Ignore rules for fetched and user-supplied files go in the `.gitignore` of your raw folder, never in the root `.gitignore`. Paywalls and access controls are never bypassed.

Manifest checks run in two modes. `metadata` runs in CI on every pull request and push and checks schemas, identifiers and references without touching data files. `full` runs locally and in `make verify-data`, and verifies every stored file, after `make fetch-data` has fetched those not in git, and the restricted files you hold. A manifest row whose `acquisition_status` records a failed attempt, a source awaiting you or a metadata-only source needs its retrieval record instead of a file. Run `make check-contracts` in `full` mode before opening a pull request and report the result in it. An output that would cross the threshold of originality of a source that may not be published is never committed. Keep it in `outputs/local/`, which is gitignored.

## The reproduction lock

Until the reproduction lock has merged and milestone 1 is tagged, work that touches current outcome data is limited to downloading it, reading its metadata and checking coverage. After that, a change to the lock is made as a dated amendment in the same file, and results are reported under both the original and the amended rule. Every current result cites the lock commit.

## Proposing a controversy

The register takes any named controversy about Wilkinson and Pickett's findings, from a critic or from an independent researcher. Open an issue with the criticism proposal template. It asks for the fields the register requires, the result the controversy bears on and the data that would support or test it.

A proposal made before the register is frozen is considered for the register. A proposal made after the freeze is added in a dated amendment. Either way it is welcome.

## Writing about results

Use the terminology in INTENT.md. The project's results are correlations and are described as correlations. A correlation that Wilkinson and Pickett reported without a causal interpretation is never presented as their causal inference. Causal readings and mechanisms appear only as claims attributed to their source in the claims register or the controversy register. The words "causes" and "does not cause" appear only inside such a claim. Every reproduced value is reported, whether or not it matches the original, and significance is never used to choose what to report.

## Tests and checks

Install the hooks once with `pixi run pre-commit install`. Before opening a pull request, run ruff, `pytest` and `make check-contracts` locally. CI runs the same checks.

## Commits and pull requests

Write commit messages in the imperative, with a short subject line and a body that says why. Commits written with an AI assistant carry a `Co-Authored-By` line naming it.

Push every commit to the remote as soon as you make it. Several agents work on the project at the same time, and a commit that exists only in one local clone is invisible to the others. They then build on an outdated branch, and the work conflicts when it meets. Fetch the remote branch and merge it into yours before you start and again before you push. Never end a session with commits or changes that exist only locally.

The pull request template is the merge package the plan requires. Fill in every item. A thread pull request from a branch in this repository auto-merges into `main` with a merge commit once every required check passes. A maintainer reviews `main` at each milestone, and only after that review does the integrator create the milestone's tag. A Claude session never creates a tag. An approving review becomes mandatory once more than one person contributes.

## History is never rewritten

Every commit stays in the history as it was made, with its hash, timestamp, author and message. The history records the order in which the work was done, and that order is part of the project's evidence, for example that the updated reproduction followed the lock.

- Bring a branch up to date by merging the remote branch or `main` into it.
- Merge every pull request with a merge commit.
- To correct a commit, make a new commit that corrects it.

Squash, rebase, amend, force push and any other command that rewrites or removes commits are forbidden. The one exception is purging credentials or personal data from history, which a maintainer approves and records in `docs/removals.md`. Squash and rebase are each allowed only with their own stated reason and their own explicit permission from a maintainer, given for that one case. Permission for a squash never covers a rebase, and permission for one case never covers another. The reason and the permission are recorded in the pull request description before the command is run.

## Licences

By contributing you agree that your contribution is published under the project's licences. Code and tests are under the [MIT License](LICENSE). Documents, the report, the website, figures and the project's own data collection are under [CC BY 4.0](LICENSE-docs). Data and texts fetched from elsewhere are covered by neither and keep their own terms.
