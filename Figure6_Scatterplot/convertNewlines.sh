# rmf 9.24.2021

for f in *InOld.txt; do outbase=${f%%.txt}; perl scripts/mac2unix.pl $f > ${outbase}_cleaned.txt; done