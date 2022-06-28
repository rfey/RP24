#!/bin/bash

# rmf 3.25.2020, last modified 12.9.2020

grep MOTIF fly_factor_survey.meme | cut -d ' ' -f2,3 > memeMapFile.txt
grep MOTIF JASPAR2020_CORE_insects_non-redundant_pfms_meme.txt | cut -d ' ' -f2,3 >> memeMapFile.txt

grep ^MOTIF ../memeChip/ERR649814_cnc_memeChip/meme_out/meme_renamedMotifs.txt | cut -d ' ' -f3 | while read -r line; do echo $line $line >> memeMapFile.txt; done
grep ^MOTIF ../memeChip/ERR649813_cnc_memeChip/meme_out/meme_renamedMotifs.txt | cut -d ' ' -f3 | while read -r line; do echo $line $line >> memeMapFile.txt; done
# note that the cnc motifIDs don't have an associated symbol; this script double-writes the ID
