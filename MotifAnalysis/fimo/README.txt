# rmf 3.12.2019; last modified 12.4.2020
# cleaned up 2.28.2022

# write files with lists of motif IDs from meme files
./extractMotifIDs.sh

# write map ID files
./writeMapFile.sh

# write secondary IDs file
./downloadFBIDtoAnnotation.sh
./writeSecondaryIDsFile.sh

# run fimo: motif analysis on transcripts in: transcriptAnalysis/

