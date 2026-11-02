import hashlib
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

    def test_duoctl_link_keeps_its_helper_and_licence_beside_it(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            upstream = root / "upstream"
            for name in installer.REQUIRED_ASC:
                (upstream / name).mkdir(parents=True)
                (upstream / name / "SKILL.md").write_text("skill")
            links = dict((destination.name, source)
                         for source, destination in installer.planned_links(REPO, root / "skills", root / "bin", upstream))
            self.assertIn("simulator-control", links)
            duoctl = links["duoctl"]
            # duoctl finds its helper next to its resolved path, so a symlink in bin must still reach it.
            self.assertTrue((duoctl.resolve().parent / "duoctl-helper.m").is_file())
            self.assertTrue((duoctl.resolve().parent / "LICENSE").is_file())

    def test_vendored_duoctl_matches_its_recorded_hashes(self):
        vendor = REPO / "codex/skills/simulator-control/vendor/duoctl"
        readme = (vendor / "README.md").read_text()
        for name in ("duoctl", "duoctl-helper.m"):
            digest = hashlib.sha256((vendor / name).read_bytes()).hexdigest()
            self.assertIn(f"| `{name}` | `{digest}` |", readme)


if __name__ == "__main__":
    unittest.main()
