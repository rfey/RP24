# rmf 12.21.2020, last modified 9.20.2020

import sys, re

# FUNCTION: extract enrichment score associated with each cluster and write to outfile
# INPUT: file with list of parsed DAVID files
# OUTPUT: tab delim file cluster name and enrichment score

usage = 'python ' + sys.argv[0] + ' <fileList of parsed DAVID files>'
if len(sys.argv) != 2 or '-h' in sys.argv or '--help' in sys.argv:
    print(usage)
    sys.exit()

# SUBROUTINES
def readDAVIDfile(DAVIDfile):
    scores = {}
    pattern = re.compile('Cluster-(\d*).*enrichmentScore=(\d\.\d*).*phaseStdDev=\d\.\d*(.*)Cluster.*')
    with open(DAVIDfile, 'r') as f:
        for line in f:
            if line.startswith('Cluster'):
                match = pattern.search(line)
                clusterNum = match.group(1).strip()
                score = match.group(2)
                clusterName = match.group(3).strip()
                cluster = 'Cluster_' + clusterNum + ' ' + clusterName
                scores[cluster] = score
    f.close()
    return scores

# ARGUMENTS and MAIN
fileList = sys.argv[1]

# read file with list of DAVID file names
# DAVID_ELCs_transcriptGroups0.05.parse.txt
scores = {}
pattern = re.compile('DAVID_(.LC)_.*')
with open(fileList, 'r') as F:
    for line in F:
        DAVIDfile = line.strip()  # remove newline
        # get group name
        group = pattern.search(DAVIDfile).group(1)
        scores[group] = readDAVIDfile(DAVIDfile)
F.close()

# write outfile
outfile = open('enrichmentScoresTableDAVID.txt', 'w')
outfile.write('#group\tenrichmentScore\tclusterName\n')
for group in scores:
    for cluster in scores[group]:
        score = scores[group][cluster]
        outfile.write(group + '\t' + score + '\t' + cluster + '\n')
outfile.close()
