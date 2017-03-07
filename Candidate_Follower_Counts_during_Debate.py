# -*- coding: utf-8 -*-
"""
Created on Mon Sep 26 12:50:58 2016

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
    candidate_names=["Hillary Clinton", "Donald Trump", "Tim Kaine", "Mike Pence"]
    candidate_accounts=pd.Series(['@HillaryClinton','@realDonaldTrump','@mike_pence','@timkaine'])
    candidates=pd.DataFrame({"Candidate_name":candidate_names, "Candidate_account":candidate_accounts})
    candidate_twitter_url=candidate_accounts.apply(generate_twitter_url,args=[twitter_url])
    try:
        #Add follower_count and today's date to the table
        candidates['Follower_count']=find_number_of_followers(candidate_twitter_url)
        date_now=dt.datetime.now()
        time_now=":".join([str(date_now.hour).zfill(2),str(date_now.minute).zfill(2),str(date_now.second).zfill(2)])
        candidates['time']=[time_now]*candidates.shape[0]

        #save the results to a .csv table
        candidates.to_csv("/home/composersyf/Documents/Political Data Science Project/Candidate Follower Counts during Debate/10-19-2016/"+time_now+"Candidates_new.csv",index=False)
    except (urllib.request.HTTPError,urllib.request.URLError):
        pass

    
if __name__=="__main__":
    while dt.datetime.now().hour!=23 or (dt.datetime.now().hour==23 and dt.datetime.now().minute!=30):
        scrape_follower_counts()
