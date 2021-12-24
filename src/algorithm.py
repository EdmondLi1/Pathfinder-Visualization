from queue import PriorityQueue
import constants as c
import pygame

def calculate_hCost(end_node, current_node):
    h_xDiff = abs(current_node.get_x() - end_node.get_x())
    h_yDiff = abs(current_node.get_y() - end_node.get_y())

    hCost = h_xDiff + h_yDiff

    return hCost

def reconstruct_path(cameFrom, currentNode, draw):
	while currentNode in cameFrom:
		currentNode = cameFrom[currentNode]
		currentNode.make_path()
		draw()


def pathfinding(draw, grid, startNode, endNode):
    """Function which contains the main algorithm which will find the shortest path."""
    count = 0
    startNode_Fcost = 0
   
    open_set = PriorityQueue() 
    open_set.put((startNode, count, startNode_Fcost))

    # Gscore map used to keep track of the gCosts of each node
    # gscore is the shortest distance to get from startNode to currentNode
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[startNode] = 0

    # Fscore map used to keep track of the fCosts of each node
    # fScore is the predicted distance from the currentNode to the endNode
    f_score = {node: float("inf") for row in grid for node in row}
    f_score[startNode] = calculate_hCost(endNode, startNode)

    cameFrom = {}
    open_set_hash = {startNode}

    # Loop within main simulation loop
    while not open_set.empty():

        # Create esacape incasee algorithm dies; remains in constant loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()


        currentNode = open_set.get()[0]
        open_set_hash.remove(currentNode)

        if currentNode == endNode:
            reconstruct_path(cameFrom, currentNode, draw)
            return True
            # pass

        for neighbour in currentNode.neighbours:
            tentative_g_score = g_score[currentNode] + 1
            # If the new gCost is lower than our neighbours, update it 
            if tentative_g_score < g_score[neighbour]:
                cameFrom[neighbour] = currentNode
                g_score[neighbour] = tentative_g_score
                f_score[neighbour] = tentative_g_score + calculate_hCost(endNode, neighbour)

                # If neighbour isnt in the open (vsiisted hash, add it and make it opened)
                if neighbour not in open_set_hash:
                    count += 1
                    open_set.put((neighbour, count, f_score[neighbour]))
                    open_set_hash.add(neighbour)
                    neighbour.set_state(c.OPEN)

        draw()

        if currentNode != startNode:
            currentNode.set_state(c.CLOSED)
        
    # If no path is found, return false
    return False
