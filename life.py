"""
Implement Conway's Game Of Life

By Vuong Hoang <vuonghv.cs@gmail.com>
"""
import curses
import random

# Grid NxM cells, will be init later
N = None
M = None
cells = None    # 2D array store NxM cells

CELL_ON = 1
CELL_OFF = 0

def init_params(screen):
    global N
    global M
    global cells
    
    N = curses.LINES - 3
    M = curses.COLS - 2
    cells = [[CELL_OFF] * M] * N

def draw_border(screen):
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)

    # Draw 4 corners
    screen.addstr(0, 0, '+', curses.color_pair(1))  # Top-Left
    screen.addstr(0, curses.COLS - 1, '+', curses.color_pair(1)) # Top-Right
    screen.addstr(N+1, 0, '+', curses.color_pair(1))  # Bottom-Left
    screen.addstr(N+1, curses.COLS - 1, '+', curses.color_pair(1))  # Bottom-Right

    # Draw top and bottom border
    for i in range(1, curses.COLS - 1):
        screen.addstr(0, i, '-', curses.color_pair(1))
        screen.addstr(N+1, i, '-', curses.color_pair(1))

    # Draw left and right border
    for i in range(1, N+1):
        screen.addstr(i, 0, '|', curses.color_pair(1))
        screen.addstr(i, curses.COLS - 1, '|', curses.color_pair(1))

    msg = 'Press any key to continue, Q to quit'
    screen.addstr(N+2, curses.COLS - 1 - len(msg), msg)
    screen.refresh()

def init_cells():
    global cells
    cells = []
    for i in range(0, N):
        rows = []
        for j in range(0, M):
            if random.randint(0, 1) == 1:
                rows.append(CELL_ON)
            else:
                rows.append(CELL_OFF)
        cells.append(rows)

def evolve():
    global cells
    new_cells = []
    for i in range(0, N):
        rows = []
        for j in range(0, M):
            num_alive_neighbors = 0
            if cells[(i-1)%N][(j-1)%M] == CELL_ON:
                num_alive_neighbors += 1

            if cells[(i-1)%N][j] == CELL_ON:
                num_alive_neighbors += 1

            if cells[(i-1)%N][(j+1)%M] == CELL_ON:
                num_alive_neighbors += 1

            if cells[i][(j-1)%M] == CELL_ON:
                num_alive_neighbors += 1

            if cells[i][(j+1)%M] == CELL_ON:
                num_alive_neighbors += 1

            if cells[(i+1)%N][(j-1)%M] == CELL_ON:
                num_alive_neighbors += 1

            if cells[(i+1)%N][j] == CELL_ON:
                num_alive_neighbors += 1

            if cells[(i+1)%N][(j+1)%M] == CELL_ON:
                num_alive_neighbors += 1

            if cells[i][j] == CELL_ON:
                if num_alive_neighbors < 2 or num_alive_neighbors > 3:
                    rows.append(CELL_OFF)
                else:
                    rows.append(CELL_ON)
            elif num_alive_neighbors == 3:
                rows.append(CELL_ON)
            else:
                rows.append(cells[i][j])
        new_cells.append(rows)
    cells = new_cells

def display_cells(screen):
    for i in range(0, N):
        for j in range(0, M):
            if (cells[i][j] == CELL_ON):
                # Increase i,j to not overlap border
                # TODO: Show Unicode character is funner
                screen.addstr(i+1, j+1, '*')
    screen.refresh()

def main(screen):
    screen.clear()
    curses.curs_set(0)  # Hide cursor

    init_params(screen)
    init_cells()

    while True:
        screen.clear()
        draw_border(screen)
        display_cells(screen)
        key = screen.getkey()
        if key.upper() == 'Q':
            break;
        evolve()

curses.wrapper(main)
