# rmf 4.21.2020, last modified 4.22.2020

import sys, re

usage = 'python ' + sys.argv[0] + ' <file list of fimo results>'
if len(sys.argv) != 2 or '-h' in sys.argv or '--help' in sys.argv:
    print(usage)
    sys.exit()

# SUBROUTINES
def readGFFfile(fimoGFF, motifs, pattern):
    with open(fimoGFF, 'r') as f:
        next(f)  # skip header
        for line in f:
            geneID, source, gffType, start, stop, score, strand, frame, attributes = line.strip().split('\t')
            match = pattern.search(attributes)
            motifID = match.group(1)
            pval = match.group(2)
            motifSeq = match.group(3)
            if motifID not in motifs:
                motifs[motifID] = []
            motifs[motifID].append((geneID,motifSeq,start,stop,strand,pval))
    f.close()
    return motifs

# ARGUMENTS and MAIN
fileList = sys.argv[1] # fimo file list

# read file list
motifs = {}
pattern = re.compile('Name=(.*?);.*?pvalue=(.*?);sequence=(.*?);')
with open(fileList,'r') as F:
    for line in F:
        fimoGFF = line.strip()
        motifs = readGFFfile(fimoGFF, motifs, pattern)
F.close()

# write output file
outfile = open('fimoResultsSummary.txt','w')
outfile.write('#motifID\tgeneID\tsequence\tstart\tstop\tstrand\tpval\n') # write header
for motifID in motifs:
    for info in motifs[motifID]:
        geneID, motifSeq, start, stop, strand, pval = info
        outfile.write(motifID+'\t'+geneID+'\t'+motifSeq+'\t'+start+'\t'+stop+'\t'+strand+'\t'+pval+'\n')
outfile.close()
