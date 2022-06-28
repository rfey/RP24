# rmf 12.4.2020, last modified 3.20.2021

# INPUT: flybase FBID to annotation tsv file
# OUTPUT: tab delim ID map file
# GOAL: writes file to allow conversion of flybase secondary FBgnIDs or CG number to current gene symbol

import sys

# USAGE
usage = 'python ' + sys.argv[0] + ' <Dmel fbgn_annotation_ID_*.tsv>'
details = 'Writes file to allow conversion of flybase secondary FBgnIDs or CG number to current gene symbol.'
if len(sys.argv) != 2 or '-h' in sys.argv:
    print(usage)
    if '--help' in sys.argv:
        print(details)
    sys.exit()

# ARGUMENTS and MAIN
tsvFile = sys.argv[1]  # the file must be for Dmel only, otherwise add a control statement filtering on organism abbreviation

outbase = tsvFile.replace('fbgn_annotation_ID_','').replace('.tsv','')
outfile = 'secondaryIDsFile_' + outbase + '.txt'

# read tsv file
# we want to be able to convert any secondary ID to current gene symbol
# we'll make a dict keyed by each alternate ID, with the val == current flybase geneID
geneIDs = {}
repeatIDs = []
with open(tsvFile, 'r') as F:
    for line in F:
        # make sure it's not a header and it's not blank
        if '#' not in line and line != '\n':
            info = line.strip().split('\t')  # current gene symbol, organism abbreviation, current FBgnID, secondary FBgnIDs
            currentFBgnID = info[2]
            # store alternate gene IDs in a single list
            altIDs = []
            # go through all secondary flybase geneIDs  ### NOT symbols ###
            # get comma-separated IDs into a list for storage
            if ',' in info[3]:
                IDlist = info[3].split(',')
                altIDs.extend(IDlist)
            # don't store empty string
            elif info[3] != '':
                # store single IDs
                altIDs.append(info[3])
            # now define dict keyed by these alt IDs
            for altID in altIDs:
                if altID not in geneIDs or altID == 'FBgn0050420':
                    # this is Atf-2
                    if altID == 'FBgn0050420':
                        geneIDs[altID] = 'FBgn0265193'
                    else:
                        geneIDs[altID] = currentFBgnID
                else:
                    print('Duplicate IDs! ID ' + altID + ' listed in tsv file more than once.')
                    repeatIDs.append(altID)
F.close()

# delete dict keys that do not uniquely map to current FBgnIDs
print 'Deleting the following repeated alternate IDs:'
repeatIDs = set(repeatIDs)
for ID in repeatIDs:
    print ID
    del geneIDs[ID]

# go through ID dict and write map file
# this will be a tab delim file with each alternate ID on its own line in col 1
# second col will be the current FB geneID

with open(outfile, 'w') as outfile:
    outfile.write('#alternateID\tcurrentFBgnID\n')  # write header
    for altID in geneIDs:
        outfile.write(altID + '\t' + geneIDs[altID] + '\n')
outfile.close()
