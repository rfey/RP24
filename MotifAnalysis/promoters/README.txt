# rmf 3.12.2019, last modified 5.6.2021
# cleaned version 2.28.2022

# promoter analysis on ELCs, RLCs, LLCs
# NOTE: the original files in the RP24 directory don't have transcript symbols; the copies in this directory have symbols added

### find promoter window size to use for this analysis
# in findWindowSize/

### get promoter regions for all transcripts
# NOTE: this includes the region upstream of the TSS as well as the first intron

# write transcript promoter locations file
./writeTranscriptPromoterLocFile.sh

# get promoters from all transcripts in promoter location file
./getTranscriptPromoters.sh

### organize gene groups of interest

# get rhythmic gene group files (ELCs, RLCs, LLCs)-- these form the basis for all gene groups of interest
./makeSymLinks.sh

# subset core groups by phase range 0-12 or 12-24
./filterByPhase.sh

# subset all current groups by up- and down-regulated DEGs
./makeCmd_filterAgainstDEtranscripts.sh
chmod +x cmd_filterAgainstDEtranscripts.sh
./cmd_filterAgainstDEtranscripts.sh

# process DAVID output files 
# these are uploaded from local machine after running the DAVID webtool, into DAVID_outputFiles/
# last checked to make sure they are the latest version on: 9.20.2021
# processed files are in DAVID_processedFiles/

### get transcript symbol lists for all gene groups of interest
# these will be the input for hypergeometric testing after motif searching with FIMO

./getTranscriptSymbolList.sh  # get GOI symbols from rhythmicity group files
./getRhythmicByPhase.sh # get all rhythmic genes in each phase group
