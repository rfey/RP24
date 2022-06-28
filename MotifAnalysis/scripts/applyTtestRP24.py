# rmf 9.21.2020, last modified 5.4.2021

import sys, os, re
from statistics import stdev
from scipy.stats import ttest_ind
import statsmodels.stats.multitest as multi

usage = 'python ' + sys.argv[0] + ' <gene groups file> <significant sites file> <transcript IDs file> <outbase>'
if len(sys.argv) != 5 or '-h' in sys.argv:
    print usage
    sys.exit()

# SUBROUTINES
def readGeneGroupFile(geneGroupsFile):
    RP24s = {}
    with open(geneGroupsFile,'r') as f:
        next(f)  # skip header
        for line in f:
            info = line.strip().split('\t')
            if info[2] != 'NOTEST':
                RP24s[info[0]] = float(info[2])  # key by FBID, val is RP24
    f.close()
    return RP24s

def readGOIlist(GOIlist):
    GOIs = {}
    with open(GOIlist,'r') as f:
        for line in f:
            # line will have FBID, symbol (not sig) or FBID, symbol, motifID, motifsymbol (sig)
            info = line.strip().split('\t')
            GOIs[info[0]] = info
    f.close()
    return GOIs

def getRP24s(RP24s, GOIs):
    RP24sDict = {}
    for ID in GOIs:
        FBID, symbol = ID
        if FBID in RP24s:
            RP24sDict[ID] = RP24s[FBID]  # key by (transcriptID, symbol)
        else:
            print(FBID + ' not in RP24 file!')
            sys.exit()
    return RP24sDict

# T-test
def testSignificance(RP24s1,RP24s2):
    pval = 'NO_TEST' # overwrite if conditions below are met
    # degrees of freedom must be > 0 to run a T-test (need more than 1 sample per group)
    if len(RP24s1) > 1 and len(RP24s2) > 1:
        # if standard deviation is 0, pval=nan and all adjPvals=nan
        if stdev(RP24s1) != 0 and stdev(RP24s2) != 0:
            pval = ttest_ind(RP24s1,RP24s2,equal_var=False)[1] # assume unequal variance, perform Welch's T-test
    return pval

# ARGUMENTS and MAIN
geneGroupFile = sys.argv[1]
sigTranscriptsFile = sys.argv[2]
transcriptIDsfile = sys.argv[3]
outbase = sys.argv[4]

if 'Cluster' in sigTranscriptsFile:
    pattern = re.compile('.*(Cluster.*)\.txt')
    group = pattern.search(sigTranscriptsFile).group(1)
else:
    group = sigTranscriptsFile.replace('transcripts_significantSites_', '').replace('.txt', '')
print group

print 'Reading input files...'
RP24s = readGeneGroupFile(geneGroupFile)

# read sig transcripts file
sigInfo = {}
with open(sigTranscriptsFile, 'r') as f1:
    next(f1)  # skip header
    for line in f1:
        transcriptID, transcriptSymbol, motifID, motifSymbol = line.strip().split('\t')
        if (motifID, motifSymbol) not in sigInfo:
            sigInfo[(motifID, motifSymbol)] = []
        sigInfo[(motifID, motifSymbol)].append(transcriptID)
f1.close()

# read transcript ID file
allTranscripts = {}
with open(transcriptIDsfile, 'r') as f2:
    next(f2)  # skip header
    for line in f2:
        transcriptID, transcriptSymbol = line.strip().split('\t')
        allTranscripts[transcriptID] = transcriptSymbol
f2.close()

print 'Testing for statistical significance...'
for motif in sigInfo:
    sig, notSig = [],[]
    for transcriptID in allTranscripts:
        transcriptSymbol = allTranscripts[transcriptID]
        if transcriptID in sigInfo[motif]:
            sig.append((transcriptID, transcriptSymbol))
        else:
            notSig.append((transcriptID, transcriptSymbol))

    RP24s_sig = getRP24s(RP24s, sig)  # returns a dictionary
    RP24s_notsig = getRP24s(RP24s, notSig)

    pval = testSignificance(RP24s_sig.values(), RP24s_notsig.values())

    # initiate outfile and write header with pval and motif info
    outfile = open('results_RP24Ttest_' + motif[0] + '_' + outbase + '_' + group + '.txt', 'w')  # can't have motif symbol in outfile name bc some have ()
    outfile.write('##motifID:' + motif[0] + '\tmotifSymbol:' + motif[1] + '\tpval:' + str(pval) + '\n')
    # write list of genes to file
    outfile.write('#transcriptID\ttranscriptSymbol\tRP24\tsignificant\n')
    for ID in RP24s_sig:
        outfile.write(ID[0] + '\t' + ID[1] + '\t' + str(RP24s_sig[ID]) + '\tyes\n')
    for ID in RP24s_notsig:
        outfile.write(ID[0] + '\t' + ID[1] + '\t' + str(RP24s_notsig[ID]) + '\tno\n')
    outfile.close()
