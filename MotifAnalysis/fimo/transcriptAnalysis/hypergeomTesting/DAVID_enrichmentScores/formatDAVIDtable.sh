# rmf 9.20.2021

# need to convert LLC to LLCs etc.

awk -F '\t' 'BEGIN {OFS="\t"}; $1 = $1"s" {print}' enrichmentScoresTableDAVID.txt > enrichmentScoresTableDAVID_formatted.txt
