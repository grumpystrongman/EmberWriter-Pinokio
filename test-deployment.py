"""Exercise SQLite WAL snapshots and non-destructive migration with synthetic data."""
import json
from pathlib import Path
import sqlite3
import tempfile
import unittest
from unittest.mock import patch

import manage


class DeploymentTests(unittest.TestCase):
    def test_wal_snapshot_verifies_and_releases_windows_handles(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            source = root / "source"
            source.mkdir()
            (source / "chapter.md").write_text("Synthetic manuscript", encoding="utf-8")
            con = sqlite3.connect(source / "story.db")
            try:
                con.execute("PRAGMA journal_mode=WAL")
                con.execute("CREATE TABLE revisions (body TEXT)")
                con.execute("INSERT INTO revisions VALUES ('persisted revision')")
                con.commit()
                dest = root / "staging"
                self.assertEqual(manage.copy_verified(source, dest), 2)
                dest.rename(root / "data")  # fails on Windows if backup leaves handles open
                copy = sqlite3.connect(root / "data" / "story.db")
                try:
                    self.assertEqual(copy.execute("SELECT body FROM revisions").fetchone()[0], "persisted revision")
                finally:
                    copy.close()
                self.assertFalse((root / "data" / "story.db-wal").exists())
            finally:
                con.close()

    def test_reinstall_does_not_overwrite_existing_data_or_preferences(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            source = root / "source"
            (source / "data").mkdir(parents=True)
            (source / "data" / "chapter.md").write_text("old", encoding="utf-8")
            (source / ".ember").mkdir()
            (source / ".ember" / "local-models.json").write_text('{"preferred_model":"old"}')
            launcher = root / "launcher"
            app = launcher / "app"
            app.mkdir(parents=True)
            (launcher / "config.local.json").write_text(json.dumps({"source": str(source)}))
            with patch.object(manage, "ROOT", launcher), patch.object(manage, "APP", app):
                manage.seed_data()
                (launcher / "data" / "chapter.md").write_text("new", encoding="utf-8")
                preference = app / ".ember" / "local-models.json"
                preference.write_text('{"preferred_model":"new"}')
                manage.seed_data()
                self.assertEqual((launcher / "data" / "chapter.md").read_text(), "new")
                self.assertIn('"new"', preference.read_text())
                self.assertEqual((source / "data" / "chapter.md").read_text(), "old")


if __name__ == "__main__":
    unittest.main()
