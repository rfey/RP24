#!/bin/bash

# rmf 1.31.2020, last modified 6.17.2020
# get gene expression files

for f in geneFPKMtable_*.txt; do echo $f >> fileList.geneExpr.txt; done
