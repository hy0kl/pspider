#!/bin/env bash

set -x

# check env diretory
evn_dir="log data  work"
for dir in $evn_dir
do
    if [ -d $dir ]
    then
        echo "'{$dir}' diretory is exists."
    else
        echo "'{$dir}' is NOT exists, create it ..."
        mkdir -p $dir 
    fi  
done
