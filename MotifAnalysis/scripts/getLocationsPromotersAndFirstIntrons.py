# rmf 2.7.2020, last modified 4.8.2020
# cleaned up on 2.28.2022

import sys, re

# USAGE
usage = '\npython ' + sys.argv[0] + ' <GTF file> <window>\n'
if len(sys.argv) != 3 or '-h' in sys.argv:
    print usage
    if '--help' in sys.argv:
        print 'Promoters defined as region upstream of the TSS (defined by the window arg) as well as the first annotated intron.\n'
    sys.exit()

# ARGUMENTS and MAIN
gtf = open(sys.argv[1],'r')
window = int(sys.argv[2])

info = {}
info['+'] = {}
info['-'] = {}
pattern = re.compile('transcript_id "(.*?)"; transcript_symbol "(.*?)";')
next(gtf)
for line in gtf:
    chrom, source, feature, start, stop, score, strand, frame, attributes = line.strip().split('\t')
    strandCheck = (strand == '+' or strand == '-')
    featureCheck = (feature == 'mRNA')
    # key by mRNA info
    if strandCheck and featureCheck:
        match = pattern.search(attributes)
        ID = match.group(1)
        symbol = match.group(2)
        name = ID + ';' + symbol + ';' + chrom
        # check that ID is in user-input list
        if name not in info:
            info[strand][name] = []
    # store location of exons corresponding to mRNA IDs
    if feature == 'exon':
        if ID in attributes:
            # need this so we don't store tRNA exons and the like
            if name in info[strand]:
                info[strand][name].append((int(start),int(stop)))

# sort exons by start position in case they are not in the right order in the gtf file
for name in info['+']:
    info['+'][name].sort(key=lambda x:x[0])
for name in info['-']:
    info['-'][name].sort(key=lambda x:x[0], reverse=True)  # sort in reverse for minus strand

# NOTE that coordinates are adjusted to 0-based as they are stored in the code below
locs = {}
locs['+'] = {}
locs['-'] = {}
for name in info['+']:
    if name not in locs['+']:
        locs['+'][name] = []
    e1Start,e1Stop = info['+'][name][0] # 1st exon coords
    promoter = (e1Start - window, e1Start) # get region upstream of TSS start
    locs['+'][name].append(promoter)
    # to exclude cases with only one exon and no introns
    if len(info['+'][name]) > 2:
        e2Start,e2Stop = info['+'][name][1] # 2nd exon coords
        intron1 = (e1Stop + 1, e2Start)
        locs['+'][name].append(intron1)

for name in info['-']:
    if name not in locs['-']:
        locs['-'][name] = []
    e1Start,e1Stop = info['-'][name][0] # 1st exon coords
    promoter = (e1Stop + 1, e1Stop + 1 + window) # get region upstream of TSS start
    locs['-'][name].append(promoter)
    # to exclude cases with only one exon and no introns
    if len(info['-'][name]) > 1: 
        e2Start,e2Stop = info['-'][name][1] # 2nd exon coords
        intron1 = (e2Stop + 1, e1Start)
        locs['-'][name].append(intron1)

# write outfile
outfile = open('transcriptPromoterAndFirstIntronLocs' + str(window) + 'bp.txt','w')
outfile.write('#transcriptID\ttranscriptSymbol\tchrom\tstrand\tpositions\n')
for strand in locs:
    for name in locs[strand]:
        ID,symbol,chrom = name.split(';')
        coords = ''
        for i in range(0,len(locs[strand][name])):
            start,stop = locs[strand][name][i]
            if i != len(locs[strand][name]) - 1:
                coords += str(start) + ':' + str(stop) + ','
            else:
                coords += str(start) + ':' + str(stop)
        outfile.write(ID + '\t' + symbol + '\t' + chrom + '\t' + strand + '\t' + coords + '\n')
