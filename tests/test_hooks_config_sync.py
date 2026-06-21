from __future__ import annotations

import filecmp
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


class HooksConfigSyncTests(unittest.TestCase):
    def test_root_hooks_json_matches_canonical_hooks_config(self) -> None:
        canonical = REPO_ROOT / "hooks" / "hooks.json"
        compatibility_copy = REPO_ROOT / "hooks.json"

        self.assertTrue(canonical.is_file(), "canonical hooks/hooks.json is missing")
        self.assertTrue(compatibility_copy.is_file(), "root hooks.json compatibility copy is missing")
        self.assertTrue(
            filecmp.cmp(canonical, compatibility_copy, shallow=False),
            "root hooks.json compatibility copy must match canonical hooks/hooks.json",
        )


if __name__ == "__main__":
    unittest.main()
