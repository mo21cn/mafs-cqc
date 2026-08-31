"""P2 minimal invariant tests: revision-topology truth + semantic package facts."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

PKG = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PKG / "scripts"))

from validate_p2 import _state_of, _load_artifacts, validate_semantic  # noqa: E402


class TestRevisionTopology(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r1 = PKG / "benchmarks" / "p2" / "revision_topology" / "r1_diamond"
        cls.r2 = PKG / "benchmarks" / "p2" / "revision_topology" / "r2_sequential"

    def test_r1_stages_match_expected(self):
        arts = _load_artifacts(self.r1 / "fixtures")
        expected = json_load(self.r1 / "expected_state.json")
        for stage in expected["stages"]:
            memo = {}
            currents = stage["current_revisions"]
            for key in stage["expected"]:
                aid, rev = key.rsplit("@", 1)
                actual = _state_of(aid, int(rev), arts, currents, memo)
                self.assertEqual(stage["expected"][key], actual,
                                 f"{stage['stage']}: {key} expected {stage['expected'][key]}, got {actual}")

    def test_r1_transitive_stale_through_diamond(self):
        arts = _load_artifacts(self.r1 / "fixtures")
        currents = {"P2B-A": 1, "P2B-B": 0, "P2B-C": 0, "P2B-D": 0}
        self.assertEqual(_state_of("P2B-D", 0, arts, currents, {}), "stale",
                         "D0 must be transitively stale when both parents are stale")

    def test_r2_partial_regeneration(self):
        arts = _load_artifacts(self.r2 / "fixtures")
        currents = {"P2B-A": 1, "P2B-B": 1, "P2B-C": 0}
        self.assertEqual(_state_of("P2B-B", 1, arts, currents, {}), "current")
        self.assertEqual(_state_of("P2B-C", 0, arts, currents, {}), "stale")

    def test_r2_repeated_revision_stales_everything(self):
        arts = _load_artifacts(self.r2 / "fixtures")
        currents = {"P2B-A": 2, "P2B-B": 1, "P2B-C": 0}
        self.assertEqual(_state_of("P2B-B", 1, arts, currents, {}), "stale")
        self.assertEqual(_state_of("P2B-C", 0, arts, currents, {}), "stale")


class TestSemanticPackages(unittest.TestCase):
    def test_six_cases_complete_and_valid(self):
        errors: list[str] = []
        sem = validate_semantic(errors)
        self.assertEqual(sem["case_count"], 6)
        self.assertEqual(sem["schema_valid"], 6)
        self.assertEqual(sem["trace_valid"], 6)
        self.assertEqual(sem["render_valid"], 6)
        self.assertEqual(sem["review_present"], 6)
        self.assertEqual(errors, [])

    def test_s6_single_question_case_is_valid(self):
        art = json_load(PKG / "benchmarks" / "p2" / "semantic" / "s6_narrow_source_check" / "candidate_question_set.json")
        self.assertEqual(len(art["questions"]), 1,
                         "s6 is the no-decomposition stress case; 1 CQ is the expected output")
        self.assertEqual(art["questions"][0]["question_type"], "SOURCE_CONTENT")


def json_load(p: Path):
    import json
    return json.loads(p.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
