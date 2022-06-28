#!/bin/bash

# rmf 4.6.2018; last modified 4.2.2019
# download and gunzip fastq files from ENA

wget ftp.sra.ebi.ac.uk/vol1/fastq/ERR649/ERR649811/ERR649811.fastq.gz
wget ftp.sra.ebi.ac.uk/vol1/fastq/ERR649/ERR649812/ERR649812.fastq.gz
wget ftp.sra.ebi.ac.uk/vol1/fastq/ERR649/ERR649813/ERR649813.fastq.gz
wget ftp.sra.ebi.ac.uk/vol1/fastq/ERR649/ERR649814/ERR649814.fastq.gz

for f in ERR*.fastq.gz; do newfile=cnc$f; mv $f $newfile; gunzip $newfile; done
