from xmlrpc.client import Boolean


class Vertex:
    def __init__(self, id):
        self.id = id
        self.neighbors = []

    def add_neighbor(self, vertex, directed: Boolean = False):
        if isinstance(vertex, Vertex):
            if vertex.id not in self.neighbors:
                self.neighbors.append(vertex.id)
                if not directed:
                    vertex.neighbors.append(self.id)
        else:
            print("Error adding neighbors")

    def add_neighbors(self, vertices):
        for vertex in vertices:
            if isinstance(vertex, Vertex):
                if vertex.id not in self.neighbors:
                    self.neighbors.append(vertex.id)
                    vertex.neighbors.append(self.id)
            else:
                print("Error adding neighbors")
                return

    def __eq__(self, other):
        return other == id

    def __hash__(self):
        return hash(id)

    def __str__(self):
        return str(self.id) + " : " + str(self.neighbors)
