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

        heapq.heappush(openList, root)  # need to change!!! add to the heap by the lowest cost
        foundGoal = False

        while openList and not foundGoal:
            currentNode = heapq.heappop(openList)
            closedList.add(currentNode)

            currentNode.get_successor()

            for childNode in currentNode.childs:
                if childNode.game_map.is_finished():
                    print("Result found!")
                    foundGoal = True
                    self.path_trace(pathToSolution, childNode)
                    break
                if childNode not in openList and childNode not in closedList:
                    # if (not self.existed_puzzle(childNode.puzzle, openList) and not self.existed_puzzle(
                    # childNode.puzzle, closedList)): openList.append(childNode)
                    heapq.heappush(openList, childNode)

        return pathToSolution
