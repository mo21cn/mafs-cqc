"""Committed example artifacts must validate and render reproducibly."""
from __future__ import annotations

import sys
from pathlib import Path

PKG = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PKG / "scripts"))

from validate_cqs import infer_narrative_file, validate_artifact  # noqa: E402
from render_cqs import render  # noqa: E402

OUTPUTS = sorted((PKG / "examples" / "outputs").glob("*.json"))
INPUTS = PKG / "examples" / "inputs"
RENDERED = PKG / "examples" / "rendered"


def test_examples_exist():
    assert len(OUTPUTS) == 3, f"expected 3 committed example artifacts, found {len(OUTPUTS)}"


def test_all_examples_valid_with_input_crosscheck():
    for out in OUTPUTS:
        art = __import__("json").loads(out.read_text(encoding="utf-8"))
        nf = infer_narrative_file(out, INPUTS)
        res = validate_artifact(art, nf)
        assert res["ok"], f"{out.name}: {res['errors']}"
        assert res["narrative_file_match"], f"{out.name}: narrative file mismatch"


def test_all_examples_render_reproducibly():
    for out in OUTPUTS:
        committed = RENDERED / (out.stem + ".md")
        assert committed.is_file(), f"missing committed rendering for {out.name}"
        art = __import__("json").loads(out.read_text(encoding="utf-8"))
        assert render(art) == committed.read_text(encoding="utf-8"), \
            f"committed rendering for {out.name} is not reproducible from JSON"
