#!/bin/bash

input_path='/home/composersyf/Documents/Political Data Science Project/New_Output_hash' ##change directory name here!!
cd "$input_path"
ls > ../all_directories.txt

while read -r line1
do
    d_name="$line1"
    cd "$input_path""/""$d_name"
    while read -r line2
    do
        date=`echo $line2 | cut -d \, -f 1`
        counts=`ls $date* | wc -l`
        if [ $counts -gt 1 ] 
        then
            cat $date* > "$date""_new.csv"
            ls * | grep "$date""_[0-9]\+.csv" | xargs rm
            mv "$date""_new.csv" "$date""_1.csv"
        fi
        python ../../Sort_Tweets_by_Time.py "$input_path" "$d_name" "$date" ##since $input_path contains spaces, it is necessary to enclose it with double quotation marks
    done < "daily_file_counts.csv"
    cd ..    
done < "../all_directories.txt"

cd ~
