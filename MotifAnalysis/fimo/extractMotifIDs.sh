#!/bin/bash

# rmf 3.12.2019, last modified 4.3.2020
# cleaned up 2.28.2022

# gets all the motif IDs from a meme file into one file
# resulting file is used as input for running FIMO on all motifs in a database meme file in parallel

grep MOTIF fly_factor_survey.meme | cut -d ' ' -f2 > motifList_fly_factor_survey.txt
grep MOTIF JASPAR2020_CORE_insects_non-redundant_pfms_meme.txt | cut -d ' ' -f2 > motifList_JASPAR2020.txt
grep ^MOTIF ../memeChip/ERR649813_cnc_memeChip/meme_out/meme_renamedMotifs.txt | cut -d ' ' -f3 > motifList_cnc.txt
grep ^MOTIF ../memeChip/ERR649814_cnc_memeChip/meme_out/meme_renamedMotifs.txt | cut -d ' ' -f3 >> motifList_cnc.txt
cat motifList_fly_factor_survey.txt motifList_JASPAR2020.txt motifList_cnc.txt > motifList_all.txt
