#!/bin/bash

# rmf 1.31.2020, 2.11.2020
# get transcript expression files

for f in transcriptFPKMtable_*.txt; do echo $f >> fileList.transcriptExpr.txt; done
