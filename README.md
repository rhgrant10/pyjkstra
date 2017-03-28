Pyjkstra
===============================

This is a Python implementation of Dijkstra's algorithm for finding single-source shortest paths.

Dependencies
------------

 * python >= 3.0

Features
--------

 * `PriorityQueue` class - a binary min-heap implementation of a priority queue
 * `Graph` class - a hashmap-based implementation of a graph built from a list of edges constructed from a list of edges, each represented as a tuple of two vertices and an edge weight
    - `get_distances(source)` - capable of calculating single-source shortest paths
    - `from_adjacency_file(filename)` - build a graph by parsing an input file (two such files are included in the repo as examples: `sample1000.txt` and `sample25000.txt`)

Usage
-----

From the command line, simply install into a virtual environment and run:

```console
$ cd <project_dir>
$ pyvenv env
$ source env/bin/activate
$ pip install -e .
$ pyjkstra sample25000.txt
10721073
$ 
```

License
-------

GNU General Public License v3 (GPLv3)

Authors
-------

 - Robert Grant <rhgrant10@gmail.com>
