import gc

import pandas as pd
import numpy as np
import sys
import networkx as nx  # Library to test if our methods return the right values
import matplotlib.pyplot as plt

from Graph import Graph, triplet_not_in_set
from Vertex import Vertex
from FullVertex import FullVertex
from FullGraph import FullGraph


class GraphViz:
    """
    Tool to visualize a graph
    Class visualization refs : https://www.geeksforgeeks.org/visualize-graphs-in-python/
    """

    def __init__(self):
        self.visual = []

    def addEdge(self, a, b):
        temp = [a, b]
        self.visual.append(temp)

    def visualize(self):
        G = nx.Graph()
        G.add_edges_from(self.visual)
        nx.draw_networkx(G)
        plt.show()
        plt.draw()


if __name__ == '__main__':
    args = sys.argv[-1]
    print(args)
    # g = Graph()
    # v0 = Vertex(0)
    # v1 = Vertex(1)
    # v2 = Vertex(2)
    # v3 = Vertex(3)
    # v4 = Vertex(4)
    # v5 = Vertex(5)
    # v6 = Vertex(6)
    # v7 = Vertex(7)
    # v8 = Vertex(8)
    # v9 = Vertex(9)
    #
    # v0.add_neighbor(v2)
    # v0.add_neighbor(v1)
    # v1.add_neighbor(v3)
    # v1.add_neighbor(v4)
    # g.add_vertices([v0, v1, v2, v3, v4])
    # print(g.vertices)
    # print(g.count_triadic_closure())
    # v0.add_neighbor(v2)
    # v0.add_neighbor(v3)
    #
    # v1.add_neighbor(v2)
    # v1.add_neighbor(v3)
    # v1.add_neighbor(v4)
    # v1.add_neighbor(v6)
    #
    # v2.add_neighbor(v3)
    #
    # v4.add_neighbor(v5)
    #
    # v5.add_neighbor(v6)
    #
    # v6.add_neighbor(v7)
    # v6.add_neighbor(v8)
    # v6.add_neighbor(v9)
    #
    # v7.add_neighbor(v8)
    # v7.add_neighbor(v9)
    #
    # v8.add_neighbor(v9)
    #
    # g.add_vertices([v0, v1, v2, v3, v4, v5, v6, v7, v8, v9])
    # print("G Bridges : ", str(g.count_bridges()))
    # print("G Components : ", str(g.count_components()))
    # print("G Local Bridges : ", str(g.count_local_bridges()))
    # print(g.getMaxKeys())
    # print(g.getMedianKeys())
    """
    # Graph visualization test
    vizGraph = GraphViz()
    vizGraph.addEdge(0, 1)
    vizGraph.addEdge(0, 2)
    vizGraph.addEdge(0, 3)

    vizGraph.addEdge(1, 2)
    vizGraph.addEdge(1, 3)
    vizGraph.addEdge(1, 4)
    vizGraph.addEdge(1, 6)

    vizGraph.addEdge(2, 3)

    vizGraph.addEdge(4, 5)

    vizGraph.addEdge(5, 6)

    vizGraph.addEdge(6, 7)
    vizGraph.addEdge(6, 8)
    vizGraph.addEdge(6, 9)

    vizGraph.addEdge(7, 8)
    vizGraph.addEdge(7, 9)

    vizGraph.addEdge(8, 9)

    # vizGraph.visualize()

    G = nx.Graph()
    G.add_edges_from(vizGraph.visual)
    """
    # print(list(nx.bridges(G)))
    # print(list(nx.local_bridges(G)))
    G2 = nx.Graph()
    # G2 = GraphViz()

    gr = Graph()
    if args is None:
        print("No dataset passed as argument")
        print("Using default dataset 'Project dataset.csv'\n")
        data = pd.read_csv('Project dataset.csv', index_col=[0])
    else:
        print("Using the dataset passed as argument")
        print("Dataset : ", args)
        data = pd.read_csv(args, index_col=[0])

    timeMedian = data.median()['Timestamp']

    vert = data['Source'].unique()
    # vertT = data['Target'].unique()
    vert = np.append(vert, data['Target'].unique())
    vert = np.unique(vert)
    vertices = []
    fullVert = []
    i = 0
    for x in vert:
        v = Vertex(x)
        vertices.append(v)
        fv = FullVertex(x)
        fullVert.append(fv)
        i += 1

    i = 0
    med = False
    fullGraph = FullGraph()
    fullDirectedGraph = FullGraph(True)
    tri_count, b_score, degree = 0, 0, 0
    triad_count = 0
    triadic_closures = []
    triad_set = set()
    degree_evo = []
    tri_evo = []
    bal_score_evo = []
    triangles_set = set()
    for row in data.iterrows():
        fr = row[1]['Source']
        to = row[1]['Target']
        weight = row[1]['Weight']
        ts = row[1]['Timestamp']
        temp_triad, temp_tri, temp_score = 0, 0, 0
        # G2.add_edge(int(fr), int(to))
        vertices[int(fr)].add_neighbor(vertices[int(to)])
        fullVert[int(fr)].add_neighbor(fullVert[int(to)], weight, ts)
        fullDirectedGraph.add_edge(fullVert[int(fr)], fullVert[int(to)], weight, ts)
        if not med:  # If the median timestamp isn't reached
            # G2.addEdge(int(fr), int(to))
            # fullVert[int(fr)].add_neighbor(fullVert[int(to)], weight, ts)
            med = timeMedian == ts
            if med:
                fullGraph.add_vertices(fullVert)
                tri_count, b_score, degree, triangles_set = fullGraph.balance_degree()
                degree_evo.append(degree)
                tri_evo.append(tri_count)
                bal_score_evo.append(b_score)
                triad_count, triad_set = fullGraph.count_triadic_closure_with_set()
                # triadic_closures.append(fullGraph.count_triadic_closure())
                # triadic_closures.append(triad_count)
                print("Reached median timestamp : ", timeMedian, " == ", ts)
                # print(row)
                print("fullGraph : #vertices : ", len(fullGraph.vertices))
                print("fullGraph : #Triangles : ", tri_count, " || Score : ", b_score, " || Degree : ", degree)
                print("\n")
        else:  # If the median timestamp is reached
            fullGraph.add_edge(fullVert[int(fr)], fullVert[int(to)], weight, ts)
            for v in fullGraph.vertices[int(fr)]:
                if v in fullGraph.vertices[int(to)] and v != fr and v != to:
                    tri, score = fullGraph.deg_from(fr, to, v, temp_score, temp_tri, triangles_set)
                    temp_tri = tri
                    temp_score = score
                    temp_triad += fullGraph.triadic_closure(fr, to, v, triad_set)
            triadic_closures.append(temp_triad)
            # print(temp_tri)
            tri_count += temp_tri
            b_score += temp_score
            d = b_score / tri_count
            degree_evo.append(d)
            tri_evo.append(temp_tri)
            bal_score_evo.append(temp_score)

    # bridgesG2 = list(nx.bridges(G2))
    # l_bridgesG2 = list(nx.local_bridges(G2))
    # print("Bridges : ", len(bridgesG2))
    # print("Local bridges : ", len(l_bridgesG2))
    # nx_tri = sum(nx.triangles(G2).values())

    """
    t = 0
    for a, b, c in triangles_set:
        if fullGraph.is_triangle(a, b, c):
            t += 1
        else:
            print("It's not a triable?", (a, b, c))
    
    print("Triangle count : ", t)
    """

    gr.add_vertices(vertices)
    # print("Triangle count NX : ", nx_tri)

    # fullGraph = FullGraph()
    # fullGraph.add_vertices(fullVert)
    # tri_count, b_score, degree = fullGraph.balance_degree
    print("fullGraph - #vertices : ", len(fullGraph.vertices))
    print("fullGraph - #Triangles Before : ", triad_count, "#Triadic Closure at the end : ", sum(triadic_closures))
    print("fullGraph - #Triangles : ", tri_count, " || Score : ", b_score, " || Degree : ", degree)

    # print(data.describe())
    # print(sys.getrecursionlimit())

    n_loc_bridges, n_loc_bridges_set = gr.count_local_bridges()

    tc, tc_set = gr.count_triadic_closure_with_set()

    print("")
    print("Components : ", str(gr.count_components()))
    print("Bridges : ", str(gr.count_bridges()))
    print("Local Bridges : ", n_loc_bridges)
    # print("Triadic closure : ", str(gr.count_triadic_closure()), "VS : ", tc)

