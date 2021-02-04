class GraphVertex:
    def __init__(self, pos_x, pos_y):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.edges_from = []
        self.edges_to = []

    def edge_exists(self, vertex):
        if vertex in self.edges_from:
            return True
        else: return False

    def add_edge(self, vertex):
        self.edges_from.append(vertex)
        vertex.edges_to.append(self)
    
    def remove_edge(self, vertex):
        if self.edge_exists(vertex):
            self.edges_from.remove(vertex)
            vertex.edges_to.remove(self)
        else:
            raise ValueError

class Graph:
    def __init__(self):
        self.vertexes = []

    def add_vertex(self, pos_x, pos_y):
        vertex = GraphVertex(pos_x, pos_y)
        self.vertexes.append(vertex)
        return vertex
    
    def remove_vertex(self, vertex):
        if vertex in self.vertexes:
            for vertex1 in vertex.edges_from:
                vertex1.edges_to.remove(vertex)
            for vertex1 in vertex.edges_to:
                vertex1.edges_from.remove(vertex)
            self.vertexes.remove(vertex)
        else:
            raise ValueError

