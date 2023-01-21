#!/bin/bash

if [ "$#" -lt 2 ]; then
  echo "./train_graphnarrator.sh <model> <gpu_id>"
  exit 2
fi

if [[ ${1} == *"t5"* ]]; then
  bash graphnarrator/finetune_t5.sh ${1} ${2}
fi
if [[ ${1} == *"bart"* ]]; then
  bash graphnarrator/finetune_bart.sh ${1} ${2}
fi








