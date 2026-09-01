"""P4-RA2 minimal invariant tests (contract section 19)."""
from __future__ import annotations

import json
import unittest
from pathlib import Path

PKG = Path(__file__).resolve().parents[1]
DOCS = PKG / "docs"
S5 = PKG / "benchmarks" / "p4" / "contextual" / "s5_mixed_commitment"
S1 = PKG / "benchmarks" / "p4" / "contextual" / "s1_vms_cellular_mechanism"

FORBIDDEN_S5 = ["animal experiment", "animal-experiment", "动物实验", "downstream experimental design",
                "importance context", "重要性语境"]
FORBIDDEN_S1 = ["formerly named", "unadmitted mechanism lines", "repair-history"]


def _load(p: Path):
    return json.loads(p.read_text(encoding="utf-8"))


class TestS5RationaleAuthority(unittest.TestCase):
    def setUp(self):
        self.env = _load(S5 / "budget_envelope.json")

    def test_al03_rationale_clean(self):
        al03 = next(a for a in self.env["allocations"] if a["allocation_id"] == "AL03")
        blob = al03["rationale"].lower()
        for term in FORBIDDEN_S5:
            self.assertNotIn(term.lower(), blob, f"AL03 rationale contains forbidden: {term}")

    def test_al03_amounts_untouched(self):
        al03 = next(a for a in self.env["allocations"] if a["allocation_id"] == "AL03")
        self.assertEqual(al03["activation"], "COMMITTED")
        self.assertGreater(al03["wall_clock_target_minutes"], 0)
        self.assertGreater(al03["model_token_target"], 0)

    def test_pre_ra2_evidence_preserved(self):
        pre = S5 / "budget_envelope.pre_ra2.json"
        self.assertTrue(pre.is_file(), "pre-RA2 envelope bytes not preserved")
        pre_env = _load(pre)
        al03 = next(a for a in pre_env["allocations"] if a["allocation_id"] == "AL03")
        self.assertIn("动物实验设计", al03["rationale"], "pre-RA2 evidence should show the leak")

    def test_redigestion_record_bound(self):
        rec = _load(S5 / "evaluation" / "redigestion_record.json")
        self.assertEqual(rec["diagnosis_source"], "HO+ChatGPT P4-RA1 acceptance")
        self.assertEqual(rec["revised_budget_envelope_id"], self.env["artifact_id"])
        import hashlib
        self.assertEqual(rec["revised_budget_envelope_sha256"],
                         hashlib.sha256((S5 / "budget_envelope.json").read_bytes()).hexdigest())

    def test_s5_review_records_initial_leak_and_final_state(self):
        br = _load(S5 / "evaluation" / "budget_review.json")
        prelim = br["local_claw_preliminary_review"]
        self.assertIn("initial/pre-repair observation", prelim.get("initial_leak_observation", ""))
        self.assertIn("removed", prelim.get("ra2_final_state", ""))
        self.assertEqual(br["final_semantic_adjudication"]["status"], "PENDING_HO_CHATGPT")


class TestS1RationaleCleanup(unittest.TestCase):
    def test_final_rationale_no_repair_history(self):
        env = _load(S1 / "budget_envelope.json")
        al01 = next(a for a in env["allocations"] if a["allocation_id"] == "AL01")
        for term in FORBIDDEN_S1:
            self.assertNotIn(term.lower(), al01["rationale"].lower(),
                             f"S1 AL01 rationale contains repair history: {term}")

    def test_history_preserved_in_artifacts(self):
        init = _load(S1 / "budget_envelope.initial.json")
        al01 = next(a for a in init["allocations"] if a["allocation_id"] == "AL01")
        self.assertIn("中枢与血管", al01["rationale"], "pre-repair leak should be visible in the initial artifact")
        rec = _load(S1 / "evaluation" / "redigestion_record.json")
        self.assertIn("ra2_round", rec)
        self.assertIn("repair-history", rec["ra2_round"]["measured_failure"])


class TestCanonicalTruth(unittest.TestCase):
    def test_summary_deep_count_correct(self):
        t = (DOCS / "CQC_P4_SUMMARY.md").read_text(encoding="utf-8")
        self.assertIn("3 COMMITTED + 1 RESERVE_CONDITIONAL", t)
        self.assertNotIn("4 COMMITTED (3+1 reserve)", t)

    def test_summary_contains_closure_section(self):
        t = (DOCS / "CQC_P4_SUMMARY.md").read_text(encoding="utf-8")
        self.assertIn("P4-RA1/RA2 Final Closure", t)
        for key in ("resource_authority", "s1:", "s2:", "s5:", "review_truth:",
                    "shared_requirement:", "canonical_integrity:", "p4_ra1_meaningful_push_ci_cycles: 2"):
            self.assertIn(key, t)

    def test_metrics_review_truth_fields(self):
        m = _load(DOCS / "CQC_P4_METRICS.json")
        self.assertEqual(m["contextual_review_hash_valid_count"], 6)
        self.assertEqual(m["contextual_review_machine_truth_valid_count"], 6)

    def test_metrics_perturbation_truth_fields(self):
        m = _load(DOCS / "CQC_P4_METRICS.json")
        self.assertEqual(m["budget_perturbation_case_count"], 2)
        self.assertEqual(m["budget_perturbation_source_srp_identity_valid_count"], 2)
        self.assertEqual(m["quick_standard_deep_semantic_invariance_valid_count"], 1)

    def test_ra1_cycle_count_truthful(self):
        m = _load(DOCS / "CQC_P4_METRICS.json")
        self.assertEqual(m["p4_ra1_meaningful_push_ci_cycles"], 2)
        self.assertEqual(m["meaningful_push_ci_cycles_current_step"], 1)


class TestManifestCoverage(unittest.TestCase):
    def test_manifest_contains_metrics(self):
        t = (DOCS / "CQC_P4_SHA256_MANIFEST.txt").read_text(encoding="utf-8")
        self.assertIn("docs/CQC_P4_METRICS.json", t)

    def test_mandatory_paths_all_listed(self):
        t = (DOCS / "CQC_P4_SHA256_MANIFEST.txt").read_text(encoding="utf-8")
        import sys
        sys.path.insert(0, str(PKG / "scripts"))
        from validate_p4 import MANDATORY_P4_MANIFEST_PATHS
        for p in MANDATORY_P4_MANIFEST_PATHS:
            self.assertIn(p, t, f"manifest missing mandatory path {p}")

    def test_coverage_missing_is_detected(self):
        import sys, hashlib
        sys.path.insert(0, str(PKG / "scripts"))
        from validate_p4 import validate_final_manifest
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            tmp_docs = Path(td) / "docs"
            tmp_docs.mkdir(parents=True)
            summary = tmp_docs / "CQC_P4_SUMMARY.md"
            summary.write_text("x", encoding="utf-8")
            real_sha = hashlib.sha256(summary.read_bytes()).hexdigest()
            mf = tmp_docs / "CQC_P4_SHA256_MANIFEST.txt"
            mf.write_text((f"{real_sha}  docs/CQC_P4_SUMMARY.md\n"), encoding="utf-8")
            errors: list[str] = []
            import validate_p4 as vp
            old_docs, old_pkg = vp.DOCS, vp.PKG
            vp.DOCS = tmp_docs
            vp.PKG = Path(td)
            try:
                out = vp.validate_final_manifest(errors)
            finally:
                vp.DOCS, vp.PKG = old_docs, old_pkg
            self.assertFalse(out.get("final_manifest_valid"))
            self.assertTrue(any("COVERAGE_MISSING" in e for e in errors))


if __name__ == "__main__":
    unittest.main()
