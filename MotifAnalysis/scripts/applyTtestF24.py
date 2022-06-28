# rmf 4.23.2021

import sys, os, re
from statistics import stdev
from scipy.stats import ttest_ind
import statsmodels.stats.multitest as multi

usage = 'python ' + sys.argv[0] + ' <F24 file> <significant sites file> <transcript IDs file> <outbase>'
if len(sys.argv) != 5 or '-h' in sys.argv:
    print usage
    sys.exit()

# SUBROUTINES
def readF24File(F24File):
    F24s = {}
    with open(F24File,'r') as f:
        next(f)  # skip header
        for line in f:
            transcriptID, transcriptSymbol, RP24, RP24_qVal, RP24_pVal, F24, avgRandomF24Score, F24_qVal, F24_pVal = line.strip().split('\t')
            if F24_pVal == 'NOTEST':
                F24score = 'NOTEST'
            else:
                F24score = float(F24) / float(avgRandomF24Score)
            F24s[transcriptID] = F24score  # key by FBID, val is F24
    f.close()
    return F24s

def readGOIlist(GOIlist):
    GOIs = {}
    with open(GOIlist,'r') as f:
        for line in f:
            # line will have FBID, symbol (not sig) or FBID, symbol, motifID, motifsymbol (sig)
            info = line.strip().split('\t')
            GOIs[info[0]] = info
    f.close()
    return GOIs

def getF24s(F24s, GOIs):
    F24sDict = {}
    for ID in GOIs:
        FBID, symbol = ID
        if FBID in F24s:
            if F24s[FBID] != 'NOTEST':
                F24sDict[ID] = F24s[FBID]  # key by (transcriptID, symbol)
        else:
            print(FBID + ' not in F24 file!')
            sys.exit()
    return F24sDict

# T-test
def testSignificance(F24s1,F24s2):
    pval = 'NO_TEST' # overwrite if conditions below are met
    # degrees of freedom must be > 0 to run a T-test (need more than 1 sample per group)
    if len(F24s1) > 1 and len(F24s2) > 1:
        # if standard deviation is 0, pval=nan and all adjPvals=nan
        if stdev(F24s1) != 0 and stdev(F24s2) != 0:
            pval = ttest_ind(F24s1,F24s2,equal_var=False)[1] # assume unequal variance, perform Welch's T-test
    return pval

# ARGUMENTS and MAIN
F24File = sys.argv[1]
sigTranscriptsFile = sys.argv[2]
transcriptIDsfile = sys.argv[3]
outbase = sys.argv[4]

pattern = re.compile('.*(Cluster.*)\.txt')
group = pattern.search(sigTranscriptsFile).group(1)

print 'Reading input files...'
F24s = readF24File(F24File)

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

    F24s_sig = getF24s(F24s, sig)  # returns a dictionary
    F24s_notsig = getF24s(F24s, notSig)

    pval = testSignificance(F24s_sig.values(), F24s_notsig.values())

    # initiate outfile and write header with pval and motif info
    outfile = open('results_F24Ttest_' + motif[0] + '_' + outbase + '_' + group + '.txt', 'w')  # can't have motif symbol in outfile name bc some have ()
    outfile.write('##motifID:' + motif[0] + '\tmotifSymbol:' + motif[1] + '\tpval:' + str(pval) + '\n')
    # write list of genes to file
    outfile.write('#transcriptID\ttranscriptSymbol\tF24/avgF24\tsignificant\n')
    for ID in F24s_sig:
        outfile.write(ID[0] + '\t' + ID[1] + '\t' + str(F24s_sig[ID]) + '\tyes\n')
    for ID in F24s_notsig:
        outfile.write(ID[0] + '\t' + ID[1] + '\t' + str(F24s_notsig[ID]) + '\tno\n')
    outfile.close()
