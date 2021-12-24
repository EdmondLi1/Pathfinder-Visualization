import node 
import constants as const
import algorithm
import pygame

# Square board
WIDTH = 600
HEIGHT = 600
ROWS = 50
COLS = 50
WIDTH_OF_NODE = HEIGHT // ROWS


def init_grid(rows, cols, width_node):
    """Function used to initalize a grid (board) within an array.
    Uses the node class in node.py to intilize each square on the grid."""

    grid = []

    for i in range(rows):
        grid.append([])
        for j in range(cols):
            new_node = node.Node(i, j, width_node, rows)
            grid[i].append(new_node)

    return grid


def draw_gridlines(screen, rows, cols, width, width_node, height):
    """Draws the gridlines of the grid."""
    
    # Draws horizontal lines from (x = 0 (leftmost side) to width (rightmost side))
    for i in range(rows):
        pygame.draw.line(screen, const.GRIDLINE_COLOUR, (0, i * width_node), (width, i * width_node))

        # Draw the vertical lines from (x = current col to down the screen; same x-value)
        for j in range(cols):
            pygame.draw.line(screen, const.GRIDLINE_COLOUR, (j * width_node, 0), (width_node * j, height))


def draw_grid(screen, grid, rows, cols, width_node, width, height):
    """Draws the grid with coloured nodes, along with the gridlines."""

    for row in grid:
        for node in row:
            node.draw_node(screen)

    draw_gridlines(screen, rows, cols, width, width_node, height)
    pygame.display.update()


def get_pos_mouse(pos, rows, width_node):
    y, x = pos
    row = y // width_node
    col = x // width_node

    return row, col


def main():
    """Mainline logic for the A* Pathfinding Visualization."""

    pygame.init()
    # Screen and background variables
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("A* Pathfinder Visualization")

    grid = init_grid(ROWS, COLS, WIDTH_OF_NODE)
    draw_grid(screen, grid, ROWS, COLS, WIDTH_OF_NODE, WIDTH, HEIGHT)

    start_node = None
    end_node = None

    start_algorithm = False 
    clickStart = False

    # Main simulation Loop variable
    clock = pygame.time.Clock() 
    keepGoing = True

    # main visual loop
    while keepGoing:
        clock.tick(100)
        draw_grid(screen, grid, ROWS, COLS, WIDTH_OF_NODE, WIDTH, HEIGHT)

        for event in pygame.event.get():
            # IF User has Quit.
            if event.type == pygame.QUIT:
                keepGoing = False
            
            # Mouse Events
            # Boolean values for left, right mouse click
            leftClick, middleClick, rightClick = pygame.mouse.get_pressed()

            if pygame.mouse.get_pressed():
                pos = pygame.mouse.get_pos()
                # The Nodes row, col (positionn in the grid)
                row, col = get_pos_mouse(pos, ROWS, WIDTH_OF_NODE)
                current_node = grid[row][col]

                # Left Click is to ADD nodes
                if leftClick:
                    # ADDING START NODE 
                    if (not start_node and current_node != end_node):
                        start_node = current_node
                        start_node.set_state(const.START)

                    # ADDING END NODE 
                    elif (not end_node and current_node != start_node) :
                        end_node = current_node
                        end_node.set_state(const.END)

                    # ADDING BARRIER (WALL) NODE 
                    elif (current_node != start_node and current_node != end_node):
                        current_node.set_state(const.BARRIER)

                # Right Click is to REMOVE nodes
                elif rightClick:
                    current_node.reset_state()
 
                    if current_node == start_node:
                        start_node = None

                    elif current_node == end_node:
                        end_node = None

                # Remove the start/end/nodes
                elif middleClick and not start_algorithm:
                    start_algorithm, clickStart = True, True
                    
            # Start the algorithm
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and (not start_algorithm or clickStart):
                    for row in grid:
                        for node in row:
                            node.check_neighbours(grid)

                    # Tech With tim and everyone ;)
                    algorithm.pathfinding(lambda: draw_grid(screen, grid, ROWS, COLS, WIDTH_OF_NODE, WIDTH, HEIGHT),
                    grid, start_node, end_node)
           
                # C key or BACKSPACE key to CLEAR the board; makes a new board
                elif (event.key == pygame.K_c or event.key == pygame.K_BACKSPACE):
                    start_node, end_node = None, None
                    grid = init_grid(ROWS, COLS, WIDTH)

                # Lastly, 'q' to quit the pygame window
                elif event.key == pygame.K_q:
                    keepGoing = False

    pygame.quit()

main()
