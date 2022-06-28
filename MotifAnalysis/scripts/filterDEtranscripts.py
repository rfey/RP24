# rmf 1.31.2020, last modified 11.4.2020

import sys
import numpy as np

# USAGE 
usage = 'python ' + sys.argv[0] + ' <gene group file> <rhythmic DEG file>'
details = '\nThis may also be run for transcripts: all IDs should be compatible prior to running this script.'
if len(sys.argv) != 3 or '-h' in sys.argv:
    print usage
    if '--help' in sys.argv:
        print details
    sys.exit()

geneList = sys.argv[1]
DEfile = sys.argv[2]

# read list of DE genes
DE = []
with open(DEfile,'r') as f:
    next(f)
    for line in f:
        info = line.strip().split('\t')
        DE.append(info[0])  # store flybase ID
f.close()
print 'Read in ' + str(len(DE)) + ' DE features.'

outbase1 = '.'.join(geneList.split('.')[:-1]) # join all but last element, should remove file ext
if 'upInOld.txt' in DEfile:
    outbase2 = '_upInOld'
elif 'downInOld.txt' in DEfile:
    outbase2 = '_downInOld'
else:
    print('DE file name not compatible! Should have form: A2R_downInOld.txt')
    sys.exit()

outfile = open(outbase1 + outbase2 + '.txt', 'w')

genes = []
with open(geneList,'r') as f:
    header = next(f).strip().split('\t')
    outfile.write('\t'.join(header) + '\n')
    for line in f:
        info = line.strip().split('\t')
        FBID = info[0]
        if FBID in DE:
            outfile.write('\t'.join(info) + '\n')
f.close()
outfile.close()
