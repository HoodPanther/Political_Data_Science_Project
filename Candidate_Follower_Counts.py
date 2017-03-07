# -*- coding: utf-8 -*-
"""
Created on Fri Sep 16 13:29:28 2016

@author: composersyf
"""

import os
os.chdir("/home/composersyf/Documents/Political Data Science Project")

from bs4 import BeautifulSoup
import urllib.request
import pandas as pd
import datetime as dt


def generate_twitter_url(account_name, twitter_url):
    return twitter_url+account_name[1:]

    
def find_number_of_followers(candidate_twitter_url):
    number_of_followers=[]
    for url in candidate_twitter_url:
        html = urllib.request.urlopen(url).read()
        soup=BeautifulSoup(html,'html.parser')
        all_a_tags=soup.findAll("a")
        all_titles=[]
        for t in all_a_tags:
            try:
                all_titles.append(t["title"])
            except KeyError:
                pass
        for t in all_titles:
            if "Followers" in t:
                number=int(t.split()[0].replace(",",""))
                number_of_followers.append(number)
                break
            else:
                pass
    return number_of_followers


def scrape_follower_counts():
    #generate list of candidate twitter urls
    twitter_url="https://twitter.com/"
    candidates=pd.read_csv("Candidates.csv")
    candidate_accounts=candidates["TwitterID"]
    candidate_twitter_url=candidate_accounts.apply(generate_twitter_url,args=[twitter_url])
    
    #Add follower_count and today's date to the table
    candidates['Follower_count']=find_number_of_followers(candidate_twitter_url)
    date_now=dt.datetime.now()
    time_now=":".join([str(date_now.hour).zfill(2),str(date_now.minute).zfill(2)])
    date_today="-".join([str(date_now.year),str(date_now.month).zfill(2),str(date_now.day).zfill(2)])
    candidates['date']=[date_today]*candidates.shape[0]

    #save the results to a .csv table
    candidates.to_csv("/home/composersyf/Documents/Political Data Science Project/Candidate Follower Counts/"+date_today+"_"+time_now+"Candidates_new.csv",index=False)

    
if __name__=="__main__":
    scrape_follower_counts()
