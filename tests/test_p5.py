"""P5 minimal invariant tests (contract sections 39, 44)."""
from __future__ import annotations

import hashlib
import json
import shutil
import sys
import unittest
from pathlib import Path

PKG = Path(__file__).resolve().parents[1]
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
MAFS_SCHEMAS = PKG.parent / "mafs-v3-p0" / "schemas"


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


if __name__ == "__main__":
    unittest.main()
