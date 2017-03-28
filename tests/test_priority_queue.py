#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
import random

import pyjkstra


N = 10
ITEMS = list('abcdefghij')[:N]
PRIORITIES = list(range(1, 1 + N))
DATA = list(zip(ITEMS, PRIORITIES))


class CommonTestsMixin:
    def test_first_item_is_lowest_priority(self):
        self.assertEqual(self.q[0], ITEMS[0])

    def test_extract_yields_sorted_order(self):
        extracted = []
        while self.q:
            extracted.append(self.q.extract())
        self.assertEqual(extracted, ITEMS)


class PriorityQueueTest(unittest.TestCase):
    def setUp(self):
        self.q = pyjkstra.PriorityQueue()
        self.data = list(self._get_data())
        for i, p in self.data:
            self.q.insert(item=i, priority=p)


class OrderedTests(CommonTestsMixin, PriorityQueueTest):
    def _get_data(self):
        yield from DATA

    def test_is_sorted(self):
        self.assertEqual(self.q, ITEMS)

    def test_decrease_key(self):
        # Make the first item the highest priority (least priority value)
        first, *__, last = self.q
        least = min(self.q.pri.values())
        self.q.set_priority(item=last, priority=least - 1)
        # The previously last item should now be first
        self.assertEqual(self.q[0], last)

    def test_increase_key(self):
        # Make the first item the lowest priority (greatest priority value)
        first, *__, last = self.q
        greatest = max(self.q.pri.values())
        self.q.set_priority(item=first, priority=greatest + 1)
        # The previously first item should now be last
        ordered = []
        while self.q:
            ordered.append(self.q.extract())
        self.assertEqual(ordered[-1], first)


class ReversedTests(CommonTestsMixin, PriorityQueueTest):
    def _get_data(self):
        return reversed(DATA)


class ShuffledTests(CommonTestsMixin, PriorityQueueTest):
    def _get_data(self):
        data = list(DATA)
        random.shuffle(data)
        yield from data
