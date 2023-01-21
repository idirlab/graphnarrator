# Graph Narrator

This repository is about the project -- Graph Narrattor. Graph Narrator aims at automatically generating natural language descriptions for a subgraph in knowledge graph. The training corpus we use is Wikipedia article, and the knowledge graph we use is processed Freebase that removed reverse triples and mediator nodes.

## Dataset

The dataset can be downloaded here  https://anonymfile.com/n0dyl/dataset-complete.zip



https://anonymfile.com/89nQ6/wikititle2midnpy.zip

## Data Processing Workflow

``` sh
For each Wikipedia article:
    Replace ancor text by wikipedia title
    Do Coreference Resolution  
        (to solve the problem of many sentences start from ‘He’, ‘She’ .)
    Do Wikification (replace mentions by Wikipedia title)
        (to detect as many as entities as possible to make the input graph and groundtruth sentence more matched.)
    Split the article into sentences
    For each sentence:
        Map Wikipedia title of the entity into Freebase entity
        (use the newly collected mapping file)
        For each entity pair:
            Detect edge between them
            (maybe do something to make the edge detection more accurate)
```

The entities and edges consist of the input subgraph, the sentence as the groundtruth sentence 

## Neo4j login
Username: neo4j

Password: idir
