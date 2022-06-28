# rmf 5.11.2021

# get the input numbers for the venn diagram
sort -k11g motifEnrichmentSummary_LLCphases_addendum_eScoreNA_5FPKM_N10.txt | grep -v NO_TEST | head -n2 | awk 'NR > 1 {print $5, $6, $7}'

# then plot
# <group 1> <group 2> <intersect> <outbase>     ### note that the calculations are done in the script, enter full group for group 1 and 2
python ../../../scripts/plotLLCvenn.py 394 7156 223 LLCsPhase2to6_Xrp1
