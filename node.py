from copy import deepcopy


class Node(object):
    parent = None
    cost = 1
    actions = []

    def __init__(self, map_data):
        self.map_data = map_data

    def print_flag_pos(self):
        print(self.flag_y, self.flag_x)

    def get_successor(self):
        successors = []
        # check direction of current state and parent state
        # copy_map_data = [row[:] for row in self.map_data]
        player_heading = self.map_data.player_heading
        parent_heading = self.parent.map_data.player_heading if self.parent else None
        UP = self.map_data.UP
        DOWN = self.map_data.DOWN
        LEFT = self.map_data.LEFT
        RIGHT = self.map_data.RIGHT

        for move in self.map_data.MOVES:
            if player_heading == UP:
                # move cannot be left
                if parent_heading == LEFT and move == 'l':
                    continue
                elif parent_heading == RIGHT and move == 'r':
                    continue
            elif player_heading == DOWN:
                # move cannot be left
                if parent_heading == LEFT and move == 'r':
                    continue
                elif parent_heading == RIGHT and move == 'l':
                    continue
            elif player_heading == LEFT:
                # move cannot be left
                if parent_heading == UP and move == 'r':
                    continue
                elif parent_heading == DOWN and move == 'l':
                    continue
            elif player_heading == RIGHT:
                # move cannot be left
                if parent_heading == UP and move == 'l':
                    continue
                elif parent_heading == DOWN and move == 'r':
                    continue

            copy_map_data = deepcopy(self.map_data)
            if copy_map_data.apply_move(move) == self.map_data.SUCCESS:
                # append new state
                child = Node(copy_map_data)
                child.parent = self
                child.actions = self.actions.copy()
                child.actions.append(move)
                successors.append(child)
            else:
                del copy_map_data

        return successors
