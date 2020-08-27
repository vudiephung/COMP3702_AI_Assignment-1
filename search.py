from priority_queue import *


def get_goal_position(x_size, y_size, grid_data):
    flag_x = flag_y = port_x = port_y = -1
    for y in range(y_size):
        for x in range(x_size):
            if grid_data[y][x] == 'F':
                flag_y, flag_x = y, x
            elif grid_data[y][x] == 'T':
                port_y, port_x = y, x
    return {'flag': (flag_x, flag_y), 'port': (port_x, port_y)}


def heuristic(node):
    goals_position = node.goals_position
    flag_x, flag_y = goals_position['flag']
    port_x, port_y = goals_position['port']
    d_x_flag = abs(node.player_x - flag_x)
    d_y_flag = abs(node.player_y - flag_y)

    if (port_x, port_y) != (-1, -1):
        d_x_port = abs(node.player_x - port_x)
        d_y_port = abs(node.player_y - port_y)
        return min(d_x_flag + d_y_flag, d_x_port + d_y_port) * 1.5
    else:
        return (d_x_flag + d_y_flag) * 1.5


def get_f_x(node):
    return node.cost + node.heuristic


def uniform_cost_search(root):
    openList = PriorityQueue()
    closedList = set()

    openList.insert(root, get_f_x(root))

    while not openList.is_empty():
        currentNode = openList.remove()

        if currentNode.grid_data_tuple is None:
            currentNode.grid_data_tuple = tuple(map(tuple, currentNode.grid_data))

        closedList.add(currentNode)

        suc = currentNode.get_successor()

        for childNode in suc:
            if childNode.isFinished:
                return childNode.actions
            if childNode not in closedList:
                openList.insert(childNode, get_f_x(childNode))
