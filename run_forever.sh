#!/bin/bash
for i in `seq 1 1000`;
do
 echo running $1 for the $i \'th time
 $1 >> "out.${1}"
 sleep 1
done   
