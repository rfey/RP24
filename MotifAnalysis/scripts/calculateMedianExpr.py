# rmf 4.22.2020, last modified 4.28.2020

import sys, re
import numpy as np

usage = 'python ' + sys.argv[0] + ' <GTF file> <expr file list>'
if len(sys.argv) != 3 or '-h' in sys.argv or '--help' in sys.argv:
    print(usage)
    sys.exit()

# SUBROUTINES
def readExpressionFile(exprFile,expr):
    with open(exprFile,'r') as exprFile:
        next(exprFile)  # skip header
        for line in exprFile:
            FBID, ZT0, ZT4, ZT8, ZT12, ZT16, ZT20 = line.strip().split('\t')
            vals = [float(ZT0),float(ZT4),float(ZT8),float(ZT12),float(ZT16),float(ZT20)]
            if FBID not in expr:
                expr[FBID] = []
            expr[FBID].extend(vals)
    exprFile.close()
    return expr

# ARGUMENTS and MAIN
gtfFile = sys.argv[1]
exprFileList = sys.argv[2]

if 'transcript' in exprFileList:
    pattern = re.compile('transcript_id "(.*?)";.*?transcript_symbol "(.*?)";')
    feature = 'mRNA'
    outfile = open('transcriptMedianExpression.txt','w')
elif 'gene' in exprFileList:
    pattern = re.compile('gene_id "(.*?)";.*?gene_symbol "(.*?)";')
    feature = 'gene'
    outfile = open('geneMedianExpression.txt','w')
else:
    print('File name error: file name must contain "transcript" or "gene" designation.')

# read GTF file
transcripts = {}
with open(gtfFile,'r') as gtf:
    next(gtf)
    for line in gtf:
        chrom, source, gtfType, start, stop, score, strand, frame, attributes = line.strip().split('\t')
        if gtfType == feature:
            match = pattern.search(attributes)
            transcriptID = match.group(1)
            symbol = match.group(2)
            if transcriptID not in transcripts:
                transcripts[transcriptID] = symbol
gtf.close()

# read expression files
expr = {}
expr['young'] = {}
expr['old'] = {}
with open(exprFileList,'r') as F:
    for line in F:
        exprFile = line.strip()  # remove newline
        if 'young' in exprFile:
            expr['young'] = readExpressionFile(exprFile,expr['young'])
        elif 'old' in exprFile:
                expr['old'] = readExpressionFile(exprFile,expr['old'])
        else:
            print('Check name of expression file ' + exprFile + ': should include "young" or "old".\n')
F.close()

# get median expression for all transcripts
# write to outfile as you go
outfile.write('#FBID\tsymbol\tyoungMedianExpr\toldMedianExpr\n')
for FBID in transcripts:
    symbol = transcripts[FBID]
    if FBID in expr['young']:
        yMedian = np.median(expr['young'][FBID])
    else:
        yMedian = 0.0
    if FBID in expr['old']:
        oMedian = np.median(expr['old'][FBID])
    else:
        oMedian = 0.0
    outfile.write(FBID+'\t'+symbol+'\t'+str(yMedian)+'\t'+str(oMedian)+'\n')
outfile.close()

