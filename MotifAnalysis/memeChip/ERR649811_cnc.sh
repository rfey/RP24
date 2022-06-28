#!/bin/bash
#$ -cwd               # Current working directory
#$ -S /bin/bash       # Shell
#$ -N ERR649811_cnc      # Job name
#$ -j y               # Merge stderr with stdout
#$ -o ERR649811_cnc.err      # Stdout name
#$ -q nucleotide      # Queue name
#$ -l mem_free=10G    # Limit memory request
#$ -V                 # Preserve environmental variables
meme-chip ERR649811_cnc.fasta -oc ERR649811_cnc_memeChip -meme-mod zoops