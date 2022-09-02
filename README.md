# Search Engine

Implementing a search engine in three phases.
1.binary search
2.ranked search which tf-idf was used
3.champion list (using 30 best results by tf-idf)
Also, it plots the zipf and heaps to compares the states before and after omitting the stop-words.

\*Especial point
All these parts were also implemented with elastic search!
Using bulk index and k-nearest neighbors and tf-idf all with elastic search and it was way faster

## Getting Started

### Datasets

There are two datasets. one has 4k news and the other one has 46k news for clustering. These datasets are used for KNN in elastic search.
There is also another dataset consisting of 12k news. This is used for binary search, ranked search and the champion list.

## Usage

You enter your input. It will search based on your choice from
1.binary search
2.ranked search
3.champion list
and returns you 5 most related results.

### Output

If there is no result for your search, it will inform you.
Otherwise, it will return the 5 most similar results and depicts the URL and the topic.
