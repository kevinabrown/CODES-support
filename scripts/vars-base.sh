#!/bin/sh

#<software>
mypath=$HOME/opt/$1

subdir=$mypath/bin
if [ -d "$subdir" ]; then
	export PATH=$subdir:$PATH
fi

subdir=$mypath/lib
if [ -d "$subdir" ]; then
	export LIBRARY_PATH=$subdir:$LIBRARY_PATH
	export LD_LIBRARY_PATH=$subdir:$LD_LIBRARY_PATH
fi

subdir=$mypath/include
if [ -d "$subdir" ]; then
	export CPATH=$subdir:$CPATH
	export C_INCLUDE_PATH=$subdir:$C_INCLUDE_PATH
	export CPLUS_INCLUDE_PATH=$subdir:$CPLUS_INCLUDE_PATH
fi

subdir=$mypath/lib/pkgconfig
if [ -d "$subdir" ]; then
	export PKG_CONFIG_PATH=$subdir:$PKG_CONFIG_PATH
fi

