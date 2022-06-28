# rmf 3.24.2020, last modified 5.13.2021
# cleaned up 3.1.2022

import sys, re

usage = 'python ' + sys.argv[0] + ' <file list of corrected motif enrichment results> <outbase>'
if len(sys.argv) != 3 or '-h' in sys.argv or '--help' in sys.argv:
    print(usage)
    sys.exit()

# SUBROUTINES
def readFile(resultsFile,results,pattern):
    group = pattern.search(resultsFile).group(1)
    with open(resultsFile,'r') as f:
        header = next(f).strip().split('\t')
        for line in f:
            # only want summary info-- not ind. gene IDs
            if '#' in line:
                info = line.strip().split('\t')
                motifID = info[0].replace('#','') # remove hash or won't match dict keys
                info[0] = motifID  # don't want hashes in the final ID

                # add GOI group info
                info.insert(0,group)
                # filter out NO TEST
                results.append(info)
    return results,header

fileList = open(sys.argv[1],'r')
outbase = sys.argv[2]


pattern = re.compile('.*/.*?_(.*?)_BHFDR.*')

results = []
for line in fileList:
    f = line.strip()
    results,header = readFile(f,results,pattern)


outfile = open('motifEnrichmentSummary'+outbase+'.txt','w')

# modify header
header[0] = header[0].replace('#','')
header.insert(0,'#GOIgroup')

outfile.write('\t'.join(header) + '\n')
for result in results:
    outfile.write('\t'.join(result) + '\n')
