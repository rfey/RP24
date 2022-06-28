#!/bin/bash

# rmf 9.23.2020, last modified 4.19.2021

# only plots if the pval thresh is met

# RP24
for f in results_RP24*txt; do python ../../../../scripts/graphBoxPlot_compareSiteSignificance.py $f 0.05 RP24; done

# expression
for f in results*medianExpression*.txt; do python ../../../../scripts/graphBoxPlot_compareSiteSignificance.py $f 0.05 medianExpressionFPKM; done
for f in results*meanExpression*.txt; do python ../../../../scripts/graphBoxPlot_compareSiteSignificance.py $f 0.05 meanExpressionFPKM; done

# all expr vals
for f in results_all*.txt; do python ../../../../scripts/graphBoxPlot_allExprVals.py $f 0.05 'Expression (FPKM)' allValsExpressionFPKM; done
