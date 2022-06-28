# rmf 5.4.2021
# cleaned up 3.2.2022

# goal: visualize expression differences between groups of transcripts with and without significant motif binding sites

# get files with transcriptIDs without significant binding sites
./writeNotSignificantLists.sh

# plot 3D expression profiles for groups of transcripts
./mkCmd_create3Dplots.sh
./cmd_create3Dplots.sh
