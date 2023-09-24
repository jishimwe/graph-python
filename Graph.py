import statistics

from Vertex import Vertex


def triplet_not_in_set(a, b, c, my_set):
    """
    Checks if the triplet (or any of its permutation) formed by (a, b, c) is in the set

    :param a: int representing a vertex
    :param b: int representing a vertex
    :param c: int representing a vertex
    :param my_set: a set of triplet
    :return: True if (a, b, c) or any of its permutation are not in the set, False otherwise
    """
    if (a, b, c) not in my_set and (a, c, b) not in my_set and\
            (b, a, c) not in my_set and (b, c, a) not in my_set and \
            (c, a, b) not in my_set and (c, b, a) not in my_set:
        return True
    return False


class Graph:
    """
    Class Representing a graph

    @vertices : A list of vertices representing a graph
    """

    def __init__(self):
        self._e = 0
        self.vertices = {}
        self.cpt = 0

    def add_vertex(self, vertex):
        self._e += 1
        self.vertices[vertex.id] = vertex.neighbors

    def add_vertices(self, vertices):
        for vertex in vertices:
            if isinstance(vertex, Vertex):
                self._e += 1
                self.vertices[vertex.id] = vertex.neighbors

    def add_edge(self, vertex_from: Vertex, vertex_to: Vertex):
        Vertex(vertex_from).add_neighbor(Vertex(vertex_to))
        self.vertices[vertex_to.id] = vertex_to.neighbors
        self.vertices[vertex_from.id] = vertex_from.neighbors

    def add_edge_undirected(self, vertex_from: Vertex, vertex_to: Vertex):
        vertex_from.add_neighbor(vertex_to, True)
        self.vertices[vertex_to.id] = vertex_to.neighbors
        self.vertices[vertex_from.id] = vertex_from.neighbors

    def count_components(self):
        def dfs(v):
            visited.add(v)
            for nei in self.vertices[v]:
                if nei not in visited:
                    dfs(nei)

        count = 0
        visited = set()
        for vertex_id in self.vertices:
            if vertex_id not in visited:
                count += 1
                dfs(vertex_id)
        return count

    def count_bridges(self):
        """
        Count the number of bridges in the graph

        A bridge is an edge, which when deleted, increases the number of connected components
        :return: The number of bridges in the graph
        """
        def calc_bridge(v):
            visited.add(v)
            discovered[v] = self.cpt
            low[v] = self.cpt
            self.cpt += 1
            for vertex in self.vertices[v]:
                if vertex not in visited:
                    parent[vertex] = v
                    calc_bridge(vertex)
                    low[v] = min(low[v], low[vertex])
                    if low[vertex] > discovered[v]:
                        bridges.append((v, vertex))
                elif vertex != parent[v]:
                    low[v] = min(low[v], discovered[vertex])

        visited = set()
        discovered = [float("Inf")] * len(self.vertices)
        low = [float("Inf")] * len(self.vertices)
        parent = [-1] * len(self.vertices)
        bridges = []
        for i in self.vertices:
            if i not in visited:
                calc_bridge(i)
        return len(bridges)

    def count_local_bridges(self):
        """

        :return: A tuple representing the number of local bridges as well as a set containing those local bridges
        (i.e. a set of tuple representing the edges that are a local bridge)
        """
        l_bridges = set()
        for i in self.vertices:
            for j in self.vertices[i]:
                if not (set(self.vertices[j]) & set(self.vertices[i])):
                    if (j, i) not in l_bridges:
                        l_bridges.add((i, j))
        n_bridges = len(l_bridges)
        return n_bridges, l_bridges

    def is_triangle(self, a, b, c):
        """
        Detect if three vertices form a triangle

        :param a: int representing a vertex
        :param b: int representing a vertex
        :param c: int representing a vertex
        :return: True if the three vertices form a triangle, False otherwise
        """
        if a == b or a == c or b == c:
            return False
        elif a in self.vertices[b] and a in self.vertices[c] and b in self.vertices[c]:
            return True
        return False

    def are_connected(self, id1, id2):
        return id2 in self.vertices[id1]

    def count_triadic_closure(self):
        """

        :return: the number of triadic closures in the graph
        """
        counter = 0
        for i in range(0, 3):
            for sub_id in range(0, len((self.vertices[i]))):
                for sub_sub_id in range(sub_id + 1, len((self.vertices[i]))):
                    a = i
                    b = self.vertices[i][sub_id]
                    c = self.vertices[i][sub_sub_id]
                    if not self.are_connected(b, c):
                        counter += 1
        return counter

    def count_triadic_closure_with_set(self):
        triad_set = set()
        counter = 0
        for i in range(0, 3):
            for sub_id in range(0, len((self.vertices[i]))):
                for sub_sub_id in range(sub_id + 1, len((self.vertices[i]))):
                    a = i
                    b = self.vertices[i][sub_id]
                    c = self.vertices[i][sub_sub_id]
                    if not self.are_connected(b, c) and triplet_not_in_set(a, b, c, triad_set):
                        triad_set.add((a, b, c))
                        counter += 1
        return counter, triad_set

    def getDegree(self, v):
        return len(self.vertices[v])

    def hasEdge(self, v, w):
        return v in self.vertices[w]

    def getMaxKeys(self):
        return max(list(self.vertices.keys()))

    def getMedianKeys(self):
        return int(statistics.median(list(self.vertices.keys())))
