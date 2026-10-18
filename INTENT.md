# Intent

This document sets the project's goals and scope. [RESEARCH-METHOD.md](RESEARCH-METHOD.md) is the research method, and [IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md) the technical implementation and the order of the work. Where this document summarises them, they decide.

## Goals and priorities

The project has six goals, in this order of priority.

1. Download the current version of every dataset Wilkinson and Pickett used.
2. Reproduce their findings, both from the data they released and by applying their documented method to the current version of the same data.
3. Download a package of sources supporting their findings, academic and non-academic.
4. Download a package of sources setting out controversies about their findings.
5. Download datasets that may support those controversies.
6. Publish the results on a GitHub Pages site.

Milestone 2 ends with `deliverables-v1`, a release of goals 1 to 5 that can be read on its own, with a headline table and a short summary of the deviations. It needs neither the site nor a complete U.S. state reconstruction. Milestone 3 publishes the results on the site. The project keeps one addition beyond the goals. The author claims register records and classifies what Wilkinson and Pickett claim, and it never delays a goal.

## Scope

This project is a transparent, reproducible examination of Richard Wilkinson and Kate Pickett's macro-comparative analyses in *The Spirit Level*. It is not an attempt to prove or disprove the authors.

It does three things. It repeats the comparisons the authors reported for their international and U.S. state data, including the comparisons with average income, from the data they released. It updates the same comparisons with current data, with the original sample as the primary result and the authors' eligibility rule and substitute measures as two parallel results. It assembles the source packages, the controversy register and the controversy datasets.

It does not test the controversies, does not assess causality, does not compare its results with the authors' 2024 update, and does not add analyses from the book or later publications that the research method does not include. The country analysis and the U.S. state analysis are always reported separately and never pooled.

## Research questions

**Historical reproduction.** Do the data Wilkinson and Pickett released reproduce the comparisons they reported? Each answer carries the access label of its dataset.

**Updated reproduction.** Does their documented method, applied to the current release of the same data, give comparable results? The primary answer keeps the original sample, and the parallel answers show the effect of the eligibility rule and of substitute measures.

## Terminology that the whole project follows

The project distinguishes four things. A reported correlation is what the authors computed. A mechanism is an explanation of why the correlation might exist. A causal claim says changing inequality would change outcomes. A policy prediction says a specific intervention would produce a specific result.

"Correlation does not establish causation" belongs only under proposed mechanisms, causal claims and policy predictions. It is never recorded as a criticism of the accuracy of a reported correlation.

The rule also runs the other way. A descriptive correlation that Wilkinson and Pickett reported without a causal interpretation is never presented as their causal inference. Where they did advance a causal claim, as with the theories and hypotheses behind the correlations, that claim is recorded as theirs.

The project's own results are correlations and are described as correlations. The words "causes" and "does not cause" appear only inside a claim attributed to its source.

Words such as debunk, toxic, cherry-picking, proves and disproves appear only inside quotations attributed to an identified source. Findings use neutral phrasing such as "was correlated with", "the result changed when" and "data were not sufficiently comparable to assess".

## Principles

These summarise rules set out in the research method and the plan.

- **Wilkinson and Pickett's sources first.** Each variable is traced to the source the authors used and its current successor, and a source is never chosen by the correlation it produces.
- **One specification.** Every computation rule is written once in a machine-readable analysis specification, and its source or reason once in the method rationale.
- **Declared before examined.** The current specifications are fixed in a reproduction lock before any current association is computed.
- **No silent choices.** An open point is filled by an assumption approved before the computation, and every deviation from the original method is reported.
- **Provenance before analysis.** Acquired files are stored as received and never modified, and every computation has a run record.
- **Attributed controversies and claims.** A controversy or a claim enters its register only with an identifiable author, an exact title, a year and a stable identifier, and a claim also with its locator.
- **Legal access only.** Paywalls and access controls are not bypassed. What may not be published is handled locally and recorded as a source with its link.
- **Publish what may be published.** Publishable material is published as obtained, under its own terms, and the project's own data collection under CC BY 4.0.

## Corrections carried in from spec review

The draft brief attributed a 1995 BMJ paper to "Richard Gravelle". Ken Judge wrote "Income distribution and life expectancy: a critical appraisal", BMJ 1995, PMCID PMC2551188, PMID 7496240, DOI 10.1136/bmj.311.7015.1282. Hugh Gravelle wrote "How much of the relation between population mortality and unequal distribution of income is a statistical artefact?", BMJ 1998, PMID 9487182, DOI 10.1136/bmj.316.7128.382. The draft's 21 countries and r ≈ 0.85 are not used as benchmarks.

## Done means

1. The current version of every dataset Wilkinson and Pickett used is downloaded, with its original and current source in the lineage, or the reason a series could not be updated.
2. Every comparison in the result catalogue has a historical result and the three current results, or a documented reason why it could not be produced, and every deviation from a published value is logged. A partial U.S. state reconstruction is documented as partial.
3. The supporting source package is complete under the search protocol, with academic and non-academic sources and its known gaps stated.
4. The controversy source package is complete under the same protocol, with the frozen register.
5. Every testable controversy has its datasets acquired, partially acquired or its barrier documented.
6. The site publishes every result with its figure, observations, sample, sources, comparability and deviations.

Every result names its analysis specification and version, and its run record states whether it was computed, retained or not produced. The deliverables of goals 1 to 5 are released as `deliverables-v1` after a release check from a fresh clone. The claims register has a checked source and a class for every entry, or marks it to be verified.
