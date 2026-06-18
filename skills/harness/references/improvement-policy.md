# Improvement Policy

`assets/templates/improvement.md` is optional by default.

It is required when any condition is true:

- Task classification is `Non-trivial`.
- Review status is `review_blocked_degraded`.
- A Repair cycle occurred.
- There were two or more Plan revisions.
- The task modified Harness policy, hook policy, templates, or orchestration rules.

The Improvement artifact does not expand current-loop success criteria. It records process, template, hook, and orchestration improvement candidates for a later loop.

Artifact persistence follows `references/artifact-policy.md`.
