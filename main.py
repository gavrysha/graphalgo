import pygame


pygame.init()

class GraphCell:
    def __init__(self, pos_x:int, pos_y:int):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.is_active = False


class Graph:
    __cells = []
    __rel_list = []
    __active_cell = None

    def __cell_exists(self, index:int):
        if index>=0 and index<len(self.__cells):
            return True
        return False

    def add_cell(self, pos_x:int, pos_y:int):
        self.__cells.append(GraphCell(pos_x, pos_y))
        self.__rel_list.append([])
        return self.__cells[-1]

    def delete_cell(self, cell):
        index = self.__cells.index(cell)
        del self.__cells[index]
        del self.__rel_list[index]
        for cell_rels in self.__rel_list:
            if  cell in cell_rels:
                cell_rels.remove(cell)

    def add_relation(self, cell_index1:int, cell_index2:int):
        if self.__cell_exists(cell_index1) and self.__cell_exists(cell_index2):
            self.__rel_list[cell_index1].append(self.__cells[cell_index2])

    def delete_relation(self, cell_index1:int, cell_index2:int):
        removed = False
        if self.__cell_exists(cell_index1) and self.__cell_exists(cell_index2):
            if self.__cells[cell_index2] in self.__rel_list[cell_index1]:
                self.__rel_list[cell_index1].remove(self.__cells[cell_index2])
                removed = True
            if self.__cells[cell_index1] in self.__rel_list[cell_index2]:
                self.__rel_list[cell_index2].remove(self.__cells[cell_index1])
                removed = True
        return removed

    def get_cells(self):
        return self.__cells

    def get_rel_list(self):
        return self.__rel_list


class GraphBuilder:
    def start_loop(self):
        running = True
        drag_cell = False
        drag_cell_offsets = None
        graph_cells = self.__graph.get_cells()
        new_cell = None
        new_relation_start = None
        while running:
            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    clicked_to_cell = False
                    if not new_relation_start is None:
                        for cell in graph_cells:
                            x = mouse_pos[0] - cell.pos_x
                            y = mouse_pos[1] - cell.pos_y
                            if (x*x+y*y<=self.__cell_radius*self.__cell_radius and
                                    cell!=new_relation_start):
                                if not self.__graph.delete_relation(
                                        graph_cells.index(new_relation_start),
                                        graph_cells.index(cell)):
                                    self.__graph.add_relation(
                                        graph_cells.index(new_relation_start),
                                        graph_cells.index(cell)
                                    )
                                new_relation_start = None

                    if not new_cell is None:
                        for cell in graph_cells:
                            x = mouse_pos[0] - cell.pos_x
                            y = mouse_pos[1] - cell.pos_y
                            if (x*x+y*y<=self.__cell_radius*self.__cell_radius*4 and
                                    cell!=new_cell):
                                clicked_to_cell = True
                        print(clicked_to_cell)
                        if not clicked_to_cell:
                            new_cell = None
                        continue
                    for cell in graph_cells:
                        x = mouse_pos[0] - cell.pos_x
                        y = mouse_pos[1] - cell.pos_y
                        if x*x+y*y<=self.__cell_radius*self.__cell_radius:
                            clicked_to_cell = True
                            if not self.__active_cell is None:
                                self.__active_cell.is_active = False
                            self.__active_cell = cell
                            cell.is_active = True
                            drag_cell = True
                            drag_cell_offsets = (x, y)
                    if not clicked_to_cell and not self.__active_cell is None:
                        self.__active_cell.is_active = False
                        self.__active_cell = None
                elif event.type == pygame.MOUSEBUTTONUP:
                    drag_cell = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.key.key_code('escape'):
                        if not new_cell is None:
                            self.__graph.delete_cell(new_cell)
                            new_cell = None
                        if not self.__active_cell is None:
                            self.__active_cell.is_active = False
                            self.__active_cell = None
                        if not new_relation_start is None:
                            new_relation_start = None
                    elif event.key == pygame.key.key_code('n'):
                        if not self.__active_cell is None:
                            self.__active_cell.is_active = False
                            self.__active_cell = None
                        if new_cell is None:
                            new_cell = self.__graph.add_cell(*mouse_pos)
                    elif event.key == pygame.key.key_code('r'):
                        new_relation_start = self.__active_cell
                    elif event.key == pygame.key.key_code('delete'):
                        if not self.__active_cell is None:
                            self.__graph.delete_cell(self.__active_cell)
                            self.__active_cell = None

            self.__display.fill((255, 255, 255))
            if not new_relation_start is None:
                print(pygame.mouse.get_pos())
                print(new_relation_start.pos_x, new_relation_start.pos_y)
                pygame.draw.line(self.__display,
                    (13, 23, 26),
                    (new_relation_start.pos_x,
                        new_relation_start.pos_y,
                    ),
                    pygame.mouse.get_pos(),
                    5
                )
            if not self.__active_cell is None and drag_cell:
                new_pos_x = mouse_pos[0] - drag_cell_offsets[0]
                new_pos_y = mouse_pos[1] - drag_cell_offsets[1]
                clicked_to_cell = False
                for cell in graph_cells:
                    x = new_pos_x - cell.pos_x
                    y = new_pos_y - cell.pos_y
                    if (x*x+y*y<=self.__cell_radius*self.__cell_radius*4 and
                        cell!=self.__active_cell):
                            clicked_to_cell = True
                if not clicked_to_cell:
                    self.__active_cell.pos_x = new_pos_x
                    self.__active_cell.pos_y = new_pos_y
            if not  new_cell is None:
                new_cell.pos_x = mouse_pos[0]
                new_cell.pos_y = mouse_pos[1]

            graph_rel_list = self.__graph.get_rel_list()
            print('aa', graph_rel_list)
            for cell_index1 in range(len(graph_rel_list)):
                for cell in graph_rel_list[cell_index1]:
                    pygame.draw.line(self.__display,
                        (13, 23, 26),
                        (graph_cells[cell_index1].pos_x,
                            graph_cells[cell_index1].pos_y
                        ),
                        (cell.pos_x,
                            cell.pos_y
                        ),
                        5
                    )

            for cell_index in range(len(graph_cells)):
                cell_color = (13, 23, 26)
                if graph_cells[cell_index].is_active:
                    cell_color = (0, 255, 0)
                pygame.draw.circle(self.__display, cell_color,
                    (
                        graph_cells[cell_index].pos_x, 
                        graph_cells[cell_index].pos_y
                    ),
                    self.__cell_radius
                )
                font = pygame.font.Font(None, 25)
                text = font.render(str(cell_index), True, (255, 255, 255))
                text_rect = text.get_rect(center=(
                    graph_cells[cell_index].pos_x,
                    graph_cells[cell_index].pos_y,
                    ))
                self.__display.blit(text, text_rect)
            pygame.display.flip()
            self.__clock.tick(50)

    def __init__(self):
        self.__clock = pygame.time.Clock()
        self.__graph = Graph()
        self.__graph.add_cell(100, 100)
        self.__graph.add_cell(200, 200)
        self.__graph.add_relation(0, 1)
        self.__cell_radius = 30
        self.__active_cell = None
        self.__display = pygame.display.set_mode((800, 600))


GraphBuilder().start_loop()



