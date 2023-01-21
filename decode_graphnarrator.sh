#!/bin/bash

if [ "$#" -lt 3 ]; then
  echo "./decode_graphnarrator.sh <model> <checkpoint> <gpu_id>"
  exit 2
fi

if [[ ${1} == *"bart"* ]]; then
  bash graphnarrator/test_bart.sh ${1} ${2} ${3}
fi
if [[ ${1} == *"t5"* ]]; then
  bash graphnarrator/test_t5.sh ${1} ${2} ${3}
fi








