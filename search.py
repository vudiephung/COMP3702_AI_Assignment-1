from priority_queue import *


def get_flag_position(map_data):
    for y in range(map_data.y_size):
        for x in range(map_data.x_size):
            if map_data.grid_data[y][x] == map_data.FLAG_SYMBOL:
                return y, x


# def get_tuples(node):
#     map_data = node.map_data
#     return (tuple(map(tuple, map_data.grid_data))), map_data.player_x, map_data.player_y, map_data.player_heading


def uniform_cost_search(root):
    openList = PriorityQueue()  # priority openList {(cost, grid_data)}
    closedList = set()  # set

    flag_y, flag_x = get_flag_position(root.map_data)

    g_x = root.cost
    f_x = root.cost + h(root, (flag_y, flag_x))
    print(flag_y, flag_x, root.cost, f_x)
    openList.insert(root, root.cost)

    while not openList.is_empty():
        currentNode = openList.remove()

        closedList.add(currentNode)

        suc = currentNode.get_successor()

        for childNode in suc:
            childNode.cost += currentNode.cost
            if childNode.map_data.is_finished():
                return childNode.actions

            if childNode not in closedList:
                g_x_childNode = childNode.cost
                f_x_childNode = childNode.cost + h(childNode, (flag_y, flag_x))
                openList.insert(childNode, f_x_childNode)


def h(node, goal_position):
    flag_y, flag_x = goal_position
    d_x = abs(node.map_data.player_x - flag_x)
    d_y = abs(node.map_data.player_y - flag_y)
    return d_x + d_y


def a_star():
    pass


class Search:
    pass
