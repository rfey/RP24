# rmf 4.30.2020, last modified 11.17.2020
# cleaned up 3.2.2022

import sys
import matplotlib as mpl
mpl.use('Agg')
from matplotlib import pyplot as plot
import numpy as np
from scipy import stats
import StringIO

usage = 'python ' + sys.argv[0] + ' <ELCs rhythmicity file> <RLCs rhythmicity file> <LLCs rhythmicity file>'
if len(sys.argv) != 4 or '-h' in sys.argv or '--help' in sys.argv:
    print(usage)
    sys.exit()

# SUBROUTINES
def readInfile(infile):
    youngRP24s,oldRP24s = [],[]
    with open(infile,'r') as infile:
        next(infile)  # skip header
        for line in infile:
            info = line.strip().split('\t')
            youngRP24s.append(float(info[6]))
            oldRP24s.append(float(info[7]))
    infile.close()
    return youngRP24s,oldRP24s

# ARGUMENTS and MAIN
infile1 = sys.argv[1] # ELCs
infile2 = sys.argv[2] # RLCs
infile3 = sys.argv[3] # LLCs

youngRP24sELCs,oldRP24sELCs = readInfile(infile1)
youngRP24sRLCs,oldRP24sRLCs = readInfile(infile2)
youngRP24sLLCs,oldRP24sLLCs = readInfile(infile3)

# perform KS test
youngPval = stats.ks_2samp(youngRP24sELCs,youngRP24sRLCs)[1] # ELCs vs RLCs young
print('ELCs vs RLCs young p-value= '+str(youngPval)+' (KS test)')
oldPval = stats.ks_2samp(oldRP24sRLCs,oldRP24sLLCs)[1]  # RLCs vs LLCs old
print('RLCs vs LLCs old p-value= '+str(oldPval)+' (KS test)')

# format pvalue for legend label
youngLabel = StringIO.StringIO()
youngLabel.write("KS p-value = %.3g" % youngPval)
oldLabel = StringIO.StringIO()
oldLabel.write("KS p-value = %.3g" % oldPval)

# prep for plotting
allData = youngRP24sELCs + youngRP24sRLCs + oldRP24sRLCs + oldRP24sLLCs
binWidth = 0.10
bins = np.arange(min(allData), max(allData)+binWidth, binWidth)

# plot young ELCs vs RLCs
# default: figure.figsize: [6.4, 4.8]
plot.figure(figsize=(6.4,2.4))
plot.hist(youngRP24sELCs,color='red',alpha=0.5,bins=bins,label='ELCs')
plot.hist(youngRP24sRLCs,color='purple',alpha=0.5,bins=bins,label='RLCs')
plot.hist([],color='white',label=youngLabel.getvalue())
plot.xlabel('$log_2$(RP24) in young flies')
plot.ylabel('Number of Transcripts')
plot.title('Transcripts Rhythmic in Young')
plot.legend()
plot.tight_layout()
plot.savefig('transcriptsRhythmicInYoung.pdf')
plot.clf()


# plot old RLCs vs LLCs
plot.figure(figsize=(6.4,2.4))
plot.hist(oldRP24sRLCs,color='purple',alpha=0.5,bins=bins,label='RLCs')
plot.hist(oldRP24sLLCs,color='blue',alpha=0.5,bins=bins,label='LLCs')
plot.hist([],color='white',label=oldLabel.getvalue())
plot.title('Transcripts Rhythmic in Old')
plot.xlabel('$log_2$(RP24) in old flies')
plot.ylabel('Number of Transcripts')
plot.legend()
plot.tight_layout()
plot.savefig('transcriptsRhythmicInOld.pdf')
