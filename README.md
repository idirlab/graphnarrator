# Graph Narrator

Graph Narrator aims at automatically generating natural language descriptions of subgraphs in knowledge graphs. The training corpus we use is Wikipedia article, and the knowledge graph we use is processed Freebase in which reverse triples and mediator nodes are removed.

## Dataset

The dataset can be downloaded from https://ufile.io/txdyxa6m 

The Wikipedia title to Freebase entity mid mapping file can be downloaded from https://ufile.io/wdfefvfq

## Setup
We recommend create Conda enviroment to run the code.
To create the Conda enviroment, run 
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

## Decoding

To decode the T5 model that has been fine-tuned on graph narrator dataset, run 
> ./graphnarrator/test_t5.sh <fine-tuned_model_path> <gpu_id>

Example
> ./graphnarrator/test_t5.sh /graphnarrator/t5-large-trim/best_tfmr 2


To decode the BART model that has been fine-tuned on graph narrator dataset, run 
> ./graphnarrator/test_bart.sh <fine-tuned_model_path> <gpu_id>

Example
> ./graphnarrator/test_bart.sh /graphnarrator/bart-large-trim/best_tfmr 3


## Trained Models
The T5-large model trained on Graph Narrator dataset without sentence trimmer can be downloaded from
https://ufile.io/6t6825sr

The T5-large model trained on Graph Narrator dataset with sentence trimmer can be downloaded from
https://ufile.io/257iqiqc

The T5-large model trained on Graph Narrator without sentence trimmer and then finetuned on WebNLG dataset can be downloaded from https://ufile.io/hxykjsrl

The T5-large model trained on Graph Narrator with sentence trimmer and then finetuned on WebNLG dataset can be downloaded from 
https://ufile.io/50p9dp1c
