#!/bin/bash

# rmf 9.20.2021
# cleaned up 3.1.2022

for f in DAVID*parse.txt; do outbase=${f%%.txt}; perl ../../../../scripts/mac2unix.pl $f > $outbase.cleaned.txt; done
