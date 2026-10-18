# How Economic Inequality Harms Societies: an Open Reanalysis

A transparent, reproducible examination of the macro-comparative analyses in Richard Wilkinson and Kate Pickett's *The Spirit Level*. The project does not set out to prove or disprove the authors. It produces two result families and keeps them separate in every table, figure and sentence.

## Goals

1. Download the current version of every dataset Wilkinson and Pickett used.
2. Reproduce their findings, from the released data and by their own method on the current data.
3. Download a package of sources supporting their findings, academic and non-academic.
4. Download a package of sources setting out controversies about their findings.
5. Download datasets that may support those controversies.

The five deliverables are released together as `deliverables-v1`, which completes the assignment. The project also keeps a register of the authors' claims and publishes a report and a website. Neither delays a goal.

> **Status: pre-release.** Nothing has been analysed yet. No updated-reproduction result is produced before the reproduction lock (see [Declared before examined](#declared-before-examined)) is committed.

## The results

| Result | Question | Label used in outputs |
|---|---|---|
| **Historical reproduction** | Do the data Wilkinson and Pickett released reproduce the correlations and the composite Health and Social Problems Index they reported? The label depends on what original material is accessible today. | `DIRECT REPRODUCTION`, `PARTIAL REPRODUCTION`, `ARCHIVE-BASED RECONSTRUCTION` or `INDEPENDENT RECONSTRUCTION` |
| **Updated reproduction** | Does the original method, applied unchanged to the current release of the same data, reproduce the findings? The fixed-sample result keeps the historical sample. Series with no exact or conceptual successor are left out, and a separate result adds substitute measures. The eligibility-refreshed result reapplies the original selection rule once it is verified. | `UPDATED REPRODUCTION, FIXED SAMPLE`, `UPDATED REPRODUCTION, FIXED SAMPLE, WITH SUBSTITUTES` and `UPDATED REPRODUCTION, ELIGIBILITY REFRESHED` |

Beside the results, the project delivers the two source packages, the controversy register with its datasets, and the register of the authors' claims.

## What the project does and does not claim

1. Results are reported as correlations.
2. The project tests neither the controversies nor causality. It documents them with their sources, and the controversy datasets make later tests possible.
3. Each statement by Wilkinson and Pickett in the claims register is classified as a descriptive correlation, a proposed mechanism, a causal claim or a policy prediction. A correlation they reported without a causal interpretation is never presented as their causal inference.
4. The words "causes" and "does not cause" appear only inside a claim attributed to its source.

## Vocabulary

| Term | Meaning here |
|---|---|
| Reported correlation | What the authors computed |
| Robustness | Whether that correlation survives reasonable alternative choices |
| Mechanism | An explanation of why a correlation might exist |
| Causal claim | Changing inequality would change outcomes |
| Policy prediction | A specific intervention would produce a specific result |

"Correlation does not establish causation" applies only to proposed mechanisms, causal claims and policy predictions. A correlation the authors reported without a causal interpretation is never presented as their causal inference. It is never recorded as a criticism of whether a reported correlation is accurate.

Words such as *debunk*, *toxic*, *cherry-picking*, *proves* and *disproves* appear only inside quotations attributed to an identified source. Findings use neutral phrasing: "was correlated with", "the result changed when", "data were not sufficiently comparable to assess".

## Principles

### Provenance before analysis
Every file is stored exactly as downloaded, with URL, UTC timestamp, SHA-256 checksum and licence terms. Raw folders are never overwritten.

### Wilkinson's sources first
The source lineage records, for each indicator, the source Wilkinson and Pickett used and the newest release of that same series. Where a series has ended, it names the closest successor and the reason. Sources are never chosen by the strength of the correlation they produce.

### Declared before examined
The series, years, country rule, index procedure and statistic of the updated reproduction are committed in a **reproduction lock** before any current outcome is correlated with current inequality data. The lock does not cover the historical reproduction, because the original data and correlations are already published. The blinding is procedural only, and the lock records which published results its author had seen. The lock's commit hash is stamped on every report.

### Versioned "current" data
"Current" means the version of each source retrieved during the declared acquisition window, pinned by retrieval time, release or version identifier, query parameters and checksum. A later rerun against revised live data is a new acquisition, not the same analysis.

### No silent choices
Where the original method is undocumented, alternatives are implemented side by side and labelled. The reproductions use no imputation. Outliers are never dropped without reporting both retained and excluded results.

### Attributed controversies only
A controversy enters the register only with four fields: author, exact source title, publication year, and a stable DOI, PMID, PMCID, ISBN or URL. A book also needs its edition. Generic critiques that no named author made are excluded.

### Legal access only
Paywalls and access controls are not bypassed. A restricted item gets a bibliographic record and a note that it was not downloaded.

### Everything from code
Tables, figures, manifests, the data dictionaries and the report are generated by scripts. Acquired data files are stored exactly as acquired, by the smallest official input and the storage method recorded for each source, and the final build is an offline replay from a fresh clone and that documented procedure. Data acquisition is a separate, network-enabled command.

## Controversy register (seed entries)

| Critic | Source | Year | Identifier | Status |
|---|---|---|---|---|
| Ken Judge | "Income distribution and life expectancy: a critical appraisal", *BMJ* | 1995 | PMCID PMC2551188, DOI 10.1136/bmj.311.7015.1282 | To be coded |
| Hugh Gravelle | "How much of the relation between population mortality and unequal distribution of income is a statistical artefact?", *BMJ* | 1998 | PMID 9487182, DOI 10.1136/bmj.316.7128.382 | To be coded |

Both predate *The Spirit Level* and address the income inequality and health hypothesis in general. They enter the register as general-hypothesis criticisms, each with a stated mapping to the result it bears on.

Further entries are added only with all four fields complete. Supporting literature is stored separately from criticism.

## Facts that must be verified before use

Each item is logged in `docs/source_verification/` with the passage, table or file it was verified from. Differences between reproduced and reported values go to `outputs/diagnostics/historical_reproduction_discrepancies.md`.

- [ ] The source Wilkinson and Pickett used for each indicator, and whether the series still exists.
- [ ] Whether the original material contains an analysis of U.S. states.
- [ ] Criteria by which the original countries were selected. Inferred from the released 23 countries until the book is obtained.
- [ ] Original country list and per-outcome sample sizes. No secondary-source count (21, 22 or 23) is used as a target.
- [ ] Original inequality measure and reference year.
- [ ] Original direction coding of each index component, recovered from original materials. The 2024 appendix's coding is recorded separately as update documentation.
- [ ] Original handling of missing index components.
- [ ] Details of the 2024 update, extracted from the [technical appendix](https://eprints.whiterose.ac.uk/id/eprint/215026/7/Technical_Appendix_20_07.pdf) (sample, inequality year, Gini versus 80:20).
- [ ] Current availability and terms of the Equality Trust data files. The international file was downloaded on 18 October 2026, and the U.S. state file is still to be obtained. This is the first task, because the historical reproduction depends on it.

## Planned repository layout

The full layout and file ownership are in [IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md). Data files are stored exactly as acquired, by a storage method chosen per source, and their checksums are recorded in the manifests. Whether files above 50 MiB use Git LFS is still open. `sources/supporting/` and `sources/controversies/` are the two packages. Every legally obtainable text is downloaded. Texts whose licence permits redistribution are attached to GitHub releases and mirrored on Zenodo. Other texts are identified by DOI or an archived URL and the hash of the downloaded file, which is kept locally outside git.

## Reproducibility

Every result that rests on redistributable data is reproducible from a clone, `make fetch-data` and the documented verification procedure. Results that depend on restricted inputs, such as data that require registration, carry the label `RESTRICTED INPUT` and list what a person must obtain locally. Results are replayed locally with `make all`.

```text
data/
  00_original_released/        # original files as downloaded
  00_original_reconstruction/  # sources for a reconstruction, if needed
  01_raw_current/              # current data as downloaded
  03_analysis_ready/
  04_controversy_test_data/
  local_data_required/         # per thread, files a person must obtain by hand
  metadata/manifests/          # URL, UTC time, SHA-256, size and licence per file
sources/
  supporting/                  # original-authors/, academic/, non-academic/, manifest, README, screening log
  controversies/               # academic/, non-academic/, responses/, manifest, README, screening log
code/                          # numbered Python scripts, shared helpers in code/lib/
tests/
docs/
  source_lineage.csv           # Wilkinson's source per indicator and its current release
  reproduction_lock.md         # committed before the updated reproduction
  controversy_register.md
  claims_register.csv          # statements by Wilkinson and Pickett, classified
  controversy_data_map.csv     # datasets for each testable controversy
  goal_traceability.csv        # owner, output and acceptance test per goal
  source_verification/
  data_dictionary_original.md
  data_dictionary_updated_reproduction.md
site/                          # Quarto report and results website
outputs/
```

## Running it

Commands will work once the scripts exist.

```text
git clone https://github.com/open-reanalysis/how-economic-inequality-harms-societies.git
make fetch-data       # fetches the project's LFS files and release assets and checks their hashes
make verify-data      # checks every stored data file against the manifest
make all              # offline, regenerates tables, figures and report
make clean-env        # fresh clone and locked environment, fetch-data, verify-data, then make all
make acquire          # contacts live sources, used only to add new data
```

## Definition of done

1. The current version of every dataset Wilkinson and Pickett used is downloaded, with its original source recorded in the source lineage.
2. Their findings are reproduced from the released data and by their own method on the current data, with every difference logged.
3. The supporting source package is downloaded, academic and non-academic.
4. The controversy source package is downloaded, with the frozen controversy register.
5. The controversy datasets are downloaded for every register row that names data, each linked to its controversies.
6. Original data are preserved, checksummed and analysed under the access label the evidence supports, with every retrieval attempt recorded. Access failure never permits silent substitution.
7. The reproduction lock is committed before the updated reproduction.
8. Every statement in the claims register has a checked source and a class, or is marked to be verified.
9. Every result states its dataset versions, country sample, year ranges, source IDs and reproduction-lock commit hash.
10. All scripts run end to end from a fresh clone in offline replay, and results from restricted inputs are labelled `RESTRICTED INPUT`.
11. The five deliverables are released as `deliverables-v1`.
12. As an addition, results are published on GitHub Pages from a tagged release.

## Contributing

Issues are welcome at any time. See [CONTRIBUTING.md](CONTRIBUTING.md) for how the project works, including how to propose a controversy.

## Licence and citation

Code and tests are licensed under the [MIT License](LICENSE). Documents, the report, the website, figures and result tables are licensed under [CC BY 4.0](LICENSE-docs). Raw data and third-party full texts are not covered by either licence. A derived table or figure that contains a source's values follows that source's terms where they are stricter than CC BY 4.0. These exceptions are listed in `outputs/LICENSE_EXCEPTIONS.md`. Each source keeps its own licence, recorded in its manifest entry. Citation metadata will be added with the first tagged release.
