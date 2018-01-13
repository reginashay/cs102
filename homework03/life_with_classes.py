import pygame
from pygame.locals import *
import random
from copy import deepcopy


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

        self.cell_list()

    def draw_grid(self):
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (0, y), (self.width, y))

    def run(self):
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
            self.draw_grid()
            self.draw_cell_list()
            self.clist.update()
            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

    def cell_list(self, randomize=True):
        self.clist = CellList(self.cell_width, self.cell_height,
                              randomize)
        self.grid = self.clist.grid

    def draw_cell_list(self):
        for i in range(self.cell_height):
            for j in range(self.cell_width):
                x = j * self.cell_size + 1
                y = i * self.cell_size + 1
                a = self.cell_size - 1
                b = self.cell_size - 1
                if self.grid[j][i].is_alive():
                    pygame.draw.rect(self.screen, pygame.Color('green'),
                                     (x, y, a, b))
                else:
                    pygame.draw.rect(self.screen, pygame.Color('white'),
                                     (x, y, a, b))


class Cell:

    def __init__(self, row, col, state=0):
        self.state = state
        self.row = row
        self.col = col

    def is_alive(self):
        return self.state


class CellList:

    def __init__(self, nrows, ncols, randomize=False):
        self.nrows = nrows
        self.ncols = ncols
        self.randomize = randomize
        if randomize:
            self.grid = [[Cell(i, j, random.randint(0, 1))
                          for j in range(ncols)]
                         for i in range(nrows)]
        else:
            self.grid = [[Cell(i, j, 0)
                          for j in range(ncols)]
                         for i in range(nrows)]

    def get_neighbours(self, cell):
        neighbours = []
        r, c = cell.row, cell.col
        positions = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1],
                     [1, -1], [1, 0], [1, 1]]
        for i in positions:
            if (0 <= i[0] + r < self.nrows) and (0 <= i[1] + c < self.ncols):
                neighbours.append(self.grid[r + i[0]][c + i[1]])
        return neighbours

    def update(self):
        new_grid = deepcopy(self.grid)
        for cell in self:
            neighbours = self.get_neighbours(cell)
            s = sum(c.is_alive() for c in neighbours)
            if cell.is_alive():
                if s < 2 or s > 3:
                    new_grid[cell.row][cell.col].state = 0
            else:
                if s == 3:
                    new_grid[cell.row][cell.col].state = 1
        self.grid = new_grid
        return self

    def __iter__(self):
        self.n = -1
        self.m = 0
        return self

    def __next__(self):
        self.n += 1
        if self.n == self.ncols:
            self.n = 0
            self.m += 1
        if self.m == self.nrows:
            raise StopIteration
        return self.grid[self.m][self.n]

    def __str__(self):
        string = ''
        string += '['
        for i in range(self.nrows):
            if i != 0:
                string += ' '
            string += '['
            for j in range(self.ncols):
                if j < self.ncols - 1:
                    if self.grid[i][j].state:
                        string += '1, '
                    else:
                        string += '0, '
                if j == self.ncols - 1:
                    if i != self.nrows - 1:
                        if self.grid[i][j].state:
                            string += '1],'
                        else:
                            string += '0],'
                    if i == self.nrows - 1:
                        if self.grid[i][j].state:
                            string += '1]'
                        else:
                            string += '0]'
                if i == self.nrows - 1 and j == self.ncols - 1:
                    string += ']'
            if i != self.nrows - 1:
                string += '\n'
        return string

    @classmethod
    def from_file(cls, filename):
        grid = []
        with open(filename) as f:
            for i, line in enumerate(f):
                grid.append([Cell(i, j, int(c))
                             for j, c in enumerate(line) if c in '01'])
        clist = cls(len(grid), len(grid[0]))
        clist.grid = grid
        return clist

if __name__ == '__main__':
    game = GameOfLife(480, 240, 20)
    game.run()
