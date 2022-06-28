# rmf 1.25.2021, last modified 4.12.2021

# gene ID and symbol, keep header for first one
awk -F '\t' '{print $1 "\t" $2}' ELCs_q0.05_phase0-12.txt > rhythmic_phase0-12_transcriptIDs.txt
awk -F '\t' 'NR >1 {print $1 "\t" $2}' RLCs_q0.05_phase0-12.txt >> rhythmic_phase0-12_transcriptIDs.txt
awk -F '\t' 'NR >1 {print $1 "\t" $2}' LLCs_q0.05_phase0-12.txt >> rhythmic_phase0-12_transcriptIDs.txt

awk -F '\t' '{print $1 "\t" $2}' ELCs_q0.05_phase12-24.txt > rhythmic_phase12-24_transcriptIDs.txt
awk -F '\t' 'NR >1 {print $1 "\t" $2}' RLCs_q0.05_phase12-24.txt >> rhythmic_phase12-24_transcriptIDs.txt
awk -F '\t' 'NR >1 {print $1 "\t" $2}' LLCs_q0.05_phase12-24.txt >>rhythmic_phase12-24_transcriptIDs.txt

cat ELCs_q0.05_phase0-12_transcriptList.txt RLCs_q0.05_phase0-12_transcriptList.txt LLCs_q0.05_phase0-12_transcriptList.txt > rhythmic_phase0-12_transcriptList.txt
cat ELCs_q0.05_phase12-24_transcriptList.txt RLCs_q0.05_phase12-24_transcriptList.txt LLCs_q0.05_phase12-24_transcriptList.txt > rhythmic_phase12-24_transcriptList.txt
