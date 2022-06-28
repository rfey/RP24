# rmf 4.2.2019, last modified 4.3.2020

# goal: get meme files for TFs not in database meme file
# TFs analyzed: cnc

# step 1: get files ready to run meme

./getFiles.sh # download fastq files from ChIP-seq: Nitta et al, DOI: 10.7554/eLife.04837.001
./fastq2fasta.sh # convert to fasta
./runMemeChip.sh

# RESULTS:
less ERR649811_cnc_memeChip/meme_out/meme.txt: TGGGCACAGCGCCC, E-val=2.2e+005
less ERR649812_cnc_memeChip/meme_out/meme.txt: CACAATGACAC, E-val=6.4e+001
less ERR649813_cnc_memeChip/meme_out/meme.txt: TCATCATGACA, E-val=3.0e-188
less ERR649814_cnc_memeChip/meme_out/meme.txt: CGTCATGATGA, E-val=1.3e-1213

# NOTE: all 3 motifs in ERR649813 and ERR649814 are significant

# step 2: rename motifs in meme files with significant hits
# goal: get unique motif names for fimo and downstream analysis

./renameMotifs.sh
