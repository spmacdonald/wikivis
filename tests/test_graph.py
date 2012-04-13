import unittest

from wikivis.graph import WikiGraph

class TestWikiGraph(unittest.TestCase):

    def test_insert_edge(self):
        g = WikiGraph(2)
        g.insert_edge(0, 1)

    def test_size(self):
        g = WikiGraph(2)
        self.assertEqual(2, len(g))

    def test_successors(self):
        g = WikiGraph(10)
        edges = [(1, 0), (2, 0), (3, 1), (4, 1), (5, 2), (6, 1), (7, 0), (8, 0), (9, 8)]
        for e in edges:
            g.insert_edge(*e)

        self.assertEqual([], g.successors(0))
        self.assertEqual([0], g.successors(1))
        self.assertEqual([0], g.successors(2))
        self.assertEqual([1], g.successors(3))
        self.assertEqual([1], g.successors(4))

    def test_predecessors(self):
        g = WikiGraph(10)
        edges = [(1, 0), (2, 0), (3, 1), (4, 1), (5, 2), (6, 1), (7, 0), (8, 0), (9, 8)]
        for e in edges:
            g.insert_edge(*e)

        self.assertEqual([1, 2, 7, 8], g.predecessors(0))
        self.assertEqual([3, 4, 6], g.predecessors(1))
        self.assertEqual([5], g.predecessors(2))
        self.assertEqual([], g.predecessors(3))
        self.assertEqual([9], g.predecessors(8))
