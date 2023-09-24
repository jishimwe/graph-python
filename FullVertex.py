from Vertex import Vertex


class FullVertex(Vertex):
    """
    Representation of a complete graph (i.e. including weight and timestamp)

    ...

    Attributes
    ----------
    id : int representation of vertex
    w_neighbors : array of dictionaries representation of the edges from the id vertex to its neighbors
                  with the weight and timestamp
    """
    def __init__(self, id):
        super().__init__(id)
        self.id = id
        self.w_neighbors = {}

    def add_neighbor(self, vertex, weight, timestamp, directed=False):
        super(FullVertex, self).add_neighbor(vertex, directed)
        if isinstance(vertex, FullVertex):
            # if vertex.id not in self.w_neighbors:
            self.w_neighbors[vertex.id] = ({'id': vertex.id, 'weight': weight, 'timestamp': timestamp})
            vertex.w_neighbors[self.id] = ({'id': self.id, 'weight': weight, 'timestamp': timestamp})
        else:
            print("Error adding neighbors")
