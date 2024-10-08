import unittest
from graph import *

class TestList(unittest.TestCase):

    def test_01(self):
        g = Graph('test1.txt')
        self.assertEqual([['v1', 'v2', 'v3', 'v4', 'v5'], ['v6', 'v7', 'v8', 'v9']], g.conn_components())
        self.assertTrue(g.is_bipartite())
        self.assertEqual(['v1', 'v2', 'v3', 'v4', 'v5', 'v6', 'v7', 'v8', 'v9'], g.get_vertices())
        self.assertIsNone(g.get_vertex('notingraph'))
        
    def test_02(self):
        g = Graph('test2.txt')
        self.assertEqual(g.conn_components(), [['v1', 'v2', 'v3'], ['v4', 'v6', 'v7', 'v8']])
        self.assertFalse(g.is_bipartite())

    def test_owntest1(self):
        g = Graph('owntest1.txt')
        # 0(B) - 1(R)
        # |       |
        # 2(R) - 3(B)
        # |       |
        # 4(B) - 5(R)
        self.assertEqual(g.conn_components(), [['0', '1', '2', '3', '4', '5']])
        self.assertTrue(g.is_bipartite())

    def test_owntest2(self):
        g = Graph('owntest2.txt')
        # 0(B) - 1(R)
        # |       |
        # 2(R) - 3(B)
        #   \     /
        #     4 (B)
        self.assertEqual(g.conn_components(), [['0', '1', '2', '3', '4']])
        self.assertFalse(g.is_bipartite())

    def test_owntest3(self):
        g = Graph('owntest3.txt')
        # A (b) - B (r)         F (b) - G (r)       Z (b) - Y (r)
        # |       |               |
        # C (r) - 3(B)          H (r)
        # |                       |
        # D (b)                 I (b)
        self.assertEqual(g.conn_components(), [['A', 'B', 'C', 'D'], ['F', 'G', 'H', 'I'], ['Y', 'Z']])
        self.assertTrue(g.is_bipartite())

    def test_owntest4(self):
        g = Graph('owntest4.txt')
        # A (b) - B (r)         F (b) - G (r)
        # |       |               |
        # C (r) - 3(B)          H (r) - J (b)
        # |                       |       |
        # D (b)                 I (b)     |
        #                         |       |
        #                       Y (r)     |
        #                         |      /
        #                       Z (b) --/
        self.assertEqual(g.conn_components(), [['A', 'B', 'C', 'D'], ['F', 'G', 'H', 'I', 'J', 'Y', 'Z']])
        self.assertFalse(g.is_bipartite())

    def test_owntest5_triangle(self):
        g = Graph('owntest5.txt')
        # v5 (B) - v4 (R)
        #    \     /
        #    v3 (R)

        self.assertEqual(g.conn_components(), [['v3', 'v4', 'v5']])
        self.assertFalse(g.is_bipartite())
        g.add_vertex('v6')
        self.assertEqual(g.conn_components(), [['v3', 'v4', 'v5'], ['v6']])
        g.add_edge('v6', 'v4')

        # v5 (B) - v4 (R) - v6 (B)
        #    \     /
        #    v3 (R)
        self.assertEqual(g.conn_components(), [['v3', 'v4', 'v5', 'v6']])
        self.assertFalse(g.is_bipartite())
    def test_owntest6_self(self):
        g = Graph('owntest6.txt')
        self.assertEqual(g.conn_components(), [['a']])

    def test_graph_adding(self):
        g = Graph("empty.txt")
        g.add_vertex('a')
        g.add_vertex('b')
        g.add_edge('a', 'b')

        self.assertEqual(g.conn_components(), [['a', 'b']])
        self.assertTrue(g.is_bipartite())
        g.add_vertex('c')
        g.add_edge('c', 'b')
        self.assertTrue(g.is_bipartite())
        self.assertEqual(g.conn_components(), [['a', 'b', 'c']])
        g.add_edge('a', 'c')
        self.assertFalse(g.is_bipartite())

        self.assertEqual(['a','b','c'], g.get_vertices())



if __name__ == '__main__':
   unittest.main()
