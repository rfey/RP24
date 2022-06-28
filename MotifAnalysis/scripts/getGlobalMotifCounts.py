# rmf 5.4.2020, last modified 5.20.2020

import sys

usage = 'python ' + sys.argv[0] + ' <filtered fimo file>'
if len(sys.argv) != 2 or '-h' in sys.argv or '--help' in sys.argv:
    print(usage)
    sys.exit()

fimoFile = sys.argv[1]

outbase = '_'.join(fimoFile.split('_')[1:]).split('.')[0]
outfile = open('fimoGlobalMotifCounts_' + outbase + '.txt','w')

globalCounts = {}
with open(fimoFile,'r') as f:
    next(f)  # skip header
    for line in f:
        motifID, geneID, pval = line.strip().split('\t')
        if motifID not in globalCounts:
            globalCounts[motifID] = []
        if geneID not in globalCounts[motifID]:
            globalCounts[motifID].append(geneID)
f.close()

outfile.write('#motifID\tglobalCount(K)\n')
for motifID in globalCounts:
    outfile.write(motifID+'\t'+str(len(globalCounts[motifID]))+'\n')
outfile.close()
    
