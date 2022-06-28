#!/bin/bash

# rmf 3.12.2019, last modified 3.6.2021

# gets just the transcript symbols from transcript group file
# NR>1 skips the header, print $2 prints the second column containing symbols

for f in ELCs*.txt; do base=${f%%.txt}; outfile=$base'_transcriptList.txt'; cat $f | awk 'NR>1{print $0 | "cut -f2"}' > $outfile; done

for f in RLCs*.txt; do base=${f%%.txt}; outfile=$base'_transcriptList.txt'; cat $f | awk 'NR>1{print $0 | "cut -f2"}' > $outfile; done

for f in LLCs*.txt; do base=${f%%.txt}; outfile=$base'_transcriptList.txt'; cat $f | awk 'NR>1{print $0 | "cut -f2"}' > $outfile; done

for f in DAVID_processedFiles/*.txt; do base=${f%%IDs.txt}; outfile=$base'List.txt'; cat $f | awk 'NR>1{print $0 | "cut -f2"}' > $outfile; done

