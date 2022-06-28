#!/local/cluster/bin/python

# last modified rmf 4.21.2021
# cleaned up 3.2.2022

import sys,math,argparse
import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
from mpl_toolkits.mplot3d import Axes3D

###########
## INPUT ##
###########

def readGeneIDListFile(geneIDListFile):
    IDs = []
    transcripts = {}
    with open(geneIDListFile) as F:
        next(F)  # skip header
        for line in F:
            transcriptID, transcriptSymbol, motifID, motifSymbol = line.strip().split('\t')
            IDs.append(transcriptID)
            if (motifID, motifSymbol) not in transcripts:
                transcripts[(motifID, motifSymbol)] = []
            transcripts[(motifID, motifSymbol)].append((transcriptID, transcriptSymbol))
    return(IDs, transcripts)

def readExpressionFile(expressionFile,geneIDs):
    expData = {}
    for line in open(expressionFile, 'r'):
        geneID,ZT0_R1,ZT4_R1,ZT8_R1,ZT12_R1,ZT16_R1,ZT20_R1,ZT0_R2,ZT4_R2,ZT8_R2,ZT12_R2,ZT16_R2,ZT20_R2 = line.strip().split('\t')
        if geneID in geneIDs:
            expData[geneID] = [float(ZT0_R1),float(ZT4_R1),float(ZT8_R1),float(ZT12_R1),float(ZT16_R1),float(ZT20_R1),float(ZT0_R2),float(ZT4_R2),float(ZT8_R2),float(ZT12_R2),float(ZT16_R2),float(ZT20_R2)]
    return expData

def readGeneGroupsFile(geneGroupsFile,geneIDs):
    phases = {}
    for line in open(geneGroupsFile, 'r'):
        geneID,symbol,qValue,pValue,RP24,SP,PVEC,phase,median,detectable,nonZero = line.strip().split('\t')
        if geneID in geneIDs:
            phases[geneID] = float(phase)
    return phases

def getArgs():
    parser = argparse.ArgumentParser(description="plot expression profile for several genes", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--exp1",type=str,required=True,help="expression file 1")
    parser.add_argument("--exp2",type=str,required=True,help="expression file 2")
    parser.add_argument("--gl",type=str,required=True,help="gene ID list file")
    parser.add_argument("--ggy",type=str,required=True,help="young gene groups file")
    parser.add_argument("--ggo",type=str,required=True,help="old gene groups file")
    parser.add_argument("--o",type=str,required=True,help="output base")

    args = parser.parse_args()
    return args

##################
## SUBROUNTINES ##
##################

def maxMinNormalize(expression,refExpression):
    maxExp = max(refExpression)
    minExp = min(refExpression)
    normExpression = []
    for expr in expression:
        normExpr = (expr - minExp)/(maxExp - minExp)
        normExpression.append(normExpr)
    return normExpression

def plotData(symbolMap, yExp, oExp, yPhases, oPhases, outBase, motifSymbol):
    fig = plt.figure(figsize = (12, 6))
    ax = fig.add_subplot(111, projection = '3d')
    offset = 24
    t1 = range(0,48,4) # subplot 1 x-axis
    t2 = range(offset+48,offset+48+48,4) # subplot 2 x-axis
    tOffset = range(0,offset,4)
    t = t1 + tOffset + t2

    N = len(symbolMap)
    colorWidget = cm.get_cmap('plasma',N)
    colors = {}
    geneCount = 0
    for transcript in symbolMap:
        colors[transcript] = colorWidget(float(geneCount)/float(N))
        geneCount += 1

    # plot young sorted by phase in young
    symbolMap.sort(key = lambda x:yPhases[x[0]], reverse=False)  # sort by young phase
    for transcript in symbolMap:
        transcriptID, transcriptSymbol = transcript
        if np.median(yExp[transcriptID]) >= 1.0 or np.median(oExp[transcriptID]) >= 1.0:
            print transcriptID, transcriptSymbol, yPhases[transcriptID], np.median(yExp[transcriptID]), np.median(oExp[transcriptID])
            yMaxMinExp = maxMinNormalize(yExp[transcriptID], yExp[transcriptID] + oExp[transcriptID])
            # creating a list the same length as t1
            y = [-10*geneCount-10] * len(t1)
            ax.plot(t1, y, yMaxMinExp, c = colors[transcript], alpha = 0.7, label = transcriptSymbol)

    # plot old sorted by phase in old
    symbolMap.sort(key = lambda x:oPhases[x[0]], reverse=False)  # sort by old phase
    for transcript in symbolMap:
        transcriptID, transcriptSymbol = transcript
        if np.median(yExp[transcriptID]) >= 1.0 or np.median(oExp[transcriptID]) >= 1.0:
            print transcriptID, transcriptSymbol, oPhases[transcriptID], np.median(yExp[transcriptID]), np.median(oExp[transcriptID])
            oMaxMinExp = maxMinNormalize(oExp[transcriptID], yExp[transcriptID] + oExp[transcriptID])
            # creating a list the same length as t1
            y = [-10*geneCount-10] * len(t1)
            ax.plot(t2, y, oMaxMinExp, c = colors[transcript], alpha = 0.7)


    ## go just beyond 48, up to 49 to include 48.
    linker = [ "1" ] * (offset/24)
    tickLabels = range(0,49,24) + linker + range(0,49,24)
    plt.xlim(0,offset+48+48+1)
    plt.xticks(range(0,48+offset+48+1,24),tickLabels)
    ax.view_init(5, -85)
    plt.title('Motif for ' + motifSymbol, loc = 'left')
    plt.legend(ncol=3)
    plt.savefig(outBase + '_ExpressionProfile3D.pdf', bbox_inches='tight')
    plt.clf()


##########
## MAIN ##
##########

args = getArgs()

expressionFile1 = args.exp1
expressionFile2 = args.exp2
geneIDListFile = args.gl
youngGeneGroupsFile = args.ggy
oldGeneGroupsFile = args.ggo
outBase = args.o

transcriptIDs,transcriptDict = readGeneIDListFile(geneIDListFile)
yPhases = readGeneGroupsFile(youngGeneGroupsFile,transcriptIDs)
oPhases = readGeneGroupsFile(oldGeneGroupsFile,transcriptIDs)
yExpression = readExpressionFile(expressionFile1,transcriptIDs)
oExpression = readExpressionFile(expressionFile2,transcriptIDs)

for motif in transcriptDict:
    motifID, motifSymbol = motif
    print('')
    print('Plotting for: ' + motifID + ',' + motifSymbol)
    outbase = outBase + '_' + motifID
    transcripts = transcriptDict[motif]
    plotData(transcripts, yExpression, oExpression, yPhases, oPhases, outbase, motifSymbol)
    
