import pygame
import math
from queue import PriorityQueue

WIDTH = 600

# 600 x 600 display window
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Visualizer")

RED = (0xFF, 0, 0)
GREEN = (0, 0xFF, 0)
BLUE = (0, 0, 0xFF)
YELLOW = (0xFF, 0xFF, 0)
WHITE = (0xFF, 0xFF, 0xFF)
BLACK = (0, 0, 0)
PURPLE = (0x8F, 0, 0xFF)
ORANGE = (0xFF, 0xA5, 0)
GREY = (0x80, 0x80, 0x80)
TURQUOISE = (0x30, 0xD5, 0xC8)


class Node:
    '''
    Constructor that initializes the board of nodes
    initializes number of rows, column, width, total rows

    '''

    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    '''
    Method that returns position of a node
    '''

    def get_pos(self):
        return self.row, self.col

    '''
    Method that checks if we have already checked a node in our search
    '''

    def is_closed(self):
        return self.color == RED

    '''
    Method that checks if there is an checked node for us to look into
    '''

    def is_open(self):
        return self.color == GREEN

    '''
    Checks if a node was selected as a barrier
    '''

    def is_barrier(self):
        return self.color == BLACK

    '''
    Method that will make a node the starting node 
    '''

    def make_start(self):
        self.color = ORANGE

    '''
    Method that checks if a node is the starting node
    '''

    def is_start(self):
        return self.color == ORANGE

    '''
    Method that checks if a node is our destination node
    '''

    def is_end(self):
        return self.color == TURQUOISE

    '''
    Method that resets a node 
    '''

    def reset(self):
        self.color = WHITE

    '''
    Method that notes that a node has already been searched
    '''

    def make_closed(self):
        self.color = RED

    '''
    method that notes a node is searchable
    '''

    def make_open(self):
        self.color = GREEN

    '''
    method that notes that a node is a barrier and that we have to move around it
    '''

    def make_barrier(self):
        self.color = BLACK

    '''
    method that notes that a node is our destination 
    '''

    def make_end(self):
        self.color = TURQUOISE

    '''
    Method that notes that our node is included in our final path after our destination has been found
    '''

    def make_path(self):
        self.color = PURPLE

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():  # down
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():  # up
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():  # right
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():  # left
            self.neighbors.append(grid[self.row][self.col - 1])


def __lt__(self, other):
    return False

    '''
    Method that computes the manhattan distance (Heuristic function)
    '''


def heuristic(p1, p2, ):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


'''
Method that reconstructs shortest path once found
'''


def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()


'''
A* algorithm implementation
'''


def algorithm(draw, grid, start, end):
    count = 0;
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0

    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = heuristic(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    while not open_set.empty():
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            # make path
            reconstruct_path(came_from, end, draw)
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1  # going one node over

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + heuristic(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1;
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw()

        # if the node is not the start node close it
        if current != start:
            current.make_closed()

    return False


def make_grid(rows, width):
    grid = []
    gap = width // rows

    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Node(i, j, gap, rows)
            grid[i].append(spot)

    return grid


def draw_grid(win, rows, width):
    gap = width // rows
    # draw horizontal lines
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        ## draw vertical lines
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))


'''
Method that will draw each node in the board
'''


def draw(win, grid, rows, width):
    win.fill(WHITE)

    for row in grid:
        for spot in row:
            spot.draw(win)

    draw_grid(win, rows, width)
    pygame.display.update()


'''
Method that will return the row and column where user clicked on in the board
'''


def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap

    return row, col

'''
Main method that will run the program
'''
def main(win, width):
    print()
    print()
    print("Welcome to the A* Search Visualizer")
    print("First click will input your start node")
    print("Second click will input your destination node")
    print("Press Space to run the application")
    print("Press c to reset the board")
    print()
    ROWS = int(input("Input the number of rows for the board size (Use a smaller number for a slower computer):" ))

    grid = make_grid(ROWS, width)

    start = None
    end = None

    run = True
    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            # if we press on the left mouse button
            if pygame.mouse.get_pressed()[0]:  # LEFT
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]
                if not start and spot != end:
                    start = spot
                    start.make_start()

                elif not end and spot != start:
                    end = spot
                    end.make_end()

                elif spot != end and spot != start:
                    spot.make_barrier()

            # if we press on the left mouse button
            elif pygame.mouse.get_pressed()[2]:  # RIGHT
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]
                spot.reset()
                if spot == start:
                    start = None
                elif spot == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)

                    algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)

                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)

    pygame.quit()


main(WIN, WIDTH)
