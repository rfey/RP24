# rmf 4.3.2020

import sys

# USAGE 
usage = 'python ' + sys.argv[0] + ' <fimo.gff> <new prefix>'
if len(sys.argv) != 3 or '-h' in sys.argv or '--help' in sys.argv:
    print(usage)
    sys.exit()

fimoFile = sys.argv[1]
prefix = sys.argv[2]

outpath = '/'.join(fimoFile.split('/')[0:-1])
outfile = open(outpath + '/fimo.gff','w')

with open(fimoFile,'r') as fimoFile:
    for line in fimoFile:
        if 'Name=' in line:
            line = line.replace('Name=','Name='+prefix)
        outfile.write(line)

fimoFile.close()
outfile.close()
