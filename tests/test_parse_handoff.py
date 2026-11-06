import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from parse_handoff import parse  # noqa: E402

SAMPLE = (ROOT / "sample.handoff").read_text()


class ParseHandoffTest(unittest.TestCase):
    def bad(self, text, msg):
        with self.assertRaises(ValueError) as ctx:
            parse(text)
        self.assertIn(msg, str(ctx.exception))

    def test_sample_valid(self):
        doc = parse(SAMPLE)
        self.assertEqual(doc["continue_from"], "robot_tick_8.py")
        self.assertEqual(doc["repo"], "https://github.com/fitzyracing1/lumen")
        self.assertEqual(doc["commit"], "b93be5644b6e5659606bfede4bd086d94cd215c2")
        self.assertIn("robot_tick_8.py", doc["files"])
        self.assertTrue(doc["paste"])

    def test_cli_sample_exit_zero(self):
        r = subprocess.run([sys.executable, str(ROOT / "parse_handoff.py"), str(ROOT / "sample.handoff")], capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stderr)

    def test_cli_invalid_exit_one(self):
        import tempfile
        with tempfile.NamedTemporaryFile("w", suffix=".handoff", delete=False) as f:
            f.write("nope\n")
        r = subprocess.run([sys.executable, str(ROOT / "parse_handoff.py"), f.name], capture_output=True, text=True)
        self.assertEqual(r.returncode, 1)
        self.assertIn("INVALID", r.stderr)

    def test_missing_banner(self):
        self.bad(SAMPLE.replace("# handoff v1\n", "", 1), "line 1")

    def test_wrong_banner(self):
        self.bad(SAMPLE.replace("# handoff v1", "# handoff v2", 1), "line 1")

    def test_missing_required_keys(self):
        for key in ("mission", "continue_from", "stop_rule"):
            text = "\n".join(l for l in SAMPLE.splitlines() if not l.startswith(key + ":"))
            with self.subTest(key=key):
                self.bad(text, f"missing {key}")

    def test_empty_files(self):
        lines = SAMPLE.splitlines()
        a, b = lines.index("FILES"), lines.index("PASTE")
        self.bad("\n".join(lines[: a + 1] + lines[b:]), "empty FILES")

    def test_empty_paste(self):
        lines = SAMPLE.splitlines()
        a, b = lines.index("PASTE"), lines.index("RULES")
        self.bad("\n".join(lines[: a + 1] + ["   "] + lines[b:]), "empty PASTE")

    def test_malformed_rules(self):
        self.bad(SAMPLE + "no separator here\n", "rule must split")

    def test_repo_commit_optional(self):
        text = "\n".join(l for l in SAMPLE.splitlines() if not l.startswith(("repo:", "commit:")))
        doc = parse(text)
        self.assertEqual(doc["repo"], "")
        self.assertEqual(doc["commit"], "")

    def test_bad_commit(self):
        self.bad(SAMPLE.replace("commit: b93be", "commit: zz3be", 1), "commit must")

    def test_bad_repo(self):
        self.bad(SAMPLE.replace("repo: https://", "repo: ftp://", 1), "repo must")

    def test_commit_requires_repo(self):
        text = "\n".join(l for l in SAMPLE.splitlines() if not l.startswith("repo:"))
        self.bad(text, "commit requires repo")


if __name__ == "__main__":
    unittest.main()
