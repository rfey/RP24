#!/bin/bash

# rmf 12.8.2020, last modified 4.15.2021

# usage <binding site file> <GOI list file> <promoter loc file> <xscale> <yscale> <secondaryIDs file>
for f in bindingSiteInfo*DAVID*.txt; do filebase=$(echo $f | sed 's/_FDR.*txt//' | sed 's/_p[0-9].*txt//'); outbase=${filebase##bindingSiteInfo_}; GOIfile="../../../../promoters/DAVID_processedFiles/${outbase}_transcriptList.txt"; echo python ../../../../scripts/plotMotifBindingSites_svg.py $f $GOIfile ../../../../promoters/transcriptPromoterAndFirstIntronLocs6000bp.txt 1 4 >> cmd_plotMotifBindingSites.sh; done
