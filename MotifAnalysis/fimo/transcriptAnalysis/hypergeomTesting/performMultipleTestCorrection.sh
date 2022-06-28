#!/bin/bash

# rmf 3.24.2020, last modified 6.18.2021
# cleaned up 3.1.2022

for f in significanceTestingResults/*.txt; do python ../../../scripts/performMultipleTestCorrection_BG.py $f ../../memeMapFile.txt ../geneMedianExpression.txt ../../secondaryIDsFile_fb_2020_05.txt ../../JASPARsecondaryIDsFile.txt; done

for f in significanceTestingResults/*lightActivated*txt; do python ../../../scripts/performMultipleTestCorrection_BG.py $f ../../memeMapFile.txt ../geneMedianExpression.txt ../../secondaryIDsFile_fb_2020_05.txt ../../JASPARsecondaryIDsFile.txt; done
