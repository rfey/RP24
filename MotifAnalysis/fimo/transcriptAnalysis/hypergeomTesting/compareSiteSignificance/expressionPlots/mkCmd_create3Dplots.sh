#!/bin/bash 
# rmf 5.4.2021

# ELCs not significant, then significant 
for f in transcripts_*ELC*.txt; do if test -f "$f"; then base=${f##*/}; outbase=${base%%.txt}; echo python ../../../../../scripts/plotExpressionProfilesGeneList_3D.py --exp1 ../transcriptExprYoung.txt --exp2 ../transcriptExprOld.txt --gl $f --ggy ../geneGroupFile_young.txt --ggo ../geneGroupFile_old.txt --o $outbase >> cmd_create3Dplots.sh; fi; done

for f in ../transcripts_*ELC*.txt; do if test -f "$f"; then base=${f##*/}; outbase=${base%%.txt}; echo python ../../../../../scripts/plotExpressionProfilesGeneList_3D.py --exp1 ../transcriptExprYoung.txt --exp2 ../transcriptExprOld.txt --gl $f --ggy ../geneGroupFile_young.txt --ggo ../geneGroupFile_old.txt --o $outbase >> cmd_create3Dplots.sh; fi; done

# RLCs, not significant, then significant
for f in transcripts_*RLC*.txt; do if test -f "$f"; then base=${f##*/}; outbase=${base%%.txt}; echo python ../../../../../scripts/plotExpressionProfilesGeneList_3D.py --exp1 ../transcriptExprYoung.txt --exp2 ../transcriptExprOld.txt --gl $f --ggy ../geneGroupFile_young.txt --ggo ../geneGroupFile_old.txt --o $outbase >> cmd_create3Dplots.sh; fi; done

for f in ../transcripts_*RLC*.txt; do if test -f "$f"; then base=${f##*/}; outbase=${base%%.txt}; echo python ../../../../../scripts/plotExpressionProfilesGeneList_3D.py --exp1 ../transcriptExprYoung.txt --exp2 ../transcriptExprOld.txt --gl $f --ggy ../geneGroupFile_young.txt --ggo ../geneGroupFile_old.txt --o $outbase >> cmd_create3Dplots.sh; fi; done

# LLCs, not significant, then significant 
for f in transcripts_*LLC*.txt; do if test -f "$f"; then base=${f##*/}; outbase=${base%%.txt}; echo python ../../../../../scripts/plotExpressionProfilesGeneList_3D.py --exp1 ../transcriptExprYoung.txt --exp2 ../transcriptExprOld.txt --gl $f --ggy ../geneGroupFile_young.txt --ggo ../geneGroupFile_old.txt --o $outbase >> cmd_create3Dplots.sh; fi; done

for f in ../transcripts_*LLC*.txt; do if test -f "$f"; then base=${f##*/}; outbase=${base%%.txt}; echo python ../../../../../scripts/plotExpressionProfilesGeneList_3D.py --exp1 ../transcriptExprYoung.txt --exp2 ../transcriptExprOld.txt --gl $f --ggy ../geneGroupFile_young.txt --ggo ../geneGroupFile_old.txt --o $outbase >> cmd_create3Dplots.sh; fi; done
