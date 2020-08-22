from copy import deepcopy


class Node(object):
    childs = []
    parent = None

    def __init__(self, game_map, action):
        self.game_map = game_map
        self.action = action
        self.flag_y, self.flag_x = get_flag_position(game_map)

    def print_flag_pos(self):
        print(self.flag_y, self.flag_x)

    def get_successor(self):
        # check direction of current state and parent state
        player_heading = self.game_map.player_heading
        parent_heading = self.parent.game_map.player_heading if self.parent else None
        UP = self.game_map.UP
        DOWN = self.game_map.DOWN
        LEFT = self.game_map.LEFT
        RIGHT = self.game_map.RIGH

        for move in self.game_map.MOVES:
            if player_heading == UP:
                # move cannot be left
                if parent_heading == LEFT and move == 'l':
                    continue
                if parent_heading == RIGHT and move == 'r':
                    continue
            elif player_heading == DOWN:
                # move cannot be left
                if parent_heading == LEFT and move == 'r':
                    continue
                if parent_heading == RIGHT and move == 'l':
                    continue
            elif player_heading == LEFT:
                # move cannot be left
                if parent_heading == UP and move == 'r':
                    continue
                if parent_heading == DOWN and move == 'l':
                    continue
            elif player_heading == RIGHT:
                # move cannot be left
                if parent_heading == UP and move == 'l':
                    continue
                if parent_heading == DOWN and move == 'r':
                    continue

            if self.game_map.apply_move(move) == self.game_map.SUCCESS:
                # append new state
                child = deepcopy(self)
                self.childs.append(child)

