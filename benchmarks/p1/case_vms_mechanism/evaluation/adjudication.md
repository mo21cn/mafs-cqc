# Adjudication — case_vms_mechanism (preliminary, pending HO + ChatGPT)

**Machine facts** (validate_p1): Arm B CQS 3 questions, 0 edges, schema/hash/trace/DAG/render all PASS. Arm A: 5 prepared lines.

**Coverage**: Both arms recovered the full expected critical set (core mechanism at cell resolution; population ambiguity; observability). Arm A added a translation cross-check line (QA-05) — adjudicated as search-strategy enrichment, not a distinct critical question, so not a B-miss.

**Key contrast**: The two ambiguities (population scope; omics-vs-imaging) exist in BOTH arms' outputs. In Arm A they are inline notes in a free-form document; in Arm B they are durable, per-question uncertainty fields bound to verbatim source traces. Downstream, if the operator later answers the ambiguity, Arm B's artifact can be minimally amended (which question's scope changes) while Arm A's preparation must be re-read end-to-end.

**Dependency truth**: Arm B's 0-edge graph survives the RA2 test (each question independently searchable) — sparse and honest.

**Preliminary verdict**: Arm B = structural parity on coverage + durable traceability/repairability advantage. No Arm C trigger.
