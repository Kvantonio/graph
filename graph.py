import base64  # noqa: I201, I100
import re  # noqa: I201, I100

from graphviz import Digraph  # noqa: I201, I100


class Island(object):
    def __init__(self, name):
        self.name = name
        self.connections = []
        self.color = None

    def getName(self):
        return self.name
    
    def getConnections(self):
        return self.connections

    def getNameOfConnections(self):
        return [x.name for x in self.connections]

    def findConnection(self, name):
        for item in self.connections:
            if item.name == name:
                return True
        return False

    def addConnection(self, c):
        if not self.findConnection(c):
            self.connections.append(c)


class Graph(object):
    def __init__(self):
        self.graph = []
        self.bridges = []

    def getGraph(self):
        return self.graph

    def getVertexes(self):
        return [x.name for x in self.graph]

    def getBridges(self):
        return self.bridges

    def findIslandInGraph(self, name):
        for item in self.graph:
            if item.name == name:
                return item

        return None


    def get_or_create_island(self, name):
        for item in self.graph:
            if item.name == name:
                return item

        island = Island(name)
        self.graph.append(island)
        return island


    def parseGraph(self, data):
        temp = [bridge for bridge in re.sub(r'([\r\n\s]+)',
                                            '', data).split(',')]
        temp = list(set(temp))
        temp = sorted(list(filter(lambda br: len(br) == 2,
                           [br.split('-') for br in temp])),
                           key=lambda x: (x[0], x[1]))

        for br in temp:
            self.addToGraph(br[0], br[1])

    def addToGraph(self, x1, x2):
        isl1 = self.get_or_create_island(x1)
        isl2 = self.get_or_create_island(x2)
        
        isl1.addConnection(isl2)
        self.graph = sorted(self.graph, key=lambda x: x.name)

        self.bridges.append([x1, x2])
        self.bridges = sorted(
            self.bridges,
            key=lambda x: (x[0], x[1])
        )

    def calcDegree(self):
        return {x.getName(): len(x.getConnections()) for x in self.graph}

    def createAdjacencyMatrix(self):
        res = [[0 for _ in self.getVertexes()] for _ in self.getVertexes()]
        for colum, x in enumerate(self.getVertexes()):
            for row, items in enumerate(self.getVertexes()):
                t = self.findIslandInGraph(items)
                if x in t.getNameOfConnections():
                    res[row][colum] = 1
        return res

    def adjacencyMatrixToTable(self):
        temp = self.createAdjacencyMatrix()
        res = [[''] + list(self.getVertexes())] + \
              [[item] + temp[i] for i, item in enumerate(self.getVertexes())]
        return res

    def createIncidenceMatrix(self):
        res = [[0 for _ in range(sum(list(map(lambda x: len(x.getConnections()), self.graph))))]
               for _ in self.getVertexes()]
        
        for i in range(len(self.getVertexes())):
            for j, bridge in enumerate(self.bridges):
                if list(self.getVertexes())[i] == bridge[0]:
                    res[i][j] = 1
                elif list(self.getVertexes())[i] == bridge[1]:
                    res[i][j] = -1

        return res

    def incidenceMatrixToTable(self):
        temp = self.createIncidenceMatrix()
        res = list([[''] + ['q' + str(i + 1)
                            for i, _ in enumerate(temp[0])]])
        res += [[item] + temp[i] for i, item in enumerate(self.getVertexes())]
        return res

    def getPreimage(self):
        res = {x: [] for x in self.getVertexes()}
        for x in self.getVertexes():
            for items in self.getVertexes():
                t = self.findIslandInGraph(items)
                if x in t.getNameOfConnections():
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





g = Graph()

g.parseGraph('А-Б, А-В, В-Б, В-Ж, В-Е, В-Г, Б-Д, Б-Г, Г-Д, Д-Ж, Г-Ж, Е-Ж')


print('________')

for i in g.getGraph():
    print(i.name, i.getNameOfConnections())

print('*********************')

print(g.createAdjacencyMatrix())
print('*********************')

# print(g.adjacencyMatrixToTable())

print('()&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
print(g.createIncidenceMatrix())