from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
HARNESS_GUARD_PATH = REPO_ROOT / "hooks" / "harness_guard.py"

spec = importlib.util.spec_from_file_location("harness_guard", HARNESS_GUARD_PATH)
assert spec is not None
harness_guard = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(harness_guard)


class HarnessGuardParsingTests(unittest.TestCase):
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


if __name__ == "__main__":
    unittest.main()
