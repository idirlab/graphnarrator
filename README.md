# Graph Narrator

This repository is about the project -- Graph Narrattor. Graph Narrator aims at automatically generating natural language descriptions subgraphs in a knowledge graph. The training corpus we use is Wikipedia article, and the knowledge graph we use is processed Freebase that removed reverse triples and mediator nodes.

## Dataset

The dataset can be downloaded https://anonymfile.com/n0dyl/dataset-complete.zip

The wikipedia title to Freebase entity mid mapping file can be downloaded https://anonymfile.com/89nQ6/wikititle2midnpy.zip


## Trained Models

T5-large model trained on Graph Narrator without sentence trimmer then finetuned on WebNLG dataset can be downloaded https://anonymfile.com/BXaDB/best-fmrgnoriginalwebnlg.zip


T5-large model trained on Graph Narrator with sentence trimmer then finetuned on WebNLG dataset can be downloaded https://anonymfile.com/bVqmj/best-tfmrgntrimwebnlg.zip
