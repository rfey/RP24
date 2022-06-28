#!/bin/bash

# rmf 4.1.2020, last modified 5.17.2021
# cleaned up 3.1.2022
 
ls significanceTestingResults/correctedPvals/*LCs_q0.05_phase*BHFDR* | grep -v InOld >> fileList.hypergeomCorrectedResults.phases.txt
ls significanceTestingResults/correctedPvals/*LCs_q0.05_*InOld_maxBG0.5_BHFDR* | grep -v phase >> fileList.hypergeomCorrectedResults.upAndDown.txt

for f in significanceTestingResults/correctedPvals/*LCs_q0.05_phase*InOld*BHFDR*; do echo $f >> fileList.hypergeomCorrectedResults.phasesUpAndDown.txt; done
for f in significanceTestingResults/correctedPvals/*LCs_q0.05_maxBG0.5_BHFDRcorrected.txt; do echo $f >> fileList.hypergeomCorrectedResults.coreGroups.txt; done
for f in significanceTestingResults/correctedPvals/*DAVID*BHFDR*txt; do echo $f >> fileList.hypergeomCorrectedResults.DAVIDgroups.txt; done

for f in significanceTestingResults/correctedPvals/*LCs*Phase*to*BHFDR*txt; do echo $f >> fileList.hypergeomCorrectedResults.maxPhaseGroups.txt; done
