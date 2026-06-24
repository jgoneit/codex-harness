from __future__ import annotations

import importlib.util
import json
import unittest
from contextlib import redirect_stdout
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


EXPECTED_CONTEXT = "\n".join(
    (
        "Harness is active.",
        "Minimum reasoning effort is high.",
        "Implement and Review require xhigh when available.",
        f"Do not implement before exact Plan approval: {harness_guard.PLAN_PROMPT}",
        f"Do not repair before exact Repair Plan approval: {harness_guard.REPAIR_PROMPT}",
        "Only lowercase y approves execution.",
    )
)


class HarnessGuardActivationTests(unittest.TestCase):
    def hook_output(self, prompt: str) -> str:
        output = StringIO()
        with redirect_stdout(output):
            harness_guard.handle_user_prompt_submit({"prompt": prompt})
        return output.getvalue()

    def assert_additional_context_injected(self, prompt: str) -> None:
        payload = json.loads(self.hook_output(prompt))
        self.assertEqual(
            payload["hookSpecificOutput"]["hookEventName"],
            "UserPromptSubmit",
        )
        self.assertEqual(
            payload["hookSpecificOutput"]["additionalContext"],
            EXPECTED_CONTEXT,
        )

    def assert_additional_context_not_injected(self, prompt: str) -> None:
        self.assertEqual(self.hook_output(prompt), "")

    def test_injects_context_for_line_start_harness_invocation(self) -> None:
        self.assert_additional_context_injected("$harness fix the guard trigger")

    def test_injects_context_for_leading_whitespace_harness_invocation(self) -> None:
        self.assert_additional_context_injected("  $harness fix the guard trigger")

    def test_injects_context_for_use_harness_invocation(self) -> None:
        self.assert_additional_context_injected("use $harness fix the guard trigger")

    def test_injects_context_for_leading_whitespace_use_harness_invocation(self) -> None:
        self.assert_additional_context_injected("  use $harness fix the guard trigger")

    def test_does_not_inject_context_for_sentence_middle_mention(self) -> None:
        self.assert_additional_context_not_injected("should I use $harness for this?")

    def test_does_not_inject_context_for_uppercase_harness_token(self) -> None:
        self.assert_additional_context_not_injected("$HARNESS fix the guard trigger")

    def test_does_not_inject_context_for_uppercase_use_prefix(self) -> None:
        self.assert_additional_context_not_injected("USE $harness fix the guard trigger")

    def test_does_not_inject_context_for_non_exact_harness_token(self) -> None:
        self.assert_additional_context_not_injected("$harness-extra should not activate")

    def test_does_not_inject_context_for_inline_backtick_mention(self) -> None:
        self.assert_additional_context_not_injected("Please document `$harness` in the README.")

    def test_does_not_inject_context_for_fenced_code_block_mention(self) -> None:
        self.assert_additional_context_not_injected(
            dedent(
                """
                ```text
                $harness fix the guard trigger
                ```
                """
            )
        )

    def test_does_not_inject_context_for_shorter_fence_inside_fenced_code_block(self) -> None:
        self.assert_additional_context_not_injected(
            dedent(
                """
                ````text
                ```
                $harness fix the guard trigger
                ````
                """
            )
        )

    def test_does_not_inject_context_for_quote_mention(self) -> None:
        self.assert_additional_context_not_injected("> $harness fix the guard trigger")

    def test_does_not_inject_context_for_prompt_without_harness(self) -> None:
        self.assert_additional_context_not_injected("Fix the guard trigger tests.")


if __name__ == "__main__":
    unittest.main()
