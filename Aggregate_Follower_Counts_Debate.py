# -*- coding: utf-8 -*-
"""
Created on Tue Sep 27 11:38:58 2016

@author: composersyf
"""

date="10-19-2016"

import os
os.chdir('/home/composersyf/Documents/Political Data Science Project')
import glob
file_list=glob.glob('Candidate Follower Counts during Debate/'+date+'/*')

import pandas as pd


def get_HHMM(time):
    return time[:5]

def change_to_PM(HHMM):
    return str(int(HHMM[:2])-12)+HHMM[2:]    

df_list=[]
for f in file_list:
    df_list.append(pd.read_csv(f))
    
agg_df=pd.concat(df_list,axis=0,join="outer")
clinton=agg_df[agg_df['Candidate_account']=="@HillaryClinton"]
trump=agg_df[agg_df['Candidate_account']=="@realDonaldTrump"]
pence=agg_df[agg_df['Candidate_account']=="@mike_pence"]
kaine=agg_df[agg_df['Candidate_account']=="@timkaine"]

#calculate the average follower counts per minute
clinton=clinton.sort_values(by=['time'])
trump=trump.sort_values(by=['time'])
pence=pence.sort_values(by=['time'])
kaine=kaine.sort_values(by=['time'])
clinton['HHMM']=clinton['time'].apply(get_HHMM)
trump['HHMM']=trump['time'].apply(get_HHMM)
pence['HHMM']=pence['time'].apply(get_HHMM)
kaine['HHMM']=kaine['time'].apply(get_HHMM)
clinton=clinton.groupby(['HHMM']).mean()
trump=trump.groupby(['HHMM']).mean()
pence=pence.groupby(['HHMM']).mean()
kaine=kaine.groupby(['HHMM']).mean()

#further data cleaning
clinton=clinton.reset_index([0]).rename(columns={'HHMM':"Time"})
trump=trump.reset_index([0]).rename(columns={'HHMM':"Time"})
pence=pence.reset_index([0]).rename(columns={'HHMM':"Time"})
kaine=kaine.reset_index([0]).rename(columns={'HHMM':"Time"})
clinton['Time']=clinton['Time'].apply(change_to_PM)
trump['Time']=trump['Time'].apply(change_to_PM)
pence['Time']=pence['Time'].apply(change_to_PM)
kaine['Time']=kaine['Time'].apply(change_to_PM)


#save to file
clinton.to_csv(date+"Clinton_Follower_Counts_2.csv",index=False)
trump.to_csv(date+"Trump_Follower_Counts_2.csv",index=False)
pence.to_csv(date+"Pence_Follower_Counts.csv",index=False)
kaine.to_csv(date+"Kaine_Follower_Counts.csv",index=False)

