"""RA1 minimal tests: downstream raw-hash invariant + Arm C lineage (contract sections 3.3, 10)."""
from __future__ import annotations

import hashlib
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

PKG = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PKG / "scripts"))

from validate_p1 import sha256_text, validate_case  # noqa: E402
from render_cqs import render  # noqa: E402

RAW = "测试叙事 raw narrative line.\n"


def cqs_dict(artifact_id: str) -> dict:
    return {
        "artifact_id": artifact_id,
        "schema_version": "0.1",
        "source_narrative_sha256": hashlib.sha256(RAW.encode("utf-8")).hexdigest(),
        "source_narrative": RAW,
        "questions": [
            {
                "question_id": "CQ-01",
                "statement": "A searchable scientific question?",
                "source_trace": [{"exact_quote": "raw narrative line"}],
                "question_type": "MECHANISM",
                "dependencies": [],
                "resolution_condition": "Any evidence that resolves it.",
                "uncertainty": None,
            }
        ],
    }


def prep_dict(arm: str, raw_sha: str) -> dict:
    return {
        "case_id": "case_test",
        "arm": arm,
        "generated_from": "raw_narrative.txt",
        "raw_input_sha256": raw_sha,
        "question_ids_to_search": [{"question_id": "QA-01" if arm == "A" else "CQ-01", "search_question": "x"}],
        "question_order_if_any": [],
        "reason_for_order": "",
        "questions_blocked_by_prerequisite": [],
        "questions_independently_searchable": [],
        "missing_information_before_search": [],
    }


def build_case(root: Path, *, arm_a_sha=None, arm_b_sha=None, arm_c=None) -> Path:
    case = root / "case_test"
    (case / "arm_a").mkdir(parents=True)
    (case / "arm_b").mkdir()
    (case / "evaluation").mkdir()
    raw_sha = sha256_text(RAW)
    (case / "raw_narrative.txt").write_text(RAW, encoding="utf-8")
    (case / "case_metadata.json").write_text(json.dumps(
        {"case_id": "case_test", "case_family": "C", "input_status": "RAW",
         "input_sha256": raw_sha, "source_origin": "test", "model_config": "test",
         "run_timestamp": "t", "arm_a_run_id": None, "arm_b_run_id": None, "arm_c_run_id": None},
        ensure_ascii=False), encoding="utf-8")
    (case / "arm_a" / "downstream_preparation.json").write_text(json.dumps(
        prep_dict("A", arm_a_sha or raw_sha), ensure_ascii=False), encoding="utf-8")
    (case / "arm_a" / "human_render.md").write_text("arm a render\n", encoding="utf-8")
    (case / "arm_b" / "candidate_question_set.json").write_text(json.dumps(cqs_b := cqs_dict("CQS-T-1"), ensure_ascii=False), encoding="utf-8")
    (case / "arm_b" / "downstream_preparation.json").write_text(json.dumps(
        prep_dict("B", arm_b_sha or raw_sha), ensure_ascii=False), encoding="utf-8")
    (case / "arm_b" / "human_render.md").write_text(render(cqs_b), encoding="utf-8")
    (case / "evaluation" / "comparison.json").write_text("{}", encoding="utf-8")
    (case / "evaluation" / "adjudication.md").write_text("adj\n", encoding="utf-8")
    if arm_c is not None:
        cdir = case / "arm_c"
        cdir.mkdir()
        prior_path = case / "arm_b" / "candidate_question_set.json"
        prior_sha = hashlib.sha256(prior_path.read_bytes()).hexdigest()
        (cdir / "revised_candidate_question_set.json").write_text(json.dumps(arm_c, ensure_ascii=False) + "\n", encoding="utf-8")
        rev_file_sha = hashlib.sha256((cdir / "revised_candidate_question_set.json").read_bytes()).hexdigest()
        (cdir / "failure_diagnosis.json").write_text(json.dumps({
            "case_id": "case_test", "diagnosis_source": "test",
            "prior_artifact_id": "CQS-T-1", "prior_artifact_sha256": prior_sha,
            "observed_conflict": "c", "diagnosis": "d", "implicated_fields": ["CQ-01.dependencies"],
            "repair_instruction": "r", "revised_artifact_id": "CQS-T-1-RC1",
            "revised_artifact_sha256": rev_file_sha,
        }, ensure_ascii=False), encoding="utf-8")
        (cdir / "downstream_preparation.json").write_text(json.dumps(
            {**prep_dict("C", raw_sha),
             "source_artifact_id": "CQS-T-1-RC1",
             "source_artifact_sha256": rev_file_sha},
            ensure_ascii=False), encoding="utf-8")
        (cdir / "human_render.md").write_text(render(arm_c), encoding="utf-8")
    return case


def run_validate(case: Path) -> dict:
    errors: list[str] = []
    results: list[dict] = []
    res = validate_case(case, errors, results)
    res["errors"] = errors
    return res


class TestDownstreamHashInvariant(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_matching_hashes_pass(self):
        res = run_validate(build_case(self.tmp))
        self.assertTrue(res["checks"]["arm_a_raw_hash_valid"])
        self.assertTrue(res["checks"]["arm_b_raw_hash_valid"])
        self.assertTrue(res["ok"])

    def test_mismatching_arm_a_hash_fails(self):
        bad = "0" * 64
        res = run_validate(build_case(self.tmp, arm_a_sha=bad))
        self.assertFalse(res["checks"]["arm_a_raw_hash_valid"])
        self.assertFalse(res["ok"])
        self.assertTrue(any("arm_a" in e for e in res["errors"]))

    def test_mismatching_arm_b_hash_fails(self):
        bad = "1" * 64
        res = run_validate(build_case(self.tmp, arm_b_sha=bad))
        self.assertFalse(res["checks"]["arm_b_raw_hash_valid"])
        self.assertFalse(res["ok"])

    def test_arm_c_lineage_valid_passes(self):
        revised = cqs_dict("CQS-T-1-RC1")
        revised["questions"][0]["dependencies"] = ["CQ-01"]  # must differ from prior
        revised["questions"][0]["dependencies"] = []
        revised["artifact_id"] = "CQS-T-1-RC1"
        # make revised differ: change uncertainty
        revised["questions"][0]["uncertainty"] = "revised"
        res = run_validate(build_case(self.tmp, arm_c=revised))
        self.assertTrue(res["checks"]["arm_c_lineage_valid"], res["errors"])
        self.assertTrue(res["checks"]["arm_c_raw_hash_valid"])
        self.assertTrue(res["ok"])

    def test_retry_mislabeled_as_redigestion_fails(self):
        prior = cqs_dict("CQS-T-1")
        res = run_validate(build_case(self.tmp, arm_c=prior))  # identical to prior
        self.assertFalse(res["checks"].get("arm_c_lineage_valid", True))
        self.assertFalse(res["ok"])

    def test_broken_prior_hash_binding_fails(self):
        revised = cqs_dict("CQS-T-1-RC1")
        revised["questions"][0]["uncertainty"] = "revised"
        case = build_case(self.tmp, arm_c=revised)
        fd = json.loads((case / "arm_c" / "failure_diagnosis.json").read_text(encoding="utf-8"))
        fd["prior_artifact_sha256"] = "f" * 64
        (case / "arm_c" / "failure_diagnosis.json").write_text(json.dumps(fd), encoding="utf-8")
        res = run_validate(case)
        self.assertFalse(res["checks"]["arm_c_lineage_valid"])
        self.assertFalse(res["ok"])


if __name__ == "__main__":
    unittest.main()
