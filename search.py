from priority_queue import *


def get_flag_position(x_size, y_size, grid_data):
    flag_x = flag_y = port_x = port_y = -1
    for y in range(y_size):
        for x in range(x_size):
            if grid_data[y][x] == 'F':
                flag_y, flag_x = y, x
            elif grid_data[y][x] == 'T':
                port_y, port_x = y, x
    return {'flag': (flag_x, flag_y), 'port': (port_x, port_y)}


def h(node, goal_position):
    flag_y, flag_x = goal_position
    d_x = abs(node.player_x - flag_x)
    d_y = abs(node.player_y - flag_y)
    return d_x + d_y


# def get_port_position(x_size, y_size, grid_data):
#     for y in range(y_size):
#         for x in range(x_size):
#             if grid_data[y][x] == 'T':
#                 return y, x


def get_f_x(node, flag_x, flag_y, port_x, port_y):
    existed_port = True if (port_x, port_y) != (-1, -1) else False
    f_x = node.cost + h(node, (flag_y, flag_x))
    f_x += h(node, (port_y, port_x)) if existed_port else 0
    return f_x


def uniform_cost_search(root):
    openList = PriorityQueue()  # priority openList {(cost, grid_data)}
    closedList = set()  # set

    flag_port_position = get_flag_position(root.x_size, root.y_size, root.grid_data)
    flag_x, flag_y = flag_port_position['flag']
    port_x, port_y = flag_port_position['port']

    f_x = get_f_x(root, flag_x, flag_y, port_x, port_y)
    openList.insert(root, f_x)

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
                # g_x_childNode = childNode.cost
                # f_x_childNode = childNode.cost + h(childNode, (flag_y, flag_x))
                f_x_childNode = get_f_x(childNode, flag_x, flag_y, port_x, port_y)
                openList.insert(childNode, f_x_childNode)
