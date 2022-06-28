# rmf 3.15.2021, last modified 1.18.2022
# cleaned up 3.1.2022

# require GOI BG to be greater than global BG
# this max BG thresh (and above GOI BG thresh) will be applied at multiple test correction step

./parseMaxPhaseGroups.sh

./writeFileList.transcriptLists.sh
./writeFileList.maxPhaseGroups.sh

./runHypergeomTest.sh
mv resultsHypergeomTest*txt significanceTestingResults/.

./performMultipleTestCorrection.sh
mv significanceTestingResults/resultsHypergeomTest*BHFDRcorrected.txt significanceTestingResults/correctedPvals/.

./writeFileList.correctedPvals.sh
./writeSummaryFile_motifEnrichment.sh

./filterMotifSummary.sh
./plotRefinedHeatmaps.sh


#### follow-up analyses ####

# visualize binding sites of TFs in transcript promoter regions for each group, analyses in the following directories:
bindingSitePlots/

# compare transcripts with and without significant motif binding sites for each group, analyses in the following directories:
compareSiteSignificance/
