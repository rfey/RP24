#!/bin/bash

# rmf 4.13.2021

for f in transcripts_significantSites_DAVID_*.txt; do f1=${f##*Sites_}; f2=${f1%%.txt}; file=../../../../promoters/DAVID_processedFiles/${f2}_transcriptIDs.txt; ln -s $file ${f2}_transcriptIDs.txt; done
