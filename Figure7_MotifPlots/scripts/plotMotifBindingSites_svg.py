# rmf 7.2.2020, last modified 4.14.2021
# cleaned up 3.1.2022

import sys, re
import svgwrite as svg
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plot
import matplotlib._color_data as mcd

# FUNCTION: plots promoter and first intron, with any binding sites, for all transcripts in the group of interest; one plot per motif instance

# USAGE
usage = 'python ' + sys.argv[0] + ' <binding site file> <GOI list file> <promoter loc file> <xscale> <yscale>'
if len(sys.argv) != 6 or '-h' in sys.argv or '--help' in sys.argv:
    print(usage)
    sys.exit()

# SUBROUTINES
def splitTranscriptsBySignificance(allTranscripts, sites, motif):
    sig, notsig = [],[]
    sites_filtered = {}
    for transcript in allTranscripts:
        for bindingSite in sites[transcript]:
            # make sure the binding site is for the motif we are checking
            if bindingSite[0] == motif:
                if transcript not in sig:
                    sig.append(transcript)
                if transcript not in sites_filtered:
                    sites_filtered[transcript] = []
                sites_filtered[transcript].append(bindingSite)
    for transcript in allTranscripts:
        if transcript not in sig:
            if transcript not in notsig:
                notsig.append(transcript)
    return sig, notsig, sites_filtered

def plotBindingSites(xscale, yscale, promoters, geneIDs, outfile, sites):

    print motif  # don't know why this works-- not passed into subroutine, not defined

    # initialize variables
    lineSize = 32  # height of grey rectangle that represents promoter region and first intron
    siteSize = 32  # base of triangle
    ySpacer = 20
    labelSpace = 1000 # amount of space for geneID label
    TSSspacer = 250  # white space between end of promoter region and beginning of first intron
    labelInsert = 50  # space between edge of image and geneID label
    middleElipse = TSSspacer/2
    elipseSpacer = 20  # amount of whitespace between elipse points
    elipses = [(middleElipse-elipseSpacer),(middleElipse),(middleElipse+elipseSpacer)]
    escale = max(xscale,yscale)
    triangleHeight = (ySpacer+(lineSize/2))*4
    numSpacers = 3

    xvalLegendStart = 350
    yvalLegendStart = 50
    legendBoxWidth = 64  # these are used to place legend labels
    legendBoxHeight = 32
    color = 'green'

    # scales are user-input arguments
    maxIntron = max(promoters.values())
    numGenes = len(geneIDs)
    imgHeight = ((1 + numGenes) * ((ySpacer*numSpacers)+lineSize)) + yvalLegendStart
    imgWidth = labelSpace+6000+maxIntron+TSSspacer+50
    img = svg.Drawing(outfile,size=(imgWidth*xscale,imgHeight*yscale)) # default unit is pixels

    # draw legend
    y = yvalLegendStart + 5 + (ySpacer*numSpacers) # this is the downward point of the triangle
    x1_Triangle = xvalLegendStart - 2*triangleHeight # this is the left top corner of the base
    x2_Triangle = xvalLegendStart + 2*triangleHeight # this is the right top corner of the base
    y_Triangle = y - ySpacer - lineSize + 5 # this is the base of the triangle
    points = [[xvalLegendStart*xscale,y*yscale],[x1_Triangle*xscale,y_Triangle*yscale],[x2_Triangle*xscale,y_Triangle*yscale]]
    img.add(svg.shapes.Polygon(points=points,fill=color,stroke=svg.rgb(10, 10, 16, '%')))
    img.add(img.text(motif,insert=((xvalLegendStart+legendBoxWidth+(legendBoxWidth*2))*xscale,y*yscale),font_size=48*yscale))

    # draw promoters and binding sites
    ytickPos,ytickLabels = [],[]
    legendHeight = yvalLegendStart + ((ySpacer*2)+legendBoxHeight)
    numGenes = 0
    for geneID in geneIDs:
        if geneID in promoters:
            intronLen = promoters[geneID]
            y = legendHeight + (((numSpacers*ySpacer) + lineSize)*numGenes)
            # draw promoter region
            img.add(svg.shapes.Rect(insert=(labelSpace*xscale,y*yscale),size=(6000*xscale,lineSize*yscale),fill='grey',opacity=0.5))
            # add geneID as label
            ylabel = y + (lineSize/2)
            img.add(img.text(geneID,insert=(labelInsert*xscale,ylabel*yscale+lineSize),font_size=36*yscale))

            # draw TSS symbol
            y_TSS = y - lineSize
            x_TSS = labelSpace+6000
            TSS_line = lineSize*yscale
            lineThickness = 10
            img.add(svg.shapes.Rect(insert=(x_TSS*xscale,y_TSS*yscale),size=(lineThickness*xscale,TSS_line),fill='black'))  # verticle line
            img.add(svg.shapes.Rect(insert=(x_TSS*xscale,y_TSS*yscale),size=(TSS_line,lineThickness*xscale),fill='black'))  # horizontal line
            x_arrow = x_TSS+TSS_line
            y_arrow = y_TSS
            points = [[(x_arrow+40)*xscale,y_arrow*yscale],[x_arrow*xscale,(y_arrow-10)*yscale],[x_arrow*xscale,(y_arrow+10)*yscale]] # leading point of arrowhead listed first
            img.add(svg.shapes.Polygon(points=points,fill='black',stroke=svg.rgb(10, 10, 16, '%')))  # arrowhead

            # add elipses, spacer and intron if there is an intron
            if intronLen != 0:
                # spacer btwn promoter and intron
                img.add(svg.shapes.Rect(insert=((6000+labelSpace)*xscale,y*yscale),size=(TSSspacer*xscale,lineSize*yscale),fill='white')) 
                img.add(svg.shapes.Rect(insert=((6000+labelSpace+TSSspacer)*xscale,y*yscale),size=(intronLen*xscale,lineSize*yscale),fill='grey',opacity=0.5))

                # elipses
                img.add(svg.shapes.Circle(center=((6000+labelSpace+elipses[0])*xscale,(y+(lineSize/2))*yscale),r=3,fill='black'))
                img.add(svg.shapes.Circle(center=((6000+labelSpace+elipses[1])*xscale,(y+(lineSize/2))*yscale),r=3,fill='black'))
                img.add(svg.shapes.Circle(center=((6000+labelSpace+elipses[2])*xscale,(y+(lineSize/2))*yscale),r=3,fill='black'))
        
            # draw a triangle for each binding site
            # don't want to try to do this for genes without binding sites
            if geneID in sites:
                for site in sites[geneID]:
                    motifSymbol, pval, start, stop, strand, seq = site  # this motifSymbol is the unformatted version
                    seqLen = stop-start  
                    siteStart = y + (lineSize/2)
                    # if it is in the first intron
                    if start > 6000 and stop > 6000:
                        x = labelSpace+start+TSSspacer
                        x1_Triangle = x - triangleHeight
                        x2_Triangle = x + triangleHeight
                        if strand == '+':
                            y_Triangle = y - ySpacer
                            points = [[x*xscale,siteStart*yscale],[x1_Triangle*xscale,y_Triangle*yscale],[x2_Triangle*xscale,y_Triangle*yscale]]
                            img.add(svg.shapes.Polygon(points=points,fill=color))
                        elif strand == '-':
                            y_Triangle = y + lineSize + ySpacer
                            points = [[x*xscale,siteStart*yscale],[x1_Triangle*xscale,y_Triangle*yscale],[x2_Triangle*xscale,y_Triangle*yscale]]
                            img.add(svg.shapes.Polygon(points=points,fill=color))
                        else:
                            print 'Invalid strand!', motifSymbol
                            exit()
                    # if it's not in the first intron
                    else:
                        x = labelSpace+start
                        x1_Triangle = x - triangleHeight
                        x2_Triangle = x + triangleHeight
                        if strand == '+':
                            y_Triangle = y - ySpacer
                            points = [[x*xscale,siteStart*yscale],[x1_Triangle*xscale,y_Triangle*yscale],[x2_Triangle*xscale,y_Triangle*yscale]]
                            img.add(svg.shapes.Polygon(points=points,fill=color))
                        elif strand == '-':
                            y_Triangle = y + lineSize + ySpacer
                            points = [[x*xscale,siteStart*yscale],[x1_Triangle*xscale,y_Triangle*yscale],[x2_Triangle*xscale,y_Triangle*yscale]]
                            img.add(svg.shapes.Polygon(points=points,fill=color))
                        else:
                            print 'Invalid strand!', motifSymbol
            numGenes += 1
        else:
            print 'Not in promoter file', geneID
            exit()

    img.save()




# ARGUMENTS and MAIN
bindingSiteFile = sys.argv[1]
GOIlistFile = sys.argv[2]
promoterLocFile = sys.argv[3]
xscale = float(sys.argv[4])
yscale = float(sys.argv[5])

outbase = bindingSiteFile.replace('bindingSiteInfo_','').replace('.txt','')

# read GOI list file
# initialize dict to store binding site info here
sites = {}
geneIDs = []
with open(GOIlistFile, 'r') as gFile:
    for line in gFile:
        if '#' not in line:
            transcriptSymbol = line.strip()
            if transcriptSymbol not in sites:
                sites[transcriptSymbol] = []
            geneIDs.append(transcriptSymbol)
gFile.close()
print 'Stored', len(geneIDs), 'transcript IDs...'

# read binding site file
# add binding site info to dict initialized above
motifSymbol2ID = {}
with open(bindingSiteFile,'r') as f:
    next(f)
    for line in f:
        motifID, motifSymbol, pval, geneID, start, stop, strand, bindingSequence = line.strip().split('\t')
        if geneID not in sites.keys():
            print geneID
            sys.exit()
        sites[geneID].append((motifSymbol,float(pval),int(start),int(stop),strand,bindingSequence))

        # this will overwrite for dimers, but we will not access it for dimers so it should be fine                                                                 
        if motifSymbol not in motifSymbol2ID:
            motifSymbol2ID[motifSymbol] = motifID
f.close()


# we now have a dict of binding site info keyed by gene ID
# some gene ID vals will be an empty list (no significant binding sites)
# we also have a list of geneIDs with significant binding sites (used for ordering later)

# read promoter and first intron location info
# only save for our genes of interest
promoters = {}
with open(promoterLocFile,'r') as promoterLocFile:
    next(promoterLocFile)
    for line in promoterLocFile:
        transcriptID, transcriptSymbol, chrom, strand, positions = line.strip().split('\t')
        if transcriptSymbol in sites:
            intronPosList = positions.split(',')
            if len(intronPosList) > 1:
                intronStart,intronStop = intronPosList[1].split(':')
                intronLen = int(intronStop) - int(intronStart)
            else:
                intronLen = 0
            promoters[transcriptSymbol] = intronLen
promoterLocFile.close()

# one plot per motif
for motif in motifSymbol2ID:
    sig, notsig, sites_filtered = splitTranscriptsBySignificance(geneIDs, sites, motif)

    # sort geneIDs by intron length, longest first
    # do for each subset
    sig.sort(key = lambda x:promoters[x], reverse = True)
    notsig.sort(key = lambda x:promoters[x], reverse = True)

    # redefine the list with all gene IDs to be these two sorted lists together
    # we will plot significant then not significant, each sorted by intron length
    geneIDs = sig + notsig

    # sort sites by pval
    for transcriptID in sites_filtered:
        sites_filtered[transcriptID].sort(key=lambda x:x[1])

    outfile = 'motifBindingSitesPlot_' + motifSymbol2ID[motif] + '_' + outbase + '.svg'
    plotBindingSites(xscale, yscale, promoters, geneIDs, outfile, sites_filtered)


