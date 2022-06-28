# rmf 12.2.2019, last modified 9.21.2021
# cleaned up 2.28.2022

### run fimo on all motifs in database meme files, and meme files from ../../memeChip/

# NOTE: this is run on promoters 6000 bp upstream of TSS, including the first intron of the transcript -- this means that the start-stop positions in the fimo output files refer not to genomic coordinates, but to the position relative to the input sequence, which is 6000 + however long the first intron is!

./runFimo_allTranscripts.sh # run fimo on all transcripts in genome (fly factor survey and cnc MEME files)

# clean up directory
mv allTranscripts6000*.out allTranscriptsOutput6000/.
mv *6000*out.err allTranscriptsOutput6000/backup/.
mv *6000*out.sh allTranscriptsOutput6000/backup/.

### rename files and motifs in cnc fimo files
# goal: get unique motif names for motifs in these files

./renameFimoFiles.sh
./renameMotif.sh

### motif enrichment analysis: perform hypergeometric test to get statistical significance of GOI group vs all transcripts
# NOTE: result is all GOIs tested and their pvals, not only the significant ones

./writeFileList.transcriptExpr.sh  # used for GOIs
./writeFileList.geneExpr.sh  # used for TFs
./writeMedianExprFile.sh

./writeAllTranscriptsList.sh
./writeFileList.transcriptLists.sh  # GOI lists

./writeFimoSummaryFile.sh
./filterFimoResultsFile.sh   # filter on fimo pval AND on transcript expression (median FPKM > 1)
./getGlobalMotifCounts.sh

### hypergeometric testing and subsequent analyses in hypergeomTesting/
