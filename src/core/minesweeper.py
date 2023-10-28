from collections import deque
from enum import Enum
from random import randint

class TheSlotIsAMineException(Exception):
    ...

class MinesweeperStatus(Enum):
    NOT_INITIALIZED =  0
    IN_PROGRESS = 1
    DEFEAT = 2
    VICTORY = 3

class Minesweeper:
    def __init__(self, rows, columns, mines):
        self.ROWS = rows
        self.COLUMNS = columns
        self.MINES = mines

        self.status = MinesweeperStatus.NOT_INITIALIZED

        self.DIRECTIONS_NUMBER = 8
        self.DIRECTIONS_I = [0, 0, 1, -1, 1, -1, 1, -1]
        self.DIRECTIONS_J = [1, -1, 0, 0, 1, -1, -1, 1]

        self.remaining_safe_slots = (self.ROWS * self.COLUMNS) - self.MINES
        
        self.field = self.__generate_empty_field()

    def get_value(self, i, j):
        return self.field[i][j]

    def build_field(self, selected_i, selected_j):
        self.status = MinesweeperStatus.IN_PROGRESS
        mine_positions = self.__draws_mine_positions(selected_i, selected_j)

        for slot in mine_positions:
            position_i, position_j = slot
            self.field[position_i][position_j] = -1
            self.__update_adjacent_slots(position_i, position_j)

    def select_slot(self, position_i, position_j):
        if (self.field[position_i][position_j] == -1):
            self.status = MinesweeperStatus.DEFEAT
            raise TheSlotIsAMineException()
        
        self.remaining_safe_slots -= 1

        if (self.field[position_i][position_j] > 0):
            return [(position_i, position_j)]

        unlocked_slots = self.__flood_fill(position_i, position_j)
        return unlocked_slots
    
    def get_status(self):
        if (self.remaining_safe_slots == 0):
            self.status = MinesweeperStatus.VICTORY
        return self.status
    
    def __draws_mine_positions(self, selected_i, selected_j):
        mine_positions = set()

        while len(mine_positions) != self.MINES:
            position_i = randint(0, self.ROWS-1)
            position_j = randint(0, self.COLUMNS-1)

            if not self.__is_a_possible_mine_slot(position_i, position_j, selected_i, selected_j):
                continue

            mine_positions.add((position_i, position_j))
        
        return list(mine_positions)
    
    def __is_a_possible_mine_slot(self, i, j, selected_i, selected_j):
        requeriment_i = abs(selected_i - i) > 1 
        requeriment_j = abs(selected_j - j) > 1
        return requeriment_i and requeriment_j
    
    def __is_a_valid_position(self, i, j, visited_map=None):
        range_is_ok = i >= 0 and i < self.ROWS and j >= 0 and j < self.COLUMNS
        if (visited_map is not None):
            return range_is_ok and not visited_map[i][j]

        return range_is_ok and self.field[i][j] != -1

    def __update_adjacent_slots(self, position_i, position_j):
        for index in range(self.DIRECTIONS_NUMBER):
            current_i = position_i + self.DIRECTIONS_I[index]
            current_j = position_j + self.DIRECTIONS_J[index]

            if self.__is_a_valid_position(current_i, current_j):
                self.field[current_i][current_j] += 1

    def __generate_empty_field(self):
        return [[0 for _ in range(self.COLUMNS)] for _ in range(self.ROWS)]

    def __flood_fill(self, position_i, position_j):
        visited_slots = []
        visited_map = [[False for _ in range(self.COLUMNS)] for _ in range(self.ROWS)]
        queue = deque()

        queue.append((position_i, position_j))
        visited_slots.append((position_i, position_j))
        visited_map[position_i][position_j] = True

        while queue:
            position_i, position_j = queue.popleft()

            if (self.field[position_i][position_j] != 0):
                continue

            for index in range(self.DIRECTIONS_NUMBER):
                current_i = position_i + self.DIRECTIONS_I[index]
                current_j = position_j + self.DIRECTIONS_J[index]

                if self.__is_a_valid_position(current_i, current_j, visited_map):
                    self.remaining_safe_slots -= 1
                    visited_slots.append((current_i, current_j))
                    visited_map[current_i][current_j] = True
                    queue.append((current_i, current_j))

        return visited_slots