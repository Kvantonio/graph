import base64  # noqa: I201, I100
import re  # noqa: I201, I100

from graphviz import Digraph  # noqa: I201, I100


class Graph(object):
    def __init__(self):
        self.graph = {}
        self.bridges = []

    def getGraph(self):
        return self.graph

    def getVertexes(self):
        return self.graph.keys()

    def getBridges(self):
        return self.bridges

    def parseGraph(self, data):
        temp = [bridge for bridge in re.sub(r'([\r\n\s]+)',
                                            '', data).split(',')]
        temp = list(set(temp))
        temp = list(filter(lambda br: len(br) == 2,
                           [br.split('-') for br in temp]))
        for br in temp:
            self.addToGraph(br[0], br[1])

    def addToGraph(self, x1, x2):
        self.bridges.append([x1, x2])
        if x1 not in self.graph.keys():
            self.graph[x1] = [x2]
        else:
            self.graph[x1].append(x2)

        self.graph = {x: list(set(self.graph[x])) for x in sorted(self.graph.keys())}
        self.bridges = [bridge for bridge in sorted(
            self.bridges,
            key=lambda x: (x[0], x[1])
        )]

    def calcDegree(self):
        return {x: len(self.graph[x]) for x in self.graph.keys()}

    def createAdjacencyMatrix(self):
        res = [[0 for _ in self.graph.keys()] for _ in self.graph.keys()]
        for colum, x in enumerate(self.graph.keys()):
            for row, items in enumerate(self.graph.keys()):
                if x in self.graph[items]:
                    res[row][colum] = 1
        return res

    def adjacencyMatrixToTable(self):
        temp = self.createAdjacencyMatrix()
        res = [[''] + list(self.graph.keys())] + \
              [[item] + temp[i] for i, item in enumerate(self.graph.keys())]
        return res

    def createIncidenceMatrix(self):
        res = [[0 for _ in range(sum(list(map(len, self.graph.values()))))]
               for _ in self.graph.keys()]
        for i in range(len(self.graph.keys())):
            for j, bridge in enumerate(self.bridges):
                if list(self.graph.keys())[i] == bridge[0]:
                    res[i][j] = 1
                elif list(self.graph.keys())[i] == bridge[1]:
                    res[i][j] = -1

        return res

    def incidenceMatrixToTable(self):
        temp = self.createIncidenceMatrix()
        res = list([[''] + ['q' + str(i + 1)
                            for i, _ in enumerate(temp[0])]])
        res += [[item] + temp[i] for i, item in enumerate(self.graph.keys())]
        return res

    def getPreimage(self):
        res = {x: [] for x in self.graph.keys()}
        for x in self.graph.keys():
            for items in self.graph.keys():
                if x in self.graph[items]:
                    res[x].append(items)
        return res

    def drawGraph(self):
        f = Digraph('graph', filename='static/fsm.gv',
                    node_attr={'color': 'lightblue2',
                               'style': 'filled', 'shape': 'circle'})
        f.attr(rankdir='A', size='1000')

        f.edges(self.bridges)
        return f

    @staticmethod
    def graphImgToBytes(fig):
        tempfile = fig.pipe(format='png')
        encoded = base64.b64encode(tempfile).decode('utf-8')
        return encoded

    def drf(self, bridge):
        pass


