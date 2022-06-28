# rmf 5.28.2019, last modified 10.28.2020
# cleaned up 2.28.2022
import sys, os

usage = '\npython ' + sys.argv[0] + ' <gene group file> <peak expression range>\n'
details = '<gene list file> Output of rhythmicity detection code (ex: ELCs_0.01qval.txt)\n<peak expression> Hyphen-separated range of time points in ZT (ex: 12-20)\n'
if len(sys.argv) != 3 or '-h' in sys.argv:
    print usage
    if '--help' in sys.argv:
        print details
    sys.exit()


# read gene groups file
def readGeneFile(geneGroupFile,i,toWrite):
    with open(geneGroupFile,'r') as f:
        header = next(f).strip().split('\t')  # save header
        for line in f:
            info = line.strip().split('\t')
            phase = float(info[i])
            if float(peakBounds[0]) <= phase < float(peakBounds[1]):
                FBID = info[0]
                # don't write an FBID twice for phase in bounds for both young and old
                if FBID not in toWrite:
                    toWrite[FBID] = info
    f.close()
    return toWrite, header

# ARGUMENTS and MAIN
geneGroupFile = sys.argv[1]
peaks = sys.argv[2]

peakBounds = peaks.split('-')

outbase = geneGroupFile.split('.txt')[0]
outfile = open(outbase + '_phase' + peaks + '.txt','a+')

# get column index
if 'ELC' in geneGroupFile or 'R2A' in geneGroupFile:
    col = [13]
elif 'RLC' in geneGroupFile or 'R2R' in geneGroupFile:
    col = [13,14]
elif 'LLC' in geneGroupFile or 'A2R' in geneGroupFile:
    col = [14]

toWrite = {}
for i in col:
    toWrite, header = readGeneFile(geneGroupFile,i,toWrite)
    print(len(toWrite))


outfile.write('\t'.join(header) + '\n')
for FBID in toWrite:
    outfile.write('\t'.join(toWrite[FBID]) + '\n')
outfile.close()
