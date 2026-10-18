# Contributing

This project re-examines Wilkinson and Pickett's *The Spirit Level* in the open. Contributions come from people and from Claude sessions working as threads of the [implementation plan](IMPLEMENTATION_PLAN.md). This file says how to work. The goals and scope are in [INTENT.md](INTENT.md), the research method in [RESEARCH-METHOD.md](RESEARCH-METHOD.md) and the implementation in the plan. This file links to them instead of repeating them.

Issues are welcome at any time.

## Rules that are never broken

No one computes, views or infers an association between current inequality data and current outcome data before the reproduction lock has merged and milestone 1 is tagged. Downloading data, reading metadata and checking country coverage are fine.

Acquired data files are stored exactly as acquired, with their acquisition records, and are never modified. Only data and texts whose terms allow publishing are committed. Anything else is handled locally and recorded as a source with its link, and data extracted from it stay below the threshold of originality and never take a substantial part of a database. A pull request may add data files but never modifies or deletes an existing one, except to remove credentials, personal data, licence breaches, files under a takedown request or malicious files, with a maintainer's approval and a record in `docs/removals.md`.

A controversy enters the register only with a named author, an exact title, a publication year and a stable DOI, PMID, PMCID, ISBN or URL, and a book also needs its edition.

Results are described in neutral language. The words debunk, toxic, cherry-picking, proves and disproves appear only inside attributed quotations, in code and comments as well as in prose.

## Environment

Install everything with `pixi install` and run everything through `pixi run` or `make`. The single lockfile `pixi.lock` pins every package.

Do not install packages with `pip install` or any other way outside pixi. To add a dependency, add it to `pixi.toml` from conda-forge, or from PyPI only if conda-forge lacks it, and commit the updated `pixi.lock`, `environment.yml` and `requirements.txt` together.

## Language and files

The project is written in Python. Another language is added only when a method needs a reference implementation that Python lacks, and the pull request that adds it says why.

Every rule of the computation lives in an analysis specification in `config/specs/`, and the code reads it from there. Never write a year, a direction, a weight or a sample into code or into prose as a second copy. The research method sets the rules, the specification holds their exact values, and the method rationale gives the source or reason for each value and refers to its specification key. The comparisons that are computed and reported are listed once in `config/results_catalogue.csv`. Do not keep another list of them.

Every file another script reads follows a pandera schema defined once in `code/lib/schemas.py`. A change to a schema is requested from the integrator, like any change to a scaffold file. Column names are snake_case. A unit is identified by `unit_type` and `unit_id`, an ISO 3166-1 alpha-3 code for a country and a two-digit FIPS code for a U.S. state, and must exist in its registry in `config/units/`. Shared code never assumes that a unit is a country. Dates are ISO 8601. A missing value is a null, never an empty string or the text NA. Pandas indexes are not written to file.

Numbered scripts are thin command-line tools that load a specification or record, call the library and write their outputs. Source-specific parsing goes in a reader in `code/lib/readers/`, shared transformations in `code/lib/transform.py` and computation in `code/lib/compute.py`. Historical and updated reproduction use the same scripts with different specifications. Do not build a workflow system or a plugin framework. Each script step is a Make target in your thread's `make/<thread>.mk`, with the script and its input files as prerequisites. Add the target to `ACQUIRE_TARGETS` if it downloads or records assets, or to `REPLAY_TARGETS` if it works only from files already present. `make acquire` builds acquire targets, and `make all` builds only replay targets. Put every acquire rule in the block of your `.mk` file that is read only when `MODE=acquire`, because Make builds prerequisites whichever list a target is in. A replay target that needs a restricted input also goes in `RESTRICTED_TARGETS`. Define its real rule only when the input is present, and otherwise a stand-in rule with no prerequisites that checks the recorded input checksums and keeps the committed outputs.

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

Code does not cite or copy method rules, because it reads them from the specification. Code that downloads data for a controversy cites the register row, for example `inequality-measure-002`. A reader cites the source-verification log entry for any layout fact it relies on.

Code that writes or reads an interface file names the schema the file follows.

Python functions have Google-style docstrings that state parameters, return value, units and assumptions.

Comments contain no commented-out code, no TODO without an issue reference, and no interpretation of results.

## Threads, branches and ownership

Thread pull requests go directly into `main`. Three milestones mark the points where a maintainer reviews what has merged, and each ends in a tag: `milestone-1`, `deliverables-v1` and `results-v1`. The first two deliver goals 1 to 5, and the third delivers goal 6, the site. The plan lists which thread belongs to which milestone. The integrator is a separate Claude session that creates the tags after a maintainer's approval and makes changes to scaffold files.

A thread's branch is named `<thread-id>/<short-description>`, for example `original-access/first-download`, and is branched from `main`. A thread changes only the paths listed in its ownership file `docs/ownership/<thread-id>.csv`, and `make check-contracts` enforces this. When you create a file whose name is not already covered, such as a data source or acquisition record, an extract or a run record, add its path to your ownership file. Patterns follow git's wildmatch rules, so `*` never crosses a `/`. A thread reads another thread's output only from `main` after that thread has merged into it. A change to a file owned by the scaffold thread is requested in the pull request and made by the integrator.

Pull requests from forks are not merged. If you are outside the project, propose a change in an issue, and a thread or the integrator makes it.

## Data and sources

Every data source has a record in `data/metadata/sources/`, and every request has an acquisition record in `data/metadata/acquisitions/` that lists the files it produced with their size, checksum, storage and `redistributable` flag. The shared download helper writes the acquisition record. Identifiers never contain a thread ID. Acquire the smallest official input that holds what the deliverable needs, and store the response as received. The relevant series are extracted from it by a replay step into `data/02_extracts/`. A file up to 50 MiB is committed normally. Git LFS is not used. An extract above 50 MiB is split, for example by indicator or country, so every stored file stays within 50 MiB. Never acquire a bulk archive, such as the complete WDI or WID.world download. Extract the relevant series through the provider's API or its per-indicator download. A raw file is never modified. A correction is a new acquisition whose record names the corrected acquisition or file in `corrects`. Derived files may be rebuilt at the same path. Metadata, such as a source description, an acquisition status or a lineage row, may be corrected, with the reason in the commit message or in the record's notes.

`sources/supporting/` and `sources/controversies/` are the two packages. Search and screen both under the protocol in the research method, log every search in the package's `search_log.csv` and every screening decision in its `screening_log.csv`, and state the known gaps in its README. A package is complete when the protocol is carried out and documented, not when every possible source is found. Download every text in a package that can be obtained legally, whether or not you read it. Commit a text whose terms allow publishing to its package folder and list it in its record. Keep any other text in the gitignored `local/` folder of its `sources/` folder, and record its local path, an archived landing-page URL where there is no DOI and the SHA-256 of the file. The package `README.md`, generated from the manifest, says what the package holds and what it lacks. The source-verification log cites the section or page, quotes at most a short phrase and records which version was read. A source that needs registration or acceptance of terms is recorded in your thread's file in `data/local_data_required/`, and a person obtains it. Ignore rules for user-supplied files go in the `.gitignore` of your raw folder, never in the root `.gitignore`. Paywalls and access controls are never bypassed.

Record checks run in two modes. `metadata` runs in CI on every pull request and push and checks schemas, identifiers, references, ownership and that no raw file or immutable file entry changed, without touching data files. `full` runs locally and in `make verify-data`, and hashes every stored file and the restricted files you hold. An acquisition whose status records a failed attempt, a source awaiting you or a metadata-only source needs its retrieval record instead of a file. Run `make check-contracts` in `full` mode before opening a pull request and report the result in it. An output that would cross the threshold of originality of a source that may not be published is never committed. Keep it in `outputs/local/`, which is gitignored.

When `make all` cannot run a step because a restricted input is missing, it keeps the committed output and marks the step `retained` in the run record. Only the recorded input checksums are then compared with the acquisition records, because the missing file cannot be checked. Never describe a retained result as recomputed. `RESTRICTED INPUT` describes a use restriction, not whether a result was recomputed. Commit the run record of the run that produced your committed outputs.

## The reproduction lock

Until the reproduction lock has merged and milestone 1 is tagged, work that touches current outcome data is limited to downloading it, reading its metadata and checking coverage. After that, a change to a locked specification is a new specification version recorded as a dated amendment in the lock, and results are reported under both versions. Every current result names its specification and version.

## Proposing a controversy

The register takes any named controversy about Wilkinson and Pickett's findings, from a critic or from an independent researcher. Open an issue with the criticism proposal template. It asks for the fields the register requires, the result the controversy bears on and the data that would support or test it.

A proposal made before the register is frozen is considered for the register. A proposal made after the freeze is added in a dated amendment. Either way it is welcome.

## Writing about results

Use the terminology in INTENT.md. The project's results are correlations and are described as correlations. A correlation that Wilkinson and Pickett reported without a causal interpretation is never presented as their causal inference. Causal readings and mechanisms appear only as claims attributed to their source in the claims register or the controversy register. The words "causes" and "does not cause" appear only inside such a claim. Every reproduced value is reported, whether or not it matches the original, and significance is never used to choose what to report.

## Tests and checks

Install the hooks once with `pixi run pre-commit install`. Before opening a pull request, run ruff, `make test`, `make check-data` and `make check-contracts` locally, and `make all` if your work produces outputs. CI runs the same checks.

Tests are organised by function, in the levels the plan's testing plan lists, not by thread.

- Computation tests in `tests/compute/` use small examples whose expected values are calculated by hand and written into the test, never taken from the code under test.
- Each reader has tests in `tests/readers/<reader>/` with small stored example files in `tests/fixtures/readers/<reader>/`. Ordinary tests never call an external service.
- Integrity checks cover schemas, key uniqueness, units, allowed values, references, checksums and join row counts. Pandera checks structure and value constraints, not the correctness of a computation.
- Include the edge cases that apply: a constant variable, a missing component, a duplicated key, a conflicting unit, an unknown unit, and a shuffled row order that must not change any result.
- Replay comparisons require identifiers, samples and missing units to match exactly, and floating-point values within the plan's tolerances.

A difference from a value the authors published is a research result. Log it in the discrepancy log. It is not by itself a software error, and never adjust the computation to match it.

Do not add a coverage target, browser automation, load tests or tests for every helper.

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
