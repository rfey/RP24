# rmf 9.2.2020, last modified 4.21.2021

import sys, re

usage = 'python3 ' + sys.argv[0] + ' <gtf file> <binding site info file>'
details = 'Use python version 3 for encoding unicode characters in string literals.'
if len(sys.argv) != 3 or '-h' in sys.argv or '--help' in sys.argv:
    print(usage)
    print(details)
    sys.exit()

gtfFile = sys.argv[1]
bindingSiteInfoFile = sys.argv[2] # this has transcript symbols with significant motif binding sites
# binding site file only has significant sites, so no need to filter by pvalue

secondaryIDs = {'CG15661-RA':'Ugt49C1-RA','CG17324-RB':'Ugt36F1-RB','CG4302-RA':'Ugt49B1-RA','Ugt35a-RA':'Ugt35A1-RA','Ugt35b-RA':'Ugt35B1-RA','Ugt86Da-RA':'Ugt302C1-RA','CG9507-RA':'Nepl5-RA','CG8481-RA':'Naa80-RA','IM1-RA':'BomS1-RA','AP-1-2beta-RA':'AP-1-2\u03B2-RA','alpha-Est8-RA':'\u03B1-Est8-RA','Atpalpha-RK':'Atp\u03B1-RK','ATPsynbeta-RA':'ATPsyn\u03B2-RA','CdsA-RA':'Cds-RA','Ugt86Di-RA':'Ugt302K1-RA','DIP-alpha-RC':'DIP-\u03B1-RC','beta4GalNAcTB-RA':'\u03B24GalNAcTB-RA','Dgkepsilon-RB':'Dgk\u03B5-RB','ATPsyndelta-RC':'ATPsyn\u03B4-RC','CG7971-RF':'Srrm234-RF','Liprin-gamma-RD':'Liprin-\u03B3-RD','nAChRalpha7-RA':'nAChR\u03B17-RA','Atpalpha-RG':'Atp\u03B1-RG','Atpalpha-RH':'Atp\u03B1-RH','CG3940-RA':'CAH7-RA','CG9413-RC':'sbm-RC','Clect27-RA':'slf-RA','nAChRalpha6-RG':'nAChR\u03B16-RG','su(w[a])-RC':'su(w<up>a</up>)-RC'}

# read gtf file
# we want to key by transcript symbol, so we can access transcript IDs
maps = {}
pattern = re.compile('.*?transcript_id "(.*?)"; transcript_symbol "(.*?)";')
with open(gtfFile, 'r') as gtfFile:
    for line in gtfFile:
        chrom, source, gtfType, start, stop, score, strand, frame, attributes = line.strip().split('\t')
        if gtfType == 'mRNA':
            match = pattern.search(attributes)
            transcriptID = match.group(1)
            transcriptSymbol = match.group(2)
            maps[transcriptSymbol] = transcriptID
gtfFile.close()

# read file with trancsripts with significant binding sites
sigTranscripts = {}
with open(bindingSiteInfoFile, 'r') as f:
    next(f)  # skip header
    for line in f:
        motifID,motifSymbol,pvalue,transcriptSymbol,start,stop,strand,sequence = line.strip().split('\t')
        # retrieve ID associated with symbol
        if transcriptSymbol in maps:
            transcriptID = maps[transcriptSymbol]
        elif transcriptSymbol in secondaryIDs:
            symbol = secondaryIDs[transcriptSymbol]
            transcriptID = maps[symbol]
        else:
            print('Error: Transcript ' + transcriptSymbol + ' not in maps file! Add to secondary ID dict.')
            sys.exit()
        if (motifID, motifSymbol) not in sigTranscripts:
            sigTranscripts[(motifID, motifSymbol)] = []
        # listed once for each binding site, only want to save one instance since we aren't saving site info, just transcript info
        if (transcriptID, transcriptSymbol) not in sigTranscripts[(motifID, motifSymbol)]:
            sigTranscripts[(motifID, motifSymbol)].append((transcriptID, transcriptSymbol))
f.close()


outbase = bindingSiteInfoFile.split('bindingSiteInfo_')[1].replace('_FDR0.05.txt','')
print('Printing IDs for ' + outbase + '...')

outfileSig = open('transcripts_significantSites_' + outbase + '.txt','w')
outfileSig.write('#transcriptID\ttranscriptSymbol\tmotifID\tmotifSymbol\n')
for motif in sigTranscripts:
    motifID, motifSymbol = motif
    for transcript in sigTranscripts[motif]:
        transcriptID, transcriptSymbol = transcript
        outfileSig.write(transcriptID + '\t' + transcriptSymbol + '\t' + motifID + '\t' + motifSymbol + '\n')
outfileSig.close()
