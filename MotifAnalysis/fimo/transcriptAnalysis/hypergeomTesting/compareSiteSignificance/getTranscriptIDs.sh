#!/bin/bash

# rmf 9.2.2020, last modified 4.19.2021
# cleaned up 3.1.2022

for f in ../bindingSitePlots/bindingSiteInfo*.txt; do python3 ../../../../scripts/getTranscriptIDsFor2Dplots.py ../../dmel-all-r6.21.gtf $f; done

