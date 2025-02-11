import json
from enum import Enum
from pathlib import Path
import copy


class Direction(Enum):
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"


class Game:
    def __init__(self, level: int):
        self.state: str = "playing"
        file_path = Path(__file__).parent / "levels" / f"level{level}.json"
        with open(file_path, "r") as level_file:
            level_data = json.load(level_file)

        self.player_pos = level_data["playerPos"]
        self.board = level_data["board"]

        self.moves = []

    def move(self, direction: Direction):
        x = self.player_pos[0]
        y = self.player_pos[1]
        if direction == Direction.RIGHT:
            y = y + 1
        elif direction == Direction.LEFT:
            y = y - 1
        elif direction == Direction.UP:
            x = x - 1
        elif direction == Direction.DOWN:
            x = x + 1

        if not self.check_for_border(x, y):

            dictionary = {"matrix": copy.deepcopy(self.board), "playerPos": self.player_pos}
            self.moves.append(dictionary)

            if self.board[x][y] == "B":
                if direction == Direction.RIGHT and not self.check_for_border(x, y + 1):
                    self.board[x][y] = "."
                    self.board[x][y + 1] = "B"
                elif direction == Direction.LEFT and not self.check_for_border(x, y - 1):
                    self.board[x][y] = "."
                    self.board[x][y - 1] = "B"
                elif direction == Direction.UP and not self.check_for_border(x - 1, y):
                    self.board[x][y] = "."
                    self.board[x - 1][y] = "B"
                elif direction == Direction.DOWN and not self.check_for_border(x + 1, y):
                    self.board[x][y] = "."
                    self.board[x + 1][y] = "B"

            if self.board[x][y] != "B":

                self.decrement_ephemeral_walls()
                self.update_elements("W")
                self.update_elements("L")

                if self.is_at_goal(x, y):
                    self.state = "won"
                elif self.check_for_losing(x, y):
                    self.state = "lost"

                self.player_pos = [x, y]

    def is_at_goal(self, x, y):
        return self.board[x][y] == "G"

    def check_for_losing(self, x, y):
        return self.board[x][y] == "L" or self.board[x][y] == "#"

    def check_for_border(self, x, y):
        return self.board[x][y] == "#" or self.board[x][y].isnumeric()

    def update_elements(self, el):
        new_board = copy.deepcopy(self.board)

        if el == "W":
            other_element = "L"
        else:
            other_element = "W"

        for row in range(len(self.board)):
            for column in range(len(self.board[row])):
                if self.board[row][column] == el:
                    if self.check_empty_tile(row, column + 1):
                        new_board[row][column + 1] = el
                    elif self.board[row][column + 1] == other_element:
                        new_board[row][column + 1] = "#"

                    if self.check_empty_tile(row, column - 1):
                        new_board[row][column - 1] = el
                    elif self.board[row][column - 1] == other_element:
                        new_board[row][column - 1] = "#"

                    if self.check_empty_tile(row + 1, column):
                        new_board[row + 1][column] = el
                    elif self.board[row + 1][column] == other_element:
                        new_board[row + 1][column] = "#"

                    if self.check_empty_tile(row - 1, column):
                        new_board[row - 1][column] = el
                    elif self.board[row - 1][column] == other_element:
                        new_board[row - 1][column] = "#"

        self.board = new_board

    def check_empty_tile(self, x, y):
        return self.board[x][y] == "."

    def decrement_ephemeral_walls(self):
        for row in range(len(self.board)):
            for column in range(len(self.board[row])):
                if self.board[row][column].isnumeric():
                    self.board[row][column] = str(int(self.board[row][column]) - 1)
                    if int(self.board[row][column]) == 0:
                        self.board[row][column] = "."

    def undo(self):
        if self.state == "playing" and len(self.moves) != 0:
            prev_state = self.moves.pop()
            self.board = prev_state["matrix"]
            self.player_pos = prev_state["playerPos"]

