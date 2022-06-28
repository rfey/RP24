# rmf 9.24.2021, last modified 10.27.2021

import sys, re
import numpy as np
import matplotlib as mpl
mpl.use('Agg')
from matplotlib import pyplot as plot
from cycler import cycler

# USAGE
usage = 'python ' + sys.argv[0] + ' <fileList of cleaned up/down groups> <DEGs file> <escore thresh>'
if len(sys.argv) != 4:
    print(usage)
    exit()

# SUBROUTINES
def readFile(infile, escoreThresh, allTotals, allScores, allRP24s):
    groupInfo = {}
    n = 0
    with open(infile, 'r') as infile:
        for line in infile:
            n += 1
            if line.startswith('Cluster-'):
                # there is no average info yet to store for line one
                if n != 1 and score >= escoreThresh:
                    # calculate average RP24
                    # calculates for the previous cluster
                    avgRP24 = np.mean(RP24s)
                    allRP24s.append(avgRP24)
                    groupInfo[cluster].append(avgRP24)
                    groupInfo[cluster].append(transcriptIDs)

                # read line
                cluster, total, score, phaseStdDev, description, scoreAgain = line.strip().split('\t')

                # clean up terms
                total = float(total.split('=')[1])
                score = float(score.split('=')[1])
                description = re.sub('Annotation Cluster.*', '', description)
                description = description.replace('"', '')  # remove quotes
                description = description.split(',')[0]  # get first term

                if score >= escoreThresh:
                    # store terms
                    groupInfo[cluster] = [total, score, description]
                    transcriptIDs, RP24s = [],[]
                    allTotals.append(total)
                    allScores.append(score)

            # read in transcript-level info
            if line.startswith('FBtr') and score >= escoreThresh:
                transcriptID, symbol, RP24, qval, phase, link, fig = line.strip().split('\t')
                transcriptIDs.append(transcriptID)  # need these for computing avg LFC
                RP24s.append(float(RP24))

    # store average RP24 and transcriptIDs for last cluster in file
    if score >= escoreThresh:
        avgRP24 = np.mean(RP24s)
        allRP24s.append(avgRP24)
        groupInfo[cluster].append(avgRP24)
        groupInfo[cluster].append(transcriptIDs)
    
    infile.close()
    return groupInfo, allTotals, allScores, allRP24s

def computeAverageLFC(transcriptIDs, foldChanges):
    LFCs = []
    for transcript in transcriptIDs:
        if transcript in foldChanges:
            LFC = foldChanges[transcript]
            LFCs.append(LFC)
        else:
            print('ERROR: TranscriptID ' + transcript + ' not found in DEGs.txt')
            exit()
    return np.mean(LFCs)

def storeVals(groupList, info, normTotals, normScores):
    totals, scores, labels, RP24s, LFCs = info

    # if this is the first time we've seen this group
    if len(groupList) == 0:
        groupList = [normTotals, normScores, labels, RP24s, LFCs]
    else:
        groupList[0].extend(normTotals)
        groupList[1].extend(normScores)
        groupList[2].extend(labels)
        groupList[3].extend(RP24s)
        groupList[4].extend(LFCs)
    return groupList

# ARGUMENTS and MAIN
fileList = sys.argv[1]
DEGfile = sys.argv[2]
escoreThresh = float(sys.argv[3])

# read up down files
allData = {}
allTotals, allScores, allRP24s = [],[],[]
with open(fileList, 'r') as F:
    for line in F:
        infile = line.strip()
        group = infile.replace('_cleaned.txt', '')
        allData[group], allTotals, allScores, allRP24s = readFile(infile, escoreThresh, allTotals, allScores, allRP24s)
F.close()

# read DEG file
foldChanges = {}
with open(DEGfile, 'r') as f:
    next(f)  # skip header
    for line in f:
        info = line.strip().split('\t')
        transcriptID = info[0]
        LFC = info[9]
        foldChanges[transcriptID] = float(LFC)
f.close()

d = {}
for group in allData:
    totals, LFCs, RP24s, scores, labels = [],[],[],[],[]
    for cluster in allData[group]:
        total, score, description, avgRP24, transcriptIDs = allData[group][cluster]

        # get average LFC
        avgLFC = computeAverageLFC(transcriptIDs, foldChanges)

        # store everything to lists
        LFCs.append(avgLFC)
        totals.append(total)
        RP24s.append(avgRP24)
        scores.append(score)
        labels.append(description)

    # store it all in the dict
    d[group] = (totals, scores, labels, RP24s, LFCs)


# wrangle data for plotting
maxTotal = max(allTotals)
maxScore = max(allScores)

ELCs, RLCs, LLCs = [],[],[]
for group in d:
    totals, scores, labels, RP24s, LFCs = d[group]

    if 'ELC' in group:        
        ELCs = storeVals(ELCs, d[group], totals, scores)

    elif 'RLC' in group:
        RLCs = storeVals(RLCs, d[group], totals, scores)

    elif 'LLC' in group:
        LLCs = storeVals(LLCs, d[group],totals, scores)

totals, scores, labels, RP24s, LFCs = ELCs
ELCs = zip(totals, scores, labels, RP24s, LFCs)

totals,scores,labels, RP24s, LFCs = RLCs
RLCs = zip(totals, scores, labels, RP24s, LFCs)

totals,scores,labels, RP24s, LFCs = LLCs
LLCs = zip(totals, scores, labels, RP24s, LFCs)

# plot scatter
fig, axes = plot.subplots(nrows = 1, ncols = 3, sharey = True, constrained_layout = True)

xBoundMin = min(allRP24s) - 0.1
xBoundMax = max(allRP24s) + 0.1

# order: totals, scores, descriptions, RP24s, LFCs
for entry in ELCs:
    total, score, label, RP24, LFC = entry
    im0 = axes[0].scatter(RP24, LFC, c = score, s = total, cmap = 'cool', vmin = 0, vmax = maxScore)
    axes[0].set_xlim([xBoundMin, xBoundMax])
    if abs(LFC) >= 0.58 and total >= 5 and score >= 1.3:
        print 'ELC', label, LFC
        axes[0].annotate(label, (RP24, LFC))

for entry in RLCs:
    total, score, label, RP24, LFC = entry
    im1 = axes[1].scatter(RP24, LFC, c = score, s = total, cmap = 'cool', vmin = 0, vmax = maxScore)
    axes[1].set_xlim([xBoundMin, xBoundMax])
    if abs(LFC) >= 0.58 and total >= 5 and score >= 1.3:
        print 'RLC', label, LFC, total
        axes[1].annotate(label, (RP24, LFC))

for entry in LLCs:
    total, score, label, RP24, LFC = entry
    im2 = axes[2].scatter(RP24, LFC, c = score, s = total, cmap = 'cool', vmin = 0, vmax = maxScore)
    axes[2].set_xlim([xBoundMin, xBoundMax])
    if abs(LFC) >= 0.58 and total >= 5 and score >= 1.3:
        print 'LLC', label, LFC
        axes[2].annotate(label, (RP24, LFC))

fig.colorbar(im2, ax = axes[2])

# set y axis boundaries    
bound = max(abs(min(LFCs)), abs(max(LFCs))) # get largest magnitude for symmetrical bounds
yBoundMin = -bound - 0.1
yBoundMax = bound + 0.1
plot.ylim([yBoundMin, yBoundMax])

# y axis labels
axes[1].set_xlabel('Cluster Average RP24')
axes[0].set_ylabel('Cluster Average Log Fold Change')

plot.savefig('scatterUpDownGroups_escore' + str(escoreThresh) + '.pdf')
