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
from pprint import pprint


#if len(sys.argv) != 2:
#	print("ERROR | Too many command line arguments.")
#	exit(1)


# Read input: sys_size
#sys_size = int(sys.argv[1])
#num_allocs = int(sys.argv[2])

basedir = '/home/kabrown/devel-fs0/routing'
#outdir = basedir + '/run.scoring.threshold/3x3_20'
outdir = basedir + '/run.bandwidth.scoring.q4'
lpiopath = outdir + '/riodir'

mpirun = "mpirun --report-bindings --np 1 --mca btl '^openib' --rankfile "
mpireplay = '/home/kabrown/opt/codes-1.2qx-debug2-withswm-intel-isc/bin/model-net-mpi-replay '
#codesargs = ' --synch=1 --workload_type=online --extramem=80000000 --priority_type=1 --payload_sz=65536 --mean_interval=2000 '
#codesargs = ' --synch=1 --workload_type=online --extramem=50000000 --payload_sz=8192 --max_gen_data=17039360 --mean_interval=305 '
#codesargs = ' --synch=1 --workload_type=online --extramem=50000000 --payload_sz=65536 --max_gen_data=13107200 --mean_interval=2000 '
#codesargs = ' --synch=1 --workload_type=online --extramem=10000000 --payload_sz=640 --max_gen_data=6400000 --mean_interval=20 '
codesargs = ' --synch=1 --workload_type=online --extramem=2000000 --payload_sz=160 '
codesargs = codesargs + '--lp-io-dir=' + lpiopath + ' --lp-io-use-suffix=1'


rankfilepath = basedir + '/rankfiles'
allocpath =  basedir + '/workloads'
netpath = basedir + '/conf_files'
netprefix = 'dfd8k_tapered_'

rankfiles = glob.glob(os.path.normpath(rankfilepath + "/rankfile06.*")) + \
            glob.glob(os.path.normpath(rankfilepath + "/rankfile08.*"))




rankfiles.sort()
#del(rankfiles[:12])
#pprint(rankfiles)
i = 0  # For the initial rankfile index


workloads = [
        {'name': 'full.tpr', 'qosconf': ['qos4.00a', 'qos4.01a', 'qos4.02a', 'qos4.03a'], 'threshold' : ['t16'], 'biases' : ['m2_2_2_2'], 'traffic' : ['ur'], 'loads' : ['4x10_45']},
        {'name': 'full.tpr', 'qosconf': ['qos4.00e', 'qos4.01e', 'qos4.02e', 'qos4.03e'], 'threshold' : ['t16'], 'biases' : ['m2_2_2_2'], 'traffic' : ['ur'], 'loads' : ['4x10_45']}
        ]
# bandwidth scoring
#        {'name': 'full.tpr', 'qosconf': ['noqos', 'qos2.00a', 'qos2.01a', 'qos2.02a', 'qos2.03a', 'qos2.00e', 'qos2.01e', 'qos2.02e', 'qos2.03e'], 'threshold' : ['t16'], 'biases' : ['m2_2'], 'traffic' : ['ur'], 'loads' : ['2x45', '2x10_45']}

# injection.threshold
#        {'name': 'full.tpr', 'qosconf': ['noqos'], 'threshold' : ['t0', 't04', 't08', 't16', 't32', 't64'], 'biases' : ['m2'], 'traffic' : ['ur'], 'loads' : [10, 25, 30, 35, 40, 45, 50, 55]},
#        {'name': 'full.tpr', 'qosconf': ['noqos'], 'threshold' : ['t0', 't04', 't08', 't16', 't32', 't64'], 'biases' : ['m2'], 'traffic' : ['nn'], 'loads' : [5, 10, 15, 20, 25, 30, 35]}
        #{'name': 'full.tpr', 'qosconf': ['noqos'], 'threshold' : ['min'], 'biases' : ['m2'], 'traffic' : ['ur'], 'loads' : [10, 25, 30, 35, 40, 45, 50, 55]}

#{'name': 'full.tpr', 'qosconf': ['noqos.t','qos3.t.01d', 'qos3.t.01e', 'qos3.t.01z'], 'biases' : ['m2'], 'loads' : ['3x10_75']}
#{'name': 'full.tpr', 'qosconf': ['noqos'], 'biases' : ['no'], 'loads' : [10, 25, 30, 35, 40, 45, 50, 55, 60]}
#        {'name': 'full.tpr', 'qosconf': ['noqos.t10','qos3.t10.01d', 'qos3.t10.01e', 'qos3.t10.01z','noqos.t0','qos3.t0.01d', 'qos3.t0.01e', 'qos3.t0.01z'], 'biases' : ['no','m2'], 'loads' : ['3x3_20']}
#        {'name': 'full.tpr', 'qosconf': ['noqos.t32'], 'biases' : ['m2'], 'loads' : [10, 25, 30, 35, 40, 45, 50, 55]}
#        {'name': 'full.tpr', 'qosconf': ['noqos.t16','qos3.t16.01a', 'qos3.t16.01e', 'qos3.t16.01z'], 'biases' : ['m2'], 'loads' : ['3x10_75']}

for wk in workloads:
    name = wk['name']
    
    jobcommand = ''

    for qos in wk['qosconf']:
        for threshold in wk['threshold']:
            for bias in wk['biases']:
                netfile = netpath + '/' + netprefix + qos + '.' + threshold + '_bias' + bias + '.conf' # injection threshold
                #netfile = netpath + '/' + netprefix + qos + '.t0' + '_bias' + bias + '.conf' # old
                #netfile = netpath + '/' + netprefix + qos + '.' + threshold + '.conf'  # for min and val routing

                for traffic in wk['traffic']:
                    for load in wk['loads']:
                        jobtag = name \
                                + '.' + qos \
                                + '.' + threshold \
                                + '.bias' + bias \
                                + '.' + traffic \
                                + '.load' + str(load)

                        outfile = outdir + '/' + 'out.' + jobtag
                        jobfile = os.path.normpath(outdir + '/' + str(i).zfill(3) + '.' + jobtag + '.sh')

                        loadfile = allocpath + '/' + traffic + '.load.' + str(load)
                        #loadfile = allocpath + '/load.' + str(load)    #without traffic prefix
                        #appalloc = allocpath + '/' + 'alloc.2.4159'     # for bandwidth study
                        appalloc = allocpath + '/' + 'alloc.4x10_45'     # for bandwidth study
                        #appalloc = allocpath + '/' + '8318.alloc'   # for injection load test
                        #appalloc = allocpath + '/' + 'alloc.' + str(load)   # for normal config

                        jobcommand = mpirun + ' \\\n' \
                                + rankfiles[i]  + ' \\\n' \
                                + ' ' + mpireplay + ' \\\n' \
                                + ' ' + codesargs + ' \\\n' \
                                + ' --workload_conf_file=' + loadfile + ' \\\n' \
                                + ' --alloc_file=' + appalloc + ' \\\n' \
                                + ' --disable_compute=0' \
                                + ' -- ' + netfile + ' \\\n' \
                                + ' &>> ' + str(outfile)

                        fincommand = '\n\necho "Status $?: ' + jobfile + ' : `date`" >> ~/runstatus'

                        with open(jobfile, 'w') as f:
                            f.write(jobcommand) 
                            f.write(fincommand)

                        st = os.stat(jobfile)
                        os.chmod(jobfile, st.st_mode | stat.S_IEXEC)

                        print('nohup ' + jobfile + ' &')

                        i = i + 1
                        if i == len(rankfiles):
                            i = 0

 
print("Completed.")

