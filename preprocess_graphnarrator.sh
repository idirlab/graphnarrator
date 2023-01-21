#!/bin/bash

if [ "$#" -lt 1 ]; then
  echo "./preprocess_graphnarrator.sh <dataset_folder>"
  exit 2
fi

python graphnarrator/data/generate_input_graphnarrator.py ${1}




