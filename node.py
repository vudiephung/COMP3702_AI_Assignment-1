from laser_tank import *


def copy_map_data(grid_data, x_size, y_size, player_x, player_y, player_heading, move):
    if move == 's':
        grid_data = [row[:] for row in grid_data]
    new_map_data = LaserTankMap(x_size, y_size, grid_data, player_x, player_y, player_heading)
    return new_map_data


def get_tuples(grid_data, player_x, player_y, player_heading):
    return (tuple(map(tuple, grid_data))), player_x, player_y, player_heading


class Node(object):
    actions = []
    isFinished = False

    def __init__(self, x_size, y_size, grid_data, player_x, player_y, player_heading, cost):
        self.y_size = y_size
        self.x_size = x_size
        self.grid_data = grid_data
        self.player_heading = player_heading
        self.player_y = player_y
        self.player_x = player_x
        self.cost = cost

    def __eq__(self, other):
        equal_grid = self.grid_data == other.grid_data
        equal_tank_position = self.player_x == other.player_x and \
                              self.player_y == other.player_y
        equal_heading = self.player_heading == other.player_heading
        return equal_grid and equal_tank_position and equal_heading

    def __hash__(self):
        return hash(get_tuples(self.grid_data, self.player_x, self.player_y, self.player_heading))

    def get_successor(self):
        successors = []

        for move in ('f', 'l', 'r', 's'):
            new_map_data = copy_map_data(self.grid_data, self.x_size, self.y_size,
                                         self.player_x, self.player_y, self.player_heading, move)
            if new_map_data.apply_move(move) == new_map_data.SUCCESS:
                # append new state
                child = Node(new_map_data.x_size, new_map_data.y_size, new_map_data.grid_data,
                             new_map_data.player_x, new_map_data.player_y, new_map_data.player_heading, self.cost + 1)
                child.actions = self.actions[:]
                child.actions.append(move)
                if new_map_data.is_finished():
                    child.isFinished = True
                else:
                    child.isFinished = False
                successors.append(child)
            del new_map_data

        return successors



def cell_is_blocked(grid_data, y, x):
    OBSTACLE_SYMBOL = '#'
    BRIDGE_SYMBOL = 'B'
    BRICK_SYMBOL = 'K'

    MIRROR_UL_SYMBOL = '1'
    MIRROR_UR_SYMBOL = '2'
    MIRROR_DL_SYMBOL = '3'
    MIRROR_DR_SYMBOL = '4'

    ANTI_TANK_UP_SYMBOL = 'U'
    ANTI_TANK_DOWN_SYMBOL = 'D'
    ANTI_TANK_LEFT_SYMBOL = 'L'
    ANTI_TANK_RIGHT_SYMBOL = 'R'
    ANTI_TANK_DESTROYED_SYMBOL = 'X'

    symbol = grid_data[y][x]
    # collision: obstacle, bridge, mirror (all types), anti-tank (all types)
    if symbol == OBSTACLE_SYMBOL or symbol == BRIDGE_SYMBOL or symbol == BRICK_SYMBOL or \
            symbol == MIRROR_UL_SYMBOL or symbol == MIRROR_UR_SYMBOL or \
            symbol == MIRROR_DL_SYMBOL or symbol == MIRROR_DR_SYMBOL or \
            symbol == ANTI_TANK_UP_SYMBOL or symbol == ANTI_TANK_DOWN_SYMBOL or \
            symbol == ANTI_TANK_LEFT_SYMBOL or symbol == ANTI_TANK_RIGHT_SYMBOL or \
            symbol == ANTI_TANK_DESTROYED_SYMBOL:
        return True
    return False


def cell_is_game_over(x_size, y_size, grid_data, y, x):
    WATER_SYMBOL = 'W'

    ANTI_TANK_UP_SYMBOL = 'U'
    ANTI_TANK_DOWN_SYMBOL = 'D'
    ANTI_TANK_LEFT_SYMBOL = 'L'
    ANTI_TANK_RIGHT_SYMBOL = 'R'

    # check for water
    if grid_data[y][x] == WATER_SYMBOL:
        return True

    # check for anti-tank
    # up direction
    for i in range(y, -1, -1):
        if grid_data[i][x] == ANTI_TANK_DOWN_SYMBOL:
            return True
        # if blocked, can stop checking for anti-tank
        if cell_is_blocked(grid_data, i, x):
            break

    # down direction
    for i in range(y, y_size):
        if grid_data[i][x] == ANTI_TANK_UP_SYMBOL:
            return True
        # if blocked, can stop checking for anti-tank
        if cell_is_blocked(grid_data, i, x):
            break

    # left direction
    for i in range(x, -1, -1):
        if grid_data[y][i] == ANTI_TANK_RIGHT_SYMBOL:
            return True
        # if blocked, can stop checking for anti-tank
        if cell_is_blocked(grid_data, y, i):
            break

    # right direction
    for i in range(x, x_size):
        if grid_data[y][i] == ANTI_TANK_LEFT_SYMBOL:
            return True
        # if blocked, can stop checking for anti-tank
        if cell_is_blocked(grid_data, y, i):
            break

    # no water or anti-tank danger
    return False


def cell_is_laser_movable(grid_data, y, x, heading):
    BRIDGE_SYMBOL = 'B'

    MIRROR_UL_SYMBOL = '1'
    MIRROR_UR_SYMBOL = '2'
    MIRROR_DL_SYMBOL = '3'
    MIRROR_DR_SYMBOL = '4'

    ANTI_TANK_UP_SYMBOL = 'U'
    ANTI_TANK_DOWN_SYMBOL = 'D'
    ANTI_TANK_LEFT_SYMBOL = 'L'
    ANTI_TANK_RIGHT_SYMBOL = 'R'
    ANTI_TANK_DESTROYED_SYMBOL = 'X'

    # directions
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

    MOVABLE_SYMBOLS = {UP: [BRIDGE_SYMBOL, MIRROR_UL_SYMBOL, MIRROR_UR_SYMBOL, ANTI_TANK_UP_SYMBOL,
                            ANTI_TANK_LEFT_SYMBOL, ANTI_TANK_RIGHT_SYMBOL, ANTI_TANK_DESTROYED_SYMBOL],
                       DOWN: [BRIDGE_SYMBOL, MIRROR_DL_SYMBOL, MIRROR_DR_SYMBOL, ANTI_TANK_DOWN_SYMBOL,
                              ANTI_TANK_LEFT_SYMBOL, ANTI_TANK_RIGHT_SYMBOL, ANTI_TANK_DESTROYED_SYMBOL],
                       LEFT: [BRIDGE_SYMBOL, MIRROR_UL_SYMBOL, MIRROR_DL_SYMBOL, ANTI_TANK_UP_SYMBOL,
                              ANTI_TANK_DOWN_SYMBOL, ANTI_TANK_LEFT_SYMBOL, ANTI_TANK_DESTROYED_SYMBOL],
                       RIGHT: [BRIDGE_SYMBOL, MIRROR_UR_SYMBOL, MIRROR_DR_SYMBOL, ANTI_TANK_UP_SYMBOL,
                               ANTI_TANK_DOWN_SYMBOL, ANTI_TANK_RIGHT_SYMBOL, ANTI_TANK_DESTROYED_SYMBOL]
                       }

    return grid_data[y][x] in MOVABLE_SYMBOLS[heading]


def apply_move(move, x_size, y_size, grid_data, player_x, player_y, player_heading):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

    MOVE_FORWARD = 'f'
    TURN_LEFT = 'l'
    TURN_RIGHT = 'r'
    SHOOT_LASER = 's'

    COLLISION = 1
    GAME_OVER = 2

    LAND_SYMBOL = ' '
    WATER_SYMBOL = 'W'
    OBSTACLE_SYMBOL = '#'
    BRIDGE_SYMBOL = 'B'
    BRICK_SYMBOL = 'K'
    ICE_SYMBOL = 'I'
    TELEPORT_SYMBOL = 'T'
    FLAG_SYMBOL = 'F'

    MIRROR_UL_SYMBOL = '1'
    MIRROR_UR_SYMBOL = '2'
    MIRROR_DL_SYMBOL = '3'
    MIRROR_DR_SYMBOL = '4'

    ANTI_TANK_UP_SYMBOL = 'U'
    ANTI_TANK_DOWN_SYMBOL = 'D'
    ANTI_TANK_LEFT_SYMBOL = 'L'
    ANTI_TANK_RIGHT_SYMBOL = 'R'
    ANTI_TANK_DESTROYED_SYMBOL = 'X'

    if move == MOVE_FORWARD:
        # get coordinates for next cell
        if player_heading == UP:
            next_y = player_y - 1
            next_x = player_x
            if next_y < 0:
                return COLLISION
        elif player_heading == DOWN:
            next_y = player_y + 1
            next_x = player_x
            if next_y >= y_size:
                return COLLISION
        elif player_heading == LEFT:
            next_y = player_y
            next_x = player_x - 1
            if next_x < 0:
                return COLLISION
        else:
            next_y = player_y
            next_x = player_x + 1
            if next_x >= x_size:
                return COLLISION

        # handle special tile types
        if grid_data[next_y][next_x] == ICE_SYMBOL:
            # handle ice tile - slide until first non-ice tile or blocked
            if player_heading == UP:
                for i in range(next_y, -1, -1):
                    if grid_data[i][next_x] != ICE_SYMBOL:
                        if grid_data[i][next_x] == WATER_SYMBOL:
                            # slide into water - game over
                            return GAME_OVER
                        elif cell_is_blocked(grid_data, i, next_x):
                            # if blocked, stop on last ice cell
                            next_y = i + 1
                            break
                        else:
                            next_y = i
                            break
            elif player_heading == DOWN:
                for i in range(next_y, y_size):
                    if grid_data[i][next_x] != ICE_SYMBOL:
                        if grid_data[i][next_x] == WATER_SYMBOL:
                            # slide into water - game over
                            return GAME_OVER
                        elif cell_is_blocked(grid_data, i, next_x):
                            # if blocked, stop on last ice cell
                            next_y = i - 1
                            break
                        else:
                            next_y = i
                            break
            elif player_heading == LEFT:
                for i in range(next_x, -1, -1):
                    if grid_data[next_y][i] != ICE_SYMBOL:
                        if grid_data[next_y][i] == WATER_SYMBOL:
                            # slide into water - game over
                            return GAME_OVER
                        elif cell_is_blocked(grid_data, next_y, i):
                            # if blocked, stop on last ice cell
                            next_x = i + 1
                            break
                        else:
                            next_x = i
                            break
            else:
                for i in range(next_x, x_size):
                    if grid_data[next_y][i] != ICE_SYMBOL:
                        if grid_data[next_y][i] == WATER_SYMBOL:
                            # slide into water - game over
                            return GAME_OVER
                        elif cell_is_blocked(grid_data, next_y, i):
                            # if blocked, stop on last ice cell
                            next_x = i - 1
                            break
                        else:
                            next_x = i
                            break
        if grid_data[next_y][next_x] == TELEPORT_SYMBOL:
            # handle teleport - find the other teleporter
            tpy, tpx = (None, None)
            for i in range(y_size):
                for j in range(x_size):
                    if grid_data[i][j] == TELEPORT_SYMBOL and i != next_y and j != next_x:
                        tpy, tpx = (i, j)
                        break
                if tpy is not None:
                    break
            if tpy is None:
                raise Exception("LaserTank Map Error: Unmatched teleport symbol")
            next_y, next_x = (tpy, tpx)
        else:
            # if not ice or teleport, perform collision check
            if cell_is_blocked(grid_data, next_y, next_x):
                return COLLISION

        # check for game over conditions
        if cell_is_game_over(x_size, y_size, grid_data, next_y, next_x):
            return GAME_OVER

        # no collision and no game over - update player position
        player_y = next_y
        player_x = next_x

    elif move == TURN_LEFT:
        # no collision or game over possible
        if player_heading == UP:
            player_heading = LEFT
        elif player_heading == DOWN:
            player_heading = RIGHT
        elif player_heading == LEFT:
            player_heading = DOWN
        else:
            player_heading = UP

    elif move == TURN_RIGHT:
        # no collision or game over possible
        if player_heading == UP:
            player_heading = RIGHT
        elif player_heading == DOWN:
            player_heading = LEFT
        elif player_heading == LEFT:
            player_heading = UP
        else:
            player_heading = DOWN

    elif move == SHOOT_LASER:
        # set laser direction
        if player_heading == UP:
            heading = UP
            dy, dx = (-1, 0)
        elif player_heading == DOWN:
            heading = DOWN
            dy, dx = (1, 0)
        elif player_heading == LEFT:
            heading = LEFT
            dy, dx = (0, -1)
        else:
            heading = RIGHT
            dy, dx = (0, 1)

        # loop until laser blocking object reached
        ly, lx = (player_y, player_x)
        while True:
            ly += dy
            lx += dx

            # handle boundary and immovable obstacles
            if ly < 0 or ly >= y_size or \
                    lx < 0 or lx >= x_size or \
                    grid_data[ly][lx] == OBSTACLE_SYMBOL:
                # laser stopped without effect
                return COLLISION

            # handle movable objects
            elif cell_is_laser_movable(grid_data, ly, lx, heading):
                # check if tile can be moved without collision
                if cell_is_blocked(grid_data, ly + dy, lx + dx) or \
                        grid_data[ly + dy][lx + dx] == ICE_SYMBOL or \
                        grid_data[ly + dy][lx + dx] == TELEPORT_SYMBOL or \
                        grid_data[ly + dy][lx + dx] == FLAG_SYMBOL or \
                        (ly + dy == player_y and lx + dx == player_x):
                    # tile cannot be moved
                    return COLLISION
                else:
                    old_symbol = grid_data[ly][lx]
                    grid_data[ly][lx] = LAND_SYMBOL
                    if grid_data[ly + dy][lx + dx] == WATER_SYMBOL:
                        # if new bridge position is water, convert to land tile
                        if old_symbol == BRIDGE_SYMBOL:
                            grid_data[ly + dy][lx + dx] = LAND_SYMBOL
                        # otherwise, do not replace the old symbol
                    else:
                        # otherwise, move the tile forward
                        grid_data[ly + dy][lx + dx] = old_symbol
                    break

            # handle bricks
            elif grid_data[ly][lx] == BRICK_SYMBOL:
                # remove brick, replace with land
                grid_data[ly][lx] = LAND_SYMBOL
                break

            # handle facing anti-tanks
            elif (grid_data[ly][lx] == ANTI_TANK_UP_SYMBOL and heading == DOWN) or \
                    (grid_data[ly][lx] == ANTI_TANK_DOWN_SYMBOL and heading == UP) or \
                    (grid_data[ly][lx] == ANTI_TANK_LEFT_SYMBOL and heading == RIGHT) or \
                    (grid_data[ly][lx] == ANTI_TANK_RIGHT_SYMBOL and heading == LEFT):
                # mark anti-tank as destroyed
                grid_data[ly][lx] = ANTI_TANK_DESTROYED_SYMBOL
                break

            # handle player laser collision
            elif ly == player_y and lx == player_x:
                return GAME_OVER

            # handle facing mirrors
            elif (grid_data[ly][lx] == MIRROR_UL_SYMBOL and heading == RIGHT) or \
                    (grid_data[ly][lx] == MIRROR_UR_SYMBOL and heading == LEFT):
                # new direction is up
                dy, dx = (-1, 0)
                heading = UP
            elif (grid_data[ly][lx] == MIRROR_DL_SYMBOL and heading == RIGHT) or \
                    (grid_data[ly][lx] == MIRROR_DR_SYMBOL and heading == LEFT):
                # new direction is down
                dy, dx = (1, 0)
                heading = DOWN
            elif (grid_data[ly][lx] == MIRROR_UL_SYMBOL and heading == DOWN) or \
                    (grid_data[ly][lx] == MIRROR_DL_SYMBOL and heading == UP):
                # new direction is left
                dy, dx = (0, -1)
                heading = LEFT
            elif (grid_data[ly][lx] == MIRROR_UR_SYMBOL and heading == DOWN) or \
                    (grid_data[ly][lx] == MIRROR_DR_SYMBOL and heading == UP):
                # new direction is right
                dy, dx = (0, 1)
                heading = RIGHT
            # do not terminate laser on facing mirror - keep looping

        # check for game over condition after effect of laser
        if cell_is_game_over(x_size, y_size, grid_data, player_y, player_x):
            return GAME_OVER

    return grid_data, player_x, player_y, player_heading


def is_finished(grid_data, player_x, player_y):
    if grid_data[player_y][player_x] == 'f':
        return True
    else:
        return False
