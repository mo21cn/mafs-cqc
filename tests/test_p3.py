"""P3 minimal invariant tests (contract section 27)."""
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

PKG = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PKG / "scripts"))

from render_srp import render  # noqa: E402

P3 = PKG / "benchmarks" / "p3" / "contextual"
CASES = sorted(d for d in P3.iterdir() if d.is_dir())


def _load(p: Path):
    return json.loads(p.read_text(encoding="utf-8"))


class TestSourceBinding(unittest.TestCase):
    def test_all_six_cases_present(self):
        self.assertEqual(len(CASES), 6)

    def test_source_narrative_sha_binding(self):
        for c in CASES:
            meta = _load(c / "case_metadata.json")
            srp = _load(c / "search_requirement_profile.json")
            raw = (c / "source_narrative.txt").read_text(encoding="utf-8")
            import hashlib
            sha = hashlib.sha256(raw.encode("utf-8")).hexdigest()
            self.assertEqual(sha, meta["source_narrative_sha256"], c.name)
            self.assertEqual(sha, srp["source_narrative_sha256"], c.name)
            self.assertEqual(raw, srp["source_narrative"], c.name)

    def test_source_cqs_sha_binding_and_p2_drift_free(self):
        import hashlib
        for c in CASES:
            meta = _load(c / "case_metadata.json")
            srp = _load(c / "search_requirement_profile.json")
            cqs_bytes = (c / "source_cqs.json").read_bytes()
            sha = hashlib.sha256(cqs_bytes).hexdigest()
            self.assertEqual(sha, meta["source_cqs_sha256"], c.name)
            self.assertEqual(sha, srp["source_cqs_sha256"], c.name)
            p2_bytes = (PKG / "benchmarks" / "p2" / "semantic" / c.name / "candidate_question_set.json").read_bytes()
            self.assertEqual(cqs_bytes, p2_bytes, f"{c.name}: source CQS drifted from P2 final")


class TestRequirementStructure(unittest.TestCase):
    def test_target_refs_exist_no_orphans(self):
        for c in CASES:
            srp = _load(c / "search_requirement_profile.json")
            cqs = _load(c / "source_cqs.json")
            qids = {q["question_id"] for q in cqs["questions"]}
            rids = []
            for r in srp["requirements"]:
                self.assertTrue(r["target_question_ids"], f"{c.name}: orphan requirement {r['requirement_id']}")
                for t in r["target_question_ids"]:
                    self.assertIn(t, qids, f"{c.name}: {r['requirement_id']} -> missing {t}")
                rids.append(r["requirement_id"])
            self.assertEqual(len(rids), len(set(rids)), f"{c.name}: duplicate requirement ids")

    def test_route_status_enum_and_unique_ids(self):
        for c in CASES:
            srp = _load(c / "search_requirement_profile.json")
            for r in srp["requirements"]:
                route_ids = [rt["route_id"] for rt in r["epistemic_routes"]]
                self.assertEqual(len(route_ids), len(set(route_ids)), c.name)
                for rt in r["epistemic_routes"]:
                    self.assertIn(rt["status"], ("REQUIRED", "CONDITIONAL"), c.name)
                    self.assertTrue(rt["condition"].strip(), c.name)

    def test_conditional_routes_exist_where_uncertainty_demands(self):
        srp3 = _load(P3 / "s3_antagonist_domains" / "search_requirement_profile.json")
        statuses = {rt["route_id"]: rt["status"] for r in srp3["requirements"] for rt in r["epistemic_routes"]}
        self.assertEqual(statuses.get("domain_coverage_inventory"), "CONDITIONAL",
                         "S3: inventory routes must stay conditional until referent disambiguation (P3-C)")
        srp6 = _load(P3 / "s6_narrow_source_check" / "search_requirement_profile.json")
        statuses6 = {rt["route_id"]: rt["status"] for r in srp6["requirements"] for rt in r["epistemic_routes"]}
        self.assertEqual(statuses6.get("entity_resource_identity"), "CONDITIONAL",
                         "S6: identity route must stay conditional on reference-ambiguity materiality (P3-C)")


class TestNoExecutionLeakage(unittest.TestCase):
    def test_no_provider_or_query_terms(self):
        for c in CASES:
            srp = _load(c / "search_requirement_profile.json")
            blob = json.dumps(srp["requirements"], ensure_ascii=False).lower()
            for term in ("crossref", "pubmed", "google scholar", "top-k", "api endpoint"):
                self.assertNotIn(term, blob, f"{c.name}: leaked {term}")

    def test_named_evidence_objects_allowed(self):
        blob = json.dumps(_load(P3 / "s4_avca_donor_data" / "search_requirement_profile.json")["requirements"],
                          ensure_ascii=False).lower()
        self.assertIn("arc virtual cell atlas", blob)


class TestRenderDeterminism(unittest.TestCase):
    def test_all_renders_reproducible(self):
        for c in CASES:
            srp = _load(c / "search_requirement_profile.json")
            self.assertEqual(render(srp), (c / "human_render.md").read_text(encoding="utf-8"), c.name)


class TestTypePerturbation(unittest.TestCase):
    def test_only_type_changed_and_srp_valid(self):
        for td_name in ("t1_s3_cq01", "t2_s5_cq01"):
            td = PKG / "benchmarks" / "p3" / "type_perturbation" / td_name
            review = _load(td / "evaluation" / "type_perturbation_review.json")
            base = _load(P3 / review["base_case"] / "source_cqs.json")
            pert = _load(td / "source_cqs_perturbed.json")
            qid = review["perturbed_question_id"]
            bq = next(q for q in base["questions"] if q["question_id"] == qid)
            pq = next(q for q in pert["questions"] if q["question_id"] == qid)
            self.assertEqual(bq["question_type"], review["original_question_type"])
            self.assertEqual(pq["question_type"], review["perturbed_question_type"])
            for f in ("statement", "source_trace", "dependencies", "resolution_condition", "uncertainty"):
                self.assertEqual(bq.get(f), pq.get(f), f"{td_name}: non-type field {f} changed")
            self.assertEqual(base["source_narrative"], pert["source_narrative"], td_name)

    def test_perturbation_reviews_finalized(self):
        # P3-RA2: T1 finalized VALID_PASS; T2 finalized INVALID_CONTROL_DESIGN
        t1 = _load(PKG / "benchmarks" / "p3" / "type_perturbation" / "t1_s3_cq01" / "evaluation" / "type_perturbation_review.json")
        t2 = _load(PKG / "benchmarks" / "p3" / "type_perturbation" / "t2_s5_cq01" / "evaluation" / "type_perturbation_review.json")
        self.assertEqual(t1["final_semantic_adjudication"]["status"], "VALID_PASS")
        self.assertEqual(t2["final_semantic_adjudication"]["status"], "INVALID_CONTROL_DESIGN")


if __name__ == "__main__":
    unittest.main()
