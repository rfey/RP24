# rmf 1.12.2021, last modified 9.20.2021

# filter clusters on DAVID enrichment score and TFs on expression
# usage: python scripts/filterMotifSummaryFile.py <motif summary file> <expression file> <secondary FBID file> <JASPAR secondary ID file> <FPKM threshold> <N number of transcripts in group> [enrichment score table] [enrichment score threshold]

python ../../../scripts/filterMotifSummaryFile.py motifEnrichmentSummary_coreGroups.txt ../geneMedianExpression.txt ../../secondaryIDsFile_fb_2020_05.txt ../../JASPARsecondaryIDsFile.txt 5 10

python ../../../scripts/filterMotifSummaryFile.py motifEnrichmentSummary_phases.txt ../geneMedianExpression.txt ../../secondaryIDsFile_fb_2020_05.txt ../../JASPARsecondaryIDsFile.txt 5 10

python ../../../scripts/filterMotifSummaryFile.py motifEnrichmentSummary_upAndDown.txt ../geneMedianExpression.txt ../../secondaryIDsFile_fb_2020_05.txt ../../JASPARsecondaryIDsFile.txt 5 10

python ../../../scripts/filterMotifSummaryFile.py motifEnrichmentSummary_phasesUpAndDown.txt ../geneMedianExpression.txt ../../secondaryIDsFile_fb_2020_05.txt ../../JASPARsecondaryIDsFile.txt 5 10

python ../../../scripts/filterMotifSummaryFile.py motifEnrichmentSummary_maxPhaseGroups.txt ../geneMedianExpression.txt ../../secondaryIDsFile_fb_2020_05.txt ../../JASPARsecondaryIDsFile.txt 5 10

python ../../../scripts/filterMotifSummaryFile.py motifEnrichmentSummary_DAVIDgroups.txt ../geneMedianExpression.txt ../../secondaryIDsFile_fb_2020_05.txt ../../JASPARsecondaryIDsFile.txt 5 10 DAVID_enrichmentScores/enrichmentScoresTableDAVID_formatted.txt 1.3010299956639813

python ../../../scripts/filterMotifSummaryFile.py motifEnrichmentSummary_lightActivated.txt ../geneMedianExpression.txt ../../secondaryIDsFile_fb_2020_05.txt ../../JASPARsecondaryIDsFile.txt 5 10
