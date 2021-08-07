#!/bin/bash

# reads nodename from the command line
node=$1
maxslotid=1
maxcoreid=27

#change this line to X is for you want rankileX
nid=01

#rank 0=skylake01 slot=0:x
batchid=0
for slot in $(seq 0 $maxslotid); do
	for core in $(seq 0 8 $maxcoreid); do
		echo "rank 0=${node} slot=${slot}:${core}" > rankfile${nid}.`printf %02d ${batchid}`
		batchid=$((batchid+1))
	done
done

