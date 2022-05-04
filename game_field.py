from tabulate import tabulate
from termcolor import colored
import string


class GameField:
    def __init__(self, y: int, x: int, side_choice: chr):
        self._x = x
        self._y = y
        self._field = [["."] * y for _ in range(x)]
        self._is_player_turn = side_choice in {"x", "X"}
        self._place_symbol = "X"
        self._last_placed_cell = (-1, -1)
        self._turns_count = x * y
        self._end_game_message = None
        self._is_game_over = False
        self._count_to_win = min(self._x, self._y, 5)

    def __str__(self):
        head = string.ascii_lowercase[: self._y]
        indexes = [i for i in range(1, self._x + 1)]
        return tabulate(
            self._field, headers=head, showindex=indexes, tablefmt="fancy_grid"
        )

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def has_draw(self):
        return not self._is_game_over

    @property
    def end_game_message(self):
        return self._end_game_message

    @end_game_message.setter
    def end_game_message(self, value):
        self._end_game_message = value

    def has_game_over(self):
        return self._is_game_over or not self._has_turn()

    def game_over(self):
        self._is_game_over = True

    def is_cell_empty(self, x: int, y: int):
        return self._field[x][y] == "."

    def is_player_turn(self) -> bool:
        return self._is_player_turn

    def switch_turn(self):
        self._is_player_turn = not self.is_player_turn()
        self._turns_count -= 1

    def _has_turn(self) -> bool:
        return self._turns_count != 0

    def try_put(self, x: int, y: int) -> bool:
        if self.in_bounds(x, y) and self.is_cell_empty(x, y):
            self._field[x][y] = self._place_symbol
            self._last_placed_cell = (x, y)
            self._change_place_symbol()
            return True
        return False

    def in_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self._x and 0 <= y < self._y

    def has_win(self) -> bool:
        direction_vectors = set()
        for j in range(-1, 2):
            for k in range(-1, 2):
                if j == k == 0:
                    continue
                current_x = self._last_placed_cell[0] + j
                current_y = self._last_placed_cell[1] + k
                if (
                    self.in_bounds(current_x, current_y)
                    and len(direction_vectors) < 4
                    and (-current_x, -current_y) not in direction_vectors
                ):
                    direction_vectors.add((j, k))
                    win_cells = {self._last_placed_cell}
                    self._find_same_cells_in_direction(j, k, win_cells)
                    self._find_same_cells_in_direction(-j, -k, win_cells)
                    if len(win_cells) == self._count_to_win:
                        self._color_win_cells(win_cells)
                        return True
        return False

    def _color_win_cells(self, win_cells: set):
        for coordinates in win_cells:
            x = coordinates[0]
            y = coordinates[1]
            self._field[x][y] = colored(self._field[x][y], "red")

    def _change_place_symbol(self):
        self._place_symbol = "X" if self._place_symbol == "O" else "O"

    def _find_same_cells_in_direction(self, j: int, k: int, win_cells: set):
        needed_cell = "O" if self._place_symbol == "X" else "X"
        current_x = self._last_placed_cell[0] + j
        current_y = self._last_placed_cell[1] + k
        while (
            len(win_cells) != self._count_to_win
            and self.in_bounds(current_x, current_y)
            and self._field[current_x][current_y] == needed_cell
        ):
            win_cells.add((current_x, current_y))
            current_x = current_x + j
            current_y = current_y + k
