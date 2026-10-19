# Milestone 1 implementation status

Milestone 1 is **not complete or approved**. The four latest implementation defects are corrected, but the maintainer explicitly requires missing-component acquisition before the prospective index is locked. No current-data association has been calculated; no release tag has been created or moved.

| Work | Evidence | Remaining acceptance work |
|---|---|---|
| Executable foundation | Locked Linux/Apple-silicon environment; offline numerical, reader, integrity, gate and replay tests; immutable source and execution evidence | Final PR head must pass its own Linux/macOS public replay checks |
| Original access | Restricted official international workbook, original sample-presence recovery; author report, appendix, responses and 2015 causal review acquired locally and recorded | Workbook/full-text redistribution remains unverified; released state file absent; book not used |
| Historical international | 26 correlations computed from the supplied release; three average-income comparisons have explicit missing-input barriers | Independent index reconstruction, historical income, source/version conflicts and April 2004 ranking vintage remain barriers |
| Historical states | Public Census S4 and FBI 1999 homicide sources; Census 2006 Table 105 recovered for 2002 infant mortality; prospective specification version 3 committed before the added calculation | Two comparisons computed; 15 comparisons and independent state index remain unproduced with barriers |
| Current acquisition and lineage | Pinned World Bank, WHO, UNODC, GDIM, PISA 2025 and WVS responses; source-specific coverage readers; PISA provider warnings retained; 47 lineage rows with definitions, proposed classes or logged verification barriers | WVS survey-selection/analysis-denominator decisions, diagnostic mental-health aggregates, state counterparts and other disclosed row-specific verification work |
| Refreshed eligibility | Approved UN-member/2025 Atlas GNI/population/national-income rule implemented; 193 audited states, 28 eligible; survey-year evidence; no outcome inputs | Missing ranking/income records remain explicit limitations of the nominated release, not evidence that no data exist elsewhere |
| Prospective lock | Draft review snapshot contains file hashes; current specification nominates acquired sources; current-association gate tested | Missing-component acquisition and remaining index/period choices must be resolved before an approvable lock and milestone review |

## The four latest implementation corrections

Code commit e4af283f closes the following defects, with regression tests:

1. The current-data gate no longer depends only on a specification ID prefix. Declared provenance, current raw paths and current observation provenance all trigger the gate before correlation.
2. Insufficient standardisation reference observations cannot silently remove a component through an undefined standard deviation. Availability and used flags follow usable scores.
3. Constant/too-small comparisons preserve their observed pair membership, so n and missing_units remain consistent even when r cannot be produced.
4. Replay compares the exact expected table set from Git, rejecting missing/extra tables and empty baselines as well as numerical differences.

Earlier corrections in 5cd024cb protect credentials in acquisition failures, immutable evidence identities, stale observations/figures and environment-bound restricted retention. Those protections remain in force.

## Validation at committed computation revision e0a9dfd0

Local make lint test all verify-data check-contracts completed successfully: 66 offline tests, formatting/lint, full record validation and all replay steps. Validation covers 99 source records, 63 acquisition records, 46 catalogue targets and 47 lineage rows. The available restricted inputs were held locally; their identities were checked. Public CI must instead retain restricted outputs only against compatible producer evidence.

Seven canonical producer records were generated from this committed code: original sample coverage, current source coverage, refreshed eligibility, international reproduction, state reconstruction, historical summary and prospective component assessment. Their paths and input/output hashes are in outputs/runs/. Earlier exploratory records are preserved rather than overwritten.

Previous Linux/macOS CI at 902ec181 passed with 42 tests; this is historical evidence, not evidence for the current head. An earlier local fresh-clone NumPy failure and a later interrupted supplementary environment installation were not counted as successes. Final-head CI evidence is recorded in the PR description after it completes.

## Decisions and remaining gate

The WHO terms and the explicit refreshed eligibility rule were accepted by the maintainer. The current-index lock was first deferred pending availability consequences, then explicitly held until missing components are acquired. The updated component assessment records the resulting evidence. A lower component minimum or reduced index has not been approved.

A concrete WMH national-aggregate request and WVS verification/acquisition instructions are in data/local_data_required/outcome-data.md. Researcher contact requires separate messaging authorisation. The project does not replace a missing diagnostic prevalence target with service use, lifetime prevalence or a student sample. The final lock and milestone review remain open.


## Follow-up validation and acquisitions

The official GESIS joint EVS/WVS v5 frequency and methods reports resolve the candidate's weight, published denominator and survey-period documentation. The new PDF coverage reader retains 31 survey records for 26 mapped national units; the original 23-country sample has 19 represented countries. It does not map Great Britain or Northern Ireland to the UK. Both EVS and WVS are retained where present, including same-reference-year surveys; no selection depends on outcome values. A provider reference year does not replace full fieldwork dates.

The second WMH 2025 supplement (DOI 10.1186/s13033-025-00666-w) contains pooled, not national, prevalence. The missing diagnostic component remains open. A request for explicit permission to send the prepared aggregate-data enquiry is pending; no message has been sent.

Local validation now passes 68 offline tests and validates 104 sources, 72 acquisitions, 46 catalogue targets and 47 lineage rows. The environment adds pypdf through the shared Pixi lock and its informational exports. Committed-code producer records and final-head Linux/macOS CI must be refreshed after the code commit; older green checks do not validate this revision.
