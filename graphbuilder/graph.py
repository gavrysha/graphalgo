import json

class GraphVertex:
    def __init__(self, pos_x, pos_y):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.edges = []
        self.used = False
        self.time_in = 1e10
        self.time_out = 1e10
        self.color = (13, 23, 26)

    def edge_exists(self, vertex):
        if vertex in self.edges:
            return True
        else: return False

    def add_edge(self, vertex):
        self.edges.append(vertex)
        vertex.edges.append(self)
    
    def remove_edge(self, vertex):
        if self.edge_exists(vertex):
            self.edges.remove(vertex)
            vertex.edges.remove(self)
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
            for vertex1 in vertex.edges:
                vertex1.edges.remove(vertex)
            self.vertexes.remove(vertex)
        else:
            raise ValueError

    def encode(self):
        vertexes_for_encode = {}

        for vertex in self.vertexes:
            vertexes_for_encode[hash(vertex)] = {
                'related': [str(hash(edge_from)) for edge_from in vertex.edges],
                'x': vertex.pos_x,
                'y': vertex.pos_y
            }
            
        return json.dumps(vertexes_for_encode).encode()

    @staticmethod
    def decode(binary):
        try:
            vertexes_to_decode = json.loads(binary)

            vertexes_dict = {}
            for vertex_hash in vertexes_to_decode.keys():
                vertexes_dict[vertex_hash] = GraphVertex(
                    vertexes_to_decode[vertex_hash]['x'],
                    vertexes_to_decode[vertex_hash]['y']
                )
            
            for vertex_hash in vertexes_to_decode.keys():
                for related_vertex_hash in vertexes_to_decode[vertex_hash]['related']:
                    vertexes_dict[vertex_hash].add_edge(vertexes_dict[related_vertex_hash])

            graph = Graph()
            graph.vertexes = [vertex for vertex_hash, vertex in vertexes_dict.items()]

            return graph

        except Exception as exp:
            print(exp)
            return None

