#!/bin/bash

# rmf 2.13.2020, last modified 6.18.2021

for f in ../../../promoters/ELC*_transcriptList.txt; do echo $f >> fileList.transcriptLists.txt; done
for f in ../../../promoters/RLC*_transcriptList.txt; do echo $f >> fileList.transcriptLists.txt; done
for f in ../../../promoters/LLC*_transcriptList.txt; do echo $f >> fileList.transcriptLists.txt; done
for f in ../../../promoters/rhythmic*_transcriptList.txt; do echo $f >> fileList.transcriptLists.txt; done
for f in ../../../promoters/DAVID_processedFiles/*_transcriptList.txt; do echo $f >> fileList.transcriptLists.txt; done

for f in lightActivated*_transcriptList.txt; do echo $f >> fileList.lightActivated_transcriptLists.txt; done
