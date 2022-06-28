# rmf 4.22.2020, last updated 4.24.2021
# cleaned up 3.1.2022

print('Initializing...')
import sys, re
from scipy.stats import hypergeom

# USAGE
usage = 'python ' + sys.argv[0] + ' <fimo results summary file> <global motif counts file> <GOI file list> <background transcripts file> <median expression file> <max background threshold> <FPKM threshold> <threshold for number of genes in GOI group>'
if len(sys.argv) != 9 or '-h' in sys.argv:
    print(usage)
    sys.exit()

# SUBROUTINES
def readGOIfile(GOIfile):
    GOIs = []
    with open(GOIfile,'r') as f:
        for line in f:
            GOI = line.strip()
            GOIs.append(GOI)
    f.close()
    return GOIs

# filter by expression level
def filterExpression(geneList, medianExpr, exprThresh):
    filteredGeneListSymbols = []
    filteredGeneListIDs = []
    for transcriptSymbol in geneList:
        # if not in expr files, will not be added to the filtered list
        if transcriptSymbol in medianExpr:
            transcriptID, yMedian, oMedian = medianExpr[transcriptSymbol]
            # test if passes expr threshold
            if yMedian >= exprThresh or oMedian >= exprThresh:
                filteredGeneListSymbols.append(transcriptSymbol)
                filteredGeneListIDs.append(transcriptID)
        else:
            print(transcriptSymbol + ' not found in expression files!')
    return filteredGeneListSymbols, filteredGeneListIDs

# get counts for 
def getGlobalMotifCounts(motifs,allGenes):
    globalMotifCounts = {}
    for motifID in motifs:
        K = 0
        for geneID in motifs[motifID]:
            # make sure it passes the expression filter
            if geneID in allGenes:
                K += 1
        globalMotifCounts[motifID] = K
    return globalMotifCounts

# hypergeometric test
def testSignificance(motifs,GOIs,GOIthresh,N,globalMotifCounts,maxBGthresh):
    results = {}
    n = len(GOIs) # sample size: total number of genes of interest
    for motifID in motifs:
        K = globalMotifCounts[motifID]
        k = 0  # number of sample successes: number of GOI promoters containing the motif
        genes = {}
        # don't run the test if the motif is not found in any promoter, or if it is found in over x% of all promoters
        BG = K/float(N)
        if K > 0 and n > GOIthresh and BG < maxBGthresh:
            # check how many GOI promoters contain the motif (update k)
            for gene in GOIs:
                geneSymbol, geneID = gene
                if geneSymbol in motifs[motifID]:
                    # don't count a gene more than once, even if it has multiple TF binding sites!
                    if geneSymbol not in genes:
                        genes[geneSymbol] = geneID
                        k += 1  # update number of sample successes
            pval = hypergeom.sf(k, N, K, n)
        else:
            genes['NO_TEST'] = 'NO_TEST'
            pval = 'NO_TEST'
        results[motifID] = (N,K,n,k,BG,genes,pval)
    return results

# ARGUMENTS and MAIN
fimoFile = sys.argv[1]
globalCountsFile = sys.argv[2]
GOIlistFile = sys.argv[3]
allGenesFile = sys.argv[4]
medianExprFile = sys.argv[5]
maxBGthresh = float(sys.argv[6])
exprThresh = float(sys.argv[7])
GOIthresh = float(sys.argv[8])

print('Reading input files...')
# read genes of interest file
GOIfiles = []
with open(GOIlistFile,'r') as f:
    for line in f:
        GOIfile = line.strip()
        GOIfiles.append(GOIfile)
f.close()

# read file to get all BG genes
allGenes = []
with open(allGenesFile,'r') as genesFile:
    for line in genesFile:
        geneID = line.strip()
        allGenes.append(geneID)
genesFile.close()

# read median expr file
medianExpr = {}
with open(medianExprFile,'r') as medianExprFile:
    next(medianExprFile)
    for line in medianExprFile:
        transcriptID, transcriptSymbol, yMedian, oMedian = line.strip().split('\t')
        medianExpr[transcriptSymbol] = (transcriptID,float(yMedian),float(oMedian))
medianExprFile.close()

# filter transcripts by expression threshold
# will zip into a zipped list later
print('Filtering all genes..............................')
allGeneSymbols_filtered,allGeneIDs_filtered = filterExpression(allGenes,medianExpr,exprThresh)

# read global counts file
print('Retrieving global motif counts.....')
globalMotifCounts = {}
with open(globalCountsFile,'r') as countsFile:
    next(countsFile)  # skip header
    for line in countsFile:
        motifID, K = line.strip().split('\t')
        globalMotifCounts[motifID] = int(K)
countsFile.close()

print('Reading fimo results file')
motifs = {}
with open(fimoFile,'r') as fimoFile:
    next(fimoFile) # skip header
    for line in fimoFile:
        motifID,geneID,sequence,start,stop,strand,pval = line.strip().split('\t')
        if motifID not in motifs:
            motifs[motifID] = []
        # make sure each passes the expression threshold!
        if geneID in allGeneSymbols_filtered:
            # not saving TFBS info bc only one random significant BS will be stored when testing
            if geneID not in motifs[motifID]:
                motifs[motifID].append(geneID)
fimoFile.close()

# go through each gene group
N = len(allGeneSymbols_filtered) # population size: total number of genes
for GOIfile in GOIfiles:
    outbase = GOIfile.split('/')[-1].replace('_transcriptList.txt','') + '_maxBG' + str(maxBGthresh)
    print('Testing gene group ' + outbase + '..........')

    GOIs = readGOIfile(GOIfile)
    # filter by expression
    GOIsymbols_filtered,GOI_IDs_filtered = filterExpression(GOIs,medianExpr,exprThresh) # could check against allGenes instead?
    GOIs_filtered = zip(GOIsymbols_filtered,GOI_IDs_filtered)
    # test statistical significance
    results = testSignificance(motifs,GOIs_filtered,GOIthresh,N,globalMotifCounts,maxBGthresh)

    outfile = 'resultsHypergeomTest_' + outbase + '.txt'
    with open(outfile,'w') as outfile:
        outfile.write('#motifID\tN\tK\tn\tk\tBG\tpval\n')
        for motifID in results:
            N,K,n,k,BG,genes,pval = results[motifID]
            outfile.write('#'+motifID+'\t'+str(N)+'\t'+str(K)+'\t'+str(n)+'\t'+str(k)+'\t'+str(BG)+'\t'+str(pval)+'\n')
            for geneSymbol in genes:
                geneID = genes[geneSymbol]
                outfile.write(geneID+'\t'+geneSymbol+'\n')
    outfile.close()
