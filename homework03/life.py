import pygame
from pygame.locals import *
import random


class GameOfLife:

    def __init__(self, width=640, height=480, cell_size=10, speed=10):
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        # Скорость протекания игры
        self.speed = speed

    def draw_grid(self):
        """ Отрисовать сетку """
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (0, y), (self.width, y))

    def run(self):
        """ Запустить игру """
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))

        # Создание списка клеток
        self.clist = self.cell_list()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
            self.draw_grid()

            # Отрисовка списка клеток
            self.draw_cell_list(self.clist)
            # Выполнение одного шага игры (обновление состояния ячеек)
            clist2 = self.clist.copy()
            self.clist = self.update_cell_list(clist2)

            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

    def cell_list(self, randomize=True):
        """ Создание списка клеток.
        :param randomize: Если True, то создается список клеток, где
        каждая клетка равновероятно может быть живой (1) или мертвой (0).
        :return: Список клеток, представленный в виде матрицы
        """
        if randomize is True:
            self.clist = [[random.randint(0, 1)
                           for i in range(int(self.cell_width))]
                          for j in range(int(self.cell_height))]
        else:
            self.clist = [[0 for i in range(int(self.cell_width))]
                          for j in range(int(self.cell_height))]
        return self.clist

    def draw_cell_list(self, clist):
        """ Отображение списка клеток
        :param rects: Список клеток для отрисовки в виде матрицы
        """
        x, y = 0, 0
        m, n = 0, 0
        c = 0
        a = self.cell_size - 1
        for row in range(len(clist)):
            for col in range(len(clist[row])):
                c += 1
                if clist[row][col] == 1:
                    pygame.draw.rect(self.screen, pygame.Color('green'),
                                     (x + 1, y + 1, a, a))
                    x += a + 1
                    m += 1
                else:
                    pygame.draw.rect(self.screen, pygame.Color('white'),
                                     (x + 1, y + 1, a, a))
                    x += a + 1
                    n += 1
            x = 0
            y += a + 1

    def get_neighbours(self, cell):
        """ Вернуть список соседей для указанной ячейки
        :param cell: Позиция ячейки в сетке, задается кортежем вида (row, col)
        :return: Одномерный список ячеек, смежных к ячейке cell
        """
        neighbours = []
        row, col = cell
        positions = [[-1, -1], [-1, 0], [-1, 1], [0, -1],
                     [0, 1], [1, -1], [1, 0], [1, 1]]
        for i in positions:
            if (0 <= i[0] + row < self.cell_height) and (0 <= i[1] + col < self.cell_width):
                neighbours.append(self.clist[row + i[0]][col + i[1]])
        return neighbours

    def update_cell_list(self, cell_list):
        """ Выполнить один шаг игры.
        Обновление всех ячеек происходит одновременно. Функция возвращает
        новое игровое поле.
        :param cell_list: Игровое поле, представленное в виде матрицы
        :return: Обновленное игровое поле
        """
        new_clist = [['.']*self.cell_width for _ in range(self.cell_height)]
        for row in range(0, self.cell_height):
            for col in range(0, self.cell_width):
                neighbours = self.get_neighbours((row, col))
                if cell_list[row][col] == 1:
                    if neighbours.count(1) == 2 or neighbours.count(1) == 3:
                        new_clist[row][col] = 1
                    else:
                        new_clist[row][col] = 0
                if cell_list[row][col] == 0:
                    if neighbours.count(1) == 3:
                        new_clist[row][col] = 1
                    else:
                        new_clist[row][col] = 0
        self.clist = new_clist
        return self.clist

if __name__ == '__main__':
    game = GameOfLife(400, 300, 10)
    game.run()
