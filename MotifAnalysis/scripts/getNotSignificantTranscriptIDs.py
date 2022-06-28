# rmf 4.19.2021

import sys, os

usage = 'python ' + sys.argv[0] + ' <significant transcript ID file> <all transcript IDs file>'
if len(sys.argv) != 3 or '-h' in sys.argv or '--help' in sys.argv:
    print usage
    exit()

# ARGUMENTS and MAIN
sigTranscriptsFile = sys.argv[1]
allTranscriptsFile = sys.argv[2]

allTranscripts = []
with open(allTranscriptsFile, 'r') as f:
    next(f)
    for line in f:
        info = line.strip().split('\t')
        transcriptID = info[0]
        symbol = info[1]
        allTranscripts.append((transcriptID, symbol))
f.close()

sigTranscripts = {}
with open(sigTranscriptsFile, 'r') as F:
    next(F)
    for line in F:
        transcriptID, transcriptSymbol, motifID, motifSymbol = line.strip().split('\t')
        if (motifID, motifSymbol) not in sigTranscripts:
            sigTranscripts[(motifID, motifSymbol)] = []
        sigTranscripts[(motifID, motifSymbol)].append((transcriptID, transcriptSymbol))
F.close()

# get not significant transcripts for each motif
notSig = {}
for ID in allTranscripts:
    for motif in sigTranscripts:
        if ID not in sigTranscripts[motif]:
            if motif not in notSig:
                notSig[motif] = []
            notSig[motif].append(ID)


# write outfile
out = os.path.basename(sigTranscriptsFile)
outfile = open(out.replace('significant', 'noSignificant'), 'w')

outfile.write('#transcriptID\ttranscriptSymbol\tmotifID\tmotifSymbol\n') 
for motif in notSig:
    motifID, motifSymbol = motif
    for transcript in notSig[motif]:
        transcriptID, symbol = transcript
        outfile.write(transcriptID + '\t' + symbol + '\t' + motifID + '\t' + motifSymbol + '\n')
outfile.close()
