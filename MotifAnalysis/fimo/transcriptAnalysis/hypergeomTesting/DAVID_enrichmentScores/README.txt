# rmf 12.21.2020, last modified 9.20.2021
# cleaned up 3.1.2022

# get table of enrichment scores for each cluster to enable filtering for heatmap

# upload parsed DAVID files from local machine
# they have form: DAVID_LLC_transcript_q0.05.parse.txt
# accessed 9.20.2021

# get file list of parsed DAVID files
./convertNewlines.sh
./writeFileList.parsedDAVID.sh

# write table of clusters and enrichment scores
./getEnrichmentScoreTable.sh
./formatDAVIDtable.sh
