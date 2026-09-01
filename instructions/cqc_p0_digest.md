# CQC-P0 Model Digestion Instruction

You are digesting a research narrative into a `CandidateQuestionSet` v0.1 artifact.

Rules of digestion:

1. **Preserve source intent.** Every question must remain traceable to the
   narrative. Each question carries `source_trace` entries whose
   `exact_quote` fields are verbatim substrings of the narrative.
2. **Decompose only where a distinct evidence landscape exists.** A question
   is the smallest unit for which a different body of evidence could
   materially change the research framing. Do not split lexical fragments;
   do not merge separate evidence landscapes.
3. **Preserve ambiguity.** If the narrative is ambiguous, keep the ambiguity
   visible in `uncertainty` (free text) or `null` when truly none. Do not
   "clean up" an ambiguous narrative into false certainty.
4. **Expose prerequisites.** Record `dependencies` (question_id list) only
   when they materially affect search order or interpretation.
5. **Provisional typing.** Use the master-contract vocabulary as guidance
   (ENTITY_RESOLUTION, SOURCE_CONTENT, TERMINOLOGY_OR_NAMING,
   HISTORICAL_LINEAGE, MECHANISM, CAUSAL_CLAIM, NOVELTY_OR_PRIOR_ART,
   MEASUREMENT_OR_OBSERVABILITY, INTERVENTION_OR_CONTROL, GENERALIZATION,
   TRANSLATION, TOOL_OR_METHOD). If none fits, use an honest new type and
   report it; do not coerce.
6. **Resolution conditions, not search plans.** State what evidence would
   materially resolve, falsify, narrow, or change the state of the question.

Forbidden during P0 digestion:

- open-ended research ideation (questions not entailed by the narrative;
  if you notice a valuable unentailed expansion, keep it OUT of the artifact
  and report it to the operator separately);
- answering the questions yourself;
- search planning, axis assignment, literature retrieval;
- converting uncertainty into assumptions.
