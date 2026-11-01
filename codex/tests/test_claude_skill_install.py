import importlib.util
from pathlib import Path
import tempfile
import unittest


REPO = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("claude_skill_install", REPO / "claude/install-shared-skills.py")
installer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)


class ClaudeSkillInstallTests(unittest.TestCase):
    def test_rerun_preserves_live_shared_sources(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            upstream = root / "upstream"
            for name in installer.REQUIRED_ASC:
                source = upstream / name
                source.mkdir(parents=True)
                (source / "SKILL.md").write_text("original")
            links = installer.planned_links(REPO, root / "skills", root / "bin", upstream)
            installer.install_links(links)
            installer.install_links(links)
            for source, destination in links:
                self.assertTrue(destination.is_symlink())
                self.assertEqual(destination.resolve(), source.resolve())
            (upstream / "asc-cli-usage/SKILL.md").write_text("updated")
            self.assertEqual((root / "skills/asc-cli-usage/SKILL.md").read_text(), "updated")

    def test_conflicting_installation_stops_before_any_links_are_created(self):
        for kind in ("file", "directory", "broken_symlink"):
            with self.subTest(kind=kind), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                source = root / "source"
                source.write_text("source")
                conflict = root / "existing"
                if kind == "file":
                    conflict.write_text("keep")
                elif kind == "directory":
                    conflict.mkdir()
                else:
                    conflict.symlink_to(root / "missing")
                with self.assertRaises(ValueError):
                    installer.install_links([(source, root / "first"), (source, conflict)])
                self.assertFalse((root / "first").exists())
                self.assertTrue(conflict.exists() or conflict.is_symlink())
                if kind == "file":
                    self.assertEqual(conflict.read_text(), "keep")

    def test_missing_asc_pack_requires_setup_without_creating_destinations(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            with self.assertRaisesRegex(ValueError, "asc install-skills"):
                installer.planned_links(REPO, root / "skills", root / "bin", root / "missing")
            self.assertEqual(list(root.iterdir()), [])


if __name__ == "__main__":
    unittest.main()
