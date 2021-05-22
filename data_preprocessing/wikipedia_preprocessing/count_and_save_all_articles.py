# -*- coding: utf-8 -*-

import os
import re
import difflib
import time
import tqdm
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import urllib.parse
from urllib.parse import unquote
from itertools import combinations, permutations
from collections import defaultdict
import json
import nltk
import sys
import pickle
#from nltk.tokenize import sent_tokenize
from collections import OrderedDict
import resource



def get_all_files(path):
    Filelist = []
    for root, dirs, files in os.walk(path):
        for dir_name in dirs:
            inner_path = os.path.join(root, dir_name)
            for home, nones, fs in os.walk(inner_path):
                for f in fs:
                    Filelist.append(os.path.join(inner_path, f))
    return Filelist
                    
                    
def extract_articles(textfile):
    articles = []
    f = open(textfile, 'r')
    bs = BeautifulSoup(f,"lxml")
    for doc in bs.find_all("doc"):
        wiki_id = doc.get("id")
        wiki_title = doc.get("title")
        wiki_url = doc.get("url")
        #print(doc)
        #print("_________"*8)
        links = []
        a_s = doc.find_all('a')
        
        for a in a_s:
            #print('current a is ', a)
            link_text = a.text
            if 'href' in a.attrs:
                link_title = urllib.parse.unquote(a.attrs['href'])
                
            else:
                link_title = link_text
            links.append((a, link_title, link_text))
           
                
        articles.append((wiki_id, wiki_title, wiki_url, doc, links))
        #str = a.get("href")
        #if str:
            #links.append(urllib.parse.unquote(str))
    f.close()
    return articles


if __name__ == "__main__":

    sys.setrecursionlimit(3000)
    
    max_rec = 0x100000
    resource.setrlimit(resource.RLIMIT_STACK, [0x100 * max_rec, resource.RLIM_INFINITY])
    sys.setrecursionlimit(max_rec)
                        
    path = '/home/xiao/Projects/graphdescriber/data/GraphDescriber_Dataset_with_Wikification/WikipediaArticles_original/text/'
    
    i = 0
    
    article_all = []
    filelist = list(get_all_files(path))
    
    
    #filelist = ['/home/xiao/Projects/graphdescriber/data/GraphDescriber_Dataset_with_Wikification/WikipediaArticles_original/text/EK/wiki_82']
    for file in filelist:
        if i % 100 == 0:
            print('current file is ', file)
        articles = extract_articles(file)
        #print(articles)
        article_all = article_all + articles
        if i % 100 == 0:
            print('finish number of files: ', i)
        i+=1
    
    print('number of wikipedia articles is ', len(article_all))
    
    
    
    pickle_file = open('/home/xiao/Projects/graphdescriber/data/GraphDescriber_Dataset_with_Wikification/article_original_all.pickle', "wb" )    
    pickle.dump(article_all, pickle_file)  
    pickle_file.close()
    print('done save article_all.pickle')
    
    
    mylist=[]
    file1 = open(r'/home/xiao/Projects/graphdescriber/data/GraphDescriber_Dataset_with_Wikification/article_original_all.pickle', "rb")
    mylist=pickle.load(file1) 
    print(mylist[-1])
    file1.close()
