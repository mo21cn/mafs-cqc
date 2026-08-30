# Narrative B — Virtual Cell novelty-framing task

## Research intent (operator voice)

We want to build a foundation model that predicts how cell states respond to genetic and chemical perturbations, learned from large perturbation maps, and we want to frame it as a step toward a "virtual cell". Before committing the framing, we need to know whether this combination is already claimed by existing work.

## What we believe the landscape looks like

Several teams have pretrained transformer-style foundation models on large-scale single-cell transcriptomics data — for example scGPT, Geneformer, scBERT and scVI-lineage models — mostly targeting cell-type annotation, batch integration, and gene-network inference.

More recent work and several well-funded programs explicitly use the phrase "virtual cell" for models that simulate cellular behavior under perturbation. The boundary between "representation model", "perturbation-response predictor", and "causal mechanism model" is blurred in public claims, and each team emphasizes a different one.

## Where we think our differentiation lies

Our differentiation is systematic generalization across perturbation combinations: most published evaluations report single-gene knockouts or single-drug responses, while we want double- and triple-perturbation settings with held-out combination classes.

## What is unclear to us

We do not know the actual coverage of existing perturbation-prediction models over combination settings, we do not know whether a community benchmark for combination generalization already exists, and we do not know which specific "virtual cell" claims have already been publicly staked by which teams.

Our novelty framing may drift as the literature moves quickly, so the uncertainty must stay visible rather than being resolved by assumption.
