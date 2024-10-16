# Graph Narrator

Graph Narrator aims at automatically generating natural language descriptions of subgraphs in knowledge graphs. The training corpus we use is Wikipedia article, and the knowledge graph we use is processed Freebase in which reverse triples and mediator nodes are removed.

## Dataset

The dataset can be downloaded from [here](https://drive.google.com/file/d/1tpHYWRyoG4nU2FWFVGELPFKJrQk-8-yq/view?usp=drive_link)

The Wikipedia title to Freebase entity mid mapping file can be downloaded from [here](https://drive.google.com/file/d/1CZDhUfmxsDBYqn-P2uNoBJ0X7iIaJelh/view?usp=drive_link)

## Setup

We recommend createv Conda enviroment to run the code.
To create the Conda enviroment, run

> ./setup_environment.sh

## Preprocessing

Unzip the dataset folder, run

> python graphnarrator/data/generate_input_graphnarrator.py dataset_xml_folder_path

## Finetuning

To fine-tune the T5 model on graph narrator dataset, run

> ./graphnarrator/finetune_t5.sh t5-<small/base/large> gpu_id

Example

> ./graphnarrator/finetune_t5.sh t5-large 0

To fine-tune the BART model on graph narrator dataset, run

> ./graphnarrator/finetune_bart.sh bart-<base/large> gpu_id

Example

> ./graphnarrator/finetune_bart.sh bart-large 1

## Decoding

To decode the T5 model that has been fine-tuned on graph narrator dataset, run

> ./graphnarrator/test_t5.sh fine-tuned_model_path gpu_id

Example

> ./graphnarrator/test_t5.sh /graphnarrator/t5-large-trim/best_tfmr 2

To decode the BART model that has been fine-tuned on graph narrator dataset, run

> ./graphnarrator/test_bart.sh fine-tuned_model_path gpu_id

Example

> ./graphnarrator/test_bart.sh /graphnarrator/bart-large-trim/best_tfmr 3

## Trained Models

The GNST-T5 model (T5-large model finetuned on GraphNarrative dataset with sentence trimming) can be downloaded from
[here](https://drive.google.com/drive/folders/1-SntceYhJ2LaBSHPkUKXy2Pv_EFSqsFM)

The GN-T5 model (T5-large model finetuned on GraphNarrative without sentence trimming) can be downloaded from
[here](https://drive.google.com/drive/folders/17Xy5nLGnPYJLrdIevWeZMA1c01cpuzpV)

The T5-large model trained on Graph Narrator without sentence trimmer and then finetuned on WebNLG dataset can be downloaded from
[here](https://drive.google.com/drive/folders/1QZTKQjROrDX7Qf3H5Ug7c7JHHnrBsD-N?usp=sharing)

The T5-large model trained on Graph Narrator with sentence trimmer and then finetuned on WebNLG dataset can be downloaded from
[here](https://drive.google.com/drive/folders/1p14bu_eUMPVXcvv-w4dJA8fDFmufdJ9r?usp=drive_link)

# Inference Documentation for T5 Model

This section provides details on how to perform inference using the T5 model (`graphnarrator_webnlg.ckpt`). It includes information on input format and example graphs to help guide the inference process.

## Inference with the T5 Model

- To perform inference using the T5 model, prepend the input with `"translate graph to English"`.
- The input graph should follow the format `<H> <R> <T>`, where:
  - `<H>`: Head entity
  - `<R>`: Relation
  - `<T>`: Tail entity

### Example Graph for Inference

- An example graph input for inference is:

  ```text
  translate graph to English <H> Paris <R> is the capital of <T> France
  ```

Head Entity (<H>): Paris
Relation (<R>): is the capital of
Tail Entity (<T>): France```

### Additional Notes

Ensure the input format is correct for the model to generate the desired output.
The head (<H>), relation (<R>), and tail (<T>) entities should be clearly defined.
Always start the input with "translate graph to English" to indicate the type of inference required.

### Requirements

Python 3.6+
PyTorch
Transformers (transformers library from Hugging Face).

from the graphnarrator folder,

```bash
./setup_environment.sh
```
