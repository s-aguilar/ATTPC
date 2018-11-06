#!/bin/bash

#$ -pe smp 16           # Specify 'parallel env' and number of legally requested cores 'smp 1' NOTE: if more than 10GB memory needed, might need to request m$
#$ -q debug             # Specify queue type. 'debug'-> 4h/64GB; 'long"-> 15D/256GB; Going shorter means shorter wall-time
#$ -N seabassJob        # Specify job's name

module load python/3.6.4
export PATH="/afs/crc.nd.edu/group/nsl/activetarget/users/saguilar/anaconda3/bin:$PATH"
python /afs/crc.nd.edu/group/nsl/activetarget/users/saguilar/tbjcATTPCanalyzor-master/Multi.py


