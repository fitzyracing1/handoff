import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from parse_handoff import parse  # noqa: E402

SAMPLE = (ROOT / "sample.handoff").read_text()
V1 = SAMPLE.replace("# handoff v2", "# handoff v1", 1)


class ParseHandoffTest(unittest.TestCase):
    def bad(self, text, msg):
        with self.assertRaises(ValueError) as ctx:
            parse(text)
        self.assertIn(msg, str(ctx.exception))

    def test_sample_valid(self):
        doc = parse(SAMPLE)
        self.assertEqual(doc["version"], 2)
        self.assertEqual(doc["continue_from"], "lumen.py")
        self.assertEqual(doc["repo"], "https://github.com/fitzyracing1/lumen")
        self.assertEqual(doc["commit"], "b93be5644b6e5659606bfede4bd086d94cd215c2")
        self.assertIn("lumen.py", doc["files"])
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
        self.bad(SAMPLE.replace("# handoff v2\n", "", 1), "line 1")

    def test_wrong_banner(self):
        self.bad(SAMPLE.replace("# handoff v2", "# handoff v0", 1), "line 1")

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

    def test_repo_commit_optional_in_v1(self):
        text = "\n".join(l for l in V1.splitlines() if not l.startswith(("repo:", "commit:")))
        doc = parse(text)
        self.assertEqual(doc["repo"], "")
        self.assertEqual(doc["commit"], "")

    def test_bad_commit(self):
        self.bad(SAMPLE.replace("commit: b93be", "commit: zz3be", 1), "commit must")

    def test_bad_repo(self):
        self.bad(SAMPLE.replace("repo: https://", "repo: ftp://", 1), "repo must")

    def test_commit_requires_repo(self):
        text = "\n".join(l for l in V1.splitlines() if not l.startswith("repo:"))
        self.bad(text, "commit requires repo")

    def test_v1_pinned_valid(self):
        self.assertEqual(parse(V1)["version"], 1)

    def test_v2_requires_repo_and_commit(self):
        for key in ("repo", "commit"):
            text = "\n".join(l for l in SAMPLE.splitlines() if not l.startswith(key + ":"))
            with self.subTest(key=key):
                self.bad(text, f"v2 requires {key}")

    def test_v1_bad_repo_and_commit_still_rejected(self):
        self.bad(V1.replace("repo: https://", "repo: ftp://", 1), "repo must")
        self.bad(V1.replace("commit: b93be", "commit: B93BE", 1), "commit must")

    def test_unknown_banner(self):
        self.bad(SAMPLE.replace("# handoff v2", "# handoff v3", 1), "line 1")

    def test_missing_fences(self):
        lines = SAMPLE.splitlines()
        self.bad("\n".join([lines[0]] + lines[2:]), "opening")
        self.bad("\n".join(l for i, l in enumerate(lines) if not (i > 1 and l == "---")), "closing")

    def test_rules_optional(self):
        lines = SAMPLE.splitlines()
        self.assertEqual(parse("\n".join(lines[: lines.index("RULES")]))["rules"], {})

    def test_paste_verbatim(self):
        doc = parse(SAMPLE)
        lines = SAMPLE.splitlines()
        a, b = lines.index("PASTE"), lines.index("RULES")
        self.assertEqual(doc["paste"], "\n".join(lines[a + 1 : b]))

    def test_sample_files_match_pinned_lumen_tree(self):
        # Snapshot of the lumen tree at the pinned commit (offline; the runtime re-checks live).
        tree = (ROOT / "tests" / "lumen_tree_b93be56.txt").read_text().split()
        for path in parse(SAMPLE)["files"]:
            self.assertIn(path, tree)


if __name__ == "__main__":
    unittest.main()
