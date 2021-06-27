"""
    Module for working with graph
"""

import base64  # noqa: I201, I100
import re  # noqa: I201, I100

from graphviz import Digraph  # noqa: I201, I100


class Vertex:
    """ Class for work and storing data of the vertex of the graph """
    def __init__(self, name):
        self.name = name
        self.connections = []
        self.color = None

    def get_name_of_connections(self):
        """ get name of connections with this vertex (str) not objects """
        return [x.name for x in self.connections]

    def find_connection(self, name):
        """
            if find connection with that name - return this,
            else return False
        """
        for item in self.connections:
            if item.name == name:
                return item
        return False

    def add_connection(self, connection):
        """ add NEW connection with this vertex, if vertex is exist nothing happens """
        if not self.find_connection(connection):
            self.connections.append(connection)


class Graph:
    """ Class for working and displaying the graph """
    def __init__(self):
        self.vertices = []
        self.bridges = []

    def get_vertices(self) -> object:
        """ Return all vertices on this graph """
        return self.vertices

    def get_name_vertices(self):
        """ Return all vertices names on this graph """
        return [x.name for x in self.vertices]

    def get_bridges(self) -> list:
        """ Return list of bridges between of vertices"""
        return self.bridges

    def find_vertex_in_graph(self, name):
        """
            Get name of vertex and return the vertex (object) if it exist
            else return None

            !!! TODO:This method may be changed the find algorithm!!!
        """
        for item in self.vertices:
            if item.name == name:
                return item
        return None

    def get_or_create_island(self, name):
        """
            get name of vertex and return it if vertex find
            else create vertex with this name

            !!!
                TODO: This method may be changed algorithm the find vertex
                and will be supplemented with arguments that may be
                needed in subsequent algorithms
            !!!
        """
        for item in self.vertices:
            if item.name == name:
                return item

        island = Vertex(name)
        self.vertices.append(island)
        return island

    def parse_graph(self, data):
        """
            Parsed graph from the received string (used on the site)
        """
        temp = re.sub(r'([\r\n\s\t]+)', '', data).split(',')
        temp = list(set(temp))
        temp = sorted(list(filter(lambda br: len(br) == 2,
                                  [br.split('-') for br in temp])),
                      key=lambda x: (x[0], x[1]))

        for bridge in temp:
            self.add_to_graph(bridge[0], bridge[1])

    def add_to_graph(self, vertex1, vertex2):
        """
            Get two vertices and create them if there are none.
            Add vertex2 to connections vertex1.
            Vertex2 if it was created has no connections
            but will be added to graph.
        """
        isl1 = self.get_or_create_island(vertex1)
        isl2 = self.get_or_create_island(vertex2)

        isl1.add_connection(isl2)
        self.vertices = sorted(self.vertices, key=lambda x: x.name)

        self.bridges.append([vertex1, vertex2])
        self.bridges = sorted(
            self.bridges,
            key=lambda x: (x[0], x[1])
        )

    def calc_degree(self):
        """ Calculates the degree of the vertices of the graph"""
        return {x.name: len(x.connections) for x in self.vertices}

    def create_adjacency_matrix(self):
        """ Create graph adjacency matrix """
        res = [[0 for _ in self.get_name_vertices()] for _ in self.get_name_vertices()]
        for column, vertex in enumerate(self.get_name_vertices()):
            for row, intersection in enumerate(self.get_name_vertices()):
                crossed_vertex = self.find_vertex_in_graph(intersection)
                if vertex in crossed_vertex.get_name_of_connections():
                    res[row][column] = 1
        return res

    def adjacency_matrix_to_table(self):
        """
            Converts adjacency matrix to tabular form.
            Immediately uses the creation method so no
            data transfer is required.

            !!! TODO: remake the method so that it can accept a matrix
        """
        temp = self.create_adjacency_matrix()
        res = [[''] + list(self.get_name_vertices())] + \
              [[item] + temp[i] for i, item in enumerate(self.get_name_vertices())]
        return res

    def create_incidence_matrix(self):
        """ Create graph incidence matrix """
        res = [[0 for _ in range(sum(list(map(lambda x: len(x.connections), self.vertices))))]
               for _ in self.get_name_vertices()]

        for i in range(len(self.get_name_vertices())):
            for j, bridge in enumerate(self.bridges):
                if list(self.get_name_vertices())[i] == bridge[0]:
                    res[i][j] = 1
                elif list(self.get_name_vertices())[i] == bridge[1]:
                    res[i][j] = -1
        return res

    def incidence_matrix_to_table(self):
        """
            Converts incidence matrix to tabular form.
            Immediately uses the creation method so no
            data transfer is required.

            !!! TODO: remake the method so that it can accept a matrix
            !!! TODO: correctly display degree for oriental graph
        """
        temp = self.create_incidence_matrix()
        res = list([[''] + ['q' + str(i + 1)
                            for i, _ in enumerate(temp[0])]])
        res += [[item] + temp[i] for i, item in enumerate(self.get_name_vertices())]
        return res

    def get_vertices_image(self):
        """ Return vertices image """
        return {x.name: x.get_name_of_connections() for x in self.vertices}

    def get_vertices_preimage(self):
        """ Return vertices pre-image """
        res = {x: [] for x in self.get_name_vertices()}
        for vertex in self.get_name_vertices():
            for intersection in self.get_name_vertices():
                crossed_vertex = self.find_vertex_in_graph(intersection)
                if vertex in crossed_vertex.get_name_of_connections():
                    res[vertex].append(intersection)
        return res

    def draw_graph(self):
        """ Creates a graph for displaying in the site) """
        file = Digraph('graph', filename='static/fsm.gv',
                       node_attr={'color': 'lightblue2',
                                  'style': 'filled', 'shape': 'circle'})
        file.attr(rankdir='A', size='1000')

        file.edges(self.bridges)
        return file

    @staticmethod
    def graph_image_to_bytes(fig):
        """ Convert image for bytes """
        temp_file = fig.pipe(format='png')
        encoded = base64.b64encode(temp_file).decode('utf-8')
        return encoded

    def dfs(self, bridge):
        """ depth-first search for graph """
        pass

# g = Graph()
# g.parseGraph('А-Б, А-В, В-Б, В-Ж, В-Е, В-Г, Б-Д, Б-Г, Г-Д, Д-Ж, Г-Ж, Е-Ж')
