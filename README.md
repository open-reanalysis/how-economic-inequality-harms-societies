# How Economic Inequality Harms Societies: an Open Reanalysis

A transparent, reproducible examination of the macro-comparative analyses in Richard Wilkinson and Kate Pickett's *The Spirit Level*. The project does not set out to prove or disprove the authors. The research method is in [RESEARCH-METHOD.md](RESEARCH-METHOD.md), the goals and scope in [INTENT.md](INTENT.md), and the implementation in [IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md). This page summarises them.

## Goals

1. Download the current version of every dataset Wilkinson and Pickett used.
2. Reproduce their findings, from the released data and by their own method on the current data.
3. Download a package of sources supporting their findings, academic and non-academic.
4. Download a package of sources setting out controversies about their findings.
5. Download datasets that may support those controversies.
6. Publish the results on a GitHub Pages site.

The deliverables of goals 1 to 5 are released together as `deliverables-v1`, with a headline table and a short summary of the deviations, and the site publishes the results later. The project also keeps a register of the authors' claims, which never delays a goal.

> **Status: pre-release.** Nothing has been analysed yet. No updated-reproduction result is produced before the reproduction lock (see [prospective decisions](RESEARCH-METHOD.md#prospective-decisions-corrections-and-validation)) is committed.

## The results

Every comparison the authors reported for their international and U.S. state data, including those with average income, is listed once in `config/results_catalogue.csv` and attempted in four ways. Each comparison and variant remains visible with a specific reason when it cannot be produced.

| Result | Data and sample | Role |
|---|---|---|
| **Historical reproduction** | The released data, or a documented reconstruction, and the original sample | Labelled with the access status of its dataset |
| **Updated reproduction** | Current releases of the same or successor series, original sample | The primary current result |
| **Updated reproduction, refreshed sample** | As above, with the authors' eligibility rule applied to current data | Parallel result |
| **Updated reproduction, with substitutes** | As the primary result, adding substitute measures | Parallel result |

Each result reports its data provenance, sample, series comparability, method deviations and replay state separately. A headline table puts the published, the historical and the updated value of each comparison side by side.

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
| Mechanism | An explanation of why a correlation might exist |
| Causal claim | Changing inequality would change outcomes |
| Policy prediction | A specific intervention would produce a specific result |

"Correlation does not establish causation" applies only to proposed mechanisms, causal claims and policy predictions. A correlation the authors reported without a causal interpretation is never presented as their causal inference. It is never recorded as a criticism of whether a reported correlation is accurate.

Words such as *debunk*, *toxic*, *cherry-picking*, *proves* and *disproves* appear only inside quotations attributed to an identified source. Findings use neutral phrasing: "was correlated with", "the result changed when", "data were not sufficiently comparable to assess".

## Principles

These summarise the principles in [INTENT.md](INTENT.md) and the rules in the research method.

- **Wilkinson and Pickett's sources first.** Each variable is traced to the source the authors used and its current successor.
- **One specification.** Every computation rule is written once in a machine-readable analysis specification.
- **Declared before examined.** The current specifications are fixed in a reproduction lock before any current association is computed.
- **No silent choices.** Open points are filled by assumptions approved in advance, and every deviation is reported.
- **Provenance before analysis.** Acquired files are stored as received and never modified, and every computation has a run record.
- **Attributed controversies only.** A controversy enters the register only with an identifiable author, title, year and stable identifier.
- **Legal access only.** Paywalls and access controls are not bypassed.

## Controversy register (seed entries)

| Critic | Source | Year | Identifier | Status |
|---|---|---|---|---|
| Ken Judge | "Income distribution and life expectancy: a critical appraisal", *BMJ* | 1995 | PMCID PMC2551188, DOI 10.1136/bmj.311.7015.1282 | To be coded |
| Hugh Gravelle | "How much of the relation between population mortality and unequal distribution of income is a statistical artefact?", *BMJ* | 1998 | PMID 9487182, DOI 10.1136/bmj.316.7128.382 | To be coded |

Both predate *The Spirit Level* and address the income inequality and health hypothesis in general. They enter the register as general-hypothesis criticisms, each with a stated mapping to the result it bears on.

Further entries are added only with all four fields complete. Supporting literature is stored separately from criticism.

## Facts to establish

The facts the method must establish before use, such as the authors' sources, the eligibility details, the direction coding and the handling of missing index components, are listed in [RESEARCH-METHOD.md](RESEARCH-METHOD.md#historical-evidence-and-reconstruction). The international file was downloaded on 18 October 2026, and the U.S. state file is still to be obtained.

## Planned repository layout

The full layout and file ownership are in [IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md). Data files are stored exactly as acquired in git, and their size and checksum are recorded in their acquisition records. Bulk archives are not acquired. Only the relevant series are extracted from them. `sources/supporting/` and `sources/controversies/` are the two packages. Every legally obtainable text is downloaded. Texts whose terms allow publishing are published in their package in the repository. Other texts are recorded as sources with their link, DOI or archived URL and the hash of the downloaded file, which is kept locally outside git.

## Reproducibility

Every result that rests on redistributable data is reproducible from a clone and the documented verification procedure. Results that depend on restricted inputs, such as data that require registration, carry the label `RESTRICTED INPUT` and list what a person must obtain locally. Results are replayed locally with `make all`. Each result is reported as computed in the run, retained because a required input was missing, or not produced.

```text
data/
  00_original_released/        # original files as downloaded
  00_original_reconstruction/  # sources for a reconstruction, if needed
  01_raw_current/              # current data as downloaded
  02_extracts/                 # relevant series extracted from stored responses
  03_analysis_ready/
  04_controversy_test_data/
  local_data_required/         # per thread, files a person must obtain by hand
  metadata/sources/            # one record per data source
  metadata/acquisitions/       # one record per request, with its files, sizes and SHA-256
config/
  specs/                       # analysis specifications, the single source of computation rules
  results_catalogue.csv        # every comparison that is computed and reported
  units/                       # registries of countries and U.S. states
sources/
  supporting/                  # original-authors/, academic/, non-academic/, responses/, manifest, README, search and screening logs
  controversies/               # academic/, books/, reports/, responses/, manifest, README, search and screening logs
code/                          # thin numbered scripts, readers and computation core in code/lib/
tests/                         # compute, readers, integrity, e2e, replay, eligibility, report
templates/                     # templates for specifications, records and package tables
RESEARCH-METHOD.md             # the research method
docs/
  source_lineage.csv           # meaning, original and current data source per variable
  method_rationale.md          # sources and reasons for the rules in the specifications
  reproduction_lock.md         # identifies the locked specifications
  worklist.md                  # schedule and decisions of the current run
  ownership/                   # paths owned by each thread
  controversy_register.csv
  claims_register.csv          # statements by Wilkinson and Pickett, classified
  controversy_data_map.csv     # datasets for each testable controversy
  goal_traceability.csv        # owner, output and acceptance test per goal
  source_verification/
report/                        # prose of the report sections
site/                          # generated report published on GitHub Pages
outputs/                       # tables, observations/, figures/, diagnostics/ and runs/ with run records
```

## Running it

Commands will work once the scripts exist.

```text
git clone https://github.com/open-reanalysis/how-economic-inequality-harms-societies.git
make verify-data      # checks every stored data file against its acquisition record
make test             # computation, reader and end-to-end tests, offline
make check-data       # schemas, keys, units, references and join row counts
make storage-report   # data and repository size against the review thresholds
make all              # offline, regenerates tables, figures, headline table and site
make clean-env        # fresh clone and locked environment, verify-data, then make all
make acquire          # contacts live sources, used only to add new data
```

## Definition of done

The completion criteria are in [INTENT.md](INTENT.md#done-means), and each goal's acceptance test is in [IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md#goals-and-priorities).

## Contributing

Issues are welcome at any time. See [CONTRIBUTING.md](CONTRIBUTING.md) for how the project works, including how to propose a controversy.

## Licence and citation

Code and tests are licensed under the [MIT License](LICENSE). Documents, the report, the website, figures and the project's own data collection are licensed under [CC BY 4.0](LICENSE-docs). The data collection is the project's own, assembled from extracts that stay below the threshold of originality and take no substantial part of any database, and from values the project derives. Data and texts fetched from elsewhere are published as they are, under their own terms, which are recorded with each source. Material whose terms do not allow publishing is handled locally and recorded as a source with its link. Citation metadata will be added with the first tagged release.
