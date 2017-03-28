#!/usr/bin/env python
# -*- coding: utf-8 -*-
import collections
import math
import argparse


class PriorityQueue(list):
    def __init__(self):
        super().__init__()
        self.pri = {}
        self.idx = {}

    def insert(self, item, priority):
        """Insert an item with a priority.

        :param item: hashable value
        :param priority: comparable value
        """
        index = len(self)
        self.append(item)
        self.pri[item] = priority
        self.idx[item] = index
        self._shift_up(index)

    def extract(self):
        """Extract the "highest" priority item.

        :return: the top item
        """
        index = 0
        self._swap(index, -1)
        item = self.pop()
        self._shift_down(index)
        del self.pri[item]
        del self.idx[item]
        return item

    def set_priority(self, item, priority):
        """Set the priority of an item.

        :param item: the item whose priority is changing
        :param priority: the new priority
        """
        current = self.pri[item]
        if current == priority:
            return

        self.pri[item] = priority
        if current < priority:
            self._shift_down(self.idx[item])
        else:
            self._shift_up(self.idx[item])

    def get_priority(self, item):
        """Return the priority of an item.

        :param item: the item whose priority will be returned
        :return: the priority of the given item
        """
        return self.pri[item]

    def _shift_up(self, index):
        # Swap upwards into place
        priority = self.pri[self[index]]
        parent = self._get_parent_index(index)
        while priority < self.pri[self[parent]]:
            self._swap(parent, index)
            index = parent
            parent = self._get_parent_index(index)

    def _shift_down(self, index):
        # Shift the max node downward
        size = len(self)
        child = self._get_min_child(index, size=size)
        while child is not None and self.pri[self[child]] < self.pri[self[index]]:
            self._swap(index, child)
            index = child
            child = self._get_min_child(index, size=size)

    def _swap(self, i, j):
        # Swap the items at the given indicies
        a, b = self[i], self[j]
        self[i], self[j] = self[j], self[i]
        self.idx[a], self.idx[b] = self.idx[b], self.idx[a]

    def _get_child_indices(self, index):
        # Return the two child indicies for the given index
        return 2 * index + 1, 2 * index + 2

    def _get_parent_index(self, index):
        # Return the parent index of the given index
        return max(0, (index + 1) // 2 - 1)

    def _get_min_child(self, index, size=None):
        # Return the index of the smaller child (or None if no children)
        size = size or len(self)
        left, right = self._get_child_indices(index)
        if left < size and right < size:
            if self.pri[self[left]] < self.pri[self[right]]:
                child = left
            else:
                child = right
        elif left < size:
            child = left
        else:  # right must be >= size, so no children
            child = None
        return child

    def __contains__(self, item):
        """Return True if item is in the queue.

        :param item: an item
        :return: True if item is in the queue
        :rtype: bool
        """
        return item in self.pri


class Graph:
    """Adjacency list representation of a graph."""

    def __init__(self, *edges):
        """Create a new graph from zero or more edges.

        Each edge must be two hashable vertices and a comparable weight value.
        That is, each vertex must be a valid dictionary key and the weights of
        any two edges must be comparable.

        :param list edges: zero or more edges, where each edge is (u, v, w)
        """
        self.edges = collections.defaultdict(dict)
        for (u, v, w) in edges:
            self.edges[u][v] = w

    @property
    def vertices(self):
        """Return all of the vertices in the graph."""
        return self.edges  # seems wrong; is in fact correct

    def get_distances(self, source):
        """Return a map of vertices to their distances from the given vertex.

        :param source: the vertex from which to find distances
        :return: a map of vertices to their distances from the source vertex
        :rtype: dict
        """
        queue = PriorityQueue()
        for vertex in self.vertices:
            distance = 0 if vertex == source else math.inf
            queue.insert(item=vertex, priority=distance)

        distances = {}
        while queue:
            u = queue[0]
            neighbors = self.edges[u].items()
            for v, w in [(v, w) for v, w in neighbors if v in queue]:
                distance = queue.get_priority(u) + w
                if distance < queue.get_priority(v):
                    queue.set_priority(item=v, priority=distance)
                    distances[v] = distance
            queue.extract()
        return distances

    @classmethod
    def from_adjacency_file(cls, filepath, symmetric=False):
        """Create a graph by parsing an adjacency file.

        Any positional and keyword arguments after the filepath are passed to
        the graph initializer.

        :param str filepath: path to the file
        :param bool symmetric: whether edge (u, v) implies edge (v, u)
        :return: a graph representation of the file
        :rtype: Graph
        """
        edges = []
        with open(filepath) as f:
            header = next(f).strip()
            n, m = (int(exp.split('=')[1]) for exp in header.split())
            u = None
            v = None
            vertices = set()
            edge_count = 0
            for line in f:
                parts = line.strip().split()
                if len(parts) == 1:
                    u = parts[0]
                    vertices.add(u)
                elif len(parts) == 2:
                    v, w = parts
                    edges.append((u, v, int(w)))
                    edge_count += 1
                    if symmetric:
                        edges.append((v, u, int(w)))
                    vertices.add(v)
            if len(vertices) != n or edge_count != m:
                print('n = {n}, m = {m}'.format(**locals()))
                print('len(vertices) = {}'.format(len(vertices)))
                print('len(edges) = {}'.format(edge_count))
                raise ValueError('Bad format: the file did not contain the '
                                 'specified number of vertices or edges. '
                                 'Please check the file and retry.')
        return cls(*edges)


def find_sum_of_sssp_distances(filepath, source='0', symmetric=True):
    """Return the sum of the single source shortest path distances."""
    graph = Graph.from_adjacency_file(filepath=filepath, symmetric=symmetric)
    distances = graph.get_distances(source='0')
    return sum(distances.values())


def main(args=None):
    parser = argparse.ArgumentParser(description='Print sum of single source '
                                                 'shortest paths')
    parser.add_argument('filepath')
    parser.add_argument('-v', '--source', default='0',
                        help='source vertex')
    parser.add_argument('-s', '--symmetric', type=bool, default=True,
                        help='whether edge (u, v) implies edge (v, u)')
    args = parser.parse_args(args)
    total = find_sum_of_sssp_distances(filepath=args.filepath,
                                       source=args.source,
                                       symmetric=args.symmetric)
    print(total)


if __name__ == '__main__':
    main()  # pragma: no cover
