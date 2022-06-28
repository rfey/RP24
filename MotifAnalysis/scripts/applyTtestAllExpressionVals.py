# rmf 9.21.2020, last modified 5.4.2021
# cleaned up 3.2.2022

import sys, os, re
from statistics import stdev
from scipy.stats import ttest_ind
import statsmodels.stats.multitest as multi
import numpy as np

usage = 'python ' + sys.argv[0] + ' <expression file> <significant sites file> <transcript IDs file> <outbase>'
if len(sys.argv) != 5 or '-h' in sys.argv:
    print usage
    sys.exit()

# SUBROUTINES
def getMedian(expr, GOIs):
    exprDict = {}
    for ID in GOIs:
        FBID, symbol = ID
        if FBID in expr:
            exprDict[ID] = expr[FBID]  # key by (transcriptID, symbol)
        else:
            print(FBID + ' not in expression file!')
            sys.exit()
    return exprDict

# T-test
def testSignificance(expr1, expr2):
    pval = 'NO_TEST' # overwrite if conditions below are met
    # degrees of freedom must be > 0 to run a T-test (need more than 1 sample per group)
    if len(expr1) > 1 and len(expr2) > 1:
        # if standard deviation is 0, pval=nan and all adjPvals=nan
        if stdev(expr1) != 0 and stdev(expr2) != 0:
            pval = ttest_ind(expr1, expr2, equal_var=False)[1] # assume unequal variance, perform Welch's T-test
    return pval

# ARGUMENTS and MAIN
exprFile = sys.argv[1]
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
# read expression file
expr = {}
with open(exprFile,'r') as exprFile:
    next(exprFile)  # skip header                                                                                                                                            
    for line in exprFile:
        FBID, ZT0, ZT4, ZT8, ZT12, ZT16, ZT20, ZT24, ZT28, ZT32, ZT36, ZT40, ZT44 = line.strip().split('\t')
        expr[FBID] = [float(ZT0),float(ZT4),float(ZT8),float(ZT12),float(ZT16),float(ZT20),float(ZT24),float(ZT28),float(ZT32),float(ZT36),float(ZT40),float(ZT44)]
exprFile.close()
print 'Read in median expression for', len(expr), 'transcripts.'

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

    expr_sig = {}
    sigVals = []
    for ID in sig:
        expr_sig[ID] = expr[ID[0]]
        sigVals.extend(expr_sig[ID])

    expr_notsig = {}
    notsigVals = []
    for ID in notSig:
        expr_notsig[ID] = expr[ID[0]]
        notsigVals.extend(expr_notsig[ID])
    
    pval = testSignificance(sigVals, notsigVals)

    # initiate outfile and write header with pval and motif info
    outfile = open('results_allValsExpressionTtest_' + motif[0] + '_' + outbase + '_' + group + '.txt', 'w')  # can't have motif symbol in outfile name bc some have ()
    outfile.write('##motifID:' + motif[0] + '\tmotifSymbol:' + motif[1] + '\tpval:' + str(pval) + '\n')
    # write list of genes to file
    outfile.write('#transcriptID\ttranscriptSymbol\tmedianExpression\tsignificant\n')
    for ID in expr_sig:
        vals = [str(val) for val in expr_sig[ID]]
        outfile.write(ID[0] + '\t' + ID[1] + '\t' + ','.join(vals) + '\tyes\n')
    for ID in expr_notsig:
        vals = [str(val) for val in expr_notsig[ID]]
        outfile.write(ID[0] + '\t' + ID[1] + '\t' + ','.join(vals) + '\tno\n')
    outfile.close()
