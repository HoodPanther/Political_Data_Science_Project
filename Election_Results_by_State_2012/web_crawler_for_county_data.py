# -*- coding: utf-8 -*-
"""
Created on Mon Nov 14 15:29:25 2016

@author: composersyf
"""

import os
os.chdir("/home/composersyf/Documents/Political Data Science Project")

import urllib.request
from bs4 import BeautifulSoup

import pandas as pd
import numpy as np
import html5lib

html_page=urllib.request.urlopen('http://www.politico.com/2012-election/results/president/california/').read()
soup=BeautifulSoup(html_page,'html.parser')
all_counties=soup.findAll('tbody',{'id':re.compile('county[0-9]{4}')})
len(all_counties)