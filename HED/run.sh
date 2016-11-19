#!/bin/bash

#PBS -l walltime=30:00:00
#PBS -l nodes=18:ppn=4
#PBS -t 0-31%10


for cv in `seq 1 4`;
do
	cv_path='cv'$cv'/'
	#echo $cv_path
	
	for Ce in `seq 0  5`;
		do
			#echo Ce : $Ce
			for Cn in `seq 1 2 5` ;
			do
						#echo Cn : $Cn
						python mainHED.py -d '../../wordspotting_dataset' -v $cv_path -n $Cn -e $Ce -o '../../out_dir' &
			done

		done
 
	
done

wait