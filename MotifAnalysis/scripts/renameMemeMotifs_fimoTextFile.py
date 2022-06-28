# rmf 4.3.2020, last modified 5.12.2020

import sys

# USAGE 
usage = 'python ' + sys.argv[0] + ' <fimo.txt> <new prefix>'
if len(sys.argv) != 3 or '-h' in sys.argv or '--help' in sys.argv:
    print(usage)
    sys.exit()

fimoFile = sys.argv[1]
prefix = sys.argv[2]

outpath = '/'.join(fimoFile.split('/')[0:-1])
outfile = open(outpath + '/fimo.txt','w')

with open(fimoFile,'r') as fimoFile:
    outfile.write(next(fimoFile))
    for line in fimoFile:
        info = line.strip().split('\t')
        info[0] = prefix + info[0]
        outfile.write('\t'.join(info) + '\n')

fimoFile.close()
outfile.close()
