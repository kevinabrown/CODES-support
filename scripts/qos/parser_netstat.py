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
from pprint import pprint

#if len(sys.argv) != 2:
#	print("ERROR | Too many command line arguments.")
#	exit(1)

outdir = '/home/kabrown/fs0-ipdps2021/experiments/survey.orig'

#print(sys.argv[1])
#files = glob.glob(os.path.normpath(sys.argv[1] + "/*.out"))

files = glob.glob(os.path.normpath(outdir + "/out.*"))


# latency : '[QOS_Class:0] Average number of hops traversed 5.369879 average chunk latency 244.559769 us maximum chunk latency 7389.169481 us avg message size 34952576.000000 bytes finished messages 15120 finished chunks 3303024480'
latencyre = re.compile("\[QOS_Class:(\d)\]\s+Average number of hops traversed ([\d\.\d]+) average chunk latency ([\d\.\d]+) us maximum chunk latency ([\d\.\d]+) us avg message size ([\d\.\d]+) bytes finished messages ([\d\.\d]+) finished chunks ([\d\.\d]+)");

# name : 'rmin_t1_l0.01.out'
routingre = re.compile("\[QOS_Class:(\d)\] ADAPTIVE ROUTING STATS: ([\d\.\d]+) chunks routed minimally ([\d\.\d]+) chunks routed non-minimally completed packets ([\d\.\d]+)")

# gerenated pacekts


# Find name of files to get routing, traffic, and load

#resfile = open('resfile_workload.txt', 'w')
#writer = csv.writer(resfile)
#writer.writerow('routing, traffic, load, avgtime, maxtime'.split(', '))

for filename in files:
    outline = []
    myfile = open(filename, 'r')

    classid = ""
    avghops = ""
    chunkavg = ""
    chunkmax = ""
    msgsizeavg = ""
    msgcount = ""
    chunkcount = ""

    outtext = "\n" + filename + "\n"

    for filen in myfile:
        if latencyre.match(filen):
            classid = latencyre.match(filen).group(1)
            avghops = latencyre.match(filen).group(2)
            chunkavg = latencyre.match(filen).group(3)
            chunkmax = latencyre.match(filen).group(4)
            msgsizeavg = latencyre.match(filen).group(5)
            msgcount = latencyre.match(filen).group(6)
            chunkcount = latencyre.match(filen).group(7)

            outtext = outtext + "\n\tClass ID: " + classid + "\n"
            outtext = outtext + "\tAvg Hops: " + avghops + "\n"
            outtext = outtext + "\tAvg Packet Latency: " + chunkavg + "\n"
            outtext = outtext + "\tMax Packet Latency: " + chunkmax + "\n"
            outtext = outtext + "\tTotal Packets: " + chunkcount + "\n"

    print(outtext)

    myfile.close()
