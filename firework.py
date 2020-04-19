import curses
import random

def draw_border(screen):
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)

    # TODO: Still don't know why cannot draw border at COLS - 1 / LINES - 1
    for i in range(0, curses.COLS - 1):
        screen.addstr(0, i, '*', curses.color_pair(1) | curses.A_BOLD)
        screen.addstr(curses.LINES - 1, i, '*', curses.color_pair(1) | curses.A_BOLD)

    for i in range(0, curses.LINES - 1):
        screen.addstr(i, 0, '*', curses.color_pair(1) | curses.A_BOLD)
        screen.addstr(i, curses.COLS - 1, '*', curses.color_pair(1) | curses.A_BOLD)

    screen.refresh()

def fire_up(screen, pos_x: int, pos_y: int, height: int):
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    for i in range(0, height):
        screen.addstr(pos_y - i, pos_x, '*', curses.color_pair(2))
        curses.napms(200)
        screen.refresh()

def blow_up(screen, start_x: int, start_y: int):
    # TODO: Implement BLOW EFFECT
    color = curses.color_pair(2)
    R = 15
    for i in range(0, R):
        # Draw bottom and top line
        for x in range(start_x - i, start_x + i + 1):
            if random.randint(0, 3) == 1:
                screen.addstr(start_y - i, x, '*', color)
            if random.randint(0, 3) == 1:
                screen.addstr(start_y + i, x, '*', color)

        # Draw left and right line
        for y in range(start_y - i, start_y + i + 1):
            if random.randint(0, 3) == 1:
                screen.addstr(y, start_x - i, '*', color)
            if random.randint(0, 3) == 1:
                screen.addstr(y, start_x + i, '*', color)

        curses.napms(100)
        screen.refresh()

def main(screen):
    screen.clear()
    curses.curs_set(0)  # Hide cursor

    draw_border(screen)

    # Fire a firework from center bottom of screen
    start_x = curses.COLS // 2
    start_y = curses.LINES - 2
    height = curses.LINES // 2
    fire_up(screen, start_x, start_y, height)

    blow_up(screen, start_x, start_y - height - 1)

    screen.getkey()

curses.wrapper(main)
