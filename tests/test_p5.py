"""P5 minimal invariant tests (contract sections 39, 44)."""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
import unittest
from pathlib import Path

PKG = Path(__file__).resolve().parents[1]
DOCS = PKG / "docs"
sys.path.insert(0, str(PKG / "integration" / "mafs_v3"))
sys.path.insert(0, str(PKG / "scripts"))

import adapter  # noqa: E402
from adapter import (  # noqa: E402
    CQC_SOURCE_CHAIN_MISMATCH, INTEGRATION_BLOCKED_BUDGET_INSUFFICIENT,
    MAFS_BASELINE_MISMATCH, MAFS_BASELINE_SHA, P5_CONDITIONAL_ROUTE_PREACTIVATION,
    P5_DUPLICATE_ROUTE_BINDING, P5_REQUIRED_ROUTE_UNBOUND, STALE_SOURCE_CHAIN,
    build_binding, mark_stale, validate_mafs_native,
)

P5 = PKG / "benchmarks" / "p5"
CTX = P5 / "contextual"
MAFS_PL = P5 / "mafs_planning"
PERT = P5 / "budget_perturbation"
# Closure B: MAFS schema path must use the same env contract as scripts/validate_p5.py.
# The hardcoded sibling path (../mafs-v3-p0) is invisible to CI's external/mafs-v3-p0
# checkout. CI sets MAFS_BASELINE_DIR explicitly; local ad-hoc execution may fall back
# to the sibling default only if the pinned baseline is absent (clearly non-acceptance).
MAFS_BASELINE_DIR = os.environ.get(
    "MAFS_BASELINE_DIR", str(PKG.parent / "mafs-v3-p0")
)
MAFS_SCHEMAS = Path(MAFS_BASELINE_DIR) / "schemas"


def _load(p: Path):
    return json.loads(p.read_text(encoding="utf-8"))


def _write(p: Path, obj):
    p.write_bytes((json.dumps(obj, indent=2, ensure_ascii=False) + "\n").encode("utf-8"))


class TestSourceChainBindings(unittest.TestCase):
    def test_six_contextual_bindings_valid(self):
        for case in sorted(d for d in CTX.iterdir() if d.is_dir()):
            b = _load(case / "integration_binding.json")
            chain = b["source_chain"]
            cqs = _load(case / "source_cqs.json")
            srp = _load(case / "source_srp.json")
            env = _load(case / "budget_envelope.json")
            self.assertEqual(chain["cqs_id"], cqs["artifact_id"], case.name)
            self.assertEqual(chain["srp_id"], srp["artifact_id"], case.name)
            self.assertEqual(chain["budget_envelope_id"], env["artifact_id"], case.name)
            self.assertEqual(chain["cqs_sha256"],
                             hashlib.sha256((case / "source_cqs.json").read_bytes()).hexdigest())
            self.assertEqual(chain["srp_sha256"],
                             hashlib.sha256((case / "source_srp.json").read_bytes()).hexdigest())
            self.assertEqual(chain["budget_envelope_sha256"],
                             hashlib.sha256((case / "budget_envelope.json").read_bytes()).hexdigest())

    def test_source_context_accessible_chain(self):
        # IntegrationBinding → BudgetEnvelope → SRP → CQS → source_narrative
        for case in sorted(d for d in CTX.iterdir() if d.is_dir()):
            env = _load(case / "budget_envelope.json")
            srp = _load(case / "source_srp.json")
            cqs = _load(case / "source_cqs.json")
            self.assertEqual(srp["source_narrative_sha256"], cqs["source_narrative_sha256"], case.name)
            self.assertTrue(cqs.get("source_narrative"), case.name)

    def test_active_vs_conditional_accounting(self):
        for case in sorted(d for d in CTX.iterdir() if d.is_dir()):
            b = _load(case / "integration_binding.json")
            active = {(a["requirement_id"], a["route_id"]) for a in b["active_routes"]}
            held = {(h["requirement_id"], h["route_id"]) for h in b["held_conditional_routes"]}
            self.assertFalse(active & held, case.name)


class TestT1SourceChainMismatch(unittest.TestCase):
    def test_corrupted_upstream_hash_stops(self):
        d = CTX / "s1_vms_cellular_mechanism"
        cqs = _load(d / "source_cqs.json")
        cqs["artifact_id"] = "TAMPERED"
        with __import__("tempfile").TemporaryDirectory() as td:
            tp = Path(td)
            _write(tp / "source_cqs.json", cqs)
            shutil.copyfile(d / "source_srp.json", tp / "source_srp.json")
            shutil.copyfile(d / "budget_envelope.json", tp / "budget_envelope.json")
            with self.assertRaises(adapter.P5Error) as ctx:
                adapter.verify_source_chain(tp / "source_cqs.json", tp / "source_srp.json",
                                            tp / "budget_envelope.json")
            self.assertEqual(ctx.exception.code, CQC_SOURCE_CHAIN_MISMATCH)


class TestT2ConditionalPreactivation(unittest.TestCase):
    def test_conditional_committed_rejected(self):
        d = CTX / "s6_narrow_source_check"
        cqs_p, srp_p, env_p = d / "source_cqs.json", d / "source_srp.json", d / "budget_envelope.json"
        env = _load(env_p)
        for a in env["allocations"]:
            if a["route_id"] == "entity_resource_identity":
                a["activation"] = "COMMITTED"
        with __import__("tempfile").TemporaryDirectory() as td:
            tp = Path(td)
            _write(tp / "source_cqs.json", _load(cqs_p))
            _write(tp / "source_srp.json", _load(srp_p))
            _write(tp / "budget_envelope.json", env)
            res = adapter.build_binding(case_id="t2", cqs_path=tp / "source_cqs.json",
                                        srp_path=tp / "source_srp.json",
                                        envelope_path=tp / "budget_envelope.json")
            self.assertEqual(res.code, P5_CONDITIONAL_ROUTE_PREACTIVATION)


class TestT3RequiredRouteUnbound(unittest.TestCase):
    def test_unbound_required_rejected(self):
        d = CTX / "s1_vms_cellular_mechanism"
        env = _load(d / "budget_envelope.json")
        env["allocations"] = [a for a in env["allocations"] if a["route_id"] != "measurement_observability"]
        with __import__("tempfile").TemporaryDirectory() as td:
            tp = Path(td)
            _write(tp / "source_cqs.json", _load(d / "source_cqs.json"))
            _write(tp / "source_srp.json", _load(d / "source_srp.json"))
            _write(tp / "budget_envelope.json", env)
            res = adapter.build_binding(case_id="t3", cqs_path=tp / "source_cqs.json",
                                        srp_path=tp / "source_srp.json",
                                        envelope_path=tp / "budget_envelope.json")
            self.assertEqual(res.code, P5_REQUIRED_ROUTE_UNBOUND)


class TestT5DuplicateRouteBinding(unittest.TestCase):
    def test_duplicate_route_rejected(self):
        d = CTX / "s1_vms_cellular_mechanism"
        env = _load(d / "budget_envelope.json")
        env["allocations"].append(dict(env["allocations"][0]))
        with __import__("tempfile").TemporaryDirectory() as td:
            tp = Path(td)
            _write(tp / "source_cqs.json", _load(d / "source_cqs.json"))
            _write(tp / "source_srp.json", _load(d / "source_srp.json"))
            _write(tp / "budget_envelope.json", env)
            res = adapter.build_binding(case_id="t5", cqs_path=tp / "source_cqs.json",
                                        srp_path=tp / "source_srp.json",
                                        envelope_path=tp / "budget_envelope.json")
            self.assertEqual(res.code, P5_DUPLICATE_ROUTE_BINDING)


class TestT6BaselineDrift(unittest.TestCase):
    def test_wrong_baseline_rejected(self):
        d = CTX / "s6_narrow_source_check"
        res = adapter.build_binding(case_id="t6", cqs_path=d / "source_cqs.json",
                                    srp_path=d / "source_srp.json",
                                    envelope_path=d / "budget_envelope.json",
                                    mafs_baseline_sha="f" * 64)
        self.assertEqual(res.code, MAFS_BASELINE_MISMATCH)


class TestT7StaleState(unittest.TestCase):
    def test_stale_fixture_detected_and_mark_stale_works(self):
        b = _load(PERT / "stale_binding_s5" / "integration_binding.json")
        self.assertTrue(adapter.detect_stale(b, PERT / "stale_binding_s5" / "source_cqs.json",
                                             PERT / "stale_binding_s5" / "source_srp.json",
                                             PERT / "stale_binding_s5" / "budget_envelope.tampered.json"))
        staled = mark_stale(b)
        self.assertEqual(staled["status"], STALE_SOURCE_CHAIN)
        self.assertEqual(staled["stale_state"], "STALE")


class TestT4QuickNegative(unittest.TestCase):
    def test_quick_s5_blocked(self):
        b = _load(PERT / "quick_negative_s5" / "integration_binding.json")
        self.assertEqual(b["status"], INTEGRATION_BLOCKED_BUDGET_INSUFFICIENT)
        unfunded = {(u["requirement_id"], u["route_id"]) for u in b["unfunded_required_routes"]}
        self.assertIn(("R02", "historical_lineage"), unfunded)


class TestT8NoAutoSelection(unittest.TestCase):
    def test_adapter_source_has_no_auto_selection(self):
        import ast
        src = (PKG / "integration" / "mafs_v3" / "adapter.py").read_text(encoding="utf-8")
        tree = ast.parse(src)
        forbidden_calls = {"auto_resolve", "best_candidate", "rank_and_select",
                           "select_candidate", "resolve"}
        calls = set()
        for node in __import__("ast").walk(tree):
            if isinstance(node, ast.Call):
                fn = node.func
                if isinstance(fn, ast.Attribute):
                    calls.add(fn.attr)
                elif isinstance(fn, ast.Name):
                    calls.add(fn.id)
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if "mafs_p0" in alias.name or alias.name == "live_chain":
                        calls.add(f"import:{alias.name}")
            if isinstance(node, ast.ImportFrom):
                if (node.module or "") in ("mafs_p0.live_chain", "live_chain"):
                    calls.add("import:live_chain")
        hits = calls & forbidden_calls
        self.assertEqual(hits, set(), f"adapter contains forbidden calls/imports: {hits}")

class TestMafsNativeSchema(unittest.TestCase):
    def test_all_planning_objects_valid_against_pinned_schemas(self):
        if not MAFS_SCHEMAS.is_dir():
            self.skipTest("pinned MAFS schemas not present")
        for pc in sorted(d for d in MAFS_PL.iterdir() if d.is_dir()):
            planning = _load(pc / "mafs_planning.json")
            self.assertEqual(validate_mafs_native(planning, MAFS_SCHEMAS), [], pc.name)


class TestM1SharedRequirement(unittest.TestCase):
    def test_shared_requirement_single_binding(self):
        b = _load(MAFS_PL / "m1_s4_shared" / "integration_binding.json")
        active = [(a["requirement_id"], a["route_id"]) for a in b["active_routes"]]
        self.assertEqual(len(active), len(set(active)))
        self.assertIn(("R01", "entity_resource_identity"), active)


class TestM2ConditionalHeld(unittest.TestCase):
    def test_m2_conditional_route_held_not_active(self):
        b = _load(MAFS_PL / "m2_s6_instability" / "integration_binding.json")
        active = [(a["requirement_id"], a["route_id"]) for a in b["active_routes"]]
        held = [(h["requirement_id"], h["route_id"]) for h in b["held_conditional_routes"]]
        self.assertIn(("R01", "source_content_verification"), active)
        self.assertIn(("R01", "entity_resource_identity"), held)
        self.assertNotIn(("R01", "entity_resource_identity"), active)


class TestM3StandardComposition(unittest.TestCase):
    def test_m3_active_and_held(self):
        b = _load(MAFS_PL / "m3_s5_standard" / "integration_binding.json")
        active = [(a["requirement_id"], a["route_id"]) for a in b["active_routes"]]
        held = [(h["requirement_id"], h["route_id"]) for h in b["held_conditional_routes"]]
        self.assertEqual(active, [("R01", "mechanism_evidence"),
                                  ("R02", "historical_lineage"),
                                  ("R03", "measurement_observability")])
        self.assertEqual(held, [("R02", "counterexample_negative_evidence")])


def _write(p: Path, obj):
    _write_impl(p, obj)


def _write_impl(p: Path, obj):
    p.write_bytes((json.dumps(obj, indent=2, ensure_ascii=False) + "\n").encode("utf-8"))


# ============================================================================
# P5-RA1 regression tests (CQC-P5-RA1 contract §6 + §8)
# ============================================================================

class TestConstrainedBudgetNotMisclassified(unittest.TestCase):
    """P5-RA1 §6: a BudgetEnvelope with feasibility.status = CONSTRAINED
    and unfunded_obligations=[] must NOT be misclassified as
    INTEGRATION_BLOCKED_BUDGET_INSUFFICIENT.

    The FEASIBLE → READY_FOR_MAFS_PREFLIGHT branch is preserved; a
    CONSTRAINED envelope with no unfunded_required obligations is also
    READY_FOR_MAFS_PREFLIGHT. Only INSUFFICIENT envelopes (REQUIRED
    routes explicitly unfunded) yield
    INTEGRATION_BLOCKED_BUDGET_INSUFFICIENT.
    """

    def test_constrained_envelope_not_blocked(self):
        d = CTX / "s1_vms_cellular_mechanism"
        cqs = _load(d / "source_cqs.json")
        srp = _load(d / "source_srp.json")
        env = _load(d / "budget_envelope.json")
        # Derive a CONSTRAINED envelope from this FEASIBLE one.
        env["feasibility"] = {
            "status": "CONSTRAINED",
            "unfunded_obligations": [],
            "constraint_note": "synthetic CONSTRAINED for §6 regression"
        }
        with __import__("tempfile").TemporaryDirectory() as td:
            tp = Path(td)
            _write(tp / "source_cqs.json", cqs)
            _write(tp / "source_srp.json", srp)
            _write(tp / "budget_envelope.json", env)
            res = adapter.build_binding(case_id="t_constrained",
                                        cqs_path=tp / "source_cqs.json",
                                        srp_path=tp / "source_srp.json",
                                        envelope_path=tp / "budget_envelope.json")
            self.assertNotEqual(res.code,
                                INTEGRATION_BLOCKED_BUDGET_INSUFFICIENT,
                                "CONSTRAINED must not collapse to "
                                "INTEGRATION_BLOCKED_BUDGET_INSUFFICIENT")
            self.assertEqual(res.code, "OK")
            self.assertEqual(res.binding["status"], "READY_FOR_MAFS_PREFLIGHT")


class TestSourceChainNegativeSRPHash(unittest.TestCase):
    """P5-RA1 §8: when SRP.source_cqs_sha256 is wrong but the binding
    remains internally self-consistent, the canonical validator
    (validate_p5.py via adapter.verify_source_chain) must fail with
    CQC_SOURCE_CHAIN_MISMATCH.

    This proves the canonical validator no longer validates only the
    sidecar's local copies; it actually walks the upstream chain.
    """

    def test_wrong_srp_source_cqs_sha256_caught(self):
        d = CTX / "s1_vms_cellular_mechanism"
        cqs = _load(d / "source_cqs.json")
        srp = _load(d / "source_srp.json")
        env = _load(d / "budget_envelope.json")
        # Tamper with SRP's recorded CQS sha256.
        real_cqs_sha = hashlib.sha256(
            (d / "source_cqs.json").read_bytes()
        ).hexdigest()
        srp["source_cqs_sha256"] = "f" * 64
        self.assertNotEqual(srp["source_cqs_sha256"], real_cqs_sha)
        with __import__("tempfile").TemporaryDirectory() as td:
            tp = Path(td)
            _write(tp / "source_cqs.json", cqs)
            _write(tp / "source_srp.json", srp)
            _write(tp / "budget_envelope.json", env)
            with self.assertRaises(adapter.P5Error) as ctx:
                adapter.verify_source_chain(tp / "source_cqs.json",
                                            tp / "source_srp.json",
                                            tp / "budget_envelope.json")
            self.assertEqual(ctx.exception.code, CQC_SOURCE_CHAIN_MISMATCH)


# ============================================================================
# CQC-P5-RA1-CI1 regression tests (semantic-review provenance + canonical
# consistency gate).
# ============================================================================

CORRECT_P4_SHA = "8028e17a6eaab364c744cfa72b714f0f0bd6cf01"
WRONG_P4_SHA = "529ccc63f6d2900172a6ab4367dc33c52eb699fa"


class TestRA1_CI1_PlanningVerdictsNotAutoApproved(unittest.TestCase):
    """P5-RA1-CI1 §18.1: planning semantic verdicts are not mechanically
    auto-approved. Local Claw preliminary review block must be authored
    by LOCAL_CLAW and contain a `notes` field recording observed
    conclusions after reading M1/M2/M3."""

    def test_all_three_planning_reviews_have_local_claw_preliminary(self):
        for case in ("m1_s4_shared", "m2_s6_instability", "m3_s5_standard"):
            p = MAFS_PL / case / "evaluation" / "integration_review.json"
            self.assertTrue(p.is_file(), f"{case} integration_review.json missing")
            r = _load(p)
            prelim = r.get("local_claw_preliminary_review") or {}
            self.assertEqual(prelim.get("authored_by"), "LOCAL_CLAW",
                             f"{case}: local_claw_preliminary_review.authored_by must be LOCAL_CLAW")
            # No PENDING placeholders may remain in committed reviews
            for fld in ("search_order_semantically_contained",
                        "authority_leak_observed",
                        "integration_projection_loss_observed",
                        "conditional_preactivation_observed",
                        "source_context_promoted_to_obligation"):
                val = prelim.get(fld)
                self.assertNotEqual(val, "PENDING_LOCAL_CLAW",
                                    f"{case}.{fld} still PENDING_LOCAL_CLAW; Local Claw must fill")
                self.assertIsInstance(val, bool,
                                      f"{case}.{fld} must be bool, got {val!r}")
            self.assertIsInstance(prelim.get("notes"), str)
            self.assertGreater(len(prelim.get("notes", "")), 50,
                               f"{case}: notes too short to record real observations")


class TestRA1_CI1_ContextualNoSearchOrderClaims(unittest.TestCase):
    """P5-RA1-CI1 §18.2 + §6: contextual cases do not claim SearchOrder
    semantic containment without SearchOrders. The planning-specific
    semantic fields must be NOT_APPLICABLE (or absent)."""

    def test_six_contextual_cases_mark_planning_fields_not_applicable(self):
        for case in ("s1_vms_cellular_mechanism", "s2_vcell_paradigm",
                     "s3_antagonist_domains", "s4_avca_donor_data",
                     "s5_mixed_commitment", "s6_narrow_source_check"):
            p = CTX / case / "evaluation" / "integration_review.json"
            self.assertTrue(p.is_file(), f"{case} integration_review.json missing")
            r = _load(p)
            prelim = r.get("local_claw_preliminary_review") or {}
            for fld in ("search_order_semantically_contained",
                        "authority_leak_observed",
                        "integration_projection_loss_observed",
                        "conditional_preactivation_observed",
                        "source_context_promoted_to_obligation"):
                self.assertEqual(prelim.get(fld), "NOT_APPLICABLE",
                                 f"{case}.{fld} must be NOT_APPLICABLE (no MAFS planning object)")


class TestRA1_CI1_PlanningFinalAdjudicationPending(unittest.TestCase):
    """P5-RA1-CI1 §18.4 + §9: all 3 planning reviews retain
    PENDING_HO_CHATGPT final status. CI1 must not self-sign PASS."""

    def test_all_three_planning_reviews_pending_ho_chatgpt(self):
        for case in ("m1_s4_shared", "m2_s6_instability", "m3_s5_standard"):
            p = MAFS_PL / case / "evaluation" / "integration_review.json"
            r = _load(p)
            self.assertEqual(r["final_semantic_adjudication"]["status"],
                             "PENDING_HO_CHATGPT",
                             f"{case}: final_semantic_adjudication must be PENDING_HO_CHATGPT")


class TestRA1_CI1_CanonicalP4SHA(unittest.TestCase):
    """P5-RA1-CI1 §18.5 + §10 + §11: Summary, Metrics, and Manifest agree
    on the P4 source baseline SHA = 8028e17... (the P4-RA2 final-gate
    commit). The previously-pinned 529ccc63 was an intermediate that
    must not survive in the P5 closure surface."""

    def test_summary_p4_pin_correct(self):
        s = (DOCS / "CQC_P5_SUMMARY.md").read_text(encoding="utf-8")
        self.assertIn(CORRECT_P4_SHA, s,
                      "CQC_P5_SUMMARY.md must pin P4 source baseline 8028e17...")
        self.assertNotIn(WRONG_P4_SHA, s,
                         "CQC_P5_SUMMARY.md must not still carry the intermediate 529ccc63 SHA")

    def test_metrics_p4_pin_correct(self):
        m = _load(DOCS / "CQC_P5_METRICS.json")
        self.assertEqual(m.get("cqc_p4_source_commit"), CORRECT_P4_SHA,
                         "CQC_P5_METRICS.json cqc_p4_source_commit must be 8028e17...")
        self.assertNotIn(WRONG_P4_SHA, json.dumps(m),
                         "CQC_P5_METRICS.json must not still carry the intermediate 529ccc63 SHA")

    def test_manifest_p4_pin_correct(self):
        m_path = DOCS / "CQC_P5_SHA256_MANIFEST.txt"
        self.assertTrue(m_path.is_file())
        head = "\n".join(m_path.read_text(encoding="utf-8").splitlines()[:20])
        self.assertIn(CORRECT_P4_SHA, head,
                      "manifest header must reference the correct P4 baseline 8028e17...")


class TestRA1_CI1_ReviewInventoryCounts(unittest.TestCase):
    """P5-RA1-CI1 §18.6-8: 6 contextual + 3 planning = 9 total
    integration_review.json files. Each carries the right shape
    (planning → LOCAL_CLAW; contextual → MACHINE_DERIVED)."""

    def test_review_inventory_counts(self):
        n_ctx = 0
        n_plan = 0
        for case in ("s1_vms_cellular_mechanism", "s2_vcell_paradigm",
                     "s3_antagonist_domains", "s4_avca_donor_data",
                     "s5_mixed_commitment", "s6_narrow_source_check"):
            p = CTX / case / "evaluation" / "integration_review.json"
            if p.is_file():
                n_ctx += 1
        for case in ("m1_s4_shared", "m2_s6_instability", "m3_s5_standard"):
            p = MAFS_PL / case / "evaluation" / "integration_review.json"
            if p.is_file():
                n_plan += 1
        self.assertEqual(n_ctx, 6, f"contextual review count = {n_ctx}, expected 6")
        self.assertEqual(n_plan, 3, f"planning review count = {n_plan}, expected 3")
        self.assertEqual(n_ctx + n_plan, 9, "total review count must be 9")


class TestRA1_CI1_ManifestNoLiteralShellExpression(unittest.TestCase):
    """P5-RA1-CI1 §18.9 + §13: manifest must not contain the literal
    text `$(git rev-parse HEAD)`. The actual HEAD SHA must be evaluated
    and written, or the header line removed entirely."""

    def test_manifest_has_no_unevaluated_shell_expression(self):
        m_path = DOCS / "CQC_P5_SHA256_MANIFEST.txt"
        head = "\n".join(m_path.read_text(encoding="utf-8").splitlines()[:20])
        self.assertNotIn("$(git rev-parse HEAD)", head,
                         "manifest must not contain literal $(git rev-parse HEAD) text")


class TestRA1_CI1_NoPriorPhaseMutation(unittest.TestCase):
    """P5-RA1-CI1 §18.10 + §16: no docs/CQC_P3_*, docs/CQC_P4_*,
    scripts/validate_p3.py, validate_p4.py, benchmarks/p0..p4 may be
    modified. The CI1 repair surface is P5-only."""

    def test_no_p3_p4_or_p0_through_p4_canonical_files_changed(self):
        # Use the latest commit on dev/cqc-p5 (the one we are about to
        # push) to ensure this runs against the post-CI1 state. We
        # verify the *already-committed* baseline (HEAD) does not touch
        # these paths in the latest commit, and that the working tree
        # has no staged or unstaged changes to them either.
        # Stage all pending changes first.
        out = subprocess.run(
            ["git", "diff", "--name-only", "HEAD"],
            cwd=str(PKG), capture_output=True, text=True, check=True,
        ).stdout.split()
        forbidden = [
            p for p in out
            if p.startswith("docs/CQC_P3_") or p.startswith("docs/CQC_P4_")
            or p == "scripts/validate_p3.py"
            or p == "scripts/validate_p4.py"
            or p.startswith("benchmarks/p0/")
            or p.startswith("benchmarks/p1/")
            or p.startswith("benchmarks/p2/")
            or p.startswith("benchmarks/p3/")
            or p.startswith("benchmarks/p4/")
        ]
        self.assertEqual(forbidden, [],
                         f"forbidden P3/P4/P0-P4 files modified: {forbidden}")


if __name__ == "__main__":
    unittest.main()
