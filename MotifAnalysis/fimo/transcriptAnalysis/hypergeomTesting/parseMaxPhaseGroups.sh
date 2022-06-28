# rmf 4.30.2021, last modified 5.17.2021
# cleaned up 3.1.2022

awk 'NR > 1 {print $2}' R2A_youngPhases20.0to24.0.txt > ELCs_youngPhase20to24_transcriptList.txt

awk 'NR > 1 {print $2}' R2R_youngPhases20.0to24.0.txt > RLCs_youngPhase20to24_transcriptList.txt

awk 'NR > 1 {print $2}' R2R_oldPhases21.0to1.0.txt > RLCs_oldPhase21to1_transcriptList.txt

awk 'NR > 1 {print $2}' A2R_oldPhases2.0to6.0.txt > LLCs_oldPhase2to6_transcriptList.txt
