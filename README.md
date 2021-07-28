# Graph Describer

This repository is about the idir project -- graphnarrattor. What it does is to generate descriptions for a subgraph in knowledge graph.
Now it is on the first stage, patterns to describe an edge in knowledge graph.
The knowledge graph we use is wikidata and freebase.

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
