# -*- coding: utf-8 -*-
"""
Created on Sat Nov 12 22:00:27 2016

@author: composersyf
"""

import os
os.chdir("/home/composersyf/Documents/Political Data Science Project")

import urllib.request
from bs4 import BeautifulSoup

import pandas as pd
import numpy as np
import html5lib

import glob
file_list=glob.glob('Result by State/*.html')

def clean_one_state(filename):
    
    state_name=filename.split('/')[1].split(' ')[0]
    with open(filename) as f:
        html_page=f.read()
    
    soup=BeautifulSoup(html_page,'html.parser')
    all_tables=soup.findAll('table')
    county_names = soup.findAll("header", { "class" : "results-header"})
    reporting=soup.findAll('p',{'class':'reporting'})
    result_dict={}
    for i in range(1,len(all_tables)):
        result_dict[county_names[i].text.strip("\n")]={'reporting':reporting[i].text}
        all_rows=all_tables[i].findAll('tr')
        for j in range(len(all_rows)):
            if all_rows[j].findAll('th')[0].text.split('  ')==[all_rows[j].findAll('th')[0].text]:
                c_name=' '.join(all_rows[j].findAll('th')[0].text.split(' ')[-2:])
            else:
                c_name=all_rows[j].findAll('th')[0].text.split('  ')[1]
            c_vote=all_rows[j].findAll('td')[1].text
            result_dict[county_names[i].text.strip("\n")][c_name]=c_vote            
    result_df=pd.DataFrame.from_dict(result_dict,orient='index')
    rest_colnames=np.setdiff1d(result_df.columns.values,'reporting')
    all_colnames=np.concatenate([rest_colnames,['reporting']])
    result_df=result_df.loc[:,all_colnames]
    if state_name in ['Alaska','District-of-Columbia']:
        result_df.ix[0,'reporting']=result_df.ix[0,'reporting'].split('\xa0\xa0\xa0')[0]
    result_df.to_csv('Result by State/Cleaned/'+state_name+'.csv')


if __name__=='__main__':    
    for f in file_list:
        clean_one_state(f)