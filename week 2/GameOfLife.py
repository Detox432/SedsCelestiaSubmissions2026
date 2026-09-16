import pygame
import templates

class Grid:
    def __init__(self, rows, cols):
        self.grid = [[0 for _ in range(cols)] for _ in range(rows)]
        self.rows = rows
        self.cols = cols

    def get(self, row, col):
        # TODO: Implement get logic to return state at (row, col)
        pass

    def set(self, row, col, state):
        # TODO: Implement set logic to set state at (row, col)
        pass

    def clear(self):
        # TODO: Implement clear logic to reset all cells to 0
        pass

    def countNeighbors(self, row, col):
        # TODO: Implement neighbor counting logic
        pass

    def nextGeneration(self):
        newGrid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        changedCells = []

        for row in range(self.rows):
            for col in range(self.cols):
                neighbors = self.countNeighbors(row, col)
                current = self.grid[row][col]
                newState = 0

                # TODO: Implement Conway's Game of Life rules to compute newState

                newGrid[row][col] = newState

                if current != newState:
                    changedCells.append((row, col))

        self.grid = newGrid
        return changedCells

def drawCell(screen, grid, row, col, cellSize):
    x = col * cellSize
    y = row * cellSize

    # TODO: Implement cell fill drawing logic (alive vs dead state colors)

    # Grid line outline
    pygame.draw.rect(
        screen,
        (30, 30, 30),
        (x, y, cellSize, cellSize),
        1
    )

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

CELL_SIZE = 16

rows = 720 // CELL_SIZE
cols = 1280 // CELL_SIZE

grid = Grid(rows, cols)
templates.template7(grid)

for row in range(grid.rows):
    for col in range(grid.cols):
        drawCell(screen, grid, row, col, CELL_SIZE)

pygame.display.flip()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    changedCells = grid.nextGeneration()

    for row, col in changedCells:
        drawCell(screen, grid, row, col, CELL_SIZE)

    pygame.display.flip()
    clock.tick(3)

pygame.quit()
