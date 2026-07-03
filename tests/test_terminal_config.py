import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from terminal_config.cli import PROFILES, parser
from terminal_config.context import Context
from terminal_config.runner import Runner


class TerminalConfigTests(unittest.TestCase):
    def test_profiles_only_reference_known_modules(self):
        known = {"core", "fonts", "desktop", "neovim"}
        for modules in PROFILES.values():
            self.assertLessEqual(set(modules), known)

    def test_cli_dry_run(self):
        args = parser().parse_args(["--profile", "wsl", "--dry-run"])
        self.assertTrue(args.dry_run)
        self.assertEqual(args.profile, "wsl")

    def test_lockfile_has_immutable_git_commits(self):
        lock = json.loads((ROOT / "versions.lock.json").read_text())
        for spec in lock["git"].values():
            self.assertRegex(spec["commit"], r"^[0-9a-f]{40}$")
        self.assertRegex(lock["font"]["sha256"], r"^[0-9a-f]{64}$")

    def test_verified_download_rejects_bad_hash(self):
        lock = json.loads((ROOT / "versions.lock.json").read_text())
        ctx = Context(ROOT, Path.home(), Runner(False), lock)
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "source"
            target = Path(directory) / "target"
            source.write_bytes(b"safe")
            with self.assertRaises(RuntimeError):
                ctx.download_verified(source.as_uri(), target, "0" * 64)
            self.assertFalse(target.exists())

    def test_verified_download_accepts_expected_hash(self):
        lock = json.loads((ROOT / "versions.lock.json").read_text())
        ctx = Context(ROOT, Path.home(), Runner(False), lock)
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "source"
            target = Path(directory) / "target"
            source.write_bytes(b"safe")
            expected = hashlib.sha256(b"safe").hexdigest()
            ctx.download_verified(source.as_uri(), target, expected)
            self.assertEqual(target.read_bytes(), b"safe")


if __name__ == "__main__":
    unittest.main()
