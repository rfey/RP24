# rmf 3.24.2020, last modified 5.18.2021
# cleaned up 3.1.2022

import sys
import statsmodels.stats.multitest as multi

# USAGE
usage = 'python ' + sys.argv[0] + ' <test results file> <meme map file> <gene median expression file> <secondary FBID file> <secondary JASPAR ID file>'
if len(sys.argv) != 6 or '-h' in sys.argv or '--help' in sys.argv:
    print(usage)
    sys.exit()

# SUBROUTINES
def getExpr(FBID, expr, altIDs, JASPAR_IDs):
    if FBID in expr:
        FBID = FBID
    elif FBID in altIDs:
        FBID = altIDs[FBID]
    elif FBID in JASPAR_IDs:
        FBID = JASPAR_IDs[FBID]
    elif 'cnc' in FBID:
        FBID = 'FBgn0262975'
    else:
        # if ID not found, return 0.0 for the expression
        print 'ERROR: Motif ID ' + FBID + ' not found.'
        return 0.0
    return expr[FBID][0]

def filterBG(motif, info, tests, pvals):
    transcriptIDs, transcriptSymbols, motifSymbol, N, K, n, k, BG, pval, expr = info
    # this is if maxBG is higher than threshold set in hypergeom testing script
    if pval != 'NO_TEST':
        if float(BG) < float(k)/float(n):
            tests.append(motif)
            pvals.append(float(pval))
    return tests, pvals

def writeOutfile(resultsFile,header,results,testsDict):
    outfile = open(resultsFile.replace('.txt','_BHFDRcorrected.txt'),'w')
    outfile.write('\t'.join(header) + '\n')

    for motifID in results:
        transcriptIDlist,transcriptSymbolList,motifSymbol,N,K,n,k,BG,pval,exprVal = results[motifID]
        if motifID in testsDict:
            rank = testsDict[motifID][1]
            qval = testsDict[motifID][2]
        else:
            rank = 'NO_TEST'
            qval = 'NO_TEST'

        outfile.write('#'+motifID+'\t'+motifSymbol+'\t'+N+'\t'+K+'\t'+n+'\t'+k+'\t'+str(BG)+'\t'+str(pval)+'\t'+str(rank)+'\t'+str(qval)+'\t'+str(exprVal)+'\n')
        for i in range(len(transcriptIDlist)):
            outfile.write(transcriptIDlist[i]+'\t'+transcriptSymbolList[i]+'\n')
    outfile.close()

# ARGUMENTS and MAIN
resultsFile = sys.argv[1]
mapsFile = sys.argv[2]
exprFile = sys.argv[3]
secondaryFBIDfile = sys.argv[4]
secondaryJASPARfile = sys.argv[5]

# read maps file
maps = {}
with open(mapsFile,'r') as mapsFile:
    for line in mapsFile:
        memeDatabaseID, geneSymbol = line.strip().split(' ')
        maps[memeDatabaseID] = geneSymbol
mapsFile.close()

# read expresion file
expr = {}
with open(exprFile, 'r') as exprFile:
    next(exprFile)  # skip header
    for line in exprFile:
        FBID, symbol, youngMedianExpr, oldMedianExpr = line.strip().split('\t')
        expr[FBID] = (float(youngMedianExpr), float(oldMedianExpr))
exprFile.close()

# read secondary ID files
altIDs = {}
with open(secondaryFBIDfile, 'r') as sFile1:
    next(sFile1)
    for line in sFile1:
        altID, currentID = line.strip().split('\t')
        altIDs[altID] = currentID
sFile1.close()

JASPAR_IDs = {}
with open(secondaryJASPARfile,'r') as sFile2:
    next(sFile2)
    for line in sFile2:
        JASPARmotifID, motifSymbol, FBgnID = line.strip().split('\t')
        JASPAR_IDs[JASPARmotifID] = FBgnID
sFile2.close()

print 'Reading results file ' + resultsFile + '...'
symbolDict, allInfo = {},{}
with open(resultsFile,'r') as f:
    header = next(f).strip().split('\t')
    for line in f:
        # these are deflines
        if '#' in line:
            motifID, N, K, n, k, BG, pval = line.strip().split('\t')
            motifID = motifID.replace('#','')
            if motifID in maps:
                motifSymbol = maps[motifID]
            else:
                print 'No motif symbol found for', motifID, motifID_cleaned
                exit()

            allInfo[motifID] = [[], [], motifSymbol, N, K, n, k, BG, pval] # empty lists for gene IDs and symbols
            if motifSymbol not in symbolDict:
                symbolDict[motifSymbol] = []
            symbolDict[motifSymbol].append(motifID)

        else:
            # will only store lists of geneIDs if the defline for these genes was previously stored
            transcriptID,transcriptSymbol = line.strip().split('\t')
            allInfo[motifID][0].append(transcriptID)
            allInfo[motifID][1].append(transcriptSymbol)

print 'Stored', len(allInfo), 'database motif IDs.'
f.close()

results = {}
tests, pvals = [],[]

# organize tests we want to correct
# only correct once per dimer
# store expr info for the more lowly expressed dimer partner
for motifSymbol in symbolDict:
    if len(symbolDict[motifSymbol]) == 2:
        motif1, motif2 = symbolDict[motifSymbol]

        FBID1 = motif1.split('_')[0]
        FBID2 = motif2.split('_')[0]

        # median expression in young
        exprFBID1 = getExpr(FBID1, expr, altIDs, JASPAR_IDs)
        exprFBID2 = getExpr(FBID2, expr, altIDs, JASPAR_IDs)

        if exprFBID1 < exprFBID2:
            # add expression info
            results[motif1] = allInfo[motif1]  # need new dict or we will have the other dimer partner left over in the original one
            results[motif1].append(exprFBID1)
            tests, pvals = filterBG(motif1, results[motif1], tests, pvals)

        elif exprFBID2 < exprFBID1:
            results[motif2] = allInfo[motif2]
            results[motif2].append(exprFBID2)
            tests, pvals = filterBG(motif2, results[motif2], tests, pvals)

        else:
            print FBID1, exprFBID1, FBID2, exprFBID2
            exit()

    # if it's not a dimer, no need to check expression, just add it to the info
    elif len(symbolDict[motifSymbol]) == 1:
        motif = symbolDict[motifSymbol][0]

        # get expression and add to motif info
        FBID = motif.split('_')[0]
        exprFBID = getExpr(FBID, expr, altIDs, JASPAR_IDs)
        results[motif] = allInfo[motif]
        results[motif].append(exprFBID)

        tests, pvals = filterBG(motif, results[motif], tests, pvals)
    else:
        print motifSymbol, symbolDict[motifSymbol]
        exit()

print 'There are', len(tests), 'motif IDs stored for multiple test correction.'

# update header
header.insert(1, "motifSymbol")
header.extend(["rank", "qval", "youngMedianExpression"])

# if there are no tests to correct-- nothing passed the thresholds
testsDict = {}  # define here so we can check it when writing outfile
if len(tests) == 0:
    # write outfile without calculating q-values
    writeOutfile(resultsFile,header,results,testsDict)
    sys.exit()

print('Correcting ' + str(len(tests)) + ' tests...')

# first sort by pval to get rank
testInfo = zip(tests,pvals)
testInfo.sort(key=lambda x:x[1])
tests,pvals = zip(*testInfo)

ranks = []
rank = 0
for pval in pvals:
    rank += 1
    ranks.append(rank)

# multiple test correction
qvals = multi.multipletests(pvals,is_sorted=True,method='fdr_bh')[1]

# get in dictionary form
correctedTestInfo = zip(tests,pvals,ranks,qvals)
correctedTestInfo.sort(key=lambda x:x[0])  # sort by results file
for motifID,pval,rank,qval in correctedTestInfo:
    testsDict[motifID] = (pval,rank,qval)



print 'Writing output file...'
writeOutfile(resultsFile,header,results,testsDict)
