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

from allennlp.predictors.predictor import Predictor
import allennlp_models.tagging



model_url = 'https://storage.googleapis.com/allennlp-public-models/coref-spanbert-large-2021.03.10.tar.gz'
#predictor = Predictor.from_path("https://storage.googleapis.com/allennlp-public-models/coref-spanbert-large-2021.03.10.tar.gz")
predictor = Predictor.from_path(model_url)  # load the model



nltk.download('punkt')



def remove_doc_string(string):
    rule = r'<doc(.*?)>'
    txts = re.findall(rule, string)
    txt = txts[0]
    string = string.replace(txt, '')
    string = string.replace('<doc>', '')
    string = string.replace('</doc>', '')
    return string



#print(remove_doc_string('<doc id="32721594" title="Barnaby Fitzpatrick" url="https://en.wikipedia.org/wiki?curid=32721594">'))



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
            link_text = a.text
            link_title = urllib.parse.unquote(a.attrs['href'])
            links.append((a, link_title, link_text))
        articles.append((wiki_id, wiki_title, wiki_url, doc, links))
        #str = a.get("href")
        #if str:
            #links.append(urllib.parse.unquote(str))
    f.close()
    return articles


def replace_href_by_title(article):
    wiki_id, wiki_title, wiki_url, doc, links = article
    doc_original = doc
    for link in links:
        a, link_title, link_text = link
        doc = str(doc).replace(str(a), link_title)
    doc = str(re.sub(r'\n\n+','\n', str(doc)))
    doc = remove_doc_string(doc)
    article_new = (wiki_id, wiki_title, wiki_url, doc_original, links, doc)
    return article_new
        


def remove_brackets_content(string):
    new_string = re.sub(u"\\(.*?\\)|\\{.*?}|\\[.*?]", "", string)
    #new_string = re.sub(' +', ' ', new_string)
    #new_string = re.sub('\s+', ' ', new_string)
    return new_string



def preprocess_before_coreference_resolution(article_text):
    
    article_text = remove_brackets_content(article_text)
    
    return article_text


def do_coreference_resolution(article_text):
    
    article_text = preprocess_before_coreference_resolution(article_text)
    
    #prediction = predictor.predict(document = article_text)
    #print(prediction['clusters'])

    #print(predictor.coref_resolved(article_text))
    
    resolved_doc = predictor.coref_resolved(article_text)
    return resolved_doc





if __name__ == "__main__":

    #print(sys.getrecursionlimit())
    
    sys.setrecursionlimit(3000)

    path = '/home/xiao/Projects/graphdescriber/data/GraphDescriber_Dataset_with_Wikification/WikipediaArticles_original/text/'
    
    cnt = 0
    filelist = get_all_files(path)
    
    np.save('filelist.npy', filelist)
    
    print('done save filelist')
    print('filelsit: ', filelist)
    
    print('number of files ', len(filelist))
    print(resource.getrlimit(resource.RLIMIT_STACK))
    print(sys.getrecursionlimit())

    max_rec = 0x100000
    resource.setrlimit(resource.RLIMIT_STACK, [0x100 * max_rec, resource.RLIM_INFINITY])
    sys.setrecursionlimit(max_rec)
    
    #filelist = ['/home/xiao/Projects/graphdescriber/data/GraphDescriber_Dataset_with_Wikification/WikipediaArticles_original/test/AA/wiki_00', '/home/xiao/Projects/graphdescriber/data/GraphDescriber_Dataset_with_Wikification/WikipediaArticles_original/test/AD/wiki_99']
    
    tqdm_files = tqdm.tqdm(filelist)
    
    
    for file in tqdm_files:
        
        wikipedia_articles_coreference_resolved = []
    
        current_article_bunch = file
        
        articles = extract_articles(current_article_bunch)
        
        print('number of articles in this file: ', len(articles))
        
        i = 0

        for article in articles:
            #article is a tuple
            #article_new is a tuple
            #article_tuple = replace_href_by_title(article)
            
            wiki_id, wiki_title, wiki_url, doc_original, links, doc = replace_href_by_title(article)
     
            article_text = preprocess_before_coreference_resolution(doc)
            
            resolved_doc = do_coreference_resolution(article_text)
            
            
            article_object = {}
            
            article_object['wiki_id'] = wiki_id
            article_object['wiki_title'] = wiki_title
            article_object['wiki_url'] = wiki_url
            article_object['wiki_article_original'] = doc_original
            article_object['links_in_article'] = links
            article_object['article_text_replace_href_by_title'] = doc
            article_object['article_text_before_coref'] = article_text
            article_object['article_text_coref_resolved'] = resolved_doc
            
            
            print('done number of articles: ', i)
            
            #print(article_object)
            
            i+=1
            wikipedia_articles_coreference_resolved.append(article_object)
            #print(article_tuple1)
            #break
            
        
        pickle_file = open('/home/xiao/Projects/graphdescriber/data/GraphDescriber_Dataset_with_Wikification/wikipedia_articles_coreference_resolved/' + 'wiki_coreference_resolved_' + str(cnt) +'.pickle', "wb" )    
        pickle.dump(wikipedia_articles_coreference_resolved, pickle_file)  
        pickle_file.close()
        print('done save wikipedia_articles_coreference_resolved.pickle', cnt)
       
        cnt += 1
        tqdm_files.set_description("Processing %s" % file)
    
    
  
    print('done all files')
    
    
    
    mylist=[]
    file = open(r'/home/xiao/Projects/graphdescriber/data/GraphDescriber_Dataset_with_Wikification/wikipedia_articles_coreference_resolved/wiki_coreference_resolved_1.pickle', "rb")
    mylist=pickle.load(file) 
    print(mylist[0].keys())
    
    print('number of articles', len(mylist))
    
    print(list(mylist[1].values())[0])
    print("____________"*8)
    print(list(mylist[1].values())[1])
    print("____________"*8)
    print(list(mylist[1].values())[2])
    print("____________"*8)
    print(list(mylist[1].values())[3])
    print("____________"*8)
    print(list(mylist[1].values())[4])
    print("____________"*8)
    print(list(mylist[1].values())[5])
    print("____________"*8)
    print(list(mylist[1].values())[6])
    print("____________"*8)
    print(list(mylist[1].values())[7])
    print("____________"*8)

    

    
                
            