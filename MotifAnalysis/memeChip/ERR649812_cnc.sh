#!/bin/bash
#$ -cwd               # Current working directory
#$ -S /bin/bash       # Shell
#$ -N ERR649812_cnc      # Job name
#$ -j y               # Merge stderr with stdout
#$ -o ERR649812_cnc.err      # Stdout name
#$ -q nucleotide      # Queue name
#$ -l mem_free=10G    # Limit memory request
#$ -V                 # Preserve environmental variables
meme-chip ERR649812_cnc.fasta -oc ERR649812_cnc_memeChip -meme-mod zoops