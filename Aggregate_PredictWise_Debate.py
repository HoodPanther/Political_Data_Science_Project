# -*- coding: utf-8 -*-
"""
Created on Tue Sep 27 11:04:23 2016

@author: composersyf
"""

date="09-26-2016"

import os
os.chdir('/home/composersyf/Documents/Political Data Science Project')
import glob
file_list=glob.glob('PredictWise during Debate/'+date+'/*')

import pandas as pd


def aggregate_data():
    df_list=[]
    for f in file_list:
        df_list.append(pd.read_csv(f))
    
    agg_df=pd.concat(df_list,axis=0,join="outer")    
    democratic=agg_df[agg_df['Party']=="Democratic"]
    republican=agg_df[agg_df['Party']=="Republican"]
    
    column_index=list(range(agg_df.shape[1]))
    democratic=democratic.sort_values(by=['hour','minute']).iloc[:,[column_index[-2+i] for i in column_index]]
    republican=republican.sort_values(by=['hour','minute']).iloc[:,[column_index[-2+i] for i in column_index]]
    
    democratic.to_csv(date+"Democratic_PredictWise.csv",index=False)
    republican.to_csv(date+"Republican_PredictWise.csv",index=False)
    
    
if __name__=="__main__":
    aggregate_data()