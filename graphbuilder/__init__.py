import pygame
from .graph import Graph


pygame.init()


class GraphBuilder:
    def __intersecting_vertex(self, pos_x, pos_y, exceptions=[]):
        for vertex in self.graph.vertexes:
            x = pos_x - vertex.pos_x
            y = pos_y - vertex.pos_y
            if x*x+y*y <= self.vertex_radius*self.vertex_radius*4 and not vertex in exceptions:
                return True
        return False

    def start_loop(self):
        running = True
        drag_vertex = False

        drag_vertex_offsets = None
        new_vertex = None
        new_edge_start = None
        active_vertex = None
        while running:
            mouse_pos = pygame.mouse.get_pos()

            clicked_vertex = None
            for vertex in self.graph.vertexes:
                x = mouse_pos[0] - vertex.pos_x
                y = mouse_pos[1] - vertex.pos_y
                if x*x+y*y <= self.vertex_radius*self.vertex_radius:
                    clicked_vertex = vertex
                    break

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if new_vertex is None and new_edge_start is None:
                        active_vertex = clicked_vertex
                        if not active_vertex is None:
                            drag_vertex = True
                            drag_vertex_offsets = (
                                mouse_pos[0] - clicked_vertex.pos_x,
                                mouse_pos[1] - clicked_vertex.pos_y
                            )

                    if not new_vertex is None:
                        if not self.__intersecting_vertex(
                            new_vertex.pos_x, new_vertex.pos_y,
                            [new_vertex]
                        ):
                            new_vertex = None

                    if not new_edge_start is None and not clicked_vertex is None:
                        if new_edge_start.edge_exists(clicked_vertex):
                            new_edge_start.remove_edge(clicked_vertex)
                        else:
                            new_edge_start.add_edge(clicked_vertex)
                        new_edge_start = None
                        active_vertex = clicked_vertex

                elif event.type == pygame.MOUSEBUTTONUP:
                    drag_vertex = False

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.key.key_code('escape'):
                        if not new_vertex is None:
                            self.graph.remove_vertex(new_vertex)
                            new_vertex = None
                        active_vertex = None
                        new_edge_start = None
                    elif event.key == pygame.key.key_code('v') and new_edge_start is None:
                        active_vertex = None
                        if new_vertex is None:
                            new_vertex = self.graph.add_vertex(*mouse_pos)
                    elif event.key == pygame.key.key_code('e'):
                        new_edge_start = active_vertex
                    elif event.key == pygame.key.key_code('delete'):
                        if not active_vertex is None:
                            self.graph.remove_vertex(active_vertex)
                            active_vertex = None
                            new_edge_start = None

            if drag_vertex:
                new_pos_x = mouse_pos[0] - drag_vertex_offsets[0]
                new_pos_y = mouse_pos[1] - drag_vertex_offsets[1]
                if not self.__intersecting_vertex(new_pos_x, new_pos_y, [active_vertex]):
                    active_vertex.pos_x = new_pos_x
                    active_vertex.pos_y = new_pos_y

            if not new_vertex is None:
                new_vertex.pos_x = mouse_pos[0]
                new_vertex.pos_y = mouse_pos[1]

            self.display.fill((255, 255, 255))

            for vertex1 in self.graph.vertexes:
                for vertex2 in vertex1.edges_from:
                    pygame.draw.line(self.display,
                                     (13, 23, 26),
                                     (
                                         vertex1.pos_x,
                                         vertex1.pos_y
                                     ),
                                     (
                                         vertex2.pos_x,
                                         vertex2.pos_y
                                     ),
                                     5
                                     )

            if not new_edge_start is None:
                pygame.draw.line(self.display,
                                 (13, 23, 26),
                                 (
                                     new_edge_start.pos_x,
                                     new_edge_start.pos_y,
                                 ),
                                 pygame.mouse.get_pos(),
                                 5
                                 )

            for vertex_index in range(len(self.graph.vertexes)):
                vertex_color = (13, 23, 26)
                if self.graph.vertexes[vertex_index] == active_vertex:
                    vertex_color = (0, 255, 0)
                pygame.draw.circle(self.display, vertex_color,
                                   (
                                       self.graph.vertexes[vertex_index].pos_x,
                                       self.graph.vertexes[vertex_index].pos_y
                                   ),
                                   self.vertex_radius
                                   )
                font = pygame.font.Font(None, 25)
                text = font.render(str(vertex_index+1), True, (255, 255, 255))
                text_rect = text.get_rect(center=(
                    self.graph.vertexes[vertex_index].pos_x,
                    self.graph.vertexes[vertex_index].pos_y,
                ))
                self.display.blit(text, text_rect)

            pygame.display.flip()
            self.clock.tick(100)

    def __init__(self):
        self.display = pygame.display.set_mode((800, 600))
        self.graph = Graph()
        self.graph.add_vertex(100, 200)
        self.graph.add_vertex(300, 400)
        self.graph.vertexes[0].add_edge(self.graph.vertexes[1])
        self.clock = pygame.time.Clock()
        self.vertex_radius = 30
