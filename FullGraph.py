from Graph import Graph, triplet_not_in_set
from FullVertex import FullVertex


class FullGraph(Graph):
    def __init__(self, directed=False):
        super().__init__()
        self.w_vertices = {}
        self.cpt = 0
        self.directed = directed

    def add_vertex(self, vertex):
        """
        Add a vertex to the graph

        :param vertex: An object type FullVertex
        """
        super().add_vertex(vertex)
        if vertex in self.vertices:
            self.w_vertices[vertex.id] = vertex.w_neighbors

    def add_vertices(self, vertices):
        """
        Add a list of vertices to the graph

        :param vertices: An iterable collection of FullVertices
        """
        super(FullGraph, self).add_vertices(vertices)
        for vertex in vertices:
            if isinstance(vertex, FullVertex):
                self.w_vertices[vertex.id] = vertex.w_neighbors

    def add_edge(self, vertex_from: FullVertex, vertex_to: FullVertex, weight=0, timestamp=-1):
        """
        Add an edge (as well as its weight and timestamp) to the graph

        :param vertex_from: An object type FullVertex
        :param vertex_to:  An object type FullVertex
        :param weight: The weight of the edge
        :param timestamp: A timestamp for when the edge was created
        """
        super(FullGraph, self).add_edge(vertex_from, vertex_to)
        vertex_from.add_neighbor(vertex_to, weight, timestamp, self.directed)
        self.w_vertices[vertex_to.id] = vertex_to.w_neighbors
        if not self.directed:
            self.w_vertices[vertex_from.id] = vertex_from.w_neighbors

    def triadic_closure(self, a, b, c, triad_set):
        if self.is_triangle(a, b, c) and triplet_not_in_set(a, b, c, triad_set):
            triad_set.add((a, b, c))
            return 1
        return 0

    def tri_degree(self, a, b, c):
        """
        Calculate the degree of balance for a triangle in the graph.
        An edge is (+) if its weight >= 0 and (-) otherwise

        :param a: int representing a vertex
        :param b: int representing a vertex
        :param c: int representing a vertex
        :return: 1 if balanced,
                 2/3 if weakly balanced,
                 0 if unbalanced
        """
        bal = 0
        bal = bal + 1 if (self.w_vertices[a][b]['weight'] >= 0) else bal - 1
        bal = bal + 1 if (self.w_vertices[b][c]['weight'] >= 0) else bal - 1
        bal = bal + 1 if (self.w_vertices[c][a]['weight'] >= 0) else bal - 1
        return 1 if (bal == 3 or bal == -1) else 0 if bal == -3 else 2/3

    def deg_from(self, a, b, c, prev_deg, tri_count, tri_set):
        """
        (a, b, c) represent three vertices. This function checks if they form a triangle.
        In the affirmative, it updates the triangle count, triangle sets as well as the degree of balance

        :param a: int representing a vertex
        :param b: int representing a vertex
        :param c: int representing a vertex
        :param prev_deg: a previously calculated degree score
        :param tri_count: a previously calculated number of triangles
        :param tri_set:  a set containing the triangle found so far
        :return: an updated triangle count and balance degree
        """
        if self.is_triangle(a, b, c) and triplet_not_in_set(a, b, c, tri_set):
            tri_set.add((a, b, c))
            tri_count += 1
            prev_deg += self.tri_degree(a, b, c)
        return tri_count, prev_deg

    def balance_degree(self):
        """
        Calculate the degree of structural balance of the graph

        Complexity: O(i+j+k)

        :return: a tuple representing the number of triangles in the graph, the balance score
                 and the degree of structural balance of that graph
                 as well as a set containing all triplet of the triangles formed
                 (tr_count, b_score, b_deg, triangles)
        """
        tr_count = 0
        triangles = set()  # set containing all the formed triangles
        tri_deg = []  # List of tuple vertices that form a triangle
        for i in self.vertices:
            for j in self.vertices[i]:
                if j != i:
                    for k in self.vertices[j]:
                        if self.is_triangle(i, j, k) and triplet_not_in_set(i, j, k, triangles):
                            tr_count += 1
                            triangles.add((i, j, k))
                            tri_deg.append(self.tri_degree(i, j, k))
        b_score = sum(tri_deg)
        b_deg = b_score / tr_count
        return tr_count, b_score, b_deg, triangles

    # def page_rank(self):
    #     if not self.directed:
    #         return None
    #     damp = 1 / len(self.vertices)
    #     rank = [damp] * len(self.vertices)
    #     for i in self.vertices:
    #         for j in self.vertices[i]:
    #             for k in self.vertices[j]:
    #
    #                 rank[i] = rank[i] * self.w_vertices[j] /
    #             return 0
