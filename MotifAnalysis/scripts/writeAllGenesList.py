# rmf 4.22.2020

import sys
from Bio import SeqIO

usage = 'python ' + sys.argv[0] + ' <all promoters fasta file> <outfile name>'
if len(sys.argv) != 3 or '-h' in sys.argv or '--help' in sys.argv:
    print(usage)
    sys.exit()

fastaFile = sys.argv[1]
outfile = sys.argv[2]

allGenes = []
for record in SeqIO.parse(fastaFile,'fasta'):
    allGenes.append(record.id)

# write outfile
outfile = open(outfile,'w')
for geneID in allGenes:
    outfile.write(geneID + '\n')
outfile.close()
