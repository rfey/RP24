#!/bin/bash

# rmf 5.4.2021

for f in ../transcripts_*DAVID*txt; do b1=${f##../transcripts_significantSites_}; b2=${b1%%.txt}; python ../../../../../scripts/getNotSignificantTranscriptIDs.py $f ../${b2}_transcriptIDs.txt; done
