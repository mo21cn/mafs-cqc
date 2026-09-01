# CQC-UPSTREAM-FREEZE — Structured Summary

> Contract: `CQC-UPSTREAM-FREEZE-v0.1` — `CQC-P5 CLOSED / ACCEPTED → CQC-UPSTREAM-FREEZE`
>
> This document is the freeze-acceptance artifact. It records the
> canonical P0→P5 upstream producer line as one frozen lineage.
> No scientific or semantic redesign is performed; the freeze step is
> type-stable, hash-stable, and history-preserving.

## A. Freeze Header

```yaml
contract_id: CQC-UPSTREAM-FREEZE-v0.1
status: READY_FOR_FREEZE_ACCEPTANCE
repository: mo21cn/mafs-cqc
source_branch: dev/cqc-p5
p5_accepted_head: 35ac05b269016a15c90564dca736b54129ce4d82
p4_accepted_baseline: 8028e17a6eaab364c744cfa72b714f0f0bd6cf01
mafs_compatibility_baseline: cd09699fc8cc160ab5cfff00a41e714961dd2109
```

## B. P0→P5 Lineage

| Phase | One-line summary | Frozen acceptance state |
|---|---|---|
| P0 | P0 — Human Summary (artifact contract + minimal validation surface) | READY_FOR_REVIEW |
| P1 | P1 — Structured Summary (real-task digestion replay; frozen bench/p1) | READY_FOR_REVIEW |
| P2 | P2 — Structured Summary (granularity & commitment boundary; frozen bench/p2) | READY_FOR_REVIEW |
| P3 | P3 — Canonical Summary (Final) (SearchRequirementProfile; frozen bench/p3) | CQC-P3-RA3-CLOSED |
| P4 | P4 — Canonical Summary (Final) (BudgetEnvelope; frozen bench/p4) | CQC-P4-RA2-CLOSED |
| P5 | P5 — Structured Summary (MAFS integration adapter; frozen bench/p5) | READY_FOR_REVIEW |

The frozen baseline at P4 is the final-gate commit
`CQC-P4-RA2-FINAL-GATE: coverage fixture uses Path object for PKG
monkeypatch + manifest entry rebound for tests/test_p4_ra2.py` (SHA
`8028e17a6eaab364c744cfa72b714f0f0bd6cf01`). P5 was accepted on top of
this baseline; no P3/P4 scientific semantics were changed during P5.

## C. Frozen Artifact Chain

```text
Research Narrative
    ↓
CandidateQuestionSet  (CQS)
    ↓
SearchRequirementProfile  (SRP)
    ↓
BudgetEnvelope
    ↓
CQCMAFSIntegrationBinding
```

This is the producer-facing artifact protocol. The contract
`CQC_P5_MAFS_INTEGRATION_ADAPTER_ARTIFACT_LINEAGE_CLOSURE_v0.1` freezes
this chain as the canonical P5 output.

## D. Authority Matrix

| Layer | Owner | Authority type |
|---|---|---|
| CQS | model / caller | admission authority (which scientific questions are admitted) |
| SRP | model / caller | evidence-obligation authority (which routes are required) |
| BudgetEnvelope | model / caller | resource authority (which routes are funded / held / unfunded) |
| CQCMAFSIntegrationBinding | machine (deterministic) | lineage / compatibility sidecar (NOT cognitive) |

CQC owns: artifact schemas, artifact generation semantics, source
lineage, hash continuity, revision / stale-state semantics,
producer-side compatibility tests.

MAFS does not own these semantics. MAFS owns: Axis, SearchOrder,
retrieval / provenance runtime, discover() → cognitive checkpoint →
resolve(), and (future) consumer-side integration.

No fourth CQC cognitive artifact was earned or added during P0→P5.

## E. M1/M2/M3 Semantic Acceptance

HO + ChatGPT final semantic adjudication (CQC-P5-RA1-CI1 §2):

```text
M1 — S4 Shared Requirement: PASS
M2 — S6 Productive Instability: PASS
M3 — S5 STANDARD: PASS
```

The distinction "structural traceability ≠ semantic containment" is
frozen as a CQC operating principle (see §6.5).

- Mechanical lineage (source-chain / route-join / conditional non-
  activation / MAFS baseline pin / MAFS-native schema validity / stale-
  state / search-order lineage traceability) was machine-derived and
  9/9 PASS.
- Local Claw authored the preliminary semantic review for M1/M2/M3 after
  reading the actual artifacts (source_cqs.json / source_srp.json /
  budget_envelope.json / integration_binding.json / mafs_planning.json)
  and recorded observed conclusions in the
  `local_claw_preliminary_review` block of each evaluation file.
- HO + ChatGPT performed the final semantic adjudication as PASS.
- All 3/3 planning reviews retain `final_semantic_adjudication.status =
  PENDING_HO_CHATGPT` (CI1 must never self-sign PASS); the
  PENDING_HO_CHATGPT marker is the standing final-state field
  regardless of HO+ChatGPT's actual decision in the freeze contract.

## F. Earned / Not Earned

**Earned:**
- 6/6 contextual source-chain bindings
- 3/3 MAFS-native planning packages (schema-validated against pinned
  MAFS schemas)
- 3/3 HO+ChatGPT semantic containment adjudications (M1/M2/M3)
- shared requirement preserved (M1 S4: R01 serves CQ-01+CQ-02)
- productive instability preserved (held CONDITIONAL routes; no pre-
  activation)
- S5 QUICK insufficiency blocks execution without deleting R02/
  historical_lineage
- stale-state detection works (stale fixture → STALE_SOURCE_CHAIN)
- source context remains reachable
- MAFS baseline pinned to `cd09699fc8cc160ab5cfff00a41e714961dd2109`
- MAFS production remains untouched
- no automatic CandidatePointer selection
- no automatic resolve()
- full MAFS preflight = NOT_EVALUATED (this is a consumer-side concern)
- 101 CQC tests pass (was 90 at P0; +11 from P5-RA1 + CI1)

**Not earned:**
- full MAFS `run_preflight()` execution (NOT_EVALUATED)
- scientific correctness judgments
- cost prediction accuracy
- EvidenceLandscapePackage
- any consumer-side adapter in MAFS (Path C freezes this as a separate
  contract: `MAFS-REPOSITORY-SIDE-CQC-INTEGRATION`)

The runtime authority boundary remains:

```text
planning
  → discover()
  → STOP
  → explicit cognitive selection
  → resolve()
```

## G. Governance Exception

One execution-governance exception is retained as an audit scar
(CQC-P5-RA1-CI1 §3):

```text
CI1 first push:
  b121a1acd39ee3f4a6280b9e3e6f24df563a7aee
  → CI FAILURE

Reason:
  manifest staging omission / stale generated manifest

Then:
  a force-amend / second push occurred without prior HO+ChatGPT
  authorization

Final evidence:
  35ac05b269016a15c90564dca736b54129ce4d82
  → independent CI SUCCESS

Disposition:
  GOVERNANCE_EXCEPTION_RECORDED
```

This does **not** invalidate P5 technical or semantic acceptance.
The freeze step records the event; it is not erased.

Standing rule (preserved for the next dev cycle):

> CI success cannot be predicted by an artifact committed before CI
> runs. The CI1 force-amend / second push is a
> recorded exception;
> establishes no authorization precedent;
> future second push requires HO+ChatGPT authorization.

## H. Repository Ownership / Path C

Path C is frozen (CQC-P5-RA1 Amendment A):

```text
CQC remains an independent sibling repository.
MAFS remains an independent repository.
```

Forbidden:

```text
vendor CQC into MAFS
make CQC a MAFS git submodule
copy CQC implementation into MAFS
merge CQC implementation ownership into MAFS
```

Permanent principle:

> **Merge the protocol, not the repositories.**

The integration unit is the artifact protocol, not repository
ownership.

## I. Post-Freeze Next Step

```text
CQC-UPSTREAM-FREEZE
  ↓ (frozen as of the final main commit)
separate bounded authorization
  ↓
MAFS-REPOSITORY-SIDE-CQC-INTEGRATION  (Path C)
  → thin MAFS-side consumer adapter
  → consumes CQS / SRP / BudgetEnvelope / CQCMAFSIntegrationBinding
  → produces MAFS-native Axis / SearchOrder
  → no copying / vendoring / absorbing CQC implementation
```

No tag, no GitHub Release, no package publication is authorized in
this freeze step. The next development action requires the separate
`MAFS-REPOSITORY-SIDE-CQC-INTEGRATION` contract under Path C.
