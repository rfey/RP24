# rmf 9.21.2020, last modified 4.14.2021
# cleaned up 3.2.2022

# RP24
# young RLCs
python ../../../../scripts/applyTtestRP24.py geneGroupFile_young.txt transcripts_significantSites_DAVID_RLCs_transcriptGroups0.05_Cluster7_locomotor_rhythm.txt DAVID_RLCs_transcriptGroups0.05_Cluster7_locomotor_rhythm_transcriptIDs.txt youngRLCs

python ../../../../scripts/applyTtestRP24.py geneGroupFile_young.txt transcripts_significantSites_DAVID_RLCs_transcriptGroups0.05_Cluster13_Removed_in_mature_form.txt DAVID_RLCs_transcriptGroups0.05_Cluster13_Removed_in_mature_form_transcriptIDs.txt youngRLCs

python ../../../../scripts/applyTtestRP24.py geneGroupFile_young.txt transcripts_significantSites_DAVID_RLCs_transcriptGroups0.05_Cluster11_RmlC-like_jelly_roll_fold.txt DAVID_RLCs_transcriptGroups0.05_Cluster11_RmlC-like_jelly_roll_fold_transcriptIDs.txt youngRLCs

# old RLCs
python ../../../../scripts/applyTtestRP24.py geneGroupFile_old.txt transcripts_significantSites_DAVID_RLCs_transcriptGroups0.05_Cluster7_locomotor_rhythm.txt DAVID_RLCs_transcriptGroups0.05_Cluster7_locomotor_rhythm_transcriptIDs.txt oldRLCs 

python ../../../../scripts/applyTtestRP24.py geneGroupFile_old.txt transcripts_significantSites_DAVID_RLCs_transcriptGroups0.05_Cluster13_Removed_in_mature_form.txt DAVID_RLCs_transcriptGroups0.05_Cluster13_Removed_in_mature_form_transcriptIDs.txt oldRLCs

python ../../../../scripts/applyTtestRP24.py geneGroupFile_old.txt transcripts_significantSites_DAVID_RLCs_transcriptGroups0.05_Cluster11_RmlC-like_jelly_roll_fold.txt DAVID_RLCs_transcriptGroups0.05_Cluster11_RmlC-like_jelly_roll_fold_transcriptIDs.txt oldRLCs

# old LLCs
python ../../../../scripts/applyTtestRP24.py geneGroupFile_old.txt transcripts_significantSites_DAVID_LLCs_transcriptGroups0.05_Cluster12_Biosynthesis_of_antibiotics.txt DAVID_LLCs_transcriptGroups0.05_Cluster12_Biosynthesis_of_antibiotics_transcriptIDs.txt oldLLCs

python ../../../../scripts/applyTtestRP24.py geneGroupFile_old.txt transcripts_significantSites_DAVID_LLCs_transcriptGroups0.05_Cluster18_calcium_ion-regulated_exocytosis_of_neurotransmitter.txt DAVID_LLCs_transcriptGroups0.05_Cluster18_calcium_ion-regulated_exocytosis_of_neurotransmitter_transcriptIDs.txt  oldLLCs

python ../../../../scripts/applyTtestRP24.py geneGroupFile_old.txt transcripts_significantSites_DAVID_LLCs_transcriptGroups0.05_Cluster4_Pleckstrin_homology-like_domain.txt DAVID_LLCs_transcriptGroups0.05_Cluster4_Pleckstrin_homology-like_domain_transcriptIDs.txt oldLLCs

python ../../../../scripts/applyTtestRP24.py geneGroupFile_old.txt transcripts_significantSites_DAVID_LLCs_transcriptGroups0.05_Cluster6_calcium_ion_transmembrane_transport.txt DAVID_LLCs_transcriptGroups0.05_Cluster6_calcium_ion_transmembrane_transport_transcriptIDs.txt oldLLCs

python ../../../../scripts/applyTtestRP24.py geneGroupFile_old.txt transcripts_significantSites_DAVID_LLCs_transcriptGroups0.05_Cluster9_Zinc_finger_LIM-type.txt DAVID_LLCs_transcriptGroups0.05_Cluster9_Zinc_finger_LIM-type_transcriptIDs.txt oldLLCs

# LLCs phase 2-6
python ../../../../scripts/applyTtestRP24.py geneGroupFile_old.txt transcripts_significantSites_LLCs_phase2to6.txt LLCs_phase2to6_transcriptIDs.txt oldLLCs
