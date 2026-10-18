# How Economic Inequality Harms Societies: an Open Reanalysis

A transparent, reproducible examination of the macro-comparative analyses in Richard Wilkinson and Kate Pickett's *The Spirit Level*. The project does not set out to prove or disprove the authors. It produces four separate results and keeps them separate in every table, figure and sentence.

> **Status: pre-release.** Nothing has been analysed yet. The analysis lock (see [Declared before examined](#declared-before-examined)) has not been committed. No result is reported until it has.

## The results

| Result | Question | Label used in outputs |
|---|---|---|
| **Original reproduction** | Do the data Wilkinson and Pickett released reproduce the correlations and the composite Health and Social Problems Index they reported? The label depends on what original material is accessible today. | `DIRECT REPRODUCTION`, `PARTIAL REPRODUCTION`, `ARCHIVE-BASED RECONSTRUCTION` or `INDEPENDENT RECONSTRUCTION` |
| **Current replication** | Using current data, a pre-specified country sample and a pre-specified source hierarchy, are comparable cross-sectional correlations present today? | `CURRENT` |
| **Sensitivity** | Do the original reproduction or the current replication change under alternatives that a named source has raised, whether a critic, the original authors or an independent researcher, or that the analysis lock declares with a stated rationale? | `SENSITIVITY` + register ID or lock rationale ID |
| **Causal assessment** | Do the causal claims that Wilkinson and Pickett or named critics advance survive designs matched to those claims? | Evidence tier 1 to 4 and one verdict per outcome: `CAUSAL EFFECT SUPPORTED`, `CAUSAL EFFECT NOT SUPPORTED`, `REVERSE OR COMMON-CAUSE PATTERN` or `UNDETERMINED`, with the claim ID. A claim country-level data cannot address is `NOT TESTABLE IN THIS DESIGN` |

A further section, **interpretation**, records what the analysis does and does not establish.

## What the project does and does not claim

1. Descriptive results are reported as correlations.
2. Causal claims are assessed only where the data and a method declared in the analysis lock can support an assessment. Each statement by Wilkinson and Pickett is first classified as a descriptive correlation, a proposed mechanism or a causal claim, and a correlation they reported without a causal interpretation is never presented as their causal inference.
3. Every result states the assumptions it relies on. A causal assessment also states what its design cannot rule out, and a claim that country-level data cannot address is reported as not testable in this design.
4. A causal conclusion is possible in either direction. Each outcome gets one of four verdicts from rules locked before the current data are analysed, and each verdict carries the same burden of proof. A cross-section alone never reaches a causal conclusion, and a null result from an underpowered design is reported as undetermined.
5. The words "causes" and "does not cause" appear only next to a verdict the locked rules produced, with the assumptions it rests on.

## Vocabulary

| Term | Meaning here |
|---|---|
| Reported correlation | What the authors computed |
| Robustness | Whether that correlation survives reasonable alternative choices |
| Mechanism | An explanation of why a correlation might exist |
| Causal claim | Changing inequality would change outcomes |
| Policy prediction | A specific intervention would produce a specific result |

"Correlation does not establish causation" applies only to proposed mechanisms, causal claims and policy predictions. A correlation the authors reported without a causal interpretation is never presented as their causal inference. It is never recorded as a criticism of whether a reported correlation is accurate.

Words such as *debunk*, *toxic*, *cherry-picking*, *proves* and *disproves* appear only inside quotations attributed to an identified source. Findings use neutral phrasing: "was correlated with", "the estimate was sensitive to", "the result changed when", "data were not sufficiently comparable to assess".

Causal readings, mechanisms and policy predictions are reported only when explicitly advanced by Wilkinson and Pickett or another cited source, or as results of a causal design declared in the analysis lock, and each is labelled as an author claim, critic claim or project result.

## Principles

### Provenance before analysis
Every file is stored exactly as downloaded, with URL, UTC timestamp, SHA-256 checksum and licence terms. Raw folders are never overwritten.

### Declared before examined
Country inclusion rules, inequality measure, source hierarchy, year alignment and index construction are written down and committed in an **analysis lock** before any current outcome is correlated with current inequality data. The lock does not cover the original reproduction, because the original data and correlations are already published. The blinding is procedural only, and the lock records which published results its author had seen. The lock's commit hash is stamped on every report. Sources are never chosen by the strength of the correlation they produce.

### Source hierarchy, not fixed sources
For each indicator the lock names a preferred source, permitted fallbacks, minimum comparability conditions and the circumstances that justify a fallback. A fallback is recorded before the outcome is joined to inequality.

### Versioned "current" data
"Current" means the version of each source retrieved during the declared acquisition window, pinned by retrieval time, release or version identifier, query parameters and checksum. A later rerun against revised live data is a new acquisition, not the same analysis.

### No silent choices
Where the original method is undocumented, alternatives are implemented side by side and labelled. The primary analysis uses no imputation. Outliers are never dropped without reporting both retained and excluded results.

### Attributed alternatives, symmetrically
An alternative enters the executable register only with four fields: author, exact source title, publication year, and a stable DOI, PMID, PMCID, ISBN or URL. A book also needs its edition. Generic critiques that no named author made are excluded. Whether the source is a critic, the original authors or an independent researcher never decides whether an alternative is tested, and the lock records in advance which way each test could move the original result.

### Legal access only
Paywalls and access controls are not bypassed. A restricted item gets a bibliographic record and a note that it was not downloaded.

### Everything from code
Tables, figures, manifests, the data dictionary and the report are generated by scripts. Acquired data files are committed exactly as acquired, and the final build is an offline replay from a fresh clone. Data acquisition is a separate, network-enabled command.

## Criticism register (seed entries)

| Critic | Source | Year | Identifier | Status |
|---|---|---|---|---|
| Ken Judge | "Income distribution and life expectancy: a critical appraisal", *BMJ* | 1995 | PMCID PMC2551188, DOI 10.1136/bmj.311.7015.1282 | To be coded |
| Hugh Gravelle | "How much of the relation between population mortality and unequal distribution of income is a statistical artefact?", *BMJ* | 1998 | PMID 9487182, DOI 10.1136/bmj.316.7128.382 | To be coded |

Both predate *The Spirit Level* and address the income inequality and health hypothesis in general. They enter the register as general-hypothesis criticisms, each with a stated mapping to the result it bears on.

Further entries are added only with all four fields complete. Supporting literature is stored separately from criticism.

## Facts that must be verified before use

Each item is logged in `docs/source_verification/` with the passage, table or file it was verified from. Differences between reproduced and reported values go to `outputs/diagnostics/original_reproduction_discrepancies.md`.

- [ ] Original country list and per-outcome sample sizes. No secondary-source count (21, 22 or 23) is used as a target.
- [ ] Original inequality measure and reference year.
- [ ] Original direction coding of each index component, recovered from original materials. The 2024 appendix's coding is recorded separately as update documentation.
- [ ] Original handling of missing index components.
- [ ] Details of the 2024 update, extracted from the [technical appendix](https://eprints.whiterose.ac.uk/id/eprint/215026/7/Technical_Appendix_20_07.pdf) (sample, inequality year, Gini versus 80:20).
- [ ] Current availability and terms of the Equality Trust data files. This is the first task, because the original reproduction depends on it.

## Planned repository layout

The full layout and file ownership are in [IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md). Data files are committed exactly as acquired, files above 50 MiB through Git LFS, and their checksums are recorded in the manifests. Sources are bibliographic records with links. Texts whose licence permits redistribution are attached to GitHub releases and mirrored on Zenodo. Other texts are identified by DOI or an archived URL and the hash of the file read.

## Reproducibility

Every result that rests on redistributable data is reproducible from a clone alone, with no data package, archive or release asset. Results that depend on restricted inputs, such as data that require registration, carry the label `RESTRICTED INPUT` and list what a person must obtain locally. CI replays every step whose inputs are committed and skips steps whose inputs are restricted.

```text
data/
  00_original_released/        # original files as downloaded, committed
  00_original_reconstruction/  # sources for a reconstruction, if needed
  01_raw_current/              # current data as downloaded, committed
  02_harmonised/
  03_analysis_ready/
  04_controversy_test_data/
  metadata/manifests/          # URL, UTC time, SHA-256, size, licence, LFS flag per file
sources/                       # bibliographic records with links, one folder per source type
code/                          # numbered Python and R scripts, shared helpers in code/lib/
tests/
docs/
  analysis_lock.md             # committed before current outcome analysis
  inclusion_rules.md
  controversy_register.md
  claims_register.csv          # statements by Wilkinson and Pickett, classified
  source_verification/
  data_dictionary.md
site/                          # Quarto report and results website
outputs/
```

## Running it

Commands will work once the scripts exist.

```text
git clone https://github.com/open-reanalysis/how-economic-inequality-harms-societies.git
make verify-data      # checks every committed data file against the manifest
make all              # offline, regenerates tables, figures and report
make clean-env        # fresh clone and locked environment, verify-data, then make all
make acquire          # contacts live sources, used only to add new data
```

## Out of scope

- Analysing U.S.-state material in the first release. If the original package contains it, only its existence, file names and provenance are recorded.

## Definition of done

1. Original data are preserved, checksummed and analysed under the access label the evidence supports, with every retrieval attempt recorded.
2. Every required primary dataset is validated, or a predeclared fallback or labelled omission applies. Access failure never permits silent substitution.
3. Original findings are reproduced, or every non-reproduction is explained in the reproduction discrepancy log.
4. The analysis lock is committed before current outcome analysis.
5. Every controversy in the report is attributed to an identifiable source.
6. Every assessed statement by Wilkinson and Pickett is in the claims register with a checked source and a class. Every causal claim is assessed with a declared design that states its assumptions, or marked not testable in this design with the reason. Every outcome has an evidence tier and a verdict with all nine criteria tabulated, and the power simulation and negative-control results are published.
7. Test data for each stated criticism are saved.
8. Every result states its dataset versions, country sample, year ranges, source IDs and lock commit hash.
9. All scripts run end to end from a fresh clone in offline replay, and results from restricted inputs are labelled `RESTRICTED INPUT`.
10. Results are published on GitHub Pages from a tagged release.

## Contributing

Issues and pull requests are welcome at any time. See [CONTRIBUTING.md](CONTRIBUTING.md) for how the project works, including how Python and R divide the work and how to propose a criticism.

## Licence and citation

Code and tests are licensed under the [MIT License](LICENSE). Documents, the report, the website, figures and result tables are licensed under [CC BY 4.0](LICENSE-docs). Raw data and third-party full texts are not covered by either licence. A derived table or figure that contains a source's values follows that source's terms where they are stricter than CC BY 4.0. These exceptions are listed in `outputs/LICENSE_EXCEPTIONS.md`. Each source keeps its own licence, recorded in its manifest entry. Citation metadata will be added with the first tagged release.
