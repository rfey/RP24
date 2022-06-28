# rmf 3.2.2022


# NOTE: original workflow available in the MotifAnalysis directory

# Figure 7A heatmap and bar plot
./plotRefinedHeatmaps.sh

# Figure 7B box plot
./plotBoxplot.sh

# Figure 7D binding site locations image
./plotMotifBindingSites.sh

# NOTE that Figure 7C was downloaded from our expression plot visualization webtool, accessible at:
http://hendrixlab.cgrb.oregonstate.edu/cgi-bin/getTranscriptExpressionFigures.cgi

# tips:
1) some browsers automatically use https; you must change to http to get rid of "Not Found" error
2) you should be able to add "?geneName=" + the gene name at the end of the url as an alternative to using the dropdown menu
     ex: http://hendrixlab.cgrb.oregonstate.edu/cgi-bin/getTranscriptExpressionFigures.cgi?geneName=cwo
     this would give expression plots for all isoforms of the gene cwo (clockwork orange)
