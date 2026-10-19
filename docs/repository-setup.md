# Repository setup: approval pending

The code, source records, tests and CI workflow are in this PR. The following live GitHub settings **have not been applied**. Automatic approval review rejected the attempted action because the implementation request did not explicitly authorise these exact persistent branch/tag protection and merge-setting changes on shared refs.

This is a reviewable proposal, not a script or a workflow that applies the changes.

| Proposed change | Effect |
|---|---|
| Protect the default branch with no bypass actors | Require a pull request, both Validate (ubuntu-latest) and Validate (macos-14), up-to-date checks and resolved review conversations; block deletion and force pushes |
| Permit only merge commits | Disable squash and rebase merges; preserve the plan's history policy |
| Enable repository support for auto-merge | Make the feature available for eligible future PRs; this does not enable auto-merge on this draft PR |
| Protect milestone-*, deliverables-* and results-* tags | Only organisation owners may create, update or delete matching tags; no existing tag is created, moved or deleted by this proposal |

The approving-review count remains zero while there is only one human contributor, as the plan states. Milestone approval remains a separate human decision. These controls affect every contributor using the matching shared refs, which is why the automatic review requested explicit approval.

If approved, apply the proposal through GitHub administration and record the returned rule IDs and observed settings. Until then, do not describe repository protections or merge governance as configured. Their absence does not prevent testing the PR branch, and does not authorise a current-data analysis or release tag.
