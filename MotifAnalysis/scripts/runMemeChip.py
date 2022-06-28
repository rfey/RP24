# rmf 3.27.2018; last modified 4.2.2019

import sys, os
from subprocess import call

# runs meme-chip on fasta file: discovers motifs
usage = 'USAGE: python ' + sys.argv[0] + ' <fasta file> <options>'
if len(sys.argv) != 3 or '-h' in sys.argv or '--help' in sys.argv:
    print usage
    sys.exit()

def run_qsub(cmd, prefix):
    err_file = prefix + '.err'
    script_file = prefix + '.sh'
    with open(script_file, 'w') as out:
        # passes defined variables, in format(), into scriptstring variable, into placeholder {}
        out.write(scriptstring.format(job_name = prefix, err_file = err_file, command = cmd))
    call(['qsub', script_file])

scriptstring = '''#!/bin/bash
#$ -cwd               # Current working directory
#$ -S /bin/bash       # Shell
#$ -N {job_name}      # Job name
#$ -j y               # Merge stderr with stdout
#$ -o {err_file}      # Stdout name
#$ -q nucleotide      # Queue name
#$ -l mem_free=10G    # Limit memory request
#$ -V                 # Preserve environmental variables
{command}'''

commandstring = 'meme-chip {input_file} -oc {output_dir} {options}'

input_file = sys.argv[1]
# get the filename of the input file without the absolute path and assign to variable
file_name = input_file.split('/')[-1]
# get the filename without the extension and assign to variable
prefix = file_name.split('.')[0]
output_dir = prefix + "_memeChip"
options = sys.argv[2]
cmd = commandstring.format(input_file = input_file, output_dir=output_dir,options=options)
run_qsub(cmd, prefix)
