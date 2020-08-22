import node
import heapq


def get_flag_position(game_map):
    for y in range(game_map.y_size):
        for x in range(game_map.x_size):
            if game_map.grid_data[y][x] == game_map.FLAG_SYMBOL:
                return y, x


class Search:
    def uniform_cost_search(self, root):
        pathToSolution = []
        openList = []  # priority queue
        closedList = {}  # set

        heapq.heappush(openList, root)
