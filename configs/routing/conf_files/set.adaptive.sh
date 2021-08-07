#!/bin/bash

thold=$1

sed -i "s/adaptive_threshold=\"[0-9]*\"/adaptive_threshold=\"${thold}\"/g" /home/kabrown/devel-fs0/routing/conf_files/dfd8k_tapered_noqos.t_biasm2.conf 
sed -i "s/adaptive_threshold=\"[0-9]*\"/adaptive_threshold=\"${thold}\"/g" /home/kabrown/devel-fs0/routing/conf_files/dfd8k_tapered_qos3.t.01d_biasm2.conf
sed -i "s/adaptive_threshold=\"[0-9]*\"/adaptive_threshold=\"${thold}\"/g" /home/kabrown/devel-fs0/routing/conf_files/dfd8k_tapered_qos3.t.01e_biasm2.conf
sed -i "s/adaptive_threshold=\"[0-9]*\"/adaptive_threshold=\"${thold}\"/g" /home/kabrown/devel-fs0/routing/conf_files/dfd8k_tapered_qos3.t.01z_biasm2.conf
