# Intent

## Goals and priorities

The project has six goals, in this order of priority.

1. Download the current version of every dataset Wilkinson and Pickett used.
2. Reproduce their findings, both from the data they released and by applying their documented method to the current version of the same data.
3. Download a package of sources supporting their findings, academic and non-academic.
4. Download a package of sources setting out controversies about their findings.
5. Download datasets that may support those controversies.
6. Publish the results on a GitHub Pages site.

Milestone 2 ends with an independent release of the deliverables of goals 1 to 5. Milestone 3 publishes the results on the site. The project keeps one addition beyond the goals. The author claims register records and classifies what Wilkinson and Pickett claim, and it never delays a goal. The original material contains an analysis of the U.S. states, as the authors' notes on sources and methods show. That analysis is part of goals 1 and 2, as a second dataset for the same hypothesis that is always reported separately from the country analysis.

## Purpose

This project is a transparent, reproducible examination of Richard Wilkinson and Kate Pickett's macro-comparative analyses in *The Spirit Level*. It is not an attempt to prove or disprove the authors. It produces two result families and keeps them separate in every table, figure and sentence. The first is whether the data the authors released produce the correlations they reported. The second is whether their documented method, applied unchanged to the current release of the same data, produces comparable correlations today.

Beside the results it delivers two documented collections. The source packages gather the evidence that supports the findings and the controversies about them. The registers record each controversy and each claim of the authors with its source. The project tests neither the controversies nor causality. It documents them, and the controversy datasets make later tests possible.

## Research questions

**Historical reproduction.** Can the reported correlations and the composite Health and Social Problems Index be reproduced from the data Wilkinson and Pickett released? The answer carries one of four labels depending on what original material is accessible today, `DIRECT REPRODUCTION`, `PARTIAL REPRODUCTION`, `ARCHIVE-BASED RECONSTRUCTION` or `INDEPENDENT RECONSTRUCTION`, and that label appears on every historical reproduction output.

**Updated reproduction.** Does the original method, applied unchanged to the current release of the same data, reproduce the reported correlations and the index? Its analysis specifications are fixed, and identified in a reproduction lock, before any current association is computed. It has three results. The fixed-sample result keeps the verified historical sample, and a separately labelled version of it adds substitute measures. The eligibility-refreshed result applies the authors' stated selection rule to current data. For the countries the rule is the 50 richest countries with more than 3 million people and comparable income distribution data. Outcome data never decide which country is eligible. Any changed sample, outcome, measure or model is a modern extension, not a reproduction.

## Terminology that the whole project follows

The project distinguishes four things. A reported correlation is what the authors computed. A mechanism is an explanation of why the correlation might exist. A causal claim says changing inequality would change outcomes. A policy prediction says a specific intervention would produce a specific result.

"Correlation does not establish causation" belongs only under proposed mechanisms, causal claims and policy predictions. It is never recorded as a criticism of the accuracy of a reported correlation.

The rule also runs the other way. A descriptive correlation that Wilkinson and Pickett reported without a causal interpretation is never presented as their causal inference. Where they did advance a causal claim, as with the theories and hypotheses behind the correlations, that claim is recorded as theirs.

The project's own results are correlations and are described as correlations. The words "causes" and "does not cause" appear only inside a claim attributed to its source.

Words such as debunk, toxic, cherry-picking, proves and disproves appear only inside quotations attributed to an identified source. Findings use neutral phrasing such as "was correlated with", "the result changed when" and "data were not sufficiently comparable to assess".

## Principles

**Provenance before analysis.** Every file is stored exactly as downloaded, with URL, UTC timestamp, SHA-256 checksum and licence terms. Nothing in a raw folder is ever overwritten.

**Wilkinson and Pickett's sources first.** For each indicator the source lineage records the source Wilkinson and Pickett used, from the released data and the authors' published notes on sources and methods, and the newest release of that same series. Where a series has ended or changed definition, the lineage names the closest successor and the reason. No other source replaces theirs without a recorded reason, and a source is never chosen by the strength of the correlation it produces. Each current series is classed as an exact successor, a conceptual successor, a substitute, as having no current equivalent, or as not yet verified. A substitute measure never replaces the original one in the updated reproduction. It appears only in a separately labelled result.

**One specification.** Every rule the computation uses, from the sample and the years to unit conversions, direction coding, missing values, standardisation, the index and the statistics, is written once in a machine-readable analysis specification. The method rationale explains the source and the reason for each rule without restating it, and the code reads the rules instead of repeating them.

**Declared before examined.** The analysis specifications of the updated reproduction are fixed, and the reproduction lock identifies them by ID, version and checksum, before anyone computes, views or infers an association between current inequality data and current outcome data. The blinding is procedural only. The original correlations and the 2024 update's correlations are published, so the lock records which of them its author had seen. Every current result names its specification and version, and the report states the lock commit.

**Versioned current data.** Current means the version of each source retrieved during the declared acquisition window. Each dataset is pinned by retrieval timestamp, release or version identifier where available, query parameters, raw-file checksum and source metadata. A later rerun against revised live data is a new acquisition, not the same analysis.

**No silent choices.** Where the original method is undocumented, the analysis specification records one choice and the method rationale its reasons. Where two sources give values for the same variable, they are compared, the comparison is published, and they are combined into the project's own series by a rule recorded before any correlation is computed. The primary source keeps its values, the other fills only gaps, and values are never averaged. The reproductions use no imputation and delete no outliers.

**Attributed controversies only.** A controversy enters the register only with four fields filled in. These are the source's author, the exact title, the publication year and a stable DOI, PMID, PMCID, ISBN or URL. A book also needs its edition and year, checked against the publisher's or a library's record. Generic critiques that no named author made are excluded. A controversy found after the register is frozen is added in a dated amendment.

**Attributed author claims.** A statement by Wilkinson or Pickett enters the claims register only with the same four fields, which may be an ISBN for a book, together with its page or chapter. A book also needs its edition, checked against the publisher's or a library's record. Its wording is a short verbatim quotation or a concise paraphrase marked as such. A statement whose source has not been checked is marked to be verified and is not classified.

**Legal access only.** Paywalls and access controls are not bypassed. A restricted item gets its bibliographic record and a note that it was not downloaded. A legally obtained item whose terms do not allow publishing is handled locally and recorded as a source with its link.

**Publish what may be published.** Material whose terms allow publishing is published in the repository as it was obtained, under its own terms. From material that may not be published, the project extracts only values below the threshold of originality and never a substantial part of a database. The project's own data collection, assembled from such extracts and from derived values, is published under CC BY 4.0.

**Everything from code.** Final tables, figures, metadata views and the report are generated by scripts. Acquisition and replay are separate commands. Acquired data files are stored exactly as acquired, as the smallest official input that holds what each deliverable needs, and are never modified. Derived files are rebuilt in place, and a run record identifies the code, specification and inputs of every computation. Metadata may be corrected, and git keeps every earlier version. A clone and the documented acquisition and verification procedure rebuild every package and replay the reproductions offline from checksummed files, and later revisions of live databases cannot change a reproduced result. Restricted material is never committed, and results that depend on it are labelled `RESTRICTED INPUT`. Every result states whether it was computed in the run, retained because a required input was missing, or could not be produced, and whether its inputs were checked from the files themselves or only from their recorded checksums.

**Original method only.** Reproduction outputs use only the statistics and procedures the original study documented. The project adds no statistics of its own.

## Corrections carried in from spec review

The draft brief attributed a 1995 BMJ paper to "Richard Gravelle". The criticism register uses the correct authors instead. Ken Judge wrote "Income distribution and life expectancy: a critical appraisal", BMJ 1995, PMCID PMC2551188, PMID 7496240, DOI 10.1136/bmj.311.7015.1282. Hugh Gravelle wrote "How much of the relation between population mortality and unequal distribution of income is a statistical artefact?", BMJ 1998, PMID 9487182, DOI 10.1136/bmj.316.7128.382. These identifiers were checked during plan review and are logged again by the controversy register thread.

The draft fixed the original exercise at 21 countries and treated r ≈ 0.85 as a benchmark. Neither number is used as a target, and no country count from a secondary source is used as a benchmark. The original country list, the usable country set for each outcome and the composite-index sample remain unresolved until verified from primary documentation or a provenance-verified original data release. Reconstructed sample sizes and coefficients are reported exactly as observed.

The technical appendix to *The Spirit Level at 15*, at https://eprints.whiterose.ac.uk/id/eprint/215026/7/Technical_Appendix_20_07.pdf, is used only for what it says about the original method, its timing and the meaning of 80:20. Those passages are recorded in the source-verification log before they are used.

*The Spirit Level* itself is not used. The authors' published notes on sources and methods, the released data with its sources sheet, and their answers to questions stand in for it. The claims they state are taken as the authors' claims. Its absence is reported as a limitation. Where this material leaves a point of the original method open, the user approves a sufficient set of assumptions before the run, and only a point they do not cover is decided during it. The choice is recorded in the analysis specification and its reason in the method rationale.

Access to the original Equality Trust data is a gate, not an assumption. A 2017 Equality Trust post says the data can be downloaded, which does not establish that the files are available today, complete, or identical to the historical release.

## Facts that must be verified before use

Each of these is recorded in the source-verification log with the passage, table or file it was verified from. Where the material does not settle one, the method rationale records the agreed choice and the analysis specification holds it. The source Wilkinson and Pickett used for each indicator and for the inequality measure, and whether that series still exists. The measure and data vintage by which the 50 richest countries were ranked, and the source that counted as comparable income distribution data, which complete the selection rule the authors stated in their 2010 responses. The original country list, per-outcome usable samples and composite-index sample. The original inequality measure and its year. The direction coding of every original index component, recovered from original materials and fixed per measure rather than per concept, since for example an intergenerational elasticity and a mobility index point in opposite directions. The original handling of missing components in the index. The original timing, which the 2024 appendix describes as an inequality measure averaged from values reported in 2003 to 2006 and measured in 1992 to 2001, with outcomes from 1999 to 2004. This is the authors' later description and is checked against the notes on sources and methods. The meaning of the term 80:20. The appendix calls it a decile ratio, while the authors' notes describe the book's measure as the 20:20 ratio of the incomes of the richest and the poorest fifths, averaged from the UN Human Development Reports of 2003 to 2006. The notes' description is used. The current availability and terms of the Equality Trust data files.

## Done means

The six goals come first. The current version of every dataset Wilkinson and Pickett used is downloaded, with the original source and the current release of each series recorded side by side in the source lineage, or the reason a series could not be updated. Their findings are reproduced from the released data and from the current data by their own method, with every difference logged. The supporting and the controversy source packages are downloaded, with every legally obtainable text held and a README for each package saying what it holds and what it lacks. Every row of the frozen register with a testable statement has a data map row whose datasets are downloaded or whose barrier is documented, and each dataset package is linked to at least one controversy.

Original data are preserved, checksummed and analysed under the access label the evidence supports, with every retrieval attempt recorded. Every non-reproduction, original or updated, is explained in an auditable discrepancy log. Access failure does not allow silent substitution or a claim that the corresponding outcome was reproduced.

The reproduction lock is committed before the updated reproduction. Every controversy is attributed to an identifiable source. Every statement by Wilkinson and Pickett in the claims register has a checked source and a class, or is marked to be verified.

Every final result identifies its analysis specification and version, its data sources, sample, years, missing units and component availability, and its run record states how it was produced.

The final clean build is an offline replay from a fresh clone, using only the project's stored and checksummed data files, which all arrive with the clone, plus any restricted files held locally. It generates the final tables, figures, metadata views and report.

The deliverables of goals 1 to 5 are released as `deliverables-v1` at the end of milestone 2. For goal 6 the report is published as a website on GitHub Pages, with links to the release and the repository, built from a tagged release and stating the release tag, the reproduction lock commit and the commit it was built from.
