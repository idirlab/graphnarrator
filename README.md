# Graph Narrator

This repository is about the project -- Graph Narrattor. It is the implementation of our paper Natural Language Generation from Large-Scale Open-Domain
Knowledge Graphs which is submitted to ACL 2023. Graph Narrator aims at automatically generating natural language descriptions for a subgraph in knowledge graph. The training corpus we use is Wikipedia article, and the knowledge graph we use is processed Freebase that removed reverse triples and mediator nodes.

## Raw data path

- Wikipedia article: /home/xiao/Projects/graphdescriber/data/GraphDescriber_Dataset_with_Wikification/WikipediaArticles_original/text
- TODO: add entity mapping path

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
