# -*- coding: utf-8 -*-
"""
Created on Mon Sep 26 13:35:07 2016

@author: composersyf
"""

import requests
import datetime as dt
import time
import numpy as np
import pandas as pd

def collect_predictwise():
    while dt.datetime.now().day!=20:
        raw_file = requests.get('http://table-cache1.predictwise.com/latest/table_1523.json')
        json_file=raw_file.json()
        
        data_df=pd.DataFrame(np.array([json_file['table'][0],json_file['table'][1]]).reshape(2,len(json_file['table'][0])))
        data_df.columns=json_file['header']
        data_df['hour']=[json_file['timestamp'].split()[1][:-2].split(":")[0].zfill(2)]*2
        data_df['minute']=[json_file['timestamp'].split()[1][:-2].split(":")[1].zfill(2)]*2
        
        data_df.to_csv("/home/composersyf/Documents/Political Data Science Project/PredictWise during Debate/10-19-2016/"+data_df['hour'][0]+":"+data_df['minute'][0]+"Predictwise.csv",index=False)
        time.sleep(60)
        

if __name__=="__main__":
    collect_predictwise()
