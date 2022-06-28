#!/bin/bash

# rmf 3.27.2018; last modified 4.2.2019

for f in ERR*fasta; do python ../scripts/runMemeChip.py $f '-meme-mod zoops'; done
