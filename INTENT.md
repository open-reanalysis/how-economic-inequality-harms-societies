# Intent

## Goals and priorities

The project has five goals, in this order of priority.

1. Download the current version of every dataset Wilkinson and Pickett used.
2. Reproduce their findings, both from the data they released and by applying their documented method to the current version of the same data.
3. Download a package of sources supporting their findings, academic and non-academic.
4. Download a package of sources setting out controversies about their findings.
5. Download datasets that may support those controversies.

Milestone 2 ends with an independent release of the five deliverables, which completes the original assignment on its own. The project keeps two additions beyond the goals. The author claims register records and classifies what Wilkinson and Pickett claim. The report and the website publish the results. Neither delays a goal. If the original material contains an analysis of U.S. states, that analysis is part of goals 1 and 2, as a second dataset for the same hypothesis that is always reported separately from the country analysis.

## Purpose

This project is a transparent, reproducible examination of Richard Wilkinson and Kate Pickett's macro-comparative analyses in *The Spirit Level*. It is not an attempt to prove or disprove the authors. It produces two result families and keeps them separate in every table, figure and sentence. The first is whether the data the authors released produce the correlations they reported. The second is whether their documented method, applied unchanged to the current release of the same data, produces comparable correlations today.

Beside the results it delivers two documented collections. The source packages gather the evidence that supports the findings and the controversies about them. The registers record each controversy and each claim of the authors with its source. The project tests neither the controversies nor causality. It documents them, and the controversy datasets make later tests possible.

## Research questions

**Historical reproduction.** Can the reported correlations and the composite Health and Social Problems Index be reproduced from the data Wilkinson and Pickett released? The answer carries one of four labels depending on what original material is accessible today, `DIRECT REPRODUCTION`, `PARTIAL REPRODUCTION`, `ARCHIVE-BASED RECONSTRUCTION` or `INDEPENDENT RECONSTRUCTION`, and that label appears on every historical reproduction output.

**Updated reproduction.** Does the original method, applied unchanged to the current release of the same data, reproduce the reported correlations and the index? It runs under a small reproduction lock that fixes only what the original method leaves open for current data. It has two results. The fixed-sample result keeps the verified historical sample. The eligibility-refreshed result applies the verified original selection rule at the current reference date, and for the countries it waits until the book confirms that rule. Any changed sample, outcome, measure or model is a modern extension, not a reproduction.

## Terminology that the whole project follows

The project distinguishes five things. A reported correlation is what the authors computed. Robustness is whether that correlation survives reasonable alternative choices. A mechanism is an explanation of why the correlation might exist. A causal claim says changing inequality would change outcomes. A policy prediction says a specific intervention would produce a specific result.

"Correlation does not establish causation" belongs only under proposed mechanisms, causal claims and policy predictions. It is never recorded as a criticism of the accuracy of a reported correlation.

The rule also runs the other way. A descriptive correlation that Wilkinson and Pickett reported without a causal interpretation is never presented as their causal inference. Where they did advance a causal claim, as with the theories and hypotheses behind the correlations, that claim is recorded as theirs.

The project's own results are correlations and are described as correlations. The words "causes" and "does not cause" appear only inside a claim attributed to its source.

Words such as debunk, toxic, cherry-picking, proves and disproves appear only inside quotations attributed to an identified source. Findings use neutral phrasing such as "was correlated with", "the result changed when" and "data were not sufficiently comparable to assess".

## Principles

**Provenance before analysis.** Every file is stored exactly as downloaded, with URL, UTC timestamp, SHA-256 checksum and licence terms. Nothing in a raw folder is ever overwritten.

**Wilkinson's sources first.** For each indicator the source lineage records the source Wilkinson and Pickett used, from the released data and the authors' published notes on sources and methods, and the newest release of that same series. Where a series has ended or changed definition, the lineage names the closest successor and the reason. No other source replaces theirs without a recorded reason, and a source is never chosen by the strength of the correlation it produces. Each current series is classed as an exact successor, a conceptual successor, a substitute, as having no current equivalent, or as not yet verified. A substitute measure never replaces the original one in the strict updated reproduction. It appears only in a separately labelled result.

**Declared before examined.** The series, reference years, lag, country rule, index procedure and statistic that the updated reproduction uses are committed as a reproduction lock before anyone computes, views or infers an association between current inequality data and current outcome data. The blinding is procedural only. The original correlations and the 2024 update's correlations are published, so the lock records which of them its author had seen. The lock's commit hash is recorded in every current result and in the report.

**Versioned current data.** Current means the version of each source retrieved during the declared acquisition window. Each dataset is pinned by retrieval timestamp, release or version identifier where available, query parameters, raw-file checksum and source metadata. A later rerun against revised live data is a new acquisition, not the same analysis.

**No silent choices.** Where the original method is undocumented, alternatives are implemented side by side and labelled. The reproductions use no imputation. Outliers are never deleted without reporting both the retained and excluded results.

**Attributed controversies only.** A controversy enters the register only with four fields filled in. These are the source's author, the exact title, the publication year and a stable DOI, PMID, PMCID, ISBN or URL. A book also needs its edition and year, checked against the publisher's or a library's record. Generic critiques that no named author made are excluded. A controversy found after the register is frozen is added in a dated amendment.

**Attributed author claims.** A statement by Wilkinson or Pickett enters the claims register only with the same four fields, which may be an ISBN for a book, together with its page or chapter. A book also needs its edition, checked against the publisher's or a library's record. Its wording is a short verbatim quotation or a concise paraphrase marked as such. A statement whose source has not been checked is marked to be verified and is not classified.

**Legal access only.** Paywalls and access controls are not bypassed. A restricted item gets its bibliographic record and a note that it was not downloaded.

**Everything from code.** Final tables, figures, manifests, the data dictionaries and the report are generated by scripts. Acquisition and replay are separate commands. Acquired data files are stored exactly as acquired, as the smallest official input that holds what each deliverable needs, by a storage method recorded per source. A clone and the documented acquisition and verification procedure rebuild every package and replay the reproductions offline from checksummed files, and later revisions of live databases cannot change a reproduced result. Restricted material is never committed, and results that depend on it are labelled `RESTRICTED INPUT`.

**Original method only.** Reproduction outputs use only the statistics and procedures the original study documented. The project adds no statistics of its own.

## Corrections carried in from spec review

The draft brief attributed a 1995 BMJ paper to "Richard Gravelle". The criticism register uses the correct authors instead. Ken Judge wrote "Income distribution and life expectancy: a critical appraisal", BMJ 1995, PMCID PMC2551188, PMID 7496240, DOI 10.1136/bmj.311.7015.1282. Hugh Gravelle wrote "How much of the relation between population mortality and unequal distribution of income is a statistical artefact?", BMJ 1998, PMID 9487182, DOI 10.1136/bmj.316.7128.382. These identifiers were checked during plan review and are logged again by the controversy register thread.

The draft fixed the original exercise at 21 countries and treated r ≈ 0.85 as a benchmark. Neither number is used as a target, and no country count from a secondary source is used as a benchmark. The original country list, the usable country set for each outcome and the composite-index sample remain unresolved until verified from primary documentation or a provenance-verified original data release. Reconstructed sample sizes and coefficients are reported exactly as observed.

Claims about the 2024 update rely on the technical appendix to *The Spirit Level at 15*, not the main report. These are the 22-country sample including Germany and Israel and excluding Singapore as a non-OECD country, the 2013 inequality reference year, the original book's use of the 80:20 ratio, and the update's use of the Gini coefficient alongside 80:20 correlations for comparison. The appendix is at https://eprints.whiterose.ac.uk/id/eprint/215026/7/Technical_Appendix_20_07.pdf. Before these details are used, the relevant passages, table definitions, country list and reference-year statements are extracted from the appendix and recorded in the source-verification log.

*The Spirit Level* itself cannot be obtained on the project's timetable. Until it is, the authors' published notes on sources and methods, the released data with its sources sheet, and their answers to questions stand in for it. The claims they state are taken as the authors' claims, and every fact only the book could confirm is marked to be verified.

Access to the original Equality Trust data is a gate, not an assumption. A 2017 Equality Trust post says the data can be downloaded, which does not establish that the files are available today, complete, or identical to the historical release.

## Facts that must be verified before use

Each of these is recorded in the source-verification log with the passage, table or file it was verified from. The source Wilkinson and Pickett used for each indicator and for the inequality measure, and whether that series still exists. Whether the original material contains an analysis of U.S. states. The criteria by which the original countries were selected, which are inferred from the released 23 countries until the book confirms them. The original country list, per-outcome usable samples and composite-index sample. The original inequality measure and its year. The direction coding of every original index component, recovered from original materials and fixed per measure rather than per concept, since for example an intergenerational elasticity and a mobility index point in opposite directions. The 2024 appendix's direction coding is recorded separately as update-method documentation and is not taken as evidence of the original coding. The original handling of missing components in the index. The original timing, which the 2024 appendix describes as an inequality measure averaged from values reported in 2003 to 2006 and measured in 1992 to 2001, with outcomes from 1999 to 2004. This is the authors' later description and is checked against the notes on sources and methods. The meaning of the term 80:20. The appendix calls it a decile ratio, while the authors' notes describe the book's measure as the 20:20 ratio of the incomes of the richest and the poorest fifths, averaged from the UN Human Development Reports of 2003 to 2006. The notes' description is used until the book is checked. The details of the 2024 update listed above, including its index built as the mean of available z-scores, with 17 countries having all ten indicators and 5 lacking the mental illness indicator. The current availability and terms of the Equality Trust data files.

## Done means

The five goals come first. The current version of every dataset Wilkinson and Pickett used is downloaded, with the original source and the current release of each series recorded side by side in the source lineage, or the reason a series could not be updated. Their findings are reproduced from the released data and from the current data by their own method, with every difference logged. The supporting and the controversy source packages are downloaded, with every legally obtainable text held and a README for each package saying what it holds and what it lacks. The controversy datasets are downloaded for every row of the frozen register that names data, and each package is linked to at least one controversy.

Original data are preserved, checksummed and analysed under the access label the evidence supports, with every retrieval attempt recorded. Every non-reproduction, original or updated, is explained in an auditable discrepancy log. Access failure does not allow silent substitution or a claim that the corresponding outcome was reproduced.

The reproduction lock is committed before the updated reproduction. Every controversy is attributed to an identifiable source. Every statement by Wilkinson and Pickett in the claims register has a checked source and a class, or is marked to be verified.

Every final result identifies its exact dataset version, country sample, outcome-year range, inequality-year range, source IDs, component availability and reproduction-lock commit hash.

The final clean build is an offline replay from a fresh clone, using only the project's stored and checksummed data files, fetched where they are not in git, plus any restricted files held locally. It generates the final tables, figures, manifests, data dictionaries and report.

The five deliverables are released as `deliverables-v1` at the end of milestone 2, and that release completes the original assignment. As an addition, the report is published as a website on GitHub Pages, with links to the release and the repository, built from a tagged release and stating the release tag, the reproduction lock commit and the commit it was built from.
