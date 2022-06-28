# rmf 12.4.2020, last modified 12.18.2020
# cleaned up 3.1.2022

# goal is to visualize binding sites of TFs from fimo analysis

# first get list of multiple test corrected results from hypergeom test
./writeFileList.motifEnrichmentCorrectedResults.sh

# parse this file, filtering by significance
./getBindingSiteInfo.sh

# visualize binding sites in groups of interest
# all genes in each group: to see if there are any obvious differences in intron length, gene IDs, etc. contributing to significant vs. no significant binding sites

./makeCmd_plotMotifBindingSites.sh
./cmd_plotMotifBindingSites.sh
