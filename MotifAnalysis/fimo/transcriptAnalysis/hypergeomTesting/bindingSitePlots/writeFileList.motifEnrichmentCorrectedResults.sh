#!/bin/bash

# rmf 12.4.2020
# cleaned up 3.1.2022

for f in ../significanceTestingResults/correctedPvals/*_BHFDRcorrected.txt; do echo $f >> fileList.motifEnrichmentCorrectedResults.txt; done

