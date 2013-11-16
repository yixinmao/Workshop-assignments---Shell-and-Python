#!/bin/bash

# All original data files are in directory: ./fluxes
# The result of monthly_precipitation data for each grid will be saved in dir: ./monthly_prec (this dir should be created in advance)
# The temperal files generated will be saved in dir: ./temp_files (this dir should be created in advance)
# The final result of areal mean precipitation of each month will be saved in file: result.txt 

### Problem 1 ###
for file in `ls ./fluxes`; do
	filename=`echo $file | sed -e 's/fluxes_/monthly_precipitation\./'`
	awk ' { sum[$2]+=$4; n[$2]+=1 } END {for (i in sum) print i,sum[i]/n[i]} '\
	     ./fluxes/$file | sort | awk ' { print $2} ' >./monthly_prec/$filename
done
# I tried to calculate the mean of the 3rd line (which is the date) instead of the 4th line to make sure that the script is correct. I did this because I can easily know the mean of date, so that I could check if the result is correct.


### Problem 2 ###
rm ./temp_files/*  # delete all previous temporary files 
for mon in `seq 1 12`; do
	touch ./temp_files/month$mon.txt
        # create 12 temporary files, each contains the monthly precipitation of every grid
	touch ./temp_files/lat.txt
	# create a file which contains the latitude of every grid
done
for file in `ls ./monthly_prec`; do
	for mon in `seq 1 12`; do  # put monthly precipitation of each grid to 12 temp files
		less ./monthly_prec/$file | head -$mon | tail -1 | cat >>./temp_files/month$mon.txt
	done
	echo $file | sed -e 's/monthly_precipitation\.//' | sed -e 's/[_].*//'\
                   | cat >>./temp_files/lat.txt
	# put lat of each grid in a file
done
rm areal_mean_monthly_prec.txt
for i in `seq 1 12`; do
	paste ./temp_files/month$i.txt ./temp_files/lat.txt \
		| awk ' {sum+=$1*cos($2/180*3.14159); weight_sum+=cos($2/180*3.14159)} \
                 END {print sum/weight_sum}' >>areal_mean_monthly_prec.txt   # write the final result to result.txt
done
# I made short test data files (whose results can be easily known) to test if my script can generate corect results. Besides, we can roughly scan the original and temporal data to make sure that the final mean values are in reasonable ranges.
	



