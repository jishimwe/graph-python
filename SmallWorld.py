import math
import sys
from queue import Queue

from Graph import Graph
from Vertex import Vertex


class PathFinder:
    def __init__(self, graph: Graph, s):
        self._distTo = dict()
        self._edgeTo = dict()
        queue = Queue()
        queue.put(s)
        self._distTo[s] = 0
        self._edgeTo[s] = None
        while not queue.empty():
            v = queue.get()
            for w in graph.vertices[v]:
                if w not in self._distTo:
                    queue.put(w)
                    self._distTo[w] = 1 + self._distTo[v]
                    self._edgeTo[w] = v

    def distanceTo(self, v):
        return self._distTo[v]

    def hasPathTo(self, v):
        return v in self._distTo

    def pathTo(self, v):
        path = []
        while v is not None:
            path += [v]
            v = self._edgeTo[v]
        return reversed(path)


def averageDegree(graph):
    return 2.0 * graph.getNbEdge() / graph.getNbVertex()


def averagePathLength(graph):
    total = 0
    for v in graph.vertices:
        pf = PathFinder(graph, v)
        for w in graph.vertices:
            total += pf.distanceTo(w)
    return 1.0 * total / (graph.getNbVertex() * (graph.getNbEdge() - 1))


def clusteringCoefficient(graph):
    total = 0
    for v in graph.vertices:
        possible = graph.getDegree(v) * (graph.getDegree(v) - 1)
        actual = 0
        for u in graph.vertices[v]:
            for w in graph.vertices[v]:
                if graph.hasEdge(u, w):
                    actual += 1
        if possible > 0:
            total += 1.0 * actual / possible
    return total / graph.getNbVertex()


def getLargestComponent(graph):
    new_graph = Graph()
    max_size = getMaxSizeComponent(graph)
    for vertex in graph.vertices:
        vertex_size_comp = getComponentSize(graph, vertex, [])
        if vertex_size_comp == max_size:
            new_vertex = Vertex(vertex)
            new_vertex.neighbors = graph.vertices[vertex]
            new_graph.add_vertex(new_vertex)
    return new_graph


def getMaxSizeComponent(graph):
    visited = []
    if len(graph.vertices) == 0:
        return 0
    largestSize = 0
    for vertex in graph.vertices:
        size = getComponentSize(graph, vertex, visited)
        if size > largestSize:
            largestSize = size
    return largestSize


def isSmallWorld(graph):
    return averageDegree(graph) > 20 * math.log(graph.getNbVertex(), 10) and averagePathLength(graph) < 10 * math.log(
        graph.getNbVertex(), 10) and clusteringCoefficient(graph) > 0.1


def getComponentSize(graph, id, visited: list):
    if id in visited:
        return 0
    componentSize = 1
    visited.append(id)
    for vertices in graph.vertices[id]:
        componentSize += getComponentSize(graph, vertices, visited)
    return componentSize
