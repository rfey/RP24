#!/bin/python

# rmf 5.17.2019, last modified 5.4.2021
# cleaned up 3.2.2022

import sys, os, re
import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# USAGE
usage = "python " + sys.argv[0] + " <T-test results file> <p-value threshold> <ylabel> <outbase>"
if len(sys.argv) != 5:
    print usage
    sys.exit()

# SUBROUTINES
def readTranscriptFile(f):
    transcripts = []
    with open(f,'r') as f:
        for line in f:
            FBID, symbol = line.strip().split('\t')
            transcripts.append(FBID)
    f.close()
    return transcripts

def getRP24s(transcripts,allRP24s):
    RP24s = []
    for transcript in transcripts:
        if transcript in allRP24s:
            RP24s.append(allRP24s[transcript])
        else:
            print("WARNING: Unable to retrieve RP24 for transcript " + transcript)
            sys.exit()
    return RP24s

def plotScatterPoints(y1,y2,subplot1,subplot2):
    x1 = np.random.normal(subplot1, 0.02, len(y1))
    plt.plot(x1, y1, 'k',linestyle='None',marker='.')
    x2 = np.random.normal(subplot2, 0.02, len(y2))
    plt.plot(x2, y2, 'k',linestyle='None',marker='.')

# ARGUMENTS and MAIN
resultsFile = sys.argv[1]
pvalThresh = float(sys.argv[2])
ylabel = sys.argv[3]  # RP24, expr, FPKM, etc
outbase1 = sys.argv[4]

# get outbase from results file
outbase2 = resultsFile.split('Ttest_')[1].replace('.txt','')
print outbase2

# read results file
if 'Cluster' in resultsFile:
    pattern = re.compile('.*(Cluster.*)\.txt')
    # get cluster from file name-- should be the same for both files
    clusterName = pattern.search(resultsFile).group(1)
else:
    clusterName = outbase2.replace('results_', '')
print clusterName

sigList, notsigList = [],[]
with open(resultsFile,'r') as resultsFile:
    header = next(resultsFile).strip().split('\t') # motif info and pval are in here
    headerInfo = []  # will hold motifID, motifSymbol, pval
    for info in header:
        info = info.split(':')[1]
        headerInfo.append(info)
    if headerInfo[2] == 'NO_TEST':
        resultsFile.close()
        exit()
    if float(headerInfo[2]) > pvalThresh:
        resultsFile.close()
        exit()

    print 'Plotting for motif', headerInfo[1], 'with pval = ', headerInfo[2]
    next(resultsFile)  # this is a normal header, can skip this one
    for line in resultsFile:
        transcriptID, transcriptSymbol, vals, sig = line.strip().split('\t')  # sig = yes or no
        valsList = vals.split(',')
        valsFloat = [float(val) for val in valsList]
        if sig == 'yes':
            sigList.extend(valsFloat)
        elif sig == 'no':
            notsigList.extend(valsFloat)
resultsFile.close()


outfile = 'boxplot_' + outbase1 + '_' + outbase2 + '.pdf'

# wrangle data
data = [sigList, notsigList]

# create a figure instance
plt.figure()
ax = plt.gca()
ax.xaxis.set_major_formatter(ticker.ScalarFormatter(useOffset = False))
plt.yscale('symlog')

# create the boxplot
bp = plt.boxplot(data, patch_artist=True, showfliers=False, widths=.6)
plt.ylabel(ylabel, size = 14)
plt.tick_params(labelsize = 14) # sets both y axis and x axis label fontsize

# arrange plot title
clusterNameCleaned = clusterName.replace('_', ' ')
title = '\"' + clusterNameCleaned + '\" transcripts\nwith motif instance for ' + headerInfo[1] + '\np-value = ' + str(round(float(headerInfo[2]), 3))
plt.title(title, size = 16)

# set new x tick locs and labels
plt.xticks([], [])

# fill with colors
colors = ['lime','orange'] * len(data)
for patch, color in zip(bp['boxes'], colors):
    patch.set_facecolor(color)
    patch.set_edgecolor('black')
    patch.set_alpha(0.5)
for median in bp['medians']:
    median.set(color='k')

# plot legend
ax.legend([bp["boxes"][0], bp["boxes"][1]], ['has motif instance','no motif instance'])


# plot scatter points
indices = list(range(0,len(data),2))
for i in indices:
    y1 = data[i]
    y2 = data[i+1]
    subplot1 = i+1
    subplot2 = i+2
    plotScatterPoints(y1,y2,subplot1,subplot2)

# save plot
plt.savefig(outfile, bbox_inches='tight')
