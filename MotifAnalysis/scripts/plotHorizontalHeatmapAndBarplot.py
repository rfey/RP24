# rmf 3.25.2020, last modified 5.20.2021
# cleaned up 3.1.2022

import sys, re
import matplotlib as mpl
mpl.use('Agg')
from matplotlib import pyplot as plot
import numpy as np

# USAGE
usage = 'python ' + sys.argv[0] + ' <summary file> <p-value threshold> <asterisk threshold> <FDR annotation (True or False)>'
details = 'Plots only clusters which have a significant TF binding site.'
if len(sys.argv) != 5 or '-h' in sys.argv or '--help' in sys.argv:
    print(usage)
    print(details)
    sys.exit()

# SUBROUTINES

# read summary file
def readSummaryFile(summaryFile):
    plotInfo, FDRs, motifDBID2symbol, motifSymbolDict, duplicateCheck = {},{},{},{},{}
    summaryFile = open(summaryFile,'r')
    next(summaryFile)  # skip header
    for line in summaryFile:
        info = line.strip().split('\t')

        # this is a non-filtered version
        if len(info) == 12:
            print 'Please submit a filtered version of the motif summary file for plotting.'
            exit()

        # this is a filtered version
        elif len(info) == 15:
            GOIgroup, motifDBID, motifSymbol, N, K, n, k, BG, pval, rank, qval, expr, eScore, youngExpr, oldExpr = info

        else:
            print('Error! Wrong number of columns in input file.')
            sys.exit()

        # take care of NO_TEST cases for pval and qval
        # set NO_TEST to 1.0 in case the square needs to be represented on the heatmap
        if pval != 'NO_TEST':
            pval = float(pval)
        elif pval == 'NO_TEST':
            pval = 1.0  
        if qval != 'NO_TEST':
            qval = float(qval)
        elif qval == 'NO_TEST':
            qval = 1.0


        # store duplicate TF info
        motifBase = re.sub(r'_(SOLEXA|SANGER|Cell|FlyReg).*', '', motifSymbol)
        if motifBase not in duplicateCheck:
            duplicateCheck[motifBase] = []
        duplicateCheck[motifBase].append((GOIgroup, motifDBID, motifSymbol, pval, qval))

        # save pvals and FDR for each motifID and GOIgroup combo
        if GOIgroup not in plotInfo:
            plotInfo[GOIgroup] = {}

        # key by database ID, which is unique
        if (GOIgroup, motifSymbol) not in motifSymbolDict:
            if motifDBID not in plotInfo[GOIgroup]:
                plotInfo[GOIgroup][motifDBID] = (float(pval), float(qval))
                motifSymbolDict[(GOIgroup, motifSymbol)] = True
            else:
                print motifDBID, 'already in', GOIgroup
                sys.exit()

        # now save an dict with motif symbol and expr
        if motifDBID not in motifDBID2symbol:
            motifDBID2symbol[motifDBID] = (motifSymbol, float(youngExpr), float(oldExpr))

    summaryFile.close()
    return plotInfo, motifDBID2symbol, duplicateCheck


def formatName(name, num):
    # example: Cluster18_calcium-dependent_phospholipid
    name = re.sub(r'Cluster\d*?_', r'Cluster ' + str(num) + ': ', name)
    name = name.replace('_', ' ') # replace any remaining underscores with space
    return name

def sortDAVIDgroups(GOIgroups):
    xTuples = {}
    # example: resultsHypergeomTest_DAVID_ELC_transcript_q0.05_Cluster10_Potassium_transport_maxBG0.5_BHFDRcorrected.txt
    # DAVID_ELCs_transcriptGroups0.05_Cluster13_presynapse
    clusterNum = re.compile('(.LCs?)_.*(Cluster(\d*)_.*)') # get GOI designation and cluster ID number
    for clusterName in GOIgroups:
        rhythmicityGroup = clusterNum.search(clusterName).group(1)  # ELC, RLC or LLC
        baseName = clusterNum.search(clusterName).group(2).split('_maxBG')[0]  # DAVID name
        num = int(clusterNum.search(clusterName).group(3))  # cluster number
        # clean up DAVID name
        cleanedName = formatName(baseName, num)
        tup = (clusterName, cleanedName, num)
        if rhythmicityGroup not in xTuples:
            xTuples[rhythmicityGroup] = []
        xTuples[rhythmicityGroup].append(tup)
    # these will store cleaned cluster names, and orignal cluster names, respectively
    xlabels, clusterNames = [], []
    print xTuples.keys()
    for group in ['ELCs','RLCs','LLCs']:
        if group in xTuples.keys():
            # sort by cluster number
            xTuples[group].sort(key = lambda x: x[2])
            names, labels, nums = zip(*xTuples[group])
            xlabels.extend(labels)
            clusterNames.extend(names)
        else:
            print('There are no saved clusters in the ' + group + ' group!')
    return xlabels, clusterNames


# ARGUMENTS and MAIN
summaryFile = sys.argv[1]
pThresh = float(sys.argv[2])  # for determining what appears on the heatmap
asteriskThresh = float(sys.argv[3])  # for determining what is marked as statistically significant (can be pval or FDR)
FDR = sys.argv[4] == 'True'  # if the user sets to true, FDR will be True; else, will be False (and the script uses pval)

outbase = summaryFile.replace('motifEnrichmentSummary_','').replace('.txt','')
if FDR == False:
    outbase = outbase + '_pval' + str(pThresh) + '_astkPval' + str(asteriskThresh)
elif FDR == True:
    outbase = outbase + '_pval' + str(pThresh) + '_astkFDR' + str(asteriskThresh)

# read summary file
print 'Reading summary file...'
plotInfo, motifDBID2symbol, duplicateCheck = readSummaryFile(summaryFile)

# filter by q-value
filtered = {}
filteredTFs = []
savedMotifs, toCheck = [],[]
savedGroups, groupCheck = [],[]
for GOIgroup in plotInfo:
    for motifDBID in plotInfo[GOIgroup]:
        pval, qval = plotInfo[GOIgroup][motifDBID]
        motifSymbol = motifDBID2symbol[motifDBID][0]
        motifBase = re.sub(r'_(SOLEXA|SANGER|Cell|FlyReg).*', '', motifSymbol)

        # keep all with significant qval
        if qval <= asteriskThresh:
            savedMotifs.append(motifBase)
            savedGroups.append(GOIgroup)
            if GOIgroup not in filtered:
                filtered[GOIgroup] = {}
            filtered[GOIgroup][motifDBID] = (pval, qval)
            filteredTFs.append(motifDBID)
        else:
            toCheck.append(motifBase)
            groupCheck.append(GOIgroup)
            
toCheck = set(toCheck)
groupCheck = set(groupCheck)


# now save lowest pval for motifs without sig qvals but with pval <= pThresh
for motifBase in toCheck:
    if motifBase not in savedMotifs:
        duplicateCheck[motifBase].sort(key = lambda x: x[3])
        # get all entries that pass pval thresh
        passThresh = []
        for info in duplicateCheck[motifBase]:
            GOIgroup, motifDBID, motifSymbol, pval, qval = info
            if pval <= pThresh:
                if GOIgroup not in filtered:
                    filtered[GOIgroup] = {}
                if motifDBID not in filtered[GOIgroup]:
                    filtered[GOIgroup][motifDBID] = (pval, qval)
                    filteredTFs.append(motifDBID)
                else:
                    print 'ERROR'
                    exit()

filteredTFs = list(set(filteredTFs))

# sort TFs on expression in young
filteredTFs.sort(key = lambda x: motifDBID2symbol[x][1], reverse = True)


# sort GOI groups for labels
# we don't need TF labels, these are plotted in the bar plot and shared with the heatmap
if 'Cluster' in filtered.keys()[0]:
    clusterLabels, clusterNames = sortDAVIDgroups(filtered.keys())  # clusterLabels are prettier versions of cluster names
else:
    clusterLabels = filtered.keys()
    clusterNames = filtered.keys()


# initialize plotting matrix and qval matrix
plottingMatrix = []
qvalMatrix = []
# rows
for i in range(len(clusterNames)):
    # columns
    plottingMatrix.append([0] * len(filteredTFs))
    qvalMatrix.append([0] * len(filteredTFs))


# fill plotting matrix using original pval dict in case some cells don't pass thresh but need to be filled
# get qvals for annotating heatmap with asterisks
for i in range(len(clusterNames)):
    for j in range(len(filteredTFs)):
        # store pval
        pval, qval = plotInfo[clusterNames[i]][filteredTFs[j]]
        plottingMatrix[i][j] = pval
        # store qval
        qvalMatrix[i][j] = qval



# plot subplots: one for heatmap, one for expression barplot
# gridspec controls ratio of one subplot to the other
fig, (ax1, ax2) = plot.subplots(2, figsize = (15, 10), gridspec_kw = {'height_ratios': [1, 5]})

print 'Plotting heatmap...'
plottingMatrix = np.array(plottingMatrix,ndmin=2)
heatmap = ax2.imshow(plottingMatrix, 
                     cmap = 'Purples_r', aspect = 'auto',
                     norm = mpl.colors.SymLogNorm(linthresh = 0.001, linscale = 0.001, vmin = 0.0, vmax = 1.0)) # plot data, custom colorbar range, aspect was 'auto'

# annotate heatmap
for i in range(len(clusterNames)):
    for j in range(len(filteredTFs)):
        qval = qvalMatrix[i][j]
        if qval <= asteriskThresh:
            ax2.text(j, i + 0.25+(0.25/2), '*', ha = 'center', va = 'center', color = 'white', fontsize = 18)


# set up gridlines
ax2 = plot.gca()
ax2.set_xticks(np.arange(-.5, len(filteredTFs), 1), minor=True)
ax2.set_yticks(np.arange(-.5, len(clusterNames), 1), minor=True)
ax2.grid(which='minor',color='black',linestyle='-',linewidth='1')

plot.xticks(np.arange(len(filteredTFs)), [])
plot.yticks(np.arange(len(clusterNames)), clusterLabels, ha='right', va = 'center', rotation_mode = 'anchor') 
plot.tick_params(top=True, bottom=False, labeltop=True, labelbottom=False) # put x axis at top of graph                                                                  


##### COLORBAR ######

# create colorbar
cbar = plot.colorbar(heatmap, orientation = 'horizontal', aspect = 40, pad = 0.05)
cbar.set_label('p-value', va='bottom')

# set color bar tick marks
mn = np.min(plottingMatrix)
mx = np.max(plottingMatrix)
logThresh = np.log10(pThresh)
tick1 = np.log10(0.1)
tick2 = np.log10(0.001)

tickLabels = [0.0, 0.01, 0.1, 1.0]

cbarTicks = cbar.get_ticks() # list of tick vals
cbarTickLabels = []
for tick in cbarTicks:
    if tick in tickLabels:
        cbarTickLabels.append(tick)
    else:
        cbarTickLabels.append('')
cbar.set_ticks(cbarTicks)
cbar.set_ticklabels(cbarTickLabels)

# set color bar tick labels
# this should give the original pval
mn_label = round(10**mn, 3)
mx_label = round(10**mx, 3)
ticklabel1 = 0.1
ticklabel2 = 0.001
thresh_label = pThresh


###### BAR PLOT ######
print 'Plotting bar plot...'

# get ylabels
fullSymbols, symbols = [],[]
youngVals, oldVals = [],[]
for TF in filteredTFs:
    fullSymbol = motifDBID2symbol[TF][0]
    symbol = re.sub(r'_(SOLEXA|SANGER|Cell|FlyReg).*', '', fullSymbol)  # clean up symbol name

    # deal with inconsistent usage
    if symbol == 'lola_PK':
        symbol = 'lola-PK'

    # save to lists
    fullSymbols.append(fullSymbol)
    symbols.append(symbol)

    # save expr info
    youngVals.append(motifDBID2symbol[TF][1])
    oldVals.append(motifDBID2symbol[TF][2])


xlabels = []
i = 0
maxLength = 0
for symbol in symbols:
    if len(symbol) > maxLength:
        maxLength = len(symbol)
    if symbols.count(symbol) > 1:
        xlabels.append(fullSymbols[i])
    else:
        xlabels.append(symbol)
    i += 1


# default bar height (width) is 0.8 
height = 0.4
xvals = np.arange(len(youngVals)) # xval locations
ax1.bar(xvals - 0.2, youngVals, color = 'red', width = height, label = 'young')
ax1.bar(xvals + 0.2, oldVals, color = 'blue', width = height, label = 'old')
ax1.legend()

# adjust x axis
ax1.set_xticks(xvals)
ax1.set_xticklabels(xlabels, rotation = 90)
ax1.set_xlim(-height, len(xvals) - height)

# adjust y axis
ax1.set_ylabel('Expression\n(FPKM)')
ax1.set_yscale('log')

# set up grid lines
ax1.set_axisbelow(True)
ax1.yaxis.grid(color = 'grey', linestyle = 'dashed')

plot.tight_layout()

print 'Saving output file...'
outFile = 'horizontalHeatmapBarplot_motifEnrichmentSummaryRefined_' + outbase + '.pdf'
plot.savefig(outFile)
