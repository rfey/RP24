#!/bin/bash

# rmf 4.22.2020, last modified 6.18.2021
# cleaned up 3.1.2022

# USAGE: python ../../../scripts/runHypergeomTest1.py <fimo results summary file> <GOI list> <all transcripts file> <median expression file> <max background threshold> <FPKM threshold> <threshold for number of genes in GOI group>

# recommend running with SGE_Batch or similar

python ../../../scripts/runHypergeomTest.py ../fimoSummaryFile_FPKM1.0_p5e-05.txt ../fimoGlobalMotifCounts_FPKM1.txt fileList.transcriptLists.txt ../allTranscriptList.txt ../transcriptMedianExpression.txt 0.5 1 5

python ../../../scripts/runHypergeomTest.py ../fimoSummaryFile_FPKM1.0_p5e-05.txt ../fimoGlobalMotifCounts_FPKM1.txt fileList.maxPhaseGroups.txt ../allTranscriptList.txt ../transcriptMedianExpression.txt 0.5 1 5

python ../../../scripts/runHypergeomTest.py ../fimoSummaryFile_FPKM1.0_p5e-05.txt ../fimoGlobalMotifCounts_FPKM1.txt fileList.lightActivated_transcriptLists.txt ../allTranscriptList.txt ../transcriptMedianExpression.txt 0.5 1 5
