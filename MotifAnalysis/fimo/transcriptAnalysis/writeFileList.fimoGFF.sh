#!/bin/bash

# rmf 12.4.2019, last modified 12.17.2020

# gets all fimo.gff files from fimo output
for f in allTranscriptsOutput6000/allTranscripts*.out/fimo.gff; do echo $f >> fileList.fimoGFFs.txt; done
