# rmf 12.29.2020, last modified 5.13.2021

import sys, re

# INPUT: DAVID cluster motif summary file from hypergeometric testing
# OUTPUT: file with same information, filtered; additional columns for expression in young and old, and enrichment score
# FUNCTION: filters DAVID clusters by enrichment score and TFs by FPKM; keeps clusters and TFs above or matching threshold

# USAGE
usage = 'python ' + sys.argv[0] + ' <motif summary file> <expression file> <secondary FBID file> <JASPAR secondary ID file> <FPKM threshold> <N number of transcripts in group> [enrichment score table] [enrichment score threshold]'
if len(sys.argv) < 7 or '-h' in sys.argv or '--help' in sys.argv:
    print(usage)
    sys.exit()

# SUBROUTINES
def readEnrichmentFile(scoreTable):
    # read enrichment score table
    scores = {}
    tablePattern = re.compile('(Cluster_\d*).*')
    with open(scoreTable, 'r') as table:
        next(table)
        for line in table:
            group, enrichmentScore, fullClusterName = line.strip().split('\t')
            if group not in scores:
                scores[group] = {}
            clusterNum = tablePattern.search(fullClusterName).group(1).replace('_', '')  # remove underscore
            scores[group][clusterNum] = float(enrichmentScore)
    table.close()
    return scores

def getEnrichmentScore(groupName, scores):
    pattern = re.compile('.*?(.LCs*).*(Cluster\d*?)_.*')
    # get cluster number and group name
    match = pattern.search(groupName)
    group = match.group(1)
    clusterNumber = match.group(2)
    # use these to access the enrichment score
    score = scores[group][clusterNumber]
    return score

# ARGUMENTS and MAIN
summaryFile = sys.argv[1]
exprFile = sys.argv[2]
FBIDmapFile = sys.argv[3]
JASPARmapFile = sys.argv[4]
exprThresh = sys.argv[5]
N = sys.argv[6]

eThresh = 'NA'
if len(sys.argv) == 9:
    scoreTable = sys.argv[7]
    eThresh = sys.argv[8]
    print 'Filtering using an enrichment score threshold of', eThresh, '...'
    scores = readEnrichmentFile(scoreTable)

print 'Reading input files...'

# read FBID map file
FBIDmap = {}
with open(FBIDmapFile, 'r') as FBIDmapFile:
    next(FBIDmapFile)  # skip header
    for line in FBIDmapFile:
        altID, currentID = line.strip().split('\t')
        FBIDmap[altID] = currentID
FBIDmapFile.close()

# read JASPAR map file
JASPARmap = {}
with open(JASPARmapFile, 'r') as JASPARmapFile:
    next(JASPARmapFile)  # skip header
    for line in JASPARmapFile:
        motifID, motifSymbol, geneID = line.strip().split('\t')
        JASPARmap[motifID] = geneID
JASPARmapFile.close()

# read expression file
expr = {}
with open(exprFile, 'r') as exprFile:
    next(exprFile)  # skip header
    for line in exprFile:
        FBID, symbol, youngMedianExpr, oldMedianExpr = line.strip().split('\t')
        expr[FBID] = (symbol, float(youngMedianExpr), float(oldMedianExpr))
exprFile.close()

# read summary file
summaryInfo = {}
with open(summaryFile, 'r') as f:
    header = next(f).strip()  # save header without newline
    for line in f:
        info = line.strip().split('\t')

        # pass thresh for number of genes in group
        if int(info[5]) >= int(N):
            groupName = info[0]
            if groupName not in summaryInfo:
                summaryInfo[groupName] = []
            summaryInfo[groupName].append(info)
f.close()

# now filter summary info by enrichment score and expression
filteredSummaryInfo = {}
scoresToWrite = {}
notFound = []

# summaryInfo[groupName] is a list of lists
for groupName in summaryInfo:
    infoList = summaryInfo[groupName]  # this is a list to which we can append score and expr

    if eThresh == 'NA':
        score = 'NA'
    else:
        score = getEnrichmentScore(groupName, scores)

    # filter by score; print if NA, because this means we are not filtering by score
    if score == 'NA' or score >= float(eThresh):
        # now filter each line by expression
        for info in infoList:
            # first get the gene ID corresponding to the motifID
            motifID = info[1]
            # don't want to split off cnc14_1 form
            if 'FB' in motifID:
                motifID = motifID.split('_')[0]
            if motifID in expr:
                exprValYoung = expr[motifID][1]
                exprValOld = expr[motifID][2]
            elif motifID in FBIDmap:
                exprValYoung = expr[FBIDmap[motifID]][1]
                exprValOld = expr[FBIDmap[motifID]][2]
            elif motifID in JASPARmap:
                exprValYoung = expr[JASPARmap[motifID]][1]
                exprValOld = expr[JASPARmap[motifID]][2]

            # this is a pseudogene; exclude as if it doesn't pass expr thresh by setting expr to 0.0
            elif motifID == 'FBgn0051782':
                exprValYoung = 0.0
                exprValOld = 0.0
            else:
                notFound.append(motifID)

            # checking both ages here so we can write both to the output file
            if exprValYoung >= float(exprThresh) or exprValOld >= float(exprThresh):
                info.extend([str(score), str(exprValYoung), str(exprValOld)])
                if groupName not in filteredSummaryInfo:
                    filteredSummaryInfo[groupName] = []
                filteredSummaryInfo[groupName].append(info)

notFound = set(notFound)
if len(notFound) != 0:
    print 'These IDs not found:'
    print notFound

# now write outfile
outbase = summaryFile.replace('.txt', '')

if eThresh != 'NA':
    eThresh = str(round(float(eThresh), 2))

outfile = outbase + '_eScore' + eThresh + '_' + exprThresh + 'FPKM_N' + N + '.txt'

with open(outfile, 'w') as outfile:
    outfile.write(header + '\tenrichmentScore\tyoungExpr\toldExpr\n')
    for groupName in filteredSummaryInfo:
        for line in filteredSummaryInfo[groupName]:
            outfile.write('\t'.join(line) + '\n')
outfile.close()
