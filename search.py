from priority_queue import *


def get_flag_position(x_size, y_size, grid_data):
    for y in range(y_size):
        for x in range(x_size):
            if grid_data[y][x] == 'F':
                return y, x


def uniform_cost_search(root):
    openList = PriorityQueue()  # priority openList {(cost, grid_data)}
    closedList = set()  # set

    flag_y, flag_x = get_flag_position(root.x_size, root.y_size, root.grid_data)

    g_x = root.cost
    f_x = root.cost + h(root, (flag_y, flag_x))

    openList.insert(root, f_x)

    while not openList.is_empty():
        currentNode = openList.remove()

        closedList.add(currentNode)

        suc = currentNode.get_successor()

        for childNode in suc:
            if childNode.isFinished:
                return childNode.actions
            if childNode not in closedList:
                g_x_childNode = childNode.cost
                f_x_childNode = childNode.cost + h(childNode, (flag_y, flag_x))
                openList.insert(childNode, f_x_childNode)


def h(node, goal_position):
    flag_y, flag_x = goal_position
    d_x = abs(node.player_x - flag_x)
    d_y = abs(node.player_y - flag_y)
    return d_x + d_y