#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import unittest

import pyjkstra


SAMPLES_DIR = os.path.dirname(__file__)


class ShortestPathTest(unittest.TestCase):
    def setUp(self):
        edges = [
            (0, 1, 10),
            (1, 0, 10),
            (0, 2, 15),
            (2, 0, 15),
            (1, 2, 2),
            (2, 1, 2),
        ]
        graph = pyjkstra.Graph(*edges)
        self.distances = graph.get_distances(source=0)

    def test_shortest_path_to_vertex_is_correct(self):
        self.assertEqual(self.distances[2], 12)

    def test_shortest_paths_sum_is_correct(self):
        self.assertEqual(sum(self.distances.values()), 22)


class RealDataTest(unittest.TestCase):
    def test_1000_vertex_graph(self):
        filepath = os.path.join(SAMPLES_DIR, 'sample1000.txt')
        answer = pyjkstra.find_sum_of_sssp_distances(filepath)
        self.assertEqual(answer, 625349)

    def test_25000_vertex_graph(self):
        filepath = os.path.join(SAMPLES_DIR, 'sample25000.txt')
        answer = pyjkstra.find_sum_of_sssp_distances(filepath)
        self.assertEqual(answer, 10721073)

    def test_vertex_and_edge_miscount(self):
        filepath = os.path.join(SAMPLES_DIR, 'sampleBad.txt')
        with self.assertRaises(ValueError):
            pyjkstra.find_sum_of_sssp_distances(filepath)
