from queue import PriorityQueue
import constants as c
import pygame

def heuristic(node_one, node_two):
    x1, y1 = node_one.get_pos()
    x2, y2 = node_two.get_pos()
    h_xDiff = abs(x1 - x2)
    h_yDiff = abs(y1 - y2)

    # hCost = h_xDiff + h_yDiff
    return abs(y1 - y2) + abs(x1 - x2)

def reconstruct_path(cameFrom, openNode, draw):
	while openNode in cameFrom:
		openNode = cameFrom[openNode]
		openNode.set_state(c.PATH)
		draw()


def pathfinding(draw, grid, startNode, endNode):
    """Function which contains the main algorithm which will find the shortest path."""
    count = 0   
    open_set = PriorityQueue() 
    open_set.put((0, count, startNode))

    # Gscore map used to keep track of the gCosts of each node
    # gscore is the shortest distance to get from startNode to currentNode
    g_score = {newNode: float("inf") for row in grid for newNode in row}
    g_score[startNode] = 0

    # Fscore map used to keep track of the fCosts of each node
    # fScore is the predicted distance from the currentNode to the endNode
    f_score = {newNode: float("inf") for row in grid for newNode in row}
    f_score[startNode] = heuristic(endNode, startNode)

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


        currentNode = open_set.get()[2]
        open_set_hash.remove(currentNode)

        if currentNode == endNode:
            reconstruct_path(cameFrom, endNode, draw)
            endNode.set_state(c.END)
            return True

        for neighbour in currentNode.neighbours:
            tentative_g_score = g_score[currentNode] + 1

            # If the new gCost is lower than our neighbours, update it 
            if tentative_g_score < g_score[neighbour]:
                cameFrom[neighbour] = currentNode
                g_score[neighbour] = tentative_g_score
                f_score[neighbour] = tentative_g_score + heuristic(endNode, neighbour)

                # If neighbour isnt in the open (vsiisted hash, add it and make it opened)
                if neighbour not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbour], count, neighbour))
                    open_set_hash.add(neighbour)
                    neighbour.set_state(c.OPEN)

        draw()

        if currentNode != startNode:
            currentNode.set_state(c.CLOSED)
        
    # If no path is found, return false
    return False
