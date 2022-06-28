# rmf 5.4.2020, last modified 5.19.2020

# filter on pvalue and FPKM
SGE_Batch -c 'python ../../scripts/filterFimoSummaryFile1.py fimoResultsSummary.txt transcriptMedianExpression.txt 0.00005 1' -r filterFimoResultsSummary -q nucleotide
