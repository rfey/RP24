#!/bin/bash

# rmf 6.18.2021

for f in significanceTestingResults_OR/correctedPvals/*lightActivated*BHFDR*txt; do echo $f >> fileList.hypergeomCorrectedResults.lightActivated.txt; done
