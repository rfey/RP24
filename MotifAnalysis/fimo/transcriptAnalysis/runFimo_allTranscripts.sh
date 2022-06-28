# rmf 12.2.2019, last modified 4.6.2020
# cleaned up 2.28.2022

# USAGE: python runFimo_userMotifs.py <MEME motif file> <list of MEME motif IDs to run> <sequence file> <outbase> <options>

# fly factor survey
python ../../scripts/runFimo_userMotifs.py ../fly_factor_survey.meme ../motifList_fly_factor_survey.txt ../../promoters/allTranscriptPromoters6000bpAndFirstIntron.fasta allTranscripts6000 '--no-qvalue --thresh 1e-4'

# JASPAR
python ../../scripts/runFimo_userMotifs.py ../JASPAR2020_CORE_insects_non-redundant_pfms_meme.txt ../motifList_JASPAR2020.txt ../../promoters/allTranscriptPromoters6000bpAndFirstIntron.fasta allTranscripts6000 '--no-qvalue --thresh 1e-4'

# cnc
python ../../scripts/runFimo_userMotifs.py ../../memeChip/ERR649813_cnc_memeChip/meme_out/meme.txt ../motifList_cnc.txt ../../promoters/allTranscriptPromoters6000bpAndFirstIntron.fasta allTranscripts6000_cncERR649813 '--no-qvalue --thresh 1e-4'

python ../../scripts/runFimo_userMotifs.py ../../memeChip/ERR649814_cnc_memeChip/meme_out/meme.txt ../motifList_cnc.txt ../../promoters/allTranscriptPromoters6000bpAndFirstIntron.fasta allTranscripts6000_cncERR649814 '--no-qvalue --thresh 1e-4'
