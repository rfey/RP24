# rmf 9.2.2020, last modified 4.21.2021
# cleaned up 3.1.2022

# goal: visualize differences between groups of transcripts with and without significant motif binding sites

# get transcriptID lists
./getTranscriptIDs.sh
./createIDlistSymLinks.sh

# run T test to compare differences in expression and rhythmicity measures
./performTtest_RP24.sh
./performTtest_meanExpression.sh
./performTtest_medianExpression.sh
./performTtest_allExpressionVals.sh
./performTtest_F24.sh

# plot box plot to visualize T test results
./plotBoxplot.sh

# get list of LLCs phase 2-6 with significant Xrp1 sites
./parseSigSitesFile_transcriptIDs.sh
