from laser_tank import *


class Node(object):
    cost = 1
    actions = []

    def __init__(self, map_data):
        self.map_data = map_data

    def __eq__(self, other):
        if other is None:
            return False
        this_map_data = self.map_data
        other_map_data = other.map_data
        equal_grid = this_map_data.grid_data == other_map_data.grid_data
        equal_tank_position = this_map_data.player_x == other_map_data.player_x and \
                              this_map_data.player_y == other_map_data.player_y
        equal_heading = this_map_data.player_heading == other_map_data.player_heading
        return equal_grid and equal_tank_position and equal_heading

    def __hash__(self):
        return hash(self.get_tuples())

    def copy(self, ):
        pass

    def print_flag_pos(self):
        print(self.flag_y, self.flag_x)

    def get_tuples(self):
        map_data = self.map_data
        return (tuple(map(tuple, map_data.grid_data))), map_data.player_x, map_data.player_y, map_data.player_heading
        # return tuple(map(tuple, map_data.grid_data))

    def get_successor(self):
        successors = []

        for move in self.map_data.MOVES:
            copy_map_data = self.copy_map_data(self.map_data)
            if copy_map_data.apply_move(move) == self.map_data.SUCCESS:
                # append new state
                child = Node(copy_map_data)
                child.actions = self.actions.copy()
                child.actions.append(move)
                successors.append(child)
            else:
                del copy_map_data

        return successors

    def copy_map_data(self, map_data):
        # copy_player_x = deepcopy(map_data.player_x)
        # copy_player_y = deepcopy(map_data.player_y)
        # copy_player_heading = deepcopy(map_data.player_heading)
        copy_grid_data = [row[:] for row in map_data.grid_data]
        copy_map_data = LaserTankMap(map_data.x_size, map_data.y_size, copy_grid_data,
                                     map_data.player_x, map_data.player_y, map_data.player_heading)
        return copy_map_data
