#!/bin/sh

#<software>
basedir=$HOME/opt/$(basename ${BASH_SOURCE[0]} .sh)
basedir=`echo $basedir | cut -d- -f2-`

source $HOME/opt/vars-base.sh $basedir
