#!/bin/bash

# rmf 2.2.2020, last modified 11.4.2020

# filter against DE transcripts from cuffdiff output

# ELCs down
for f in ELCs*.txt; do echo python ../scripts/filterDEtranscripts.py $f /nfs0/BB/Hendrix_Lab/Drosophila/CircadianRhythms/RNASeq/RP24Analysis/Hisat2AlignmentTranscripts/transcriptGroups_q0.05/upAndDownGenes/R2A_downInOld.txt >> cmd_filterAgainstDEtranscripts.sh; done

# ELCs up
for f in ELCs*.txt; do echo python ../scripts/filterDEtranscripts.py $f /nfs0/BB/Hendrix_Lab/Drosophila/CircadianRhythms/RNASeq/RP24Analysis/Hisat2AlignmentTranscripts/transcriptGroups_q0.05/upAndDownGenes/R2A_upInOld.txt >> cmd_filterAgainstDEtranscripts.sh; done

# RLCs down
for f in RLCs*.txt; do echo python ../scripts/filterDEtranscripts.py $f /nfs0/BB/Hendrix_Lab/Drosophila/CircadianRhythms/RNASeq/RP24Analysis/Hisat2AlignmentTranscripts/transcriptGroups_q0.05/upAndDownGenes/R2R_downInOld.txt >> cmd_filterAgainstDEtranscripts.sh; done

# RLCs up
for f in RLCs*.txt; do echo python ../scripts/filterDEtranscripts.py $f /nfs0/BB/Hendrix_Lab/Drosophila/CircadianRhythms/RNASeq/RP24Analysis/Hisat2AlignmentTranscripts/transcriptGroups_q0.05/upAndDownGenes/R2R_upInOld.txt >> cmd_filterAgainstDEtranscripts.sh; done

# LLCs down
for f in LLCs*.txt; do echo python ../scripts/filterDEtranscripts.py $f /nfs0/BB/Hendrix_Lab/Drosophila/CircadianRhythms/RNASeq/RP24Analysis/Hisat2AlignmentTranscripts/transcriptGroups_q0.05/upAndDownGenes/A2R_downInOld.txt >> cmd_filterAgainstDEtranscripts.sh; done

# LLCs up
for f in LLCs*.txt; do echo python ../scripts/filterDEtranscripts.py $f /nfs0/BB/Hendrix_Lab/Drosophila/CircadianRhythms/RNASeq/RP24Analysis/Hisat2AlignmentTranscripts/transcriptGroups_q0.05/upAndDownGenes/A2R_upInOld.txt >> cmd_filterAgainstDEtranscripts.sh; done

