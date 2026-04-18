from mine import *
import input_system
from tictactoe import init_position  # Импортируем данные из tictactoe.py
from time import sleep


class Cell:
    size = 6

    def __init__(self, x, y, origin=None):
        self.x = x
        self.y = y
        self.origin = origin
        self.state = "empty"  # empty, circle, cross

    def draw(self):
        if self.state == "empty":
            data = init_position["close"]
        elif self.state == "circle":
            data = init_position["circle"]  # Круг
        else:
            data = init_position["cross"]  # Крест

        data = data[::-1]

        # Рамка
        for i in range(Cell.size + 2):
            for j in range(Cell.size + 2):
                if i == 0 or j == 0 or i == Cell.size + 1 or j == Cell.size + 1:
                    mc.setBlock(
                        self.origin.x + self.x * (Cell.size + 2) + i,
                        self.origin.y,
                        self.origin.z + self.y * (Cell.size + 2) + j,
                        block.DIAMOND_BLOCK.id
                    )

        # Содержимое
        for i in range(Cell.size):
            for j in range(Cell.size):
                mc.setBlock(
                    self.origin.x + self.x * (Cell.size + 2) + 1 + i,
                    self.origin.y,
                    self.origin.z + self.y * (Cell.size + 2) + 1 + j,
                    block.WOOL.id,
                    data[i][j]
                )


class TicTacToe:
    def __init__(self):
        self.size = 3
        self.origin = pos()

        self.field = [
            [Cell(x, y, self.origin) for y in range(self.size)]
            for x in range(self.size)
        ]

        self.current = "circle"  # Начинаем с круга
        self.game_over = False

        self.draw()

    def draw(self):
        for row in self.field:
            for cell in row:
                cell.draw()

    def make_move(self, x, y):
        if self.game_over:
            return

        cell = self.field[x][y]

        if cell.state != "empty":
            mc.postToChat("Cell already taken!")
            return

        cell.state = self.current
        cell.draw()

        if self.check_win(self.current):
            mc.postToChat(self.current + " wins!")
            self.draw_winning_line(self.current)  # Рисуем линию победы
            self.game_over = True
            return

        if self.is_draw():
            mc.postToChat("Draw!")
            self.game_over = True
            return

        self.current = "cross" if self.current == "circle" else "circle"  # Смена игрока
        mc.postToChat(f"{self.current}'s turn")

    def check_win(self, player):
        for y in range(3):
            if all(self.field[x][y].state == player for x in range(3)):
                return True  # Возвращаем True, если игрок выиграл

        for x in range(3):
            if all(self.field[x][y].state == player for y in range(3)):
                return True  # Возвращаем True, если игрок выиграл

        if all(self.field[i][i].state == player for i in range(3)):
            return True  # Возвращаем True, если игрок выиграл

        if all(self.field[i][2 - i].state == player for i in range(3)):
            return True  # Возвращаем True, если игрок выиграл

        return False  # Возвращаем False, если игрок не выиграл

    def draw_winning_line(self, player):
        winning_cells = []
        for y in range(3):
            if all(self.field[x][y].state == player for x in range(3)):
                winning_cells = [(x, y) for x in range(3)]  # Вертикаль
                break

        if not winning_cells:
            for x in range(3):
                if all(self.field[x][y].state == player for y in range(3)):
                    winning_cells = [(x, y) for y in range(3)]  # Горизонталь
                    break

        if not winning_cells:
            if all(self.field[i][i].state == player for i in range(3)):
                winning_cells = [(i, i) for i in range(3)]  # Диагональ
            elif all(self.field[i][2 - i].state == player for i in range(3)):
                winning_cells = [(i, 2 - i) for i in range(3)]  # Обратная диагональ

        # Рисуем линию через выигрышные ячейки
        if winning_cells:
            for (x, y) in winning_cells:
                for i in range(Cell.size + 2):
                    mc.setBlock(
                        self.origin.x + x * (Cell.size + 2) + 1 + i,
                        self.origin.y + 1,  # Поднимаем линию на один блок выше
                        self.origin.z + y * (Cell.size + 2) + 1,
                        block.RED_WOOL.id  # Используем красный блок для линии
                    )

    def is_draw(self):
        return all(
            cell.state != "empty"
            for row in self.field
            for cell in row
        )
 

def get_cell_by_click(game):
    p = pos()

    x = (p.x - game.origin.x) // (Cell.size + 2)
    y = (p.z - game.origin.z) // (Cell.size + 2)

    if 0 <= x < 3 and 0 <= y < 3:
        return x, y

    return None, None


if __name__ == "__main__":
    game = TicTacToe()

    mc.postToChat("TicTacToe: circle starts")  # Начинаем с круга

    while not game.game_over:
        if input_system.wasPressedSinceLast(input_system.LBUTTON):
            x, y = get_cell_by_click(game)

            if x is not None:
                game.make_move(x, y)

        sleep(0.1)

