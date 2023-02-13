# Graph Narrator

This repository is for the project -- Graph Narrattor. Graph Narrator aims at automatically generating natural language descriptions subgraphs in a knowledge graph. The training corpus we use is Wikipedia article, and the knowledge graph we use is processed Freebase that removed reverse triples and mediator nodes.

## Dataset

The dataset can be downloaded https://anonymfile.com/n0dyl/dataset-complete.zip

The wikipedia title to Freebase entity mid mapping file can be downloaded https://anonymfile.com/89nQ6/wikititle2midnpy.zip

## Setup
We encourage create conda enviroment to run the code.
To create the Python enviroment, run 
> ./setup_environment.sh 

## Preprocessing
Unzip the dataset folder, run
> python graphnarrator/data/generate_input_graphnarrator.py <dataset_xml_folder_path>

## Finetuning

To fine-tune the T5 model on graph narrator dataset, run 
> ./graphnarrator/finetune_t5.sh t5-<small/base/large> <gpu_id>

Example
> ./graphnarrator/finetune_t5.sh t5-large 0

To fine-tune the BART model on graph narrator dataset, run 
> ./graphnarrator/finetune_bart.sh bart-<base/large> <gpu_id>

Example
> ./graphnarrator/finetune_bart.sh bart-large 1


## Trained Models

T5-large model trained on Graph Narrator without sentence trimmer then finetuned on WebNLG dataset can be downloaded https://anonymfile.com/BXaDB/best-fmrgnoriginalwebnlg.zip


T5-large model trained on Graph Narrator with sentence trimmer then finetuned on WebNLG dataset can be downloaded https://anonymfile.com/bVqmj/best-tfmrgntrimwebnlg.zip
