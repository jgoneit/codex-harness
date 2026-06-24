from __future__ import annotations

import hashlib
import json
import importlib.util
import os
import tempfile
import unittest
from contextlib import contextmanager, redirect_stdout
from io import StringIO
from pathlib import Path
from textwrap import dedent


REPO_ROOT = Path(__file__).resolve().parents[1]
HARNESS_GUARD_PATH = REPO_ROOT / "hooks" / "harness_guard.py"

spec = importlib.util.spec_from_file_location("harness_guard", HARNESS_GUARD_PATH)
assert spec is not None
harness_guard = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(harness_guard)


def command_hash_prefix(command: str) -> str:
    return hashlib.sha256(command.encode("utf-8")).hexdigest()[:12]


@contextmanager
def temporary_cwd():
    previous = Path.cwd()
    with tempfile.TemporaryDirectory() as root:
        os.chdir(root)
        try:
            yield Path(root)
        finally:
            os.chdir(previous)


@contextmanager
def changed_cwd(path: Path):
    previous = Path.cwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(previous)


def read_audit_records(root: Path) -> list[dict[str, str]]:
    audit_path = root / ".harness" / "audit" / "run.jsonl"
    return [
        json.loads(line)
        for line in audit_path.read_text(encoding="utf-8").splitlines()
        if line
    ]


class HarnessGuardParsingTests(unittest.TestCase):
    def hook_output(self, handler, data: dict[str, str], cwd: Path | None = None) -> str:
        output = StringIO()
        if cwd is None:
            with temporary_cwd():
                with redirect_stdout(output):
                    handler(data)
        else:
            with changed_cwd(cwd):
                with redirect_stdout(output):
                    handler(data)
        return output.getvalue()

    def assert_no_block(self, output: str) -> None:
        self.assertEqual(output, "")

    def assert_block_reason_contains(self, output: str, expected: str) -> None:
        payload = json.loads(output)
        self.assertEqual(payload["decision"], "block")
        self.assertIn(expected, payload["reason"])

    def test_strip_leading_sudo(self) -> None:
        cases = [
            (["git", "status"], (False, ["git", "status"])),
            (["sudo", "git", "status"], (True, ["git", "status"])),
            (["sudo", "-E", "-u", "root", "--", "rm", "-rf", "."], (True, ["rm", "-rf", "."])),
            (["sudo", "--user=root", "psql"], (True, ["psql"])),
        ]

        for tokens, expected in cases:
            with self.subTest(tokens=tokens):
                self.assertEqual(harness_guard.strip_leading_sudo(tokens), expected)

    def test_strip_leading_command_wrappers(self) -> None:
        cases = [
            (["FOO=1", "git", "status"], ["git", "status"]),
            (["env", "-i", "FOO=1", "python3"], ["python3"]),
            (
                ["FOO=1", "sudo", "-E", "env", "BAR=2", "bash", "-lc", "echo hi"],
                ["bash", "-lc", "echo hi"],
            ),
            (["sudo", "--user=root", "env", "--", "printenv"], ["printenv"]),
        ]

        for tokens, expected in cases:
            with self.subTest(tokens=tokens):
                self.assertEqual(harness_guard.strip_leading_command_wrappers(tokens), expected)

    def test_strip_leading_env_assignments_and_sudo_preserves_env_binary(self) -> None:
        cases = [
            (["FOO=1", "rm", "-rf", ".git"], (False, ["rm", "-rf", ".git"])),
            (["FOO=1", "sudo", "-E", "git", "reset", "--hard"], (True, ["git", "reset", "--hard"])),
            (["FOO=1", "env"], (False, ["env"])),
            (["sudo", "FOO=1", "env"], (True, ["env"])),
        ]

        for tokens, expected in cases:
            with self.subTest(tokens=tokens):
                self.assertEqual(
                    harness_guard.strip_leading_env_assignments_and_sudo(tokens),
                    expected,
                )

    def test_command_substitution_payload(self) -> None:
        command = "echo $(cat .env) tail"
        payload_start = command.index("$(") + 2
        self.assertEqual(
            harness_guard.command_substitution_payload(command, payload_start),
            ("cat .env", command.index(") ") + 1),
        )

        nested = "echo $(printf $(whoami)) tail"
        nested_payload, nested_end = harness_guard.command_substitution_payload(
            nested,
            nested.index("$(") + 2,
        )
        self.assertEqual(nested_payload, "printf $(whoami)")
        self.assertEqual(nested[nested_end:], " tail")

        unterminated = "echo $(cat .env"
        self.assertEqual(
            harness_guard.command_substitution_payload(
                unterminated,
                unterminated.index("$(") + 2,
            ),
            ("", len(unterminated)),
        )

    def test_iter_pipeline_stages(self) -> None:
        cases = [
            ("echo a | grep a | wc -l", ["echo a", "grep a", "wc -l"]),
            ("printf 'a|b' | cat", ["printf 'a|b'", "cat"]),
            ('printf "a|b" | cat', ['printf "a|b"', "cat"]),
        ]

        for command_segment, expected in cases:
            with self.subTest(command_segment=command_segment):
                self.assertEqual(harness_guard.iter_pipeline_stages(command_segment), expected)

    def test_iter_shell_wrapper_segments(self) -> None:
        cases = [
            (
                "git status && git diff; echo done\nls -al",
                ["git status", "git diff", "echo done", "ls -al"],
            ),
            ("echo 'a && b'; rg TODO src", ["echo 'a && b'", "rg TODO src"]),
            ('echo "a; b" || true', ['echo "a; b"', "true"]),
        ]

        for command_text, expected in cases:
            with self.subTest(command_text=command_text):
                self.assertEqual(harness_guard.iter_shell_wrapper_segments(command_text), expected)

    def test_stop_accepts_canonical_plan_repair_plan_and_completion(self) -> None:
        canonical_plan = dedent(
            """
            # Plan

            ## Task Classification
            Small
            ## Risk Level
            Medium
            ## Reasoning for classification
            Contract drift repair.
            ## In Scope
            Guard and required references.
            ## Out of Scope
            Dangerous-command behavior.
            ## Files / Areas to Inspect
            hooks and Harness references.
            ## Proposed Change Plan
            1. Align canonical validators.
            ## Verification Plan
            Run focused tests.
            ## Risks / Assumptions
            Existing worktree changes are preserved.
            ## Approval Gate
            Proceed with this Plan? [y/N]
            """
        )
        canonical_repair_plan = dedent(
            """
            # Repair Plan

            ## Review Findings Addressed
            Canonical artifact drift.
            ## Repair Scope
            Hook artifact validators and required references.
            ## Files Expected to Change
            hooks/harness_guard.py
            ## Verification Required
            Focused guard tests.
            ## Risks
            None beyond scoped drift repair.
            ## Repair Approval Gate
            Proceed with this Repair Plan? [y/N]
            """
        )
        canonical_completion = dedent(
            """
            # Completion Report

            ## Status
            completed
            ## Review Status
            clean_context_review_completed
            ## Repair Plan Required
            yes
            ## Changed Files
            hooks/harness_guard.py
            ## Verification
            Focused tests passed.
            ## Review Result
            PASS
            ## Approval Ledger
            | Gate | Required? | Requested? | User response | Result | Notes |
            | Plan approval | yes | yes | y | approved | accepted |
            ## Residual Risks
            none
            ## Follow-up
            none
            """
        )

        for message in (canonical_plan, canonical_repair_plan, canonical_completion):
            with self.subTest(message=message.splitlines()[1]):
                output = self.hook_output(
                    harness_guard.handle_stop,
                    {"last_assistant_message": message},
                )
                self.assert_no_block(output)

    def test_stop_blocks_canonical_plan_or_repair_plan_missing_prompt(self) -> None:
        plan_without_prompt = dedent(
            """
            # Plan

            ## Task Classification
            Small
            ## Risk Level
            Medium
            ## Reasoning for classification
            Contract drift repair.
            ## In Scope
            Guard and references.
            ## Out of Scope
            Dangerous-command behavior.
            ## Files / Areas to Inspect
            hooks and docs.
            ## Proposed Change Plan
            1. Align validators.
            ## Verification Plan
            Run tests.
            ## Risks / Assumptions
            Existing changes are preserved.
            ## Approval Gate
            """
        )
        repair_plan_without_prompt = dedent(
            """
            # Repair Plan

            ## Review Findings Addressed
            Canonical artifact drift.
            ## Repair Scope
            Hook validators and references.
            ## Files Expected to Change
            hooks/harness_guard.py
            ## Verification Required
            Focused tests.
            ## Risks
            none
            ## Repair Approval Gate
            """
        )

        plan_output = self.hook_output(
            harness_guard.handle_stop,
            {"last_assistant_message": plan_without_prompt},
        )
        self.assert_block_reason_contains(plan_output, "Harness Plan artifact is missing")

        repair_output = self.hook_output(
            harness_guard.handle_stop,
            {"last_assistant_message": repair_plan_without_prompt},
        )
        self.assert_block_reason_contains(repair_output, "Harness Repair Plan artifact is missing")

    def test_subagent_stop_accepts_canonical_phase_outputs(self) -> None:
        planner_output = dedent(
            """
            # Plan

            ## Task Classification
            Small
            ## Risk Level
            Medium
            ## Reasoning for classification
            Hook contract drift.
            ## In Scope
            Guard and references.
            ## Out of Scope
            Dangerous-command behavior.
            ## Files / Areas to Inspect
            hooks/harness_guard.py
            ## Proposed Change Plan
            1. Update constants.
            ## Verification Plan
            Focused tests.
            ## Risks / Assumptions
            Existing worktree changes are preserved.
            ## Approval Gate
            Proceed with this Plan? [y/N]
            """
        )
        implementer_output = dedent(
            """
            # Implementation Summary

            ## Accepted Plan Reference
            Approved Repair Plan from main thread.
            ## Changed Files
            hooks/harness_guard.py
            ## Summary of Changes
            Aligned canonical artifact checks.
            ## Scope Compliance
            Stayed inside approved files.
            ## Verification Performed
            Focused unit tests.
            ## Deviations from Plan
            none
            ## Blockers / Residual Risks
            none
            """
        )
        reviewer_output = dedent(
            """
            # Clean-context Review

            ## Inputs Reviewed
            Accepted Repair Plan and diff.
            ## Accepted Plan
            Approved canonical artifact repair.
            ## Diff / Changed Files
            hooks/harness_guard.py
            ## Verification Evidence
            Focused unit tests passed.
            ## Findings Table
            | Severity | Finding | Evidence | Required Action |
            | not_applicable | none | tests passed | none |
            ## Verdict
            PASS
            """
        )

        cases = (
            ("planner", planner_output),
            ("implementer", implementer_output),
            ("reviewer", reviewer_output),
        )
        for agent_type, message in cases:
            with self.subTest(agent_type=agent_type):
                output = self.hook_output(
                    harness_guard.handle_subagent_stop,
                    {"agent_type": agent_type, "last_assistant_message": message},
                )
                self.assert_no_block(output)

    def test_stop_audits_block_without_message_text(self) -> None:
        secret_plan_without_prompt = dedent(
            """
            # Plan

            token=super-secret-value

            ## Task Classification
            Small
            ## Risk Level
            Medium
            ## Reasoning for classification
            Audit coverage.
            ## In Scope
            Guard only.
            ## Out of Scope
            Hook config files.
            ## Files / Areas to Inspect
            hooks/harness_guard.py
            ## Proposed Change Plan
            1. Add audit tests.
            ## Verification Plan
            Focused tests.
            ## Risks / Assumptions
            None.
            ## Approval Gate
            """
        )

        with tempfile.TemporaryDirectory() as root:
            project = Path(root)
            output = self.hook_output(
                harness_guard.handle_stop,
                {"last_assistant_message": secret_plan_without_prompt},
                project,
            )

            self.assert_block_reason_contains(output, "Harness Plan artifact is missing")
            records = read_audit_records(project)
            self.assertEqual(len(records), 1)
            self.assertEqual(
                set(records[0]),
                {"timestamp", "event_name", "category", "decision", "command_sha256"},
            )
            self.assertEqual(records[0]["event_name"], "Stop")
            self.assertEqual(records[0]["category"], "stop_missing_plan_prompt")
            self.assertEqual(records[0]["decision"], "block")
            self.assertEqual(records[0]["command_sha256"], command_hash_prefix(""))
            raw_audit = (project / ".harness" / "audit" / "run.jsonl").read_text(encoding="utf-8")
            self.assertNotIn("super-secret-value", raw_audit)
            self.assertNotIn("token=", raw_audit)

    def test_subagent_stop_audits_allow_without_message_text(self) -> None:
        implementer_output = dedent(
            """
            # Implementation Summary

            token=super-secret-value

            ## Accepted Plan Reference
            Approved Plan.
            ## Changed Files
            hooks/harness_guard.py
            ## Summary of Changes
            Added audit logging.
            ## Scope Compliance
            Stayed in scope.
            ## Verification Performed
            Focused tests.
            ## Deviations from Plan
            none
            ## Blockers / Residual Risks
            none
            """
        )

        with tempfile.TemporaryDirectory() as root:
            project = Path(root)
            output = self.hook_output(
                harness_guard.handle_subagent_stop,
                {"agent_type": "implementer", "last_assistant_message": implementer_output},
                project,
            )

            self.assert_no_block(output)
            records = read_audit_records(project)
            self.assertEqual(len(records), 1)
            self.assertEqual(
                set(records[0]),
                {"timestamp", "event_name", "category", "decision", "command_sha256"},
            )
            self.assertEqual(records[0]["event_name"], "SubagentStop")
            self.assertEqual(records[0]["category"], "subagent_implementer_allow")
            self.assertEqual(records[0]["decision"], "allow")
            self.assertEqual(records[0]["command_sha256"], command_hash_prefix(""))
            raw_audit = (project / ".harness" / "audit" / "run.jsonl").read_text(encoding="utf-8")
            self.assertNotIn("super-secret-value", raw_audit)
            self.assertNotIn("token=", raw_audit)


if __name__ == "__main__":
    unittest.main()
