import pygame
import constants as c

class Node:
    def __init__(self, row, col, width, max_rows):
        """Initizate all the parameters/attribute the class Node contains. Each <Node> object will have:
        row, col, (x, y -> for drawing on pygame), colour (type of Node), neighbours attribute, width 
        (WITDH_OF_NODE), and MAX_ROWS (on the grid)."""
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.colour = c.WHITE
        self.neighbours = []
        self.width = width
        self.max_rows = max_rows

    def get_pos(self):
        """Returns the position of the Node."""
        # Index based on y, x
        return self.row, self.col

    def get_x(self):
        """Returns the x-coordinate of the node. In this case, its 'y'."""
        # y = col * width (x-dir)
        return self.y
    
    def get_y(self):
        """Returns the x-coordinate of the node. In this case, its 'x'."""
        # x = row * width (y-dir)
        return self.x
    
    def is_state(self, state):
        """Function that returns boolean state."""
        return self.colour == state

    def set_state(self, state):
        """Sets the current state of the node (symbolized with colours)."""
        possibleStates = [c.OPEN, c.CLOSED, c.BARRIER, 
        c.START, c.END, c.PATH]

        if state in possibleStates:
            self.colour = state
 
    def reset_state(self):
        """Changes the state back to white; NULL."""
        self.colour = c.WHITE

    # Does not include Diagonalizaiton between currentNode and it's neighbours.
    def check_neighbours(self, grid):
        """Function used to check the currentNode's neighbour (up, down, left, and right). Doesn't support diagonalziation meaninng the shortnest 
        path will NOT include diagaonal paths."""
        self.neighbours = []

        if (self.row + 1 < self.max_rows and not grid[self.row + 1][self.col].is_state(c.BARRIER)): # Checks if row below (+y direction) is within our grid
            self.neighbours.append(grid[self.row + 1][self.col])

        if (self.row > 0 and not grid[self.row - 1][self.col].is_state(c.BARRIER)): # Checks if row above (-y direction) is within our grid            
            self.neighbours.append(grid[self.row - 1][self.col])
        
        # TAKEN THAT GRID IS N X N (N = MAX_ROWS; a SQUARE)
        if (self.col + 1 < self.max_rows and not grid[self.row][self.col + 1].is_state(c.BARRIER)):  # Checks if col rightward (+x direction) is within our grid 
            self.neighbours.append(grid[self.row][self.col + 1])
        
        if (self.col > 0 and not grid[self.row][self.col - 1].is_state(c.BARRIER)):  # Checks if col leftward (+x direction) is within our grid 
            self.neighbours.append(grid[self.row][self.col - 1])
  

    def draw_node(self, screen):
        """Function that allows the program to display the node in its given (x, y) and NODE_WIDTH."""
        pygame.draw.rect(screen, self.colour, (self.x, self.y, self.width, self.width))

    def __lt__(self, other):
        """Built-in function used to *avoid* errors when comparing in PriorityQueue."""
        return False
        