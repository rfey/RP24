#!/bin/bash

# rmf 12.17.2020, last modified 6.18.2021
# cleaned up 3.1.2022

# usage: plotHorizontalHeatmapAndBarplot.py <summary file> <p-value threshold> <asterisk threshold> <FDR annotation (True or False)>
# horizontal heatmap
for f in motifEnrichmentSummary_*FPKM*.txt; do python ../../../scripts/plotHorizontalHeatmapAndBarplot.py $f 0.01 0.05 True; done

for f in motifEnrichmentSummary_lightActivated_eScoreNA_5FPKM_N10.txt; do python ../../../scripts/plotHorizontalHeatmapAndBarplot.py $f 0.01 0.05 True; done

# plot only significant results
# THIS SCRIPT USED FOR FIGURE 7a
python ../../../scripts/plotHorizontalHeatmapAndBarplot_sigOnly.py motifEnrichmentSummary_DAVIDgroups_eScore1.3_5FPKM_N10.txt 0.05
