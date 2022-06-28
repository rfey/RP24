# rmf 4.14.2021

awk -F '\t' 'NR > 1 {print $1}' ../fimoSummaryFile_FPKM1.0_p5e-05.txt | sort | uniq | wc -l
