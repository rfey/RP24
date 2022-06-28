# rmf 4.29.2020, last modified 5.22.2020

import sys

usage = 'python ' + sys.argv[0] + ' <fimo results summary file> <median gene expression file> <p-value threshold> <expression threshold>'
if len(sys.argv) != 5 or '-h' in sys.argv or '--help' in sys.argv:
    print(usage)
    sys.exit()

fimoFile = sys.argv[1]
medianExprFile = sys.argv[2]
pThresh = float(sys.argv[3])
exprThresh = float(sys.argv[4])

# get genes that pass the expression threshold
IDs = []
with open(medianExprFile,'r') as exprFile:
    next(exprFile)  # skip header
    for line in exprFile:
        geneID,symbol,youngMedianExpr,oldMedianExpr = line.strip().split('\t')
        if float(youngMedianExpr) >= exprThresh or float(oldMedianExpr) >= exprThresh:
            IDs.append(symbol)
exprFile.close()

print('Genes passing expression threshold: ' + str(len(IDs)))

outfile = open('fimoSummaryFile_FPKM' + str(exprThresh) + '_p' + str(pThresh) + '.txt','w')
outfile.write('#motifID\tgeneID\tsequence\tstart\tstop\tstrand\tpvalue\n')  # write header

# parse fimo file on pval and gene expr
with open(fimoFile,'r') as fimoFile:
    next(fimoFile)  # skip header
    for line in fimoFile:
        motifID,geneID,sequence,start,stop,strand,pval = line.strip().split('\t')
        if geneID in IDs and float(pval) <= pThresh:
            outfile.write(motifID+'\t'+geneID+'\t'+sequence+'\t'+start+'\t'+stop+'\t'+strand+'\t'+pval+'\n')
fimoFile.close()
outfile.close()
