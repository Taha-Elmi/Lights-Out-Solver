import pygame
import numpy
from solver import print_solution

### Globals ###

pygame.init()

adj = [[0, 0], [0, -1], [-1, 0], [0, 1], [1, 0]]

TILE_HEIGHT = 50
TILE_WIDTH = 50
MARGIN = 2


class Game:
    def __init__(self, cells):
        self.cells = cells
        self.clear()
        self.load_level()

    def clear(self):
        self.grid = [[0 for i in range(len(self.cells))] for j in range(len(self.cells))]

    def load_level(self):
        for y in range(len(self.cells)):
            for x in range(len(self.cells[y])):
                self.grid[x][y] = int(self.cells[y][x])

    def draw(self):
        for y in range(len(self.cells)):
            for x in range(len(self.cells)):
                i = x * TILE_WIDTH + MARGIN
                j = y * TILE_HEIGHT + MARGIN
                h = TILE_HEIGHT - (2 * MARGIN)
                w = TILE_WIDTH - (2 * MARGIN)
                if self.grid[y][x] == 1:
                    pygame.draw.rect(screen, (105, 210, 231), [i, j, w, h])
                else:
                    pygame.draw.rect(screen, (255, 255, 255), [i, j, w, h])

    def get_adjacent(self, x, y):
        adjs = []
        for i, j in adj:
            if (0 <= i + x < len(self.cells)) and (0 <= j + y < len(self.cells)):
                adjs += [[i + x, j + y]]
        return adjs

    def click(self, pos):
        x = int(pos[0] / TILE_WIDTH)
        y = int(pos[1] / TILE_HEIGHT)
        adjs = self.get_adjacent(x, y)
        for i, j in adjs:
            self.grid[j][i] = (self.grid[j][i] + 1) % 2


### Main ###    

if __name__ == "__main__":

    cells = numpy.array([[1, 0, 0, 0, 1],
                         [0, 1, 0, 1, 0],
                         [0, 0, 1, 0, 0],
                         [0, 1, 0, 1, 0],
                         [1, 0, 0, 0, 1]])

    # cells = numpy.array([[1, 0, 0],
    #                      [0, 1, 0],
    #                      [0, 0, 1]])

    print_solution(cells)

    screen = pygame.display.set_mode((len(cells) * TILE_WIDTH, len(cells) * TILE_HEIGHT))
    screen.fill((167, 219, 216))
    pygame.display.set_caption("Game")

    game = Game(cells.T)
    game.draw()

    clock = pygame.time.Clock()
    keepGoing = True
    while keepGoing:
        clock.tick(30)
        game.draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                game.click(pos)
        pygame.display.flip()
    pygame.quit()
