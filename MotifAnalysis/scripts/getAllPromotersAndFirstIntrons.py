# rmf 2.9.2018, last modified 3.16.2020
# cleaned up 2.28.2022

import os, sys
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio.SeqFeature import SeqFeature, FeatureLocation

usage = 'python ' + os.path.basename(__file__) + ' <gene location file> <dm6 genome file> <feature>/n Gets all drosophila genes and writes their promoter and first intron sequences to a fasta file.\nPromoters and introns are concatenated with a linker of 5*(NNNN)\n<feature> is the genomic feature for which you want to get promoters.'
if len(sys.argv) != 4 or '-h' in sys.argv or '--help' in sys.argv:
    print usage
    sys.exit()

def readGeneLocFile(geneLocFile):
    geneLocDict = {}
    with open(geneLocFile,'r') as geneLoc:
        for line in geneLoc:
            if '#' not in line:
                FBID, symbol, chrom, strand, positions = line.strip().split('\t')
                if chrom not in geneLocDict:
                    geneLocDict[chrom] = []
                geneLocDict[chrom].append((FBID, symbol,strand,positions))
    geneLoc.close()
    return geneLocDict

def readGenomeFile(genomeFile):
    genomeDict = {}
    sequences = SeqIO.parse(genomeFile,'fasta')
    for record in sequences:
        if record.id not in genomeDict:
            genomeDict[record.id] = record.seq
    return genomeDict

def getPromoters(geneLocDict,genome):
    promoterDict = {}
    for chrom in genome:
        if chrom in geneLocDict:
            print 'Extracting promoter regions for features in chromosome: ', chrom
            for site in geneLocDict[chrom]:
                ID, symbol, strand, positions = site
                coords = positions.split(',') # should give list of start:stop, start:stop
                promoter = ''
                for coord in coords:
                    start,stop = coord.split(':')
                    sequence = genome[chrom][int(start):int(stop)]
                    if strand == "-":
                        sequence = reverseComplement(sequence)
                    # add linker of NNNNs only if there is already a sequence stored
                    if promoter == '':
                        promoter += sequence
                    else:
                        promoter += 20*'N' + sequence
                if ID not in promoterDict:
                    promoterDict[ID] = (symbol,promoter)
    return promoterDict

def reverseComplement(sequence):
    compDict = {'A':'T','C':'G','G':'C','T':'A','N':'N'}
    comp = ''
    for b in sequence:
        comp += compDict[b]
    return comp[::-1]

def writePromoterFile(promoters,feature,window):
    sequences = []
    for FBID in promoters:
        recordID = promoters[FBID][0] + ' ' + FBID  # symbol + FBID
        promoter = SeqRecord(Seq(str(promoters[FBID][1])),id=recordID)
        sequences.append(promoter)
    SeqIO.write(sequences, "all" + feature + "Promoters" + window + "bpAndFirstIntron.fasta", "fasta")

# ARGUMENTS and MAIN
geneLocFile = sys.argv[1]
genomeFile = sys.argv[2]
feature = sys.argv[3].capitalize() # genomic feature that we're extracting promoters for

print('Reading input files...')
geneLocDict = readGeneLocFile(geneLocFile)
genome = readGenomeFile(genomeFile)

print('Extracting promoter regions...')
promoters = getPromoters(geneLocDict,genome)

# get window for outfile name
key = geneLocDict.keys()[0] # doesn't matter which key (chrom) we get, promoter region length should be the same for each ID for all chroms
start,stop = geneLocDict[key][0][3].split(',')[0].split(':') # get coords for region upstream of the TSS
window = int(stop) - int(start)
print('Writing output fasta file...')
writePromoterFile(promoters,feature,str(window))
