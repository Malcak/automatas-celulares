import os
import time
import numpy as np
import pygame as pg

os.environ['SDL_VIDEO_CENTERED'] = '1'

# initialize pygame
pg.init()

# screen width and height
WIDTH, HEIGHT = 720, 720
# screen creation
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption('Game of life', 'GOF')
game_icon = pg.image.load('./assets/icon.png')
pg.display.set_icon(game_icon)

# background color
BG = 21, 21, 21
# paint the background with the @var BG color
screen.fill(BG)

# number of cells in each coordinate
cells_x, cells_y = 90, 90

# cell size at each coordinate
dim_cell_width = round(WIDTH / cells_x)
dim_cell_height = round(HEIGHT / cells_y)

# matrix with the state of the cells, 0 = dead and 1 = live
game_state = np.zeros((cells_x, cells_y))
new_game_state = np.zeros((cells_x, cells_y))

# execution control
run = True

# execution control
pause_execution = True

# variables to control updates per second
sec_per_update = 0.000000001 / 120   # elapsed time between each update
last_frame_time = time.time()   # time reference to calculate delta
delta = 0   # time difference between each iteration

# execution loop
while run:

    # a little delay to control the speeding of the program
    # time.sleep(0.04)

    # time reference
    current_time = time.time()
    time_elapsed = current_time - last_frame_time
    last_frame_time = current_time

    # the time elapsed between one iteration and another is added to delta
    delta += time_elapsed / sec_per_update

    # save game state to avoid collisions
    new_game_state = np.copy(game_state)

    # clean the screen
    screen.fill(BG)

    # listen keyboard and mouse events
    events = pg.event.get()

    for event in events:
        # detect if any key is pressed
        if event.type == pg.KEYDOWN:
            pause_execution = not pause_execution
        if event.type == pg.QUIT:
            run = False
        # detect if the mouse is pressed
        mouse_click = pg.mouse.get_pressed()
        if sum(mouse_click) > 0:
            # get the cell that was pressed to change its state
            pos_x, pos_y = pg.mouse.get_pos()
            cell_x = int(np.floor(pos_x / dim_cell_width))
            cell_y = int(np.floor(pos_y / dim_cell_height))
            new_game_state[cell_x, cell_y] = not mouse_click[2]

    # when a unit of time is completed the program is updated
    if delta >= 1:
        for y in range(0, cells_x):
            for x in range(0, cells_y):

                if not pause_execution:

                    # calculate the number of neighbors for the current cell
                    neighbors = game_state[(x - 1) % cells_x, (y - 1) % cells_y] + \
                                game_state[x % cells_x, (y - 1) % cells_y] + \
                                game_state[(x + 1) % cells_x, (y - 1) % cells_y] + \
                                game_state[(x - 1) % cells_x, y % cells_y] + \
                                game_state[(x + 1) % cells_x, y % cells_y] + \
                                game_state[(x - 1) % cells_x, (y + 1) % cells_y] + \
                                game_state[x % cells_x, (y + 1) % cells_y] + \
                                game_state[(x + 1) % cells_x, (y + 1) % cells_y]

                    # rule 1: a dead cell with 3 living neighbors revives
                    if game_state[x, y] == 0 and neighbors == 3:
                        new_game_state[x, y] = 1

                    # rule 2: a living cell with less than 2 or more than 3 living neighbors dies
                    elif game_state[x, y] == 1 and (neighbors < 2 or neighbors > 3):
                        new_game_state[x, y] = 0

                # points that define our polygon
                polygon = [
                    (x * dim_cell_width, y * dim_cell_height),
                    ((x + 1) * dim_cell_width, y * dim_cell_height),
                    ((x + 1) * dim_cell_width, (y + 1) * dim_cell_height),
                    (x * dim_cell_width, (y + 1) * dim_cell_height)
                ]

                # draw the cells for each pair of x and y
                if new_game_state[x, y] == 0:
                    pg.draw.polygon(screen, (32, 32, 32), polygon, 1)
                else:
                    pg.draw.polygon(screen, (255, 255, 255), polygon, 0)

        # the delta restarts
        delta -= 1

    # update game state
    game_state = np.copy(new_game_state)

    # refresh the screen
    pg.display.flip()

pg.quit()
