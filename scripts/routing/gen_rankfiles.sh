#!/bin/bash

nodes="skylake10 skylake11 skylake12"
maxslotid=1
maxcoreid=27

nid=10

#rank 0=skylake01 slot=0:8-9
for node in ${nodes}; do
	rid=0
	for slot in $(seq 0 $maxslotid); do
		for core in $(seq 0 10 $maxcoreid); do
			echo "rank 0=${node} slot=${slot}:${core}" > rankfile${nid}.`printf %02d ${rid}`

			rid=$((rid+1))
		done
	done

	nid=$((nid+1))
done

