"""Release-gate contract tests for the ACTUAL dedicated Pinokio launcher.

These tests validate scripts, user consent and library safety. Passing them
does NOT establish a fresh-OS installation or human-reviewed public beta.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
from unittest.mock import patch

import manage

ROOT = Path(__file__).resolve().parent


class PinokioReleaseContract(unittest.TestCase):
    def test_pinokio_targets_two_isolated_workspaces(self):
        personal = (ROOT / "start.js").read_text(encoding="utf-8")
        demo = (ROOT / "start-demo.js").read_text(encoding="utf-8")
        self.assertIn("serve.py", personal)
        self.assertIn("serve.py --mode demo", demo)
        serve = (ROOT / "serve.py").read_text(encoding="utf-8")
        self.assertIn('("demo-data" if mode == "demo" else "data")', serve)
        self.assertIn('host="127.0.0.1"', serve)
        self.assertIn("/api/projects/restore-upload", serve)
        self.assertIn('status_code=403', serve)
        self.assertIn("EMBER_DATA_DIR", serve)

    def test_models_install_is_separate_author_choice(self):
        installer = (ROOT / "install.js").read_text(encoding="utf-8")
        install_models = (ROOT / "models.js").read_text(encoding="utf-8")
        menu = (ROOT / "pinokio.js").read_text(encoding="utf-8")
        self.assertNotIn("ollama pull", installer)
        self.assertNotIn('manage.py models', installer)
        self.assertIn("manage.py models", install_models)
        self.assertIn("Install writing model", menu)
        self.assertIn("app/backend", installer)
        self.assertIn("npm ci", installer)

    def test_pinokio_script_parser_and_menu_acceptance(self):
        node = shutil.which("node")
        if not node:
            self.skipTest("Node runtime not installed")
        for source in ("pinokio.js", "setup.js", "install.js", "start.js",
                       "start-demo.js", "update.js", "reset.js", "models.js",
                       "stop.js", "stop-demo.js", "test-menu.js"):
            result = subprocess.run([node, "--check", source], cwd=ROOT,
                                    capture_output=True, text=True, timeout=20)
            self.assertEqual(result.returncode, 0, result.stderr)
        execution = subprocess.run([node, "test-menu.js"], cwd=ROOT,
                                   capture_output=True, text=True, timeout=20)
        self.assertEqual(execution.returncode, 0, execution.stderr)

    def test_update_stops_both_servers_and_snapshots_before_code_pull(self):
        update = (ROOT / "update.js").read_text(encoding="utf-8")
        self.assertLess(update.index("start-demo.js"), update.index("manage.py backup"))
        self.assertLess(update.index("start.js"), update.index("manage.py backup"))
        self.assertLess(update.index("manage.py backup"), update.index("setup.js update"))
        self.assertLess(update.index("setup.js update"), update.index("install.js"))
        reset = (ROOT / "setup.js").read_text(encoding="utf-8")
        self.assertIn("'app/backend/env'", reset)
        self.assertIn("'app/frontend/node_modules'", reset)
        self.assertNotIn("'data'", reset)
        self.assertNotIn("'demo-data'", reset)
        self.assertNotIn("'backups'", reset)

    def test_backup_preserves_sqlite_and_files_and_rejects_external_symlink(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            source = folder / "author library"
            source.mkdir()
            (source / "draft.md").write_text("AUTHOR_SAMPLE_QA_ONLY", encoding="utf-8")
            dst = folder / "verified snapshot"
            self.assertEqual(manage.copy_verified(source, dst), 1)
            self.assertEqual((dst / "draft.md").read_text(), "AUTHOR_SAMPLE_QA_ONLY")
            self.assertEqual((source / "draft.md").read_text(), "AUTHOR_SAMPLE_QA_ONLY")
            other = folder / "unrelated-secret.md"
            other.write_text("NOT_A_PART_OF_EMBERWRITER", encoding="utf-8")
            link = source / "outside.md"
            try:
                link.symlink_to(other)
            except OSError:
                self.skipTest("Filesystem won't permit creating a safe QA symlink")
            with self.assertRaisesRegex(RuntimeError, "External symlink"):
                manage.copy_verified(source, folder / "failed snapshot")
            self.assertEqual(other.read_text(), "NOT_A_PART_OF_EMBERWRITER")

    def test_demo_and_private_sources_survive_install_repair(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            launcher = root / "pinokio isolated"
            app = launcher / "app"
            app.mkdir(parents=True)
            (launcher / "data" / "projects").mkdir(parents=True)
            (launcher / "data" / "projects" / "private-chapter.md").write_text(
                "PRIVATE MANUSCRIPT NOT TEST DATA", encoding="utf-8"
            )
            (launcher / "demo-data" / "projects").mkdir(parents=True)
            (launcher / "demo-data" / "projects" / "sample-chapter.md").write_text(
                "VISIBLE SYNTHETIC DEMO", encoding="utf-8"
            )
            (app / ".ember").mkdir()
            (app / ".ember" / "my-preferences.json").write_text('{"theme":"ember"}')
            with patch.object(manage, "ROOT", launcher), patch.object(manage, "APP", app):
                manage.seed_data()
                manifest = manage.backup()
                assert (manifest / "data" / "projects" / "private-chapter.md").read_text() == (
                    "PRIVATE MANUSCRIPT NOT TEST DATA"
                )
                assert (manifest / "demo-data" / "projects" / "sample-chapter.md").read_text() == (
                    "VISIBLE SYNTHETIC DEMO"
                )
                manage.seed_data()
                self.assertEqual(
                    (app / ".ember" / "my-preferences.json").read_text(),
                    '{"theme":"ember"}',
                )
                self.assertEqual(
                    (launcher / "data" / "projects" / "private-chapter.md").read_text(),
                    "PRIVATE MANUSCRIPT NOT TEST DATA",
                )
                self.assertEqual(
                    (launcher / "demo-data" / "projects" / "sample-chapter.md").read_text(),
                    "VISIBLE SYNTHETIC DEMO",
                )

    @unittest.skipUnless(os.name == "nt", "Windows NTFS junction test")
    def test_ntfs_junction_from_data_cannot_escape_backup_root(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "source-author-library"
            source.mkdir()
            private = root / "unrelated"
            private.mkdir()
            (private / "secret.txt").write_text("OUT_OF_SCOPE", encoding="utf-8")
            alias = source / "junction"
            created = subprocess.run(["cmd.exe", "/c", "mklink", "/J", str(alias), str(private)],
                                     capture_output=True, text=True, timeout=15)
            if created.returncode != 0:
                self.skipTest("Junction unavailable on Windows test system")
            try:
                with self.assertRaisesRegex(RuntimeError, "External symlink"):
                    manage.copy_verified(source, root / "backups")
            finally:
                alias.rmdir()
            self.assertEqual((private / "secret.txt").read_text(), "OUT_OF_SCOPE")


if __name__ == "__main__":
    unittest.main()
