"""P4 minimal deterministic invariant tests (contract section 40)."""
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

PKG = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PKG / "scripts"))

from render_budget_envelope import render  # noqa: E402

CTX = PKG / "benchmarks" / "p4" / "contextual"
PERT = PKG / "benchmarks" / "p4" / "budget_perturbation"


def _load(p: Path):
    return json.loads(p.read_text(encoding="utf-8"))


def _cases():
    return sorted(d for d in CTX.iterdir() if d.is_dir())


class TestSourceBinding(unittest.TestCase):
    def test_srp_sha_binding_and_p3_drift_free(self):
        import hashlib
        for c in _cases():
            meta_env = _load(c / "budget_envelope.json")
            srp_bytes = (c / "source_srp.json").read_bytes()
            sha = hashlib.sha256(srp_bytes).hexdigest()
            self.assertEqual(sha, meta_env["source_srp_sha256"], c.name)
            p3_bytes = (PKG / "benchmarks" / "p3" / "contextual" / c.name / "search_requirement_profile.json").read_bytes()
            self.assertEqual(srp_bytes, p3_bytes, f"{c.name}: source SRP drifted from P3 accepted bytes")


class TestAllocationIntegrity(unittest.TestCase):
    def test_allocation_refs_and_activation_legality(self):
        for c in _cases():
            env = _load(c / "budget_envelope.json")
            srp = _load(c / "source_srp.json")
            legal = {}
            for r in srp["requirements"]:
                for rt in r["epistemic_routes"]:
                    legal[(r["requirement_id"], rt["route_id"])] = rt["status"]
            seen = set()
            for a in env["allocations"]:
                key = (a["requirement_id"], a["route_id"])
                self.assertIn(key, legal, f"{c.name}: {a['allocation_id']} references non-SRP route {key}")
                self.assertNotIn(a["allocation_id"], seen, f"{c.name}: duplicate allocation_id")
                seen.add(a["allocation_id"])
                expected = "COMMITTED" if legal[key] == "REQUIRED" else "RESERVE_CONDITIONAL"
                self.assertEqual(a["activation"], expected,
                                 f"{c.name}: {a['allocation_id']} illegal activation for {key}")

    def test_conditional_never_committed(self):
        for c in _cases():
            env = _load(c / "budget_envelope.json")
            srp = _load(c / "source_srp.json")
            cond = set()
            for r in srp["requirements"]:
                for rt in r["epistemic_routes"]:
                    if rt["status"] == "CONDITIONAL":
                        cond.add((r["requirement_id"], rt["route_id"]))
            for a in env["allocations"]:
                if a["activation"] == "COMMITTED":
                    self.assertNotIn((a["requirement_id"], a["route_id"]), cond,
                                     f"{c.name}: CONDITIONAL route pre-activated as COMMITTED")


class TestAccounting(unittest.TestCase):
    def test_sums_and_ordering(self):
        for c in _cases():
            env = _load(c / "budget_envelope.json")
            te = env["total_envelope"]
            self.assertGreater(te["wall_clock"]["target_minutes"], 0, c.name)
            self.assertGreater(te["model_tokens"]["target_tokens"], 0, c.name)
            self.assertGreaterEqual(te["wall_clock"]["hard_ceiling_minutes"], te["wall_clock"]["target_minutes"], c.name)
            self.assertGreaterEqual(te["model_tokens"]["hard_ceiling_tokens"], te["model_tokens"]["target_tokens"], c.name)
            committed_wc = sum(a["wall_clock_target_minutes"] for a in env["allocations"] if a["activation"] == "COMMITTED")
            committed_tok = sum(a["model_token_target"] for a in env["allocations"] if a["activation"] == "COMMITTED")
            total_wc = sum(a["wall_clock_target_minutes"] for a in env["allocations"])
            total_tok = sum(a["model_token_target"] for a in env["allocations"])
            self.assertLessEqual(committed_wc, te["wall_clock"]["target_minutes"], c.name)
            self.assertLessEqual(committed_tok, te["model_tokens"]["target_tokens"], c.name)
            self.assertLessEqual(total_wc, te["wall_clock"]["hard_ceiling_minutes"], c.name)
            self.assertLessEqual(total_tok, te["model_tokens"]["hard_ceiling_tokens"], c.name)


class TestSharedRequirement(unittest.TestCase):
    def test_s4_shared_budgeted_once(self):
        env = _load(CTX / "s4_avca_donor_data" / "budget_envelope.json")
        srp = _load(CTX / "s4_avca_donor_data" / "source_srp.json")
        shared = [r for r in srp["requirements"] if len(r["target_question_ids"]) > 1]
        self.assertEqual(len(shared), 1, "S4 must have exactly one shared requirement")
        for r in shared:
            allocs = [a for a in env["allocations"] if a["requirement_id"] == r["requirement_id"]]
            self.assertEqual(len(allocs), 1, f"shared requirement {r['requirement_id']} double-budgeted")


class TestFeasibility(unittest.TestCase):
    def test_quick_s5_insufficient_with_exact_unfunded(self):
        env = _load(PERT / "quick_constraint_s5" / "budget_envelope.json")
        self.assertEqual(env["feasibility"]["status"], "INSUFFICIENT")
        unfunded = {(u["requirement_id"], u["route_id"]) for u in env["feasibility"]["unfunded_obligations"]}
        self.assertIn(("R02", "historical_lineage"), unfunded,
                      "QUICK stress must explicitly list R02/historical_lineage as unfunded")

    def test_deep_s5_feasible_same_obligations(self):
        quick = _load(PERT / "quick_constraint_s5" / "budget_envelope.json")
        deep = _load(PERT / "deep_expansion_s5" / "budget_envelope.json")
        std = _load(CTX / "s5_mixed_commitment" / "budget_envelope.json")
        self.assertEqual(deep["feasibility"]["status"], "FEASIBLE")
        # same-SRP identity: all three bind the identical accepted P3 SRP
        for e in (quick, std, deep):
            self.assertEqual(e["source_srp_sha256"], std["source_srp_sha256"])
            self.assertEqual(e["source_srp_id"], "SRP-CQC-P3-05-R1")
        # scientific obligations live at the SRP layer: byte-identical source SRPs
        srp_quick = (PERT / "quick_constraint_s5" / "source_srp.json").read_bytes()
        srp_std = (CTX / "s5_mixed_commitment" / "source_srp.json").read_bytes()
        srp_deep = (PERT / "deep_expansion_s5" / "source_srp.json").read_bytes()
        self.assertEqual(srp_quick, srp_std)
        self.assertEqual(srp_std, srp_deep)


class TestRender(unittest.TestCase):
    def test_all_renders_reproducible(self):
        for c in _cases():
            env = _load(c / "budget_envelope.json")
            self.assertEqual(render(env), (c / "human_render.md").read_text(encoding="utf-8"), c.name)
        for td in PERT.iterdir():
            if td.is_dir() and (td / "budget_envelope.json").is_file():
                env = _load(td / "budget_envelope.json")
                self.assertEqual(render(env), (td / "human_render.md").read_text(encoding="utf-8"), td.name)

    def test_no_provider_or_type_router_leak(self):
        for c in _cases():
            blob = json.dumps(_load(c / "budget_envelope.json")["allocations"], ensure_ascii=False).lower()
            for term in ("crossref", "pubmed", "google scholar", "question_type"):
                self.assertNotIn(term, blob, f"{c.name}: leaked {term}")


if __name__ == "__main__":
    unittest.main()
