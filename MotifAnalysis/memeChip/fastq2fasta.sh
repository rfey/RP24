#!/bin/bash

# rmf 4.6.2018; last modified 4.2.2019

for f in ERR*.fastq; do base=${f%.*}; fastq2fasta.pl -i $f -o ${base##*/}.fasta; done
