# rmf last modified 3.22.2020

import os, sys
from subprocess import call

# usage: scans database of sequences for occurences of user-provided motif(s)
usage = 'USAGE: python ' + os.path.basename(__file__) + ' <MEME motif file> <list of MEME motif IDs to run> <sequence file> <outbase> <options>\nSubmits seperate job for each motif ID.'
if len(sys.argv) != 6 or '-h' in sys.argv or '--help' in sys.argv:
    print usage
    sys.exit()

# SUBROUTINES
def readMotifList(motifList):
    motifs = []
    with open(motifList,'r') as f:
        for line in f:
            motif = line.strip() # remove newline character
            motifs.append(motif)
    return motifs

def run_qsub(cmd, outbase):
    err_file = output_dir + '.err'
    script_file = output_dir + '.sh'
    with open(script_file, 'w') as out:
        # passes defined variables, in format(), into scriptstring variable, into placeholder {}
        out.write(scriptstring.format(job_name = output_dir, err_file = err_file, command = cmd))
    call(['qsub', script_file])

# SETUP for running job on the queue
scriptstring = '''#!/bin/bash
#$ -cwd              # Current working directory
#$ -S /bin/bash      # Shell
#$ -N {job_name}     # Job name             
#$ -j y              # Merge stderr with stdout
#$ -o {err_file}     # Stdout name
#$ -q nucleotide     # Queue name
#$ -l mem_free=10G   # Limit memory request
#$ -V                # Preserve environmental variables
{command}'''

commandstring = 'fimo --bgfile background_MC1.txt --motif {motif} --o {output_dir} {options} {motif_file} {sequence_file}'

# ARGUMENTS
motif_file = sys.argv[1]
motifList = sys.argv[2]
sequence_file = sys.argv[3]
outbase = sys.argv[4]
options = sys.argv[5]

motifs = readMotifList(motifList)

for motif in motifs:
    output_dir = outbase + '_' + motif + '.out'
    cmd = commandstring.format(motif_file = motif_file, sequence_file = sequence_file, output_dir = output_dir, motif = motif, options=options)
    run_qsub(cmd, outbase)
