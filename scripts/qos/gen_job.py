#!/usr/bin/python

#  $ python3 parser_worklaod_stats.out <path_to_dir>
#
# Parses the statistic printed by the CODES synthetic workloads.
# Reads all *.out files in the provided location
# Updated  20200302

import os
import re
import sys
import stat
import csv
import glob
from random import randint
from pprint import pprint


#if len(sys.argv) != 2:
#	print("ERROR | Too many command line arguments.")
#	exit(1)


# Read input: sys_size
#sys_size = int(sys.argv[1])
#num_allocs = int(sys.argv[2])
basedir = '/home/kabrown/case-studies/qos-swm/experiments'
level = 'coarse'
allocname = 'alloc1'
outdir = basedir + '/' + allocname
lpiopath = outdir + '/riodir'

mpirun = "mpirun --report-bindings --np 1 --mca btl '^openib' --rankfile "
mpireplay = '/home/kabrown/opt/codes-1.2qx-debug2-withswmfork-intel-isc/bin/model-net-mpi-replay '

#codesargs = ' --synch=1 --workload_type=online --extramem=80000000 --priority_type=1 --payload_sz=65536 --mean_interval=2000 '
#codesargs = ' --synch=1 --workload_type=online --extramem=50000000 --payload_sz=8192 --max_gen_data=17039360 --mean_interval=305 '
#codesargs = ' --synch=1 --workload_type=online --extramem=50000000 --payload_sz=65536 --max_gen_data=13107200 --mean_interval=2000 '
#codesargs = ' --synch=1 --workload_type=online --extramem=10000000 --payload_sz=640 --max_gen_data=6400000 --mean_interval=20 '

if level == 'medium' or level == 'fine':
    codesargs = ' --synch=1 --workload_type=online --extramem=50000000 --payload_sz=640 --priority_type=1 ' # for medium-grain QoS
else:
    codesargs = ' --synch=1 --workload_type=online --extramem=50000000 --payload_sz=640 ' # for coarse-grain QoS. priority_type is 0 by default

codesargs = codesargs + '--lp-io-dir=' + lpiopath + ' --lp-io-use-suffix=1'


rankfilepath = basedir + '/rankfiles'
allocpath =  basedir + '/workloads' + '/' + allocname
netpath = basedir + '/conf_files'
netprefix = 'dfd1088_tapered_'



rankfiles = glob.glob(os.path.normpath(rankfilepath + "/rankfile07*"))

rankfiles.sort()
#del(rankfiles[:12])
#pprint(rankfiles)
i = 0  # For the initial rankfile index



workloads = [
#        {'name': 'rand1088', 'qosconf': ['noqos','qos4_1'], 'compute': [0]},
#        {'name': 'spread', 'qosconf': ['noqos'], 'compute': [0]},
        {'name': 'lammps', 'qosconf': ['noqos'], 'compute': [0]},
#        {'name': 'milc', 'qosconf': ['noqos'], 'compute': [0]},
#        {'name': 'many_to_many', 'qosconf': ['noqos'], 'compute': [0]}
        ]


for wk in workloads:
    name = wk['name']
    
    jobcommand = ''

    for qos in wk['qosconf']:
        netfile = netpath + '/' + netprefix + qos + '.conf'

        for comp in wk['compute']:
            jobtag = name \
                    + '.' + allocname \
                    + '.dc' + str(comp) \
                    + '.' + qos \
                    + '.' + level

            outfile = outdir + '/' + 'out.' + jobtag
            jobfile = os.path.normpath(outdir + '/' + str(i).zfill(3) + '.' + jobtag + '.sh')

            periodfile = allocpath + '/' + name + '.period'
            loadfile = allocpath + '/' + name + '.load'
            appalloc = allocpath + '/' + name + '.alloc'

            jobcommand = mpirun + rankfiles[i] \
                    + ' ' + mpireplay \
                    + ' ' + codesargs \
                    + ' --workload_conf_file=' + loadfile \
                    + ' --alloc_file=' + appalloc \
                    + ' --disable_compute=' + str(comp) \
                    + ' -- ' + netfile \
                    + ' &>> ' + str(outfile)

            # Copy settings


            #pprint(rankfiles[i])
            #print(outfile)
            #print(str(i) + "------" + command)
            with open(jobfile, 'w') as f:
                f.write(jobcommand) 

            st = os.stat(jobfile)
            os.chmod(jobfile, st.st_mode | stat.S_IEXEC)

            print(jobfile)

            i = i + 1
            if i == len(rankfiles):
                i = 0


 
print("Completed.")

''' 

mpirun --report-bindings --np 1 --rankfile /home/kabrown/fs0-ipdps2021/experiments/rankfiles/rankfile0.11 --mca btl '^openib' \
	/home/kabrown/opt/codes-1.2qx-debug2-withswm-intel/bin/model-net-mpi-replay --synch=1 \
	--workload_type=online --extramem=10000000 --disable_compute=1 --debug_cols=1 --priority_type=1 \
	--workload_conf_file=/home/kabrown/fs0-ipdps2021/experiments/workloads/lammps.load \
	--alloc_file=/home/kabrown/fs0-ipdps2021/experiments/workloads/job.lammps.alloc \
	--lp-io-dir=/home/kabrown/fs0-ipdps2021/experiments/lpio/lpio_output --lp-io-use-suffix=1 \
	-- /home/kabrown/fs0-ipdps2021/experiments/conf_files/dfd8k_noqos.conf \
	&>> out.lammps.nocompute

'''
'''
print("System size: ", sys_size)

alloc_written = 0
all_allocs = []
marked_nodes = []
filename = "rand" + str(sys_size)
#filename += "_".join(map(str, alloc_size))
allocfile = open(filename + '.alloc', 'w')
loadfile = open(filename + '.load', 'w')

def new_alloc(size, name, qos):
    global marked_nodes

    alloc = []
    for j in range(size):
        k = randint(0, sys_size-1)

        while( k in marked_nodes):
            k = randint(0, sys_size-1)
        
        alloc.append(k)
        marked_nodes.append(k)

    alloc.sort()

    # Write to global file
    global alloc_written
    if(alloc_written != 0):
        allocfile.write("\n")
        loadfile.write("\n")

    allocfile.write(' '.join(map(str, alloc)))
    loadfile.write(str(size) + ' ' + name + ' ' + str(qos))

    alloc_written = alloc_written + 1

    #print("Allocated: ", size)

    # return 
    return alloc

def write_my_file(size, name, qos, alloc, rep):
    flag = ''
    jump = ''
    if rep == 0:
        flag = 'w'
    else:
        flag = 'a'
        jump = '\n'

    with open(name + ".alloc", flag) as f:
        f.write(jump + ' '.join(map(str, alloc)))
    with open(name+ ".load", flag) as f:
        f.write(jump + str(size) + ' ' + name + ' ' + str(qos))


workloads = [
        {'name': 'lammps', 
            'size': 2048,
            'reps': 1,
            'qos':  1},
        {'name': 'nekbone', 
            'size': 2197,
            'reps': 1,
            'qos':  1},
        {'name': 'incast', # scavenger
            'size': 512,
            'reps': 1,
            'qos':  3},
        {'name': 'lammps', 
            'size': 2048,
            'reps': 1,
            'qos':  1},
        {'name': 'incast1', # I/O
            'size': 2,
            'reps': 128,
            'qos':  2}
        ]


for wk in workloads:
    for i in range(wk['reps']):
        alloc = new_alloc(wk['size'], wk['name'], wk['qos'])
        write_my_file(wk['size'], wk['name'], wk['qos'], alloc, i)



#lammps 1
qos = 1
size = 5
name = "lammps"
alloc = new_alloc(size, name, qos)
write_my_file(name, size, alloc, qos)


#lammps 2
qos = 1
size = 5
name = "lammps"
alloc = new_alloc(size, name, qos)
write_my_file(name, size, alloc, qos)


#neckbone
qos = 1
size = 5
name = "nekbone"
alloc = new_alloc(size, name)
write_my_file(name, size, alloc)

#incast (scavenger)
qos = 3
size = 3
name = "incast"
alloc = new_alloc(size, name)
write_my_file(name, size, alloc)

#incast2 (bulk data)
rep = 2
qos = 2
name = "incast2"
with open(name + ".alloc", 'w') as f:
    with open(name + ".load", 'w') as g:
        count = 0
        for i in range(3):
            size = 2
            alloc = new_alloc(size, name)

            if(count != 0):
                f.write("\n")
                g.write("\n")

            f.write(' '.join(map(str, alloc)))
            g.write(str(size) + ' ' + name)

            count = count +1


allocfile.close()
'''

