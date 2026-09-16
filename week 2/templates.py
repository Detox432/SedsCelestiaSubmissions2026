
# templates.py

# Grid dimensions:
# Screen: 1280 x 720
# Cell size: 16
# Grid: 80 columns x 45 rows

import random

def template1(grid):
    """Block — stable 2x2 pattern"""

    cells = [
        (22, 39),
        (22, 40),
        (23, 39),
        (23, 40)
    ]

    for row, col in cells:
        grid.set(row, col, 1)


def template2(grid):
    """Blinker — period 2 oscillator"""

    cells = [
        (22, 39),
        (22, 40),
        (22, 41)
    ]

    for row, col in cells:
        grid.set(row, col, 1)


def template3(grid):
    """Glider"""

    cells = [
        (21, 40),
        (22, 41),
        (23, 39),
        (23, 40),
        (23, 41)
    ]

    for row, col in cells:
        grid.set(row, col, 1)


def template4(grid):
    """Beacon — period 2 oscillator"""

    cells = [
        (21, 39),
        (21, 40),
        (22, 39),
        (22, 40),

        (23, 41),
        (23, 42),
        (24, 41),
        (24, 42)
    ]

    for row, col in cells:
        grid.set(row, col, 1)


def template5(grid):
    """Toad — period 2 oscillator"""

    cells = [
        (22, 40),
        (22, 41),
        (22, 42),
        (23, 39),
        (23, 40),
        (23, 41)
    ]

    for row, col in cells:
        grid.set(row, col, 1)


def template6(grid):
    """Lightweight spaceship (LWSS)"""

    cells = [
        (21, 39),
        (21, 42),
        (22, 38),
        (23, 38),
        (23, 42),
        (24, 38),
        (24, 39),
        (24, 40),
        (24, 41),
        (24, 42)
    ]

    for row, col in cells:
        grid.set(row, col, 1)


def template7(grid):
    """Pulsar — large oscillator"""

    cells = [
        # Top-left
        (19, 37), (19, 38), (19, 39),
        (20, 35), (20, 41),
        (21, 35), (21, 41),
        (22, 35), (22, 41),

        # Top-right
        (19, 44), (19, 45), (19, 46),
        (20, 44), (21, 44), (22, 44),

        # Bottom-left
        (24, 35), (24, 41),
        (25, 35), (25, 41),
        (26, 35), (26, 41),

        # Bottom-right
        (24, 44), (25, 44), (26, 44),

        # Bottom horizontal
        (26, 37), (26, 38), (26, 39),

        # Middle horizontal structures
        (22, 37), (22, 38), (22, 39),
        (22, 42), (22, 43), (22, 44),

        (24, 37), (24, 38), (24, 39),
        (24, 42), (24, 43), (24, 44)
    ]

    for row, col in cells:
        grid.set(row, col, 1)

def template8(grid):

    cells = [
        (0, 5),

        (1, 4), (1, 7),

        (2, 1), (2, 4), (2, 7),

        (3, 0), (3, 2), (3, 4), (3, 6), (3, 8), (3, 9),

        (4, 1), (4, 4), (4, 7),

        (5, 4), (5, 10),

        (6, 5), (6, 6), (6, 7), (6, 8), (6, 9),

        (8, 7),

        (9, 6), (9, 8),

        (10, 7)
    ]

    startRow = grid.rows // 2 - 5
    startCol = grid.cols // 2 - 5

    for row, col in cells:
        grid.set(startRow + row, startCol + col, 1)

def randomtemplate(grid):
    for row in range(grid.rows//3, grid.rows * 2//3):
        for col in range(grid.cols//3, grid.cols * 2//3):
            state = random.randint(0,1)
            grid.set(row, col, state)
