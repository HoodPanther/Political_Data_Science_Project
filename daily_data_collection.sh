#!/bin/bash

SHELL=/bin/bash
#it is necessary to add the directory where the Bash script is stored to PATH variable in order to automatically run the script in Cron
PATH=/home/composersyf/torch/install/bin:~/bin:/home/composersyf/anaconda3/bin:/home/composersyf/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:'/home/composersyf/Documents/Political Data Science Project'
cd '/home/composersyf/Documents/Political Data Science Project'

#task 1
python Candidate_Follower_Counts.py
#task 2
datetime=`date`
output_path='/home/composersyf/Documents/Political Data Science Project/PredictWise_Daily/PredictWise-'$datetime'.json'
curl http://table-cache1.predictwise.com/latest/table_1523.json > "$output_path" #quote marks are needed to make it a valid file path 
