from priority_queue import *


def get_flag_position(game_map):
    for y in range(game_map.y_size):
        for x in range(game_map.x_size):
            if game_map.grid_data[y][x] == game_map.FLAG_SYMBOL:
                return y, x


def get_tuples(node):
    map_data = node.map_data
    return (tuple(map(tuple, map_data.grid_data))), map_data.player_x, map_data.player_y, map_data.player_heading


def uniform_cost_search(root):
    openList = PriorityQueue()  # priority openList {(cost, grid_data)}
    closedList = set()  # set

    openList.insert(root, root.cost)

    while not openList.is_empty():
        currentNode = openList.remove()

        closedList.add(get_tuples(currentNode))

        suc = currentNode.get_successor()

        for childNode in suc:
            childNode.cost += currentNode.cost
            if childNode.map_data.is_finished():
                return childNode.actions

            if get_tuples(childNode) not in closedList:
                openList.insert(childNode, childNode.cost)


class Search:
    pass
