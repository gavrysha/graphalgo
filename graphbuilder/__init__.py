import pygame
import tkinter.filedialog
import tkinter
import time

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

    def dfs(self, start, parent, answer):
        start.used = True
        if start.time_in != 1:
            start.time_in = parent.time_in + 1
        else:
            start.color = "green"
        for i in start.edges:
            if i.used != True:
                i.color = "green"
                self.update_screen(None, None, None)
                time.sleep(0.9)
                self.dfs(i, start, answer)
        start.color = "red"
        self.update_screen(None, None, None)
        time.sleep(0.9)
        start.color = (13, 23, 26)
        self.update_screen(None, None, None)
        for i in start.edges:
            if i != parent:
                start.time_out = min(start.time_in, start.time_out, i.time_out, i.time_in)
        if start.time_out == 1e10:
            start.time_out = start.time_in
        if start.time_out == start.time_in != 1e10:
            answer.append((start, parent))

        self.update_screen(None, None, None)


    def update_screen(self, new_edge_start, active_vertex, colored_edges):
        self.display.fill((225, 225, 225))

        for vertex1 in self.graph.vertexes:
            for vertex2 in vertex1.edges:
                '''if vertex1.color == "green" and vertex2.color == "green":
                    pygame.draw.line(self.display,
                                     "green",
                                     (
                                         vertex1.pos_x,
                                         vertex1.pos_y
                                     ),
                                     (
                                         vertex2.pos_x,
                                         vertex2.pos_y
                                     ),
                                     self.edge_width
                                     )
                else: '''
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
                                 self.edge_width
                                 )
        if not colored_edges is None:
            for edge in colored_edges:
                pygame.draw.line(self.display,
                                 "red",
                                 (
                                     edge[0].pos_x,
                                     edge[0].pos_y
                                 ),
                                 (
                                     edge[1].pos_x,
                                     edge[1].pos_y
                                 ),
                                 self.edge_width
                                 )
        if not new_edge_start is None:
            pygame.draw.line(self.display,
                             (13, 23, 26),
                             (
                                 new_edge_start.pos_x,
                                 new_edge_start.pos_y,
                             ),
                             pygame.mouse.get_pos(),
                             self.edge_width
                             )

        for vertex_index in range(len(self.graph.vertexes)):
            vertex_color = self.graph.vertexes[vertex_index].color
            if self.graph.vertexes[vertex_index] == active_vertex \
                    and self.graph.vertexes[vertex_index].color != "green" \
                    and self.graph.vertexes[vertex_index].color != "red":
                vertex_color = (120, 120, 120)  # (0, 255, 0)
            if vertex_index == 2 and self.graph.vertexes[vertex_index].color == "red":
                pygame.draw.circle(self.display, (13, 23, 26),
                                   (
                                       self.graph.vertexes[vertex_index].pos_x,
                                       self.graph.vertexes[vertex_index].pos_y
                                   ),
                                   self.vertex_radius
                                   )
                self.graph.vertexes[vertex_index].color = self.graph.vertexes[vertex_index].color != "red"
            else: pygame.draw.circle(self.display, vertex_color,
                               (
                                   self.graph.vertexes[vertex_index].pos_x,
                                   self.graph.vertexes[vertex_index].pos_y
                               ),
                               self.vertex_radius
                               )
            font = pygame.font.Font(None, 25)
            text = font.render(str(vertex_index + 1), True, (255, 255, 255))
            text_rect = text.get_rect(center=(
                self.graph.vertexes[vertex_index].pos_x,
                self.graph.vertexes[vertex_index].pos_y,
            ))
            if self.graph.vertexes[vertex_index].time_in != 1e10:
                if self.graph.vertexes[vertex_index].time_out == 1e10:
                    text_inout = font.render(str(self.graph.vertexes[vertex_index].time_in) + "|" + "inf", True, (0, 0, 0))
                    text_coords = text_inout.get_rect(center=(
                        self.graph.vertexes[vertex_index].pos_x + 40,
                        self.graph.vertexes[vertex_index].pos_y,
                    ))
                else:
                    text_inout = font.render(str(self.graph.vertexes[vertex_index].time_in) + "|" + str(
                        self.graph.vertexes[vertex_index].time_out), True, (0, 0, 0))
                    text_coords = text_inout.get_rect(center=(
                        self.graph.vertexes[vertex_index].pos_x + 40,
                        self.graph.vertexes[vertex_index].pos_y,
                    ))
                self.display.blit(text_inout, text_coords)
            else:
                text_inout = font.render(" inf" + "|" + "inf", True, (0, 0, 0))
                text_coords = text_inout.get_rect(center=(
                    self.graph.vertexes[vertex_index].pos_x + 45,
                    self.graph.vertexes[vertex_index].pos_y,
                ))
            self.display.blit(text_inout, text_coords)
            self.display.blit(text, text_rect)

        pygame.display.flip()
        self.clock.tick(120)

    def start_loop(self):
        answer = []
        root = tkinter.Tk()
        root.withdraw()

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
                            clicked_vertex.remove_edge(new_edge_start)
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
                    elif event.key == pygame.key.key_code('o'):
                        file_to_read = tkinter.filedialog.askopenfile('rb')
                        if not file_to_read is None:
                            self.graph = Graph.decode(file_to_read.read())
                            file_to_read.close()
                    elif event.key == pygame.key.key_code('w'):

                        if not active_vertex is None:
                            for i in self.graph.vertexes:
                                i.time_in = 1e10
                                i.time_out = 1e10
                            active_vertex.time_in = 1
                            active_vertex.time_out = 1
                            self.dfs(active_vertex, active_vertex, answer)
                        answer = list(dict.fromkeys(answer))

                        for i in answer:
                            i[0].color = "red"
                            i[1].color = "red"

                        print(answer)
                    elif event.key == pygame.key.key_code('s'):
                        filetypes = (('Graphbuilder file', '*.gbldr'), )
                        file_to_write = tkinter.filedialog.asksaveasfile(
                            'wb',
                            defaultextension='gbldr',
                            filetypes=filetypes)
                        if not file_to_write is None:
                            file_to_write.write(self.graph.encode())
                            file_to_write.close()
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

            self.update_screen(new_edge_start, active_vertex, answer)





    def __init__(self):
        self.display = pygame.display.set_mode((800, 600))
        self.graph = Graph()
        self.clock = pygame.time.Clock()
        self.vertex_radius = 20
        self.edge_width = 3
