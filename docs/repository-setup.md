# Repository setup: approved and applied

The maintainer explicitly approved the settings below on 19 October 2026 after reviewing their scope. They were then applied through the GitHub administration API. An earlier automatic approval review had blocked the operation because the general implementation request did not explicitly authorise these persistent changes; the maintainer's subsequent approval resolved that requirement.

The branch ruleset ID is `25374103`; the milestone-tag ruleset ID is `25374104`. Both are active. The repository uses default branch `main`, with `allow_merge_commit=true`, `allow_squash_merge=false`, `allow_rebase_merge=false` and `allow_auto_merge=true`.

| Applied change | Effect |
|---|---|
| Protect the default branch with no bypass actors | Require a pull request, both Validate (ubuntu-latest) and Validate (macos-14), up-to-date checks and resolved review conversations; block deletion and force pushes |
| Permit only merge commits | Disable squash and rebase merges; preserve the plan's history policy |
| Enable repository support for auto-merge | Make the feature available for eligible future PRs; auto-merge was not enabled on this draft PR |
| Protect milestone-*, deliverables-* and results-* tags | Only organisation owners may create, update or delete matching tags; no existing tag is created, moved or deleted by this proposal |

The approving-review count remains zero while there is only one human contributor, as the plan states. Milestone approval remains a separate human decision. Main has no bypass actors. Only the `OrganizationAdmin` actor class can bypass the tag creation/update/deletion rules. These controls affect every contributor using the matching shared refs.

No existing tag was created, moved or deleted, and this PR was not merged. Repository governance does not authorise current-data analysis or a release tag; those gates still require the separate research review.
