#!/bin/bash

# rmf 12.16.2020, last modified 3.6.2021

# ELCs
for f in ../DAVID_outputFiles/DAVID_ELC*_transcriptIDs.txt; do python ../../scripts/processDAVIDclusterGeneLists.py $f ../ELCs_q0.05.txt; done

# RLCs
for f in ../DAVID_outputFiles/DAVID_RLC*_transcriptIDs.txt; do python ../../scripts/processDAVIDclusterGeneLists.py $f ../RLCs_q0.05.txt; done

# LLCs
for f in ../DAVID_outputFiles/DAVID_LLC*_transcriptIDs.txt; do python ../../scripts/processDAVIDclusterGeneLists.py $f ../LLCs_q0.05.txt; done
