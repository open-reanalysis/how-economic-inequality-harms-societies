# Intent

## Purpose

This project is a transparent, reproducible examination of Richard Wilkinson and Kate Pickett's macro-comparative analyses in *The Spirit Level*. It is not an attempt to prove or disprove the authors. It produces four separate results and keeps them separate in every table, figure and sentence.

The first result is whether the original released data produce the correlations the authors reported. The second is whether a comparable association appears in current data under choices declared before the data are examined. The third is whether criticisms made by named authors materially change either result when they are tested empirically. The fourth is whether causal claims advanced by Wilkinson and Pickett or by named critics survive designs matched to those claims, where the data and a declared method can support an assessment.

## Research questions

**A. Original reproduction.** Can the reported correlations and the composite Health and Social Problems Index be reproduced from the data Wilkinson and Pickett released? The answer carries one of four labels depending on what original material is accessible today, ranging from direct reproduction from released data to independent reconstruction, and that label appears on every question A output.

**B. Current descriptive replication.** Using current data, a pre-specified country sample, a pre-specified source hierarchy and documented source-selection rules, are comparable cross-sectional correlations present today?

**C. Sensitivity.** How do the results change under alternatives that a named critic has actually raised? Every alternative is in scope only where a named criticism, a cited alternative explanation or a sensitivity rationale declared in the analysis lock identifies it. This applies equally to country inclusion and expanded samples, inequality metric, index composition, weighting, outlier treatment, time alignment, data comparability, panel models and macro-level covariates. A panel model or a covariate belongs here when it tests the robustness of a descriptive correlation. When it tests a causal claim it belongs to question E.

**D. Interpretation.** What the analysis establishes is reported as such. Correlations are described as correlations. Before any statement by Wilkinson or Pickett is assessed, it is classified as a descriptive correlation, a proposed mechanism or a causal claim, and the class is recorded next to its source in the claims register. Causal readings, alternative mechanisms and policy predictions are reported only when Wilkinson and Pickett or another cited source explicitly advances them, or as results of a causal design this project declared in the analysis lock. Each is identified as an author claim, a critic claim or a result of this project, and all of them are kept apart from questions about whether a descriptive correlation is accurate or robust.

**E. Causal assessment.** Do the causal claims that Wilkinson and Pickett or named critics advance survive designs matched to those claims? Panel models, control variables such as poverty, and the alternatives named critics raise can each serve either as a sensitivity analysis, when they test the robustness of a descriptive correlation, or as part of a causal assessment, when they test a causal claim. The type of every analysis is declared in the analysis lock before any result is examined.

## Terminology that the whole project follows

The project distinguishes five things. A reported correlation is what the authors computed. Robustness is whether that correlation survives reasonable alternative choices. A mechanism is an explanation of why the correlation might exist. A causal claim says changing inequality would change outcomes. A policy prediction says a specific intervention would produce a specific result.

"Correlation does not establish causation" belongs only under proposed mechanisms, causal claims and policy predictions. It is never recorded as a criticism of the accuracy of a reported correlation.

The rule also runs the other way. A descriptive correlation that Wilkinson and Pickett reported without a causal interpretation is never presented as their causal inference. Where they did advance a causal claim, as with the theories and hypotheses behind the correlations, that claim is recorded and assessed as theirs.

Words such as debunk, toxic, cherry-picking, proves and disproves appear only inside quotations attributed to an identified source. Findings use neutral phrasing such as "was correlated with", "the estimate was sensitive to", "the association persisted under", "the result changed when" and "data were not sufficiently comparable to assess".

## Principles

**Provenance before analysis.** Every file is stored exactly as downloaded, with URL, UTC timestamp, SHA-256 checksum and licence terms. Nothing in a raw folder is ever overwritten.

**Declared before examined.** Country inclusion rules, inequality measure, source hierarchy, year alignment, index construction, domain membership, the panel protocol, and the type of every analysis as either a sensitivity analysis or part of a causal assessment, with the identifying assumptions of each causal design, are committed as an analysis lock before anyone computes, views or infers an association between current inequality data and current outcome data. The blinding is procedural only. The original correlations and the 2024 update's correlations are published, so the lock records which of them its author had seen. The lock's commit hash is recorded in the report. It is called an internal analysis lock unless it has been archived in an immutable public record, in which case it may be called a preregistration.

**Source hierarchy before outcome analysis.** For each indicator the analysis lock names a preferred source, permitted fallback sources, the minimum comparability conditions and the circumstances that justify a fallback. A fallback is recorded before the outcome is joined to inequality and never depends on the association it produces. Sources are never chosen by the strength of the correlation they produce.

**Versioned current data.** Current means the version of each source retrieved during the declared acquisition window. Each dataset is pinned by retrieval timestamp, release or version identifier where available, query parameters, raw-file checksum and source metadata. A later rerun against revised live data is a new acquisition, not the same analysis.

**No silent choices.** Where the original method is undocumented, alternatives are implemented side by side and labelled. The primary analysis uses no imputation. Outliers are never deleted without reporting both the retained and excluded results.

**Attributed criticism only.** A criticism enters the executable register only with four fields filled in. These are the critic's name, the exact source title, the publication year and a stable DOI, PMID, PMCID or URL. Generic critiques that no named author made are excluded. A criticism found after the register is frozen is tested only as a separately reported post-lock analysis. A criticism that country-level data cannot address, such as a claim about individual-level mechanisms, is reported as not testable in this design rather than as an inconclusive test.

**Attributed author claims.** A statement by Wilkinson or Pickett enters the claims register only with the same four fields the criticism register requires, which are the author, the exact work, the publication year and a stable identifier, together with its page or chapter. Its wording is a short verbatim quotation or a concise paraphrase marked as such. A statement whose source has not been checked is marked to be verified and is not classified.

**Legal access only.** Paywalls and access controls are not bypassed. A restricted item gets its bibliographic record and a note that it was not downloaded.

**Everything from code.** Final tables, figures, manifests, the data dictionary and the report are generated by scripts. Acquisition and replay are separate commands. The analysis build replays offline from stored, checksummed files, so later revisions of live databases cannot change a reproduced result.

**Original method kept apart from modern diagnostics.** Reproduction outputs use only the statistics and procedures the original study documented. Confidence intervals, rank correlations, robust methods and influence diagnostics are reported as labelled additions.

## Corrections carried in from spec review

The draft brief attributed a 1995 BMJ paper to "Richard Gravelle". The criticism register uses the correct authors instead. Ken Judge wrote "Income distribution and life expectancy: a critical appraisal", BMJ 1995, PMCID PMC2551188, PMID 7496240, DOI 10.1136/bmj.311.7015.1282. Hugh Gravelle wrote "How much of the relation between population mortality and unequal distribution of income is a statistical artefact?", BMJ 1998, PMID 9487182, DOI 10.1136/bmj.316.7128.382. These identifiers were checked during plan review and are logged again by T2.

The draft fixed the original exercise at 21 countries and treated r ≈ 0.85 as a benchmark. Neither number is used as a target, and no country count from a secondary source is used as a benchmark. The original country list, the usable country set for each outcome and the composite-index sample remain unresolved until verified from primary documentation or a provenance-verified original data release. Reconstructed sample sizes and coefficients are reported exactly as observed.

Claims about the 2024 update rely on the technical appendix to *The Spirit Level at 15*, not the main report. These are the 22-country sample including Germany and Israel and excluding Singapore as a non-OECD country, the 2013 inequality reference year, the original book's use of the 80:20 ratio, and the update's use of the Gini coefficient alongside 80:20 correlations for comparison. The appendix is at https://eprints.whiterose.ac.uk/id/eprint/215026/7/Technical_Appendix_20_07.pdf. Before these details are used in analysis rules, the relevant passages, table definitions, country list and reference-year statements are extracted from the appendix and recorded in the source-verification log.

Access to the original Equality Trust data is a gate, not an assumption. A 2017 Equality Trust post says the data can be downloaded, which does not establish that the files are available today, complete, or identical to the historical release.

## Facts that must be verified before use

Each of these is recorded in the source-verification log with the passage, table or file it was verified from. The original country list, per-outcome usable samples and composite-index sample. The original inequality measure and its year. The direction coding of every original index component, recovered from original materials and fixed per measure rather than per concept, since for example an intergenerational elasticity and a mobility index point in opposite directions. The 2024 appendix's direction coding is recorded separately as update-method documentation and is not taken as evidence of the original coding. The original handling of missing components in the index. The original timing, which the 2024 appendix describes as an inequality measure averaged from values reported in 2003 to 2006 and measured in 1992 to 2001, with outcomes from 1999 to 2004. This is the authors' later description and is checked against the book. The meaning of the term 80:20, which the appendix calls a decile ratio although the name suggests a ratio of quintile shares, is settled from the original source and used consistently. The details of the 2024 update listed above, including its index built as the mean of available z-scores, with 17 countries having all ten indicators and 5 lacking the mental illness indicator. The current availability and terms of the Equality Trust data files.

## Causal assessment

The project assesses causal claims where the data and the declared method can support an assessment. Each claim is first attributed to its source and classified as a descriptive correlation, a proposed mechanism or a causal claim. A correlation reported by Wilkinson and Pickett without a causal interpretation is not recorded as a causal inference. Causal claims they do advance are tested with designs matched to the claim, such as panel models, covariate adjustment and the alternatives raised by named critics. Each result states the identifying assumptions it relies on and what the design cannot rule out. Where cross-sectional country data cannot address a claim, the report says so rather than treating the result as a failed test.

## Out of scope

If the original package contains U.S. state material, T1a records its existence, file names and provenance in the original-release manifest. It is not cleaned, harmonised, prepared for redistribution or analysed beyond that metadata record in the first release unless a separate scope amendment is approved.

## Done means

Original data are preserved, checksummed and analysed under the access label the evidence supports, with every retrieval attempt recorded. Original findings are reproduced, or every non-reproduction is explained in an auditable discrepancy log.

Every required primary dataset is downloaded and validated, or its absence activates a fallback declared in the analysis lock or a clearly labelled omission. Access failure does not allow silent substitution or a claim that the corresponding outcome was tested.

Country inclusion rules and the source hierarchy are committed in the analysis lock before outcome analysis. Every statement by Wilkinson and Pickett that the project assesses is in the claims register with a checked source and a class, and the register is frozen before the lock. Every causal claim is either assessed with a design declared in the lock, whose identifying assumptions and limits the result states, or marked not testable in this design with the reason. Supporting and criticism sources are organised separately. Every controversy in the report is attributed to an identifiable source. Test data for each stated criticism are saved.

Every final result identifies its exact dataset version, country sample, outcome-year range, inequality-year range, source IDs, component availability and analysis-lock commit hash.

The final clean build is an offline replay from a fresh environment, using only previously acquired and checksummed local assets. It generates the final tables, figures, manifests, data dictionary and report.

The results are published as a website on GitHub Pages, built by GitHub Actions from a tagged release and stating the release tag, the analysis-lock tag and the data snapshot it was built from.
