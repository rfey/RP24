# rmf 5.28.2019, last modified 11.10.2020

# note that though the python script refers to peak expression, this is actually filtering on phase from the gene group files (output of rhythmicity analysis)
# ZTs are start-inclusive, end-exclusive (ie, phase==ZT12 is included, but phase==ZT24 is excluded from 12-24)

# ELCs
python ../scripts/filterByPeakExpression.py ELCs_q0.05.txt 0-12
python ../scripts/filterByPeakExpression.py ELCs_q0.05.txt 12-24

# RLCs
python ../scripts/filterByPeakExpression.py RLCs_q0.05.txt 0-12
python ../scripts/filterByPeakExpression.py RLCs_q0.05.txt 12-24

# LLCs
python ../scripts/filterByPeakExpression.py LLCs_q0.05.txt 0-12
python ../scripts/filterByPeakExpression.py LLCs_q0.05.txt 12-24
