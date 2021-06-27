import base64  # noqa: I201, I100
import re  # noqa: I201, I100

from graphviz import Digraph  # noqa: I201, I100


class Vertex(object):
    def __init__(self, name):
        self.name = name
        self.connections = []
        self.color = None

    def get_name_of_connections(self):
        return [x.name for x in self.connections]

    def find_connection(self, name):
        for item in self.connections:
            if item.name == name:
                return item
        return False

    def add_connection(self, c):
        if not self.find_connection(c):
            self.connections.append(c)


class Graph(object):
    def __init__(self):
        self.vertexes = []
        self.bridges = []

    def get_vertexes(self):
        return self.vertexes

    def get_name_vertexes(self):
        return [x.name for x in self.vertexes]

    def get_bridges(self):
        return self.bridges

    def find_vertex_in_graph(self, name):
        for item in self.vertexes:
            if item.name == name:
                return item

        return None

    def get_or_create_island(self, name):
        for item in self.vertexes:
            if item.name == name:
                return item

        island = Vertex(name)
        self.vertexes.append(island)
        return island

    def parse_graph(self, data):
        temp = [bridge for bridge in re.sub(r'([\r\n\s]+)',
                                            '', data).split(',')]
        temp = list(set(temp))
        temp = sorted(list(filter(lambda br: len(br) == 2,
                           [br.split('-') for br in temp])),
                           key=lambda x: (x[0], x[1]))

        for br in temp:
            self.add_to_graph(br[0], br[1])

    def add_to_graph(self, x1, x2):
        isl1 = self.get_or_create_island(x1)
        isl2 = self.get_or_create_island(x2)
        
        isl1.add_connection(isl2)
        self.vertexes = sorted(self.vertexes, key=lambda x: x.name)

        self.bridges.append([x1, x2])
        self.bridges = sorted(
            self.bridges,
            key=lambda x: (x[0], x[1])
        )

    def calc_degree(self):
        return {x.getName(): len(x.getConnections()) for x in self.vertexes}

    def create_adjacency_matrix(self):
        res = [[0 for _ in self.get_name_vertexes()] for _ in self.get_name_vertexes()]
        for column, x in enumerate(self.get_name_vertexes()):
            for row, items in enumerate(self.get_name_vertexes()):
                t = self.find_vertex_in_graph(items)
                if x in t.getNameOfConnections():
                    res[row][column] = 1
        return res

    def adjacency_matrix_to_table(self):
        temp = self.create_adjacency_matrix()
        res = [[''] + list(self.get_name_vertexes())] + \
              [[item] + temp[i] for i, item in enumerate(self.get_name_vertexes())]
        return res

    def create_incidence_matrix(self):
        res = [[0 for _ in range(sum(list(map(lambda x: len(x.getConnections()), self.vertexes))))]
               for _ in self.get_name_vertexes()]
        
        for i in range(len(self.get_name_vertexes())):
            for j, bridge in enumerate(self.bridges):
                if list(self.get_name_vertexes())[i] == bridge[0]:
                    res[i][j] = 1
                elif list(self.get_name_vertexes())[i] == bridge[1]:
                    res[i][j] = -1
        return res

    def incidence_matrix_to_table(self):
        temp = self.create_incidence_matrix()
        res = list([[''] + ['q' + str(i + 1)
                            for i, _ in enumerate(temp[0])]])
        res += [[item] + temp[i] for i, item in enumerate(self.get_name_vertexes())]
        return res

    def get_vertexes_image(self):
        return {x.name: x.get_name_of_connections() for x in self.vertexes}

    def get_vertexes_preimage(self):
        res = {x: [] for x in self.get_name_vertexes()}
        for x in self.get_name_vertexes():
            for items in self.get_name_vertexes():
                t = self.find_vertex_in_graph(items)
                if x in t.getNameOfConnections():
                    res[x].append(items)
        return res

    def draw_graph(self):
        f = Digraph('graph', filename='static/fsm.gv',
                    node_attr={'color': 'lightblue2',
                               'style': 'filled', 'shape': 'circle'})
        f.attr(rankdir='A', size='1000')

        f.edges(self.bridges)
        return f

    @staticmethod
    def graph_image_to_bytes(fig):
        tempfile = fig.pipe(format='png')
        encoded = base64.b64encode(tempfile).decode('utf-8')
        return encoded

    def drf(self, bridge):
        pass





# g = Graph()

# g.parseGraph('А-Б, А-В, В-Б, В-Ж, В-Е, В-Г, Б-Д, Б-Г, Г-Д, Д-Ж, Г-Ж, Е-Ж')


