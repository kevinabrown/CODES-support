#!/usr/bin/python

#  $ python3 parser_worklaod_stats.out <path_to_dir>
#
# Parses the statistic printed by the CODES synthetic workloads.
# Reads all *.out files in the provided location
# Updated  20200302

import os
import re
import sys
import csv
import glob
import random
from random import randint
from pprint import pprint


#if len(sys.argv) != 2:
#	print("ERROR | Too many command line arguments.")
#	exit(1)

#files = glob.glob(os.path.normpath(sys.argv[1] + "/*.out"))

# Read input: sys_size
#sys_size = int(sys.argv[1])
sys_size = 8318
#sys_size = 8320
#sys_size = 1056

iotarget_cnt = 256
#num_allocs = int(sys.argv[2])

#alloc_size = []
#for i in range(num_allocs):
#    alloc_size.append(int(sys.argv[i+3]))

payload = 160 # B
bandwidth = 25 # GB/s

print("System size: ", sys_size)

alloc_written = 0
all_allocs = []
marked_nodes = []
filename = "rand" + str(sys_size)
#filename += "_".join(map(str, alloc_size))
allocfile = open(filename + '.alloc', 'w')
loadfile = open(filename + '.load', 'w')

def get_interval(load):
    if(load == 0):
        return 0

    bw = float(25) * 1024**3 / 1000**3
    
    interval = payload / (bw * load)

    return interval


def new_alloc(size, name, qos, load):
    global marked_nodes
    alloc = []

    # Allocate I/O targets contiguously
    if name == 'bulk_data' or name == 'bulk_data1':
        alloc = list(range(0, iotarget_cnt))
        marked_nodes.extend(alloc)
        
        # remove I/O target from I/O job size
        size = size - iotarget_cnt
    
    k=0
    # Allocate nodes for compute jobs
    for j in range(size):
        k = randint(0, sys_size-1)

        while( k in marked_nodes or k == sys_size):
            #k = k+1
            k = randint(0, sys_size-1)
        
        alloc.append(k)
        marked_nodes.append(k)
        k = k + 1

    alloc.sort()

    # Write to global file
    global alloc_written
    if(alloc_written != 0):
        allocfile.write("\n")
        loadfile.write("\n")

    allocfile.write(' '.join(map(str, alloc)))
    loadfile.write(str(len(alloc)) + ' ' + name + ' ' + str(qos) + ' ' + '{:.4f}'.format(get_interval(load)))

    alloc_written = alloc_written + 1

    #print("Allocated: ", size)

    # return 
    return alloc

# Write files for baseline run: single application
def write_my_file(size, name, qos, load, alloc, rep):
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
        f.write(jump + str(size) + ' ' + name + ' ' + str(qos) + ' ' + '{:.4f}'.format(get_interval(load)))


workloads = [
        {'name': 'synthetic1',
            'size': 512,
            'reps': 1,
            'qos':  0,
            'load': .07},
        {'name': 'synthetic1',
            'size': 2602,
            'reps': 1,
            'qos':  1,
            'load': .45},
        {'name': 'synthetic1',
            'size': 2602,
            'reps': 1,
            'qos':  2,
            'load': .45},
        {'name': 'synthetic1',
            'size': 2602,
            'reps': 1,
            'qos':  3,
            'load': .45}
        ]
'''        {'name': 'lammps',
            'size': 64,
            'reps': 1,
            'qos':  0,
            'load': 0}
        ]

        {'name': 'synthetic1',
            'size': 2772,
            'reps': 1,
            'qos':  0,
            'load': .1},
        {'name': 'synthetic1',
            'size': 2773,
            'reps': 1,
            'qos':  1,
            'load': .75},
        {'name': 'synthetic1',
            'size': 2773,
            'reps': 1,
            'qos':  2,
            'load': .75},
        {'name': 'all_reduce',
            'size': 2,
            'reps': 1,
            'qos':  0,
            'load': 0}
        ]
'''
for wk in workloads:
    for i in range(wk['reps']):
        alloc = new_alloc(wk['size'], wk['name'], wk['qos'], wk['load'])
        write_my_file(wk['size'], wk['name'], wk['qos'], wk['load'], alloc, i)




allocfile.close()

print("Total allocated nodes: ", len(marked_nodes))
print("Completed.")
