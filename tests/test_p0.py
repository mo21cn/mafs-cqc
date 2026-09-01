"""CQC-P0 unit tests: deterministic validation rules + renderer determinism."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

PKG = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PKG / "scripts"))

from validate_cqs import validate_artifact, sha256_text  # noqa: E402
from render_cqs import render  # noqa: E402

NARRATIVE = (
    "# Narrative\n\n"
    "Oxidative stress is linked to ovarian reserve decline. "
    "Hyperbaric oxygen therapy may shift the redox balance either way.\n"
)


def make_artifact(**overrides) -> dict:
    art = {
        "artifact_id": "CQS-TEST-1",
        "schema_version": "0.1",
        "source_narrative_sha256": sha256_text(NARRATIVE),
        "source_narrative": NARRATIVE,
        "questions": [
            {
                "question_id": "CQ-01",
                "statement": "Does hyperbaric oxygen shift ovarian redox balance toward protection or damage?",
                "source_trace": [
                    {"exact_quote": "Hyperbaric oxygen therapy may shift the redox balance either way."}
                ],
                "question_type": "MECHANISM",
                "dependencies": [],
                "resolution_condition": "A controlled study measuring ovarian redox markers under HBOT.",
                "uncertainty": None,
            }
        ],
    }
    for k, v in overrides.items():
        if k == "_question_overrides":
            art["questions"][0].update(v)
        else:
            art[k] = v
    return art


def run(art):
    return validate_artifact(art)


# ---- schema / envelope ------------------------------------------------------

def test_valid_minimal_passes():
    res = run(make_artifact())
    assert res["ok"], res["errors"]


def test_recomputed_hash_matches():
    art = make_artifact()
    assert art["source_narrative_sha256"] == hashlib.sha256(NARRATIVE.encode("utf-8")).hexdigest()


def test_hash_mismatch_fails():
    res = run(make_artifact(source_narrative_sha256="0" * 64))
    assert not res["source_hash_valid"] and not res["ok"]


def test_missing_required_field_fails():
    art = make_artifact()
    del art["artifact_id"]
    res = run(art)
    assert not res["schema_valid"]


def test_additional_property_rejected():
    art = make_artifact()
    art["extra_field"] = "not allowed"
    res = run(art)
    assert not res["schema_valid"]


def test_wrong_schema_version_rejected():
    res = run(make_artifact(schema_version="0.2"))
    assert not res["schema_valid"]


def test_empty_questions_fails():
    res = run(make_artifact(questions=[]))
    assert not res["schema_valid"]


# ---- questions ---------------------------------------------------------------

def test_duplicate_question_id_fails():
    art = make_artifact()
    q = dict(art["questions"][0])  # same question_id CQ-01 twice
    art["questions"].append(q)
    res = run(art)
    assert not res["question_id_unique"]


def test_exact_quote_must_be_verbatim():
    art = make_artifact(_question_overrides={
        "source_trace": [{"exact_quote": "this sentence does not exist in the narrative"}]})
    res = run(art)
    assert not res["exact_trace_valid"] and not res["ok"]


def test_question_type_is_free_string():
    art = make_artifact(_question_overrides={"question_type": "SOME_NEW_HONEST_TYPE"})
    res = run(art)
    assert res["ok"], res["errors"]


def test_uncertainty_null_and_text_both_valid():
    assert run(make_artifact())["ok"]
    art = make_artifact(_question_overrides={"uncertainty": "dose-dependence unresolved in narrative"})
    assert run(art)["ok"]


def test_empty_statement_fails():
    res = run(make_artifact(_question_overrides={"statement": ""}))
    assert not res["schema_valid"]


def test_empty_resolution_condition_fails():
    res = run(make_artifact(_question_overrides={"resolution_condition": ""}))
    assert not res["schema_valid"]


# ---- dependencies ------------------------------------------------------------

def test_unknown_dependency_target_fails():
    res = run(make_artifact(_question_overrides={"dependencies": ["CQ-99"]}))
    assert not res["dependency_dag_valid"]


def test_self_dependency_fails():
    res = run(make_artifact(_question_overrides={"dependencies": ["CQ-01"]}))
    assert not res["dependency_dag_valid"]


def test_cyclic_dependency_fails():
    art = make_artifact()
    art["questions"][0]["question_id"] = "CQ-01"
    art["questions"].append({
        "question_id": "CQ-02",
        "statement": "Second question.",
        "source_trace": [{"exact_quote": "Oxidative stress is linked to ovarian reserve decline."}],
        "question_type": "MECHANISM",
        "dependencies": ["CQ-01"],
        "resolution_condition": "Some evidence condition.",
        "uncertainty": None,
    })
    art["questions"][0]["dependencies"] = ["CQ-02"]
    res = run(art)
    assert not res["dependency_dag_valid"]


def test_valid_chain_passes():
    art = make_artifact()
    art["questions"].append({
        "question_id": "CQ-02",
        "statement": "Second question depending on CQ-01.",
        "source_trace": [{"exact_quote": "Oxidative stress is linked to ovarian reserve decline."}],
        "question_type": "CAUSAL_CLAIM",
        "dependencies": ["CQ-01"],
        "resolution_condition": "Some evidence condition.",
        "uncertainty": None,
    })
    res = run(art)
    assert res["dependency_dag_valid"] and res["ok"], res["errors"]


# ---- renderer ----------------------------------------------------------------

def test_renderer_deterministic():
    art = make_artifact()
    assert render(art) == render(art)


def test_renderer_contains_fields_verbatim():
    out = render(make_artifact())
    assert "CQ-01" in out
    assert "Does hyperbaric oxygen shift ovarian redox balance toward protection or damage?" in out
    assert '"Hyperbaric oxygen therapy may shift the redox balance either way."' in out
    assert "MECHANISM" in out
    assert "A controlled study measuring ovarian redox markers under HBOT." in out
    assert "(none)" in out  # empty dependencies + null uncertainty
