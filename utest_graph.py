import unittest

from graph import Graph


class TestGraph(unittest.TestCase):

    def setUp(self):
        self.graph = Graph()

    def test_add_many_vertices(self):
        self.graph.add_to_graph('A', 'B')
        self.graph.add_to_graph('B', 'C')
        self.graph.add_to_graph('C', 'A')
        self.assertEqual(self.graph.get_name_vertices(), ['A', 'B', 'C'])

    def test_add_one(self):
        self.graph.add_to_graph('D', 'D')
        self.assertEqual(self.graph.get_name_vertices(), ['D'])

    def test_add_int(self):
        self.graph.add_to_graph(2, 3)
        self.graph.add_to_graph(1, 3)
        self.assertEqual(self.graph.get_name_vertices(), [1, 2, 3])

    def test_add_nothing(self):
        self.graph.add_to_graph('', '')
        self.assertEqual(self.graph.get_name_vertices(), [])

    def test_multiple_add(self):
        self.graph.multiple_add_to_graph([
            ['A', 'B'],
            ['B', 'C'],
            ['C', 'A']
        ])
        self.assertEqual(self.graph.get_name_vertices(), ['A', 'B', 'C'])

    def test_multiple_add_int(self):
        self.graph.multiple_add_to_graph([[1, 2], [2, 1]])
        self.assertEqual(self.graph.get_name_vertices(), [1, 2])

    def test_multiple_add_one(self):
        self.graph.multiple_add_to_graph([
            ['A', 'A']
        ])
        self.assertEqual(self.graph.get_name_vertices(), ['A'])

    def test_multiple_add_nothing(self):
        self.graph.multiple_add_to_graph([])
        self.assertEqual(self.graph.get_name_vertices(), [])

    def test_connections(self):
        self.graph.add_to_graph('A', 'R')
        self.graph.add_to_graph('A', 'B')
        self.assertEqual(self.graph.get_vertices()[0].get_name_of_connections(), ['B', 'R'])

    def test_empty_connections(self):
        self.graph.add_to_graph('A', 'R')
        self.graph.add_to_graph('A', 'B')
        self.assertEqual(self.graph.get_vertices()[1].get_name_of_connections(), [])

    def test_parse_vertices(self):
        self.graph.parse_graph('A-B, fail_vertex,\n B-C, \t C-A')
        self.assertEqual(self.graph.get_name_vertices(), ['A', 'B', 'C'])

    def test_parse_vertices_empty(self):
        self.graph.parse_graph(' - , -fail_vertex,\n B-\r , \t-A')
        self.assertEqual(self.graph.get_name_vertices(), [])

    def test_adjacency_matrix(self):
        self.graph.parse_graph('A-B,B-C,C-A')
        self.assertEqual(
            self.graph.create_adjacency_matrix()
            , [
                [0, 1, 0],
                [0, 0, 1],
                [1, 0, 0]
            ])

    def test_adjacency_matrix_hard(self):
        self.graph.parse_graph('??-??, ??-??, ??-??, ??-??,'
                               + '??-??, ??-??, ??-??, ??-??,'
                               + '??-??, ??-??, ??-??, ??-??')
        self.assertEqual(
            self.graph.create_adjacency_matrix()
            , [
                [0, 1, 1, 0, 0, 0, 0],
                [0, 0, 0, 1, 1, 0, 0],
                [0, 1, 0, 1, 0, 1, 1],
                [0, 0, 0, 0, 1, 0, 1],
                [0, 0, 0, 0, 0, 0, 1],
                [0, 0, 0, 0, 0, 0, 1],
                [0, 0, 0, 0, 0, 0, 0],
            ])

    def test_dfs_easy(self):
        self.graph.parse_graph('A-B, A-C, B-D, B-E, C-F, E-F')

        self.assertEqual(
            self.graph.dfs("A"),
            ['A', 'B', 'D', 'E', 'F', 'C']
        )

    def test_vertices_images(self):
        self.graph.parse_graph('A-C, A-D, B-A, B-D')
        self.assertEqual(
            self.graph.get_vertices_image(),
            {
                'A': ['C', 'D'],
                'B': ['A', 'D'],
                'C': [],
                'D': []
            }
        )

    def test_vertices_preimages(self):
        self.graph.parse_graph('A-C, A-D, B-A, B-D')
        self.assertEqual(
            self.graph.get_vertices_image(),
            {
                'A': ['C', 'D'],
                'B': ['A', 'D'],
                'C': [],
                'D': []
            }
        )

    def test_vertex_is_isolated(self):
        self.graph.parse_graph('A-C, A-D, B-A')
        self.graph.add_one_vertex('F')
        self.assertEqual(self.graph.is_isolated_vertex('F'), True)

    def test_vertex_is_not_isolated(self):
        self.graph.parse_graph('A-C, A-D, B-A')
        self.assertEqual(self.graph.is_isolated_vertex('A'), False)


if __name__ == '__main__':
    unittest.main()
