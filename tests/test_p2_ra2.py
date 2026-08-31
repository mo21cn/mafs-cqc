"""P2-RA2 minimal invariant tests (contract section 12)."""
from __future__ import annotations

import json
import unittest
from pathlib import Path

PKG = Path(__file__).resolve().parents[1]
DOCS = PKG / "docs"
SEM = PKG / "benchmarks" / "p2" / "semantic"

CANON_P2_SHA = "9dcbe8c3efb28485ab4a2119e4415692a637fc35"
CANON_RA1_SHA = "a35b0bfbfa160577141ddfb34e8f6cadd7f82185"
INVALID_P2_SHA = "9dcbe8c9dd838093ee555852b62067d1ba4f70c"


def _load(p: Path):
    return json.loads(p.read_text(encoding="utf-8"))


class TestS3DanglingReference(unittest.TestCase):
    def test_s3_has_three_questions(self):
        art = _load(SEM / "s3_antagonist_domains" / "candidate_question_set.json")
        self.assertEqual(len(art["questions"]), 3)

    def test_s3_no_reference_to_deleted_cq04(self):
        art = _load(SEM / "s3_antagonist_domains" / "candidate_question_set.json")
        ids = {q["question_id"] for q in art["questions"]}
        self.assertNotIn("CQ-04", ids)
        for q in art["questions"]:
            for field in ("statement", "uncertainty", "resolution_condition"):
                txt = q.get(field) or ""
                self.assertNotIn("CQ-04", txt,
                                 f"{q['question_id']}.{field} still references deleted CQ-04")
                for ref in ("CQ-01", "CQ-02", "CQ-03"):
                    if ref in txt and ref != q["question_id"]:
                        self.assertIn(ref, ids)


class TestProvenanceTruth(unittest.TestCase):
    def test_ra1_metrics_full_length_sha_and_cycles(self):
        d = _load(DOCS / "CQC_P2_RA1_METRICS.json")
        self.assertEqual(d["evidence_commit_sha"], CANON_RA1_SHA)
        self.assertEqual(len(d["evidence_commit_sha"]), 40)
        self.assertEqual(str(d["evidence_ci_run_id"]), "33377496972")
        self.assertEqual(d["meaningful_push_ci_cycles"], 2)

    def test_ra1_pin_field_retired(self):
        d = _load(DOCS / "CQC_P2_RA1_METRICS.json")
        self.assertNotIn("metrics_pin_commit_sha", d)

    def test_p2_metrics_canonical_sha_no_invalid_no_pin(self):
        raw = (DOCS / "CQC_P2_METRICS.json").read_text(encoding="utf-8")
        d = _load(DOCS / "CQC_P2_METRICS.json")
        self.assertEqual(d["evidence_commit_sha"], CANON_P2_SHA)
        self.assertEqual(str(d["evidence_ci_run_id"]), "33357451991")
        self.assertNotIn(INVALID_P2_SHA, raw)
        self.assertNotIn("metrics_pin_commit_sha", d)
        self.assertNotIn("verified_commit_sha", d)

    def test_p2b_topology_still_passes(self):
        sys_path = str(PKG / "scripts")
        if sys_path not in __import__("sys").path:
            __import__("sys").path.insert(0, sys_path)
        import validate_p2 as vp
        errors: list[str] = []
        for sd in sorted((PKG / "benchmarks" / "p2" / "revision_topology").iterdir()):
            if sd.is_dir() and (sd / "expected_state.json").is_file():
                r = vp.validate_topology(sd, errors)
                self.assertTrue(r["ok"], f"{r['scenario']} regression")
        self.assertEqual(errors, [])


if __name__ == "__main__":
    unittest.main()
