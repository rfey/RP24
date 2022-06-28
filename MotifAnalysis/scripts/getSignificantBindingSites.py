# rmf 7.1.2020, last modified 4.26.2021
# cleaned up 3.1.2022

import sys, re

usage = 'python ' + sys.argv[0] + ' <results file list> <median expression file> <p-value threshold> <fimoSummaryFile_FPKM1.0_p5e-05.txt> <FDR (True/False)> <TF expr thresh (FPKM)>'
if len(sys.argv) != 7 or '-h' in sys.argv or '--help' in sys.argv:
    print(usage)
    sys.exit()

# SUBROUTINES
def readResultsFile(resultsFile,pThresh,expr,FDR,exprThresh,secondaryIDs):
    sigGenes = {}
    resultsFile = open(resultsFile,'r')
    next(resultsFile)
    for line in resultsFile:
        if '#' in line:
            flag = False
            motifID, motifSymbol, N, K, n, k, BG, pval, rank, qval = line.strip().split('\t')
            # filter on pvalue
            if FDR == False:
                if pval != 'NO_TEST':
                    stat = float(pval)
                else:
                    stat = 1.0
            elif FDR == True:
                if qval != 'NO_TEST':
                    stat = float(qval)
                else:
                    stat = 1.0
            if stat <= pThresh:
                motifID = motifID.replace('##','')
                motif_ID = motifID.split('_')[0] # get just FBID so we can check expression
                # make sure the ID is the most recent one so we can check expression
                if motif_ID not in expr:
                    if motif_ID in secondaryIDs:
                        motif = secondaryIDs[motif_ID]
                    else:
                        # if this gets printed, manually look up and add to secondary IDs dict
                        print 'This motif:', motif_ID, ' not in expression file! Look up this ID and add a new key:value pair to the secondaryIDs dictionary.'
                        print 'key = the above motif'
                        print 'value = the most recent FBID in flybase'
                        sys.exit()
                else:
                    motif = motif_ID
                # now filter on expression
                if expr[motif] >= exprThresh:
                    # key by original (motifID,motifSymbol) tuple; this preserves all information
                    sigGenes[(motifID, motifSymbol)] = []
                    sigGenes[(motifID, motifSymbol)].append(stat)
                    flag = True
        elif flag == True:
            # now get the individual geneIDs in the following lines
            FBID, symbol = line.strip().split('\t')
            sigGenes[(motifID, motifSymbol)].append(symbol)
    resultsFile.close()
    return sigGenes

def getBindingSiteInfo(sigGenes,fimoResults,outfile):
    count = 0
    for key in sigGenes:
        motifID, motifSymbol = key
        if motifID in fimoResults:
            stat = sigGenes[key][0]
            del sigGenes[key][0] # remove this before looping through geneIDs
            for geneID in sigGenes[key]:
                if geneID in fimoResults[motifID]:
                    for site in fimoResults[motifID][geneID]:
                        outfile.write(motifID + '\t' + motifSymbol + '\t' + str(stat) + '\t' + geneID + '\t' + '\t'.join(site) + '\n')
                else:
                    print geneID, ' not in fimo results'
    outfile.close()

# ARGUMENTS and MAIN
resultsFileList = sys.argv[1]
medianExprFile = sys.argv[2]
pThresh = float(sys.argv[3])
fimoSummaryFile = sys.argv[4]
FDR = sys.argv[5] == 'True' # True if user inputs True, False if user inputs False
exprThresh = float(sys.argv[6])

if FDR == True:
    print 'Using FDR of ' + str(pThresh)
elif FDR == False:
    print 'Using p-value of ' + str(pThresh)

# read expression file
print('Reading expression file...')
expr = {}
with open(medianExprFile,'r') as medianExprFile:
    for line in medianExprFile:
        if '#' not in line:
            FBID, symbol, youngMedianExpr, oldMedianExpr = line.strip().split('\t')
            val = max(float(youngMedianExpr),float(oldMedianExpr))
            expr[FBID] = val
medianExprFile.close()


# read fimo summary file
print('Reading fimo summary file...')
fimoResults = {}
with open(fimoSummaryFile,'r') as fimoFile:
    next(fimoFile)
    for line in fimoFile:
        motifID, geneID, sequence, start, stop, strand, pvalue = line.strip().split('\t')
        if motifID not in fimoResults:
            fimoResults[motifID] = {}
        if geneID not in fimoResults[motifID]:
            fimoResults[motifID][geneID] = []
        fimoResults[motifID][geneID].append((start,stop,strand,sequence))
fimoFile.close()

secondaryIDs = {'FBgn0000210':'FBgn0283451','FBgn0053980':'FBgn0263512','FBgn0086910':'FBgn0265276','MA0229.1':'FBgn0001269','MA0447.1':'FBgn0001150','MA1700.1':'FBgn0032979','MA0915.1':'FBgn0020307','MA1462.1':'FBgn0259789','cnc14':'FBgn0262975','FBgn0005630':'FBgn0283521','FBgn0000472':'FBgn0262656','MA0449.1':'FBgn0001168','FBgn0015014':'FBgn0264075','FBgn0052830':'FBgn0264442','FBgn0030532':'FBgn0267033','cnc13':'FBgn0262975','MA0222.1':'FBgn0000611','FBgn0000095':'FBgn0260642', 'MA0243.1':'FBgn0003345', 'FBgn0042650':'FBgn0285879', 'FBgn0033182':'FBgn0263240', 'MA0239.1':'FBgn0003145', 'MA0126.1':'FBgn0003028', 'FBgn0000413':'FBgn0267821', 'MA0026.1':'FBgn0000567', 'MA1455.1':'FBgn0039683', 'MA0529.2':'FBgn0015602', 'MA0460.1':'FBgn0003870', 'FBgn0000099':'FBgn0267978'}

print('Extracting significant transcription factor binding sites for:')
pattern = re.compile('.*?resultsHypergeomTest_(.*?)_maxBG.*')
with open(resultsFileList,'r') as F:
    for line in F:
        resultsFile = line.strip()
        print resultsFile
        outbase = pattern.search(resultsFile).group(1)
        sigGenes = readResultsFile(resultsFile,pThresh,expr,FDR,exprThresh,secondaryIDs)
        # if there are significant binding sites
        if len(sigGenes.keys()) != 0:
            # get binding site info from fimo file
            if FDR == False:
                outfile = open('bindingSiteInfo_' + outbase + '_p' + str(pThresh) + '.txt','w')
                outfile.write('#motifID\tmotifSymbol\tpvalue\tgeneID\tstart\tstop\tstrand\tsequence\n')
            elif FDR == True:
                outfile = open('bindingSiteInfo_' + outbase + '_FDR' + str(pThresh) + '.txt','w')
                outfile.write('#motifID\tmotifSymbol\tqvalue(FDR)\tgeneID\tstart\tstop\tstrand\tsequence\n')
            getBindingSiteInfo(sigGenes,fimoResults,outfile)
F.close()
