#!/bin/bash

# rmf 7.2.2020, last modified 4.7.2020

# usage: <results file list> <median expression file> <p-value threshold> <fimoSummaryFile_FPKM1.0_p5e-05.txt> <FDR (True/False)> <TF expr thresh (FPKM)>

python ../../../../scripts/getSignificantBindingSites.py fileList.motifEnrichmentCorrectedResults.txt ../../geneMedianExpression.txt 0.05 ../../fimoSummaryFile_FPKM1.0_p5e-05.txt True 5
