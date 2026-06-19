import pygame
from queue import PriorityQueue

# Инициализация pygame
pygame.init()

# Размеры окна и сетки
WIDTH = 500
ROWS = 10
CELL = WIDTH // ROWS

WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* алгоритм — Вариант 3")

# Цвета
WHITE  = (255, 255, 255)
BLACK  = (0,   0,   0  )
GREY   = (128, 128, 128)
GREEN  = (0,   200, 0  )   # в очереди (open list)
RED    = (200, 0,   0  )   # посещена (closed list)
PURPLE = (128, 0,   128)   # итоговый путь
ORANGE = (255, 165, 0  )   # старт
CYAN   = (0,   200, 200)   # финиш

# Карта препятствий варианта 3 (считана с изображения)
# True = препятствие (серая клетка), False = свободно
OBSTACLES = set([
    (0, 0),              # серые клетки
    (2, 0),
    (5, 0), (7, 0),
    (9, 0),
    (9, 1),
    (8, 2),
    (0, 3), (1, 3),
    (4, 4), (5, 4), (6, 4), (7, 4),
    (1, 5), (2, 5),
    (0, 6), (1, 6), (7, 6),
    (4, 7), (5, 7),
    (2, 8),             
    (4, 8), (7, 8),
])

# Начальная и конечная точки (col, row)
START = (0, 7)   # синяя корона
END   = (9, 9)   # красный X


class Cell:
    """Класс одной клетки сетки."""

    def __init__(self, col, row):
        self.col = col
        self.row = row
        self.color = WHITE
        self.neighbors = []

        # Проставляем препятствия из карты варианта
        if (col, row) in OBSTACLES:
            self.color = BLACK

    def get_pos(self):
        return self.col, self.row

    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == CYAN

    def make_start(self):
        self.color = ORANGE

    def make_end(self):
        self.color = CYAN

    def make_barrier(self):
        self.color = BLACK

    def make_open(self):
        # Клетка добавлена в открытый список
        self.color = GREEN

    def make_closed(self):
        # Клетка перемещена в закрытый список (уже обработана)
        self.color = RED

    def make_path(self):
        # Клетка является частью найденного пути
        self.color = PURPLE

    def reset(self):
        if not self.is_start() and not self.is_end() and not self.is_barrier():
            self.color = WHITE

    def draw(self, win):
        pygame.draw.rect(win, self.color,
                         (self.col * CELL, self.row * CELL, CELL, CELL))

    def update_neighbors(self, grid):
        """Обновить список проходимых соседей (4 направления)."""
        self.neighbors = []
        # Вниз
        if self.row < ROWS - 1 and not grid[self.col][self.row + 1].is_barrier():
            self.neighbors.append(grid[self.col][self.row + 1])
        # Вверх
        if self.row > 0 and not grid[self.col][self.row - 1].is_barrier():
            self.neighbors.append(grid[self.col][self.row - 1])
        # Вправо
        if self.col < ROWS - 1 and not grid[self.col + 1][self.row].is_barrier():
            self.neighbors.append(grid[self.col + 1][self.row])
        # Влево
        if self.col > 0 and not grid[self.col - 1][self.row].is_barrier():
            self.neighbors.append(grid[self.col - 1][self.row])

    def __lt__(self, other):
        # Нужно для PriorityQueue при одинаковом f
        return False


def heuristic(a, b):
    """Манхэттенское расстояние между клетками a и b."""
    x1, y1 = a
    x2, y2 = b
    return abs(x1 - x2) + abs(y1 - y2)


def reconstruct_path(came_from, current, draw_func):
    """Восстановить и отрисовать путь по словарю came_from."""
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw_func()


def a_star(draw_func, grid, start, end):
    """
    Алгоритм A*.

    draw_func — функция отрисовки сетки.
    grid      — двумерный список клеток.
    start     — стартовая клетка.
    end       — конечная клетка.
    """
    count = 0  # счётчик для разрешения ничьих по f
    open_set = PriorityQueue()
    open_set.put((0, count, start))  # (f, порядок, клетка)

    came_from = {}  # словарь «пришли из»

    # g — стоимость пути от старта до данной клетки
    g_score = {cell: float("inf") for col in grid for cell in col}
    g_score[start] = 0

    # f = g + h
    f_score = {cell: float("inf") for col in grid for cell in col}
    f_score[start] = heuristic(start.get_pos(), end.get_pos())

    open_set_hash = {start}  # множество для быстрой проверки наличия в очереди

    while not open_set.empty():
        # Обработка событий pygame (чтобы окно не зависало)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        # Берём клетку с наименьшим f
        current = open_set.get()[2]
        open_set_hash.discard(current)

        if current == end:
            # Путь найден — восстанавливаем и рисуем
            reconstruct_path(came_from, end, draw_func)
            end.make_end()
            start.make_start()
            return True

        # Перемещаем текущую клетку в закрытый список
        for neighbor in current.neighbors:
            tentative_g = g_score[current] + 1  # стоимость перехода = 1

            if tentative_g < g_score[neighbor]:
                # Нашли более короткий путь до соседа
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score[neighbor] = tentative_g + heuristic(
                    neighbor.get_pos(), end.get_pos()
                )

                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()  # отмечаем как «в очереди»

        draw_func()

        if current != start:
            current.make_closed()  # отмечаем как «посещённую»

    return False  # путь не найден


def make_grid():
    """Создать двумерный список клеток."""
    grid = []
    for col in range(ROWS):
        grid.append([])
        for row in range(ROWS):
            cell = Cell(col, row)
            grid[col].append(cell)
    return grid


def draw(win, grid):
    """Отрисовать сетку и разделительные линии."""
    win.fill(WHITE)

    for col in grid:
        for cell in col:
            cell.draw(win)

    # Рисуем сетку
    for i in range(ROWS):
        pygame.draw.line(win, GREY, (0, i * CELL), (WIDTH, i * CELL))
        pygame.draw.line(win, GREY, (i * CELL, 0), (i * CELL, WIDTH))

    pygame.display.update()


def main():
    grid = make_grid()

    # Устанавливаем старт и финиш
    start_cell = grid[START[0]][START[1]]
    end_cell   = grid[END[0]][END[1]]
    start_cell.make_start()
    end_cell.make_end()

    # Обновляем соседей для всех клеток
    for col in grid:
        for cell in col:
            cell.update_neighbors(grid)

    run = True
    started = False

    while run:
        draw(WIN, grid)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not started:
                    # Запускаем A* по нажатию пробела
                    started = True
                    a_star(lambda: draw(WIN, grid), grid, start_cell, end_cell)

    pygame.quit()


if __name__ == "__main__":
    main()
