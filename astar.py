import pygame
import math
from queue import PriorityQueue

WIDTH = 600

# 600 x 600 display window
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Visualizer")

# colors used for our visualizer
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


'''
Node class that contains setter and getter methods about each state of the node
'''
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

    '''
    Method that will update neighbors in the grid 
    '''
    def update_neighbors(self, grid):
        self.neighbors = []
        # if the current nodes row position is not at the top
        # and the row below is not a barrier, then add it to the neighbors list
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():  # down
            self.neighbors.append(grid[self.row + 1][self.col])

        # if the current row is positive and the row above is
        # not a barrier then add it to the neighbors list
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():  # up
            self.neighbors.append(grid[self.row - 1][self.col])

        # if the current node positive and not too far right
        # is and the row to the right is not a barrier,
        # then add it to the neighbors list
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():  # right
            self.neighbors.append(grid[self.row][self.col + 1])

        # similar logic above but we check if the row to the left is not a barrier
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():  # left
            self.neighbors.append(grid[self.row][self.col - 1])


'''
Method that compares one node to the other if they are similar.
Current node is always less than the other node
'''
def __lt__(self, other):
    return False

    '''
    Method that computes the manhattan distance (Heuristic function)
    '''
def heuristic(p1, p2, ):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)
    # old code uses euclidean distance (shortest path is slightly longer, generally speaking)
    #return int((abs(x1 - x2)**2 + abs(y1 - y2)**2)**0.5)


'''
Method that reconstructs shortest path once found via backtracking
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
    open_set = PriorityQueue() # open list where the to be explored nodes are put into
    open_set.put((0, count, start)) # put the starting node in the open set (has a h(n) of 0, count of 0)
    came_from = {}
    g_score = {node: float("inf") for row in grid for node in row}
    # initialize all of the costs to reach node n from the start node to infinity

    g_score[start] = 0 # initial cost to reach start node will be 0

    f_score = {node: float("inf") for row in grid for node in row} # estimated cost of cheapest
    # solution is initially infinity

    f_score[start] = heuristic(start.get_pos(), end.get_pos()) # get the f score for the start node
    # (manhattan distance)

    open_set_hash = {start} # insert the start node into a set
    # set keeps track of all items in PQ

    while not open_set.empty(): # while the open sets has elements

        for e in pygame.event.get(): # handling if user quits program
            if e.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2] # get the node from open set, and not the f and count score
        open_set_hash.remove(current) # remove the current node from hash set as it's been removed from PQ

        if current == end: # if we found our destination, we need to reconstruct the path
            # make path
            reconstruct_path(came_from, end, draw)
            return True

        for neighbor in current.neighbors: # for each neighbor of the current node
            temp_g_score = g_score[current] + 1  # get the g score of the next node (one more node over)

            if temp_g_score < g_score[neighbor]: # if we found a better way then the current way
                came_from[neighbor] = current # update the path as its optimal
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + heuristic(neighbor.get_pos(), end.get_pos())

                if neighbor not in open_set_hash: # if neighbor is not in the hash set
                    count += 1; # add the neighbor in the set
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw() # render the path

        # if the current node is not the start node close it
        if current != start:
            current.make_closed()

    return False # did not find path


'''
Generate the grid in the board
'''
def make_grid(rows, width):
    grid = []
    gap = width // rows

    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Node(i, j, gap, rows)
            grid[i].append(spot)

    return grid

'''
Method that will draw the physical grid on the board 
'''
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
    print("First left click will input your start node")
    print("Second left click will input your destination node")
    print("Right click to delete nodes on the board")
    print("Press Space to run the application")
    print("Press c to reset the board")
    print()
    ROWS = int(input("Input the number of rows for the board size (Use a smaller number for a slower computer):" ))

    grid = make_grid(ROWS, width)

    start = None
    end = None

    run = True
    while run: # while the program is still running
        draw(win, grid, ROWS, width) # draw the board

        for event in pygame.event.get(): # exit if somebody quit
            if event.type == pygame.QUIT:
                run = False

            # if we press on the left mouse button
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width) # get the clicked position
                spot = grid[row][col]
                if not start and spot != end:
                    start = spot
                    start.make_start() # the first left click is the start position

                elif not end and spot != start:
                    end = spot    # second click is end postion
                    end.make_end()

                elif spot != end and spot != start:
                    spot.make_barrier() # rest of the clicks are barriers

            # if we press on the right mouse button
            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]
                spot.reset() # any node that is right clicked is cleared (turned white)
                if spot == start:
                    start = None # if we right click on the start position, delete the node (make it white)
                elif spot == end:
                    end = None # if we right click on end position, delete node

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)
                            # when we hit space bar, update the condition of each node as search is started

                    algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end) # run the search algo

                if event.key == pygame.K_c: # clear the board
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)

    pygame.quit()


main(WIN, WIDTH)
