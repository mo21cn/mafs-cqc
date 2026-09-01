# Narrative A — GF / EM identity-lineage task (real replay domain: mafs-v3-p0 Replay B)

## Task origin

This narrative comes from a real operator task in the MAFS v3.0 Replay B benchmark line. The verbatim operator request is:

请调整 MAFS 搜索：von Reyn et al. 2014/2020 等论文补充材料里的 GF 神经元 ID 清单。

## Background facts established by prior verified work

The Drosophila Giant Fiber (GF) escape circuit has been studied for decades with electrophysiology, and more recently with connectomics datasets.

The 2014 paper by the von Reyn team is "A spike-timing mechanism for action selection", published in Nature Neuroscience (volume 17, pages 962-970, DOI 10.1038/nn.3741, PMID 24908103).

The standardized descending-neuron nomenclature comes from Namiki et al. 2018 in eLife ("The functional organization of descending sensory-motor pathways in Drosophila", DOI 10.7554/eLife.34272), which labels the Giant Fiber as DNp01.

The FlyWire v783 and hemibrain v1.2.1 datasets identify GF candidate bodies by numeric root IDs, but the specific root IDs supplied by the operator for the right and left GF have not been independently confirmed against dataset annotations.

## Known ambiguities in the request

Whether "von Reyn 2020" refers to a real Giant Fiber paper is doubtful: the major 2020 Drosophila connectome work is Scheffer et al. 2020 ("A connectome and analysis of the adult Drosophila central brain", eLife), from a largely overlapping Janelia collaboration, which may be what the operator conflated.

The historical label "DNg01" appears in some pre-2018 literature; no authoritative primary source has confirmed that DNg01 is a synonym of DNp01, so the two must not be silently treated as the same neuron class.

It is also unverified whether the supplementary materials of von Reyn 2014 actually contain a GF neuron ID list at all.

## Goal

Prepare an executable question set for downstream MAFS retrieval: confirm source identity and content, confirm the naming lineage, and clarify whether the 2020 citation is a conflation.
