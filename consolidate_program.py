#!/usr/bin/env python
# coding: utf-8

from sentence_splitter import SentenceSplitter, split_text_into_sentences
from collections import defaultdict
import urllib.parse
import requests
import json
import time
import os
import itertools



class WikiHandler(object):
    def __init__(self, wikipedia_to_kg_mapping_file_filename, edge_mapping_file_filename):
        self.wikipedia_to_kg_mapping_file_filename = wikipedia_to_kg_mapping_file_filename
        self.edge_mapping_file_filename = edge_mapping_file_filename
    
    def split_wikipedia_article_to_sentences(self, filename):
        #input: file name with its path from wikiextrctor result (each file has multiple wikipedia articles)
        #output: a sentences list, the element of the big list is also a list, consists of sentences from each paragraph
        splitter = SentenceSplitter(language='en')
        sentences = []
        article = []
        title = ""
        f = open(filename, encoding = 'utf8', errors='ignore')
        for line in f:
            if line.startswith('<doc id='):
                ### this is a new article
                new_article = True
            elif line.startswith('</doc>'):
                article.clear()
            else:
                if new_article == True:
                    title = line
                    #print('The title is '+ title)
                    new_article = False
                elif not line.isspace():
                    ### this is a new paragraph
                    #print("new paragraph\n")
                    sentences.append(splitter.split(text=line))
        f.close()
        return sentences

    def get_wikilinks_name_from_sentence(self, sentence):
        #input is a sentence
        #output the wikilinks in the sentence
        links_in_sentence = []
        s = sentence.split('<a href="')
        s.pop(0)
        #print(s)
        for ss in s:
            ss = urllib.parse.unquote(ss.split('"')[0])
            links_in_sentence.append(ss)
        return links_in_sentence


    def get_entity_from_wikilink_name(self, wikipedia_title):
        #input: the mapping json file (wikipedia title to knowledge graph entity id or entity name) -- a dictionary, and the wikilink name
        #output: if the title in the mapping file, output the knowedge graph entity id or entity name, if not, return ''
        wiki_to_kg = json.load(open(self.wikipedia_to_kg_mapping_file_filename, encoding='utf8', errors='ignore'))
        if wikipedia_title in wiki_to_kg:
            entity = wiki_to_kg[wikipedia_title]
        else:
            entity = ''
        return entity

    def get_edge_between_two_entities(self, entity_pair):
        #the edge mapping file is a json dictionary, the key of it is 'entity1' + '' + 'entity2', the value is edge name or edge id
        #input: [entity1, entity2],or (entity1, entity2), and edge_mapping_file_filename
        #output: the edge id or edge name between the two entities
        edge_mapping = json.load(open(self.edge_mapping_file_filename, encoding='utf8', errors='ignore'))
        if (entity_pair[0] +' '+ entity_pair[1]) in edge_mapping:
            edge = edge_mapping[entity_pair[0] +' '+ entity_pair[1]]
        
        elif (entity_pair[1] +' '+ entity_pair[0]) in edge_mapping:
            edge = edge_mapping[entity_pair[1] +' '+ entity_pair[0]]
        else:
            edge = ''
      
        return edge

    def get_entity_pairs_from_entity_list(self, entity_list):
        #input: a list of entities
        #output: the combinations of entity pairs
        length = len(entity_list)
        if length > 1:
            entity_pairs = list(itertools.combinations(entity_list,2))
        else:
            entity_pairs = []
        
        return entity_pairs


#Test
wikipedia_to_kg_mapping_file_filename = 'D:/gd_dataset/freebase_sentences_required_files/wikipedia_to_freebase.json'
edge_mapping_file_filename = 'D:/gd_dataset/freebase_sentences_required_files/freebase_edge_mapping.json'
example = WikiHandler(wikipedia_to_kg_mapping_file_filename, edge_mapping_file_filename)
sentences = example.split_wikipedia_article_to_sentences('wiki_99')
print(sentences)
for sentence in sentences:
    for ss in sentence:
        wiki_links = example.get_wikilinks_name_from_sentence(ss)
        print(wiki_links)
    
wikipedia_title = 'Foreign minister of Angola'
print(example.get_entity_from_wikilink_name(wikipedia_title))


entity_list_1 = ['Jenny', 'Danny', 'Ming']
entity_list_2 = ['Jenny']
print(example.get_entity_pairs_from_entity_list(entity_list_1))
print(example.get_entity_pairs_from_entity_list(entity_list_2))


entity_pair = ['36159754', '41359298']
print(example.get_edge_between_two_entities(entity_pair))        
        
        





