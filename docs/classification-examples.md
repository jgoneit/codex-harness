# Classification Examples

These examples show how Harness should classify concrete requests. When an example mixes categories, choose the higher-risk classification.

## Tiny

### Typo In One Sentence

- Classification: Tiny
- Reason: Fixes a misspelled word in one documentation sentence and does not change meaning, behavior, policy, or contract.
- Required gates: Concise Plan with exact Plan approval, Implement, and Completion. Review is not required unless the user, project policy, or discovered risk requires it.
- Verification expectation: Inspect the edited sentence or run the existing docs spellcheck if it is already available and local.

### Comment Grammar Cleanup

- Classification: Tiny
- Reason: Updates grammar in a code comment without changing code behavior, public docs, or workflow rules.
- Required gates: Concise Plan with exact Plan approval, Implement, and Completion. Review is not required unless the comment describes security, data, or contract behavior in a way that could mislead implementation.
- Verification expectation: Inspect the diff and run the smallest relevant formatter or lint check only if the repo normally requires it for comment-only edits.

### README Wording Without Meaning Change

- Classification: Tiny
- Reason: Rephrases a README sentence for clarity while preserving the same setup step and command.
- Required gates: Concise Plan with exact Plan approval, Implement, and Completion. Review is not required unless the README section controls release, deployment, security, or policy behavior.
- Verification expectation: Inspect the rendered or raw README section and confirm the command or instruction still matches the original meaning.

## Small

### Add A Focused Unit Test

- Classification: Small
- Reason: Adds or adjusts one local unit test for existing behavior without changing production code or public contracts.
- Required gates: Planner Plan with exact Plan approval, implementer, clean-context read-only reviewer, and Completion after Review.
- Verification expectation: Run the targeted test file or test case; if unavailable, explain why and inspect the assertion path.

### Internal Refactor In One Module

- Classification: Small
- Reason: Renames helper functions or extracts a private helper inside one module while preserving observable behavior.
- Required gates: Planner Plan with exact Plan approval, implementer, clean-context read-only reviewer, and Completion after Review.
- Verification expectation: Run the module's focused tests and inspect the diff for unchanged inputs, outputs, and error handling.

### CLI Help Text Update

- Classification: Small
- Reason: Changes `--help` wording for an existing CLI option without changing flags, exit codes, parsing, or runtime behavior.
- Required gates: Planner Plan with exact Plan approval, implementer, clean-context read-only reviewer, and Completion after Review.
- Verification expectation: Run the CLI help command or the existing help snapshot test; inspect output for wrapping and accuracy.

## Non-Trivial

### API Response Contract Change

- Classification: Non-trivial
- Reason: Adds, removes, renames, or changes the type of a field in a public API response that callers may depend on.
- Required gates: Planner, implementer, clean-context read-only reviewer, explicit Plan approval, and Completion after Review. Require scope approval if client docs, SDKs, or tests must be expanded.
- Verification expectation: Run contract tests or endpoint tests, update snapshots or docs as accepted, and verify backward-compatibility notes or migration guidance.

### Database Migration

- Classification: Non-trivial
- Reason: Creates or edits a schema/data migration that can affect stored data, rollout order, rollback, or direct DB access risk.
- Required gates: Planner, implementer, clean-context read-only reviewer, explicit Plan approval, and Completion after Review. Direct DB access or destructive SQL requires separate explicit approval.
- Verification expectation: Run migration lint or dry-run tests if available, inspect rollback behavior, and run affected model/query tests without connecting to production.

### Auth Or Security Behavior

- Classification: Non-trivial
- Reason: Changes authentication, authorization, token handling, secret handling, permission checks, or security documentation that controls implementation.
- Required gates: Planner, implementer, clean-context read-only reviewer, explicit Plan approval, and Completion after Review. Secret access requires separate explicit approval.
- Verification expectation: Run focused auth/security tests, inspect failure paths, and verify that protected data remains denied by default.

### Dependency Upgrade

- Classification: Non-trivial
- Reason: Updates a runtime, build, security, or framework dependency where transitive behavior, lockfiles, compatibility, or deployment output can change.
- Required gates: Planner, implementer, clean-context read-only reviewer, explicit Plan approval, and Completion after Review. Network access or lockfile regeneration follows environment approval rules.
- Verification expectation: Run dependency resolution locally if already available, run affected test suites, inspect lockfile changes, and check release notes when available.

### Multi-File Behavior Change

- Classification: Non-trivial
- Reason: Changes behavior across multiple modules, such as validation in one layer and rendering or persistence in another.
- Required gates: Planner, one or more domain implementers as needed, clean-context read-only reviewer, explicit Plan approval, and Completion after Review.
- Verification expectation: Run focused integration tests plus unit tests for touched modules; inspect cross-module contracts and user-visible behavior.

### Infrastructure Or Deploy Change

- Classification: Non-trivial
- Reason: Edits Terraform, Kubernetes, CI/CD deploy steps, release scripts, environment config, or production-impact operations.
- Required gates: Planner, implementer, clean-context read-only reviewer, explicit Plan approval, and Completion after Review. Deployment, production-impact commands, and destructive operations require separate explicit approval.
- Verification expectation: Run non-destructive validation such as `terraform plan`, manifest lint, or CI config checks; do not apply, destroy, deploy, or restart services without explicit approval.
