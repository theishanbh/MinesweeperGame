import math
import random
import pygame
import sys
import numpy as np

pygame.mixer.init()
pygame.init()

# WhitefishSalad = pygame.mixer.music.load("WhitefishSalad.mp3")
# pygame.mixer.music.load("ChefBrian.mp3")
# pygame.mixer.music.play()

pix_size = 50
rows = 9
col = 9
png_dict = {0: pygame.transform.scale(pygame.image.load('zero.png'), (pix_size, pix_size)),
            1: pygame.transform.scale(pygame.image.load('one.png'), (pix_size, pix_size)),
            2: pygame.transform.scale(pygame.image.load('two.png'), (pix_size, pix_size)),
            3: pygame.transform.scale(pygame.image.load('three.png'), (pix_size, pix_size)),
            4: pygame.transform.scale(pygame.image.load('four.png'), (pix_size, pix_size)),
            5: pygame.transform.scale(pygame.image.load('five.png'), (pix_size, pix_size)),
            6: pygame.transform.scale(pygame.image.load('6.png'), (pix_size, pix_size)),
            9: pygame.transform.scale(pygame.image.load('mine.png'), (pix_size, pix_size))}

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)


def bee_count(r, c):
    bee_counter = 0
    if c - 1 >= 0:
        if _grid[r][c - 1] == 9:
            bee_counter += 1
    if c + 1 < col:
        if _grid[r][c + 1] == 9:
            bee_counter += 1
    if r - 1 >= 0:
        if _grid[r - 1][c] == 9:
            bee_counter += 1
    if r + 1 < rows:
        if _grid[r + 1][c] == 9:
            bee_counter += 1
    if c - 1 >= 0 and r + 1 < rows:
        if _grid[r + 1][c - 1] == 9:
            bee_counter += 1
    if c - 1 >= 0 and r - 1 >= 0:
        if _grid[r - 1][c - 1] == 9:
            bee_counter += 1
    if c + 1 < col and r + 1 < rows:
        if _grid[r + 1][c + 1] == 9:
            bee_counter += 1
    if c + 1 < col and r - 1 >= 0:
        if _grid[r - 1][c + 1] == 9:
            bee_counter += 1
    # _grid[r][c] = bee_counter if _grid[r][c] == 0 else 9
    if _grid[r][c] == 9:
        pass
    else:
        _grid[r][c] = bee_counter


def create_grid(row, cols):
    grid = np.zeros((row, cols))
    return grid


def coordinate_assign(x, y):
    if _grid[x][y] == 9:
        _grid[x][y] = 0
        while True:
            print(",")
            rand_x = random.randrange(rows)
            rand_y = random.randrange(col)
            if _grid[rand_x][rand_y] != 9 and (rand_x != x) and (rand_x + 1 != x) and (rand_x - 1 != x):
                _grid[rand_x][rand_y] = 9
                break
            else:
                continue
    if _grid[x][y] != 0:
        bees_left = _grid[x][y]
        empty_list = [[x, y]]
        if y - 1 >= 0:
            empty_list.append([x, y - 1])
        if y + 1 < col:
            empty_list.append([x, y + 1])
        if x - 1 >= 0:
            empty_list.append([x - 1, y])
        if x + 1 < rows:
            empty_list.append([x + 1, y])
        if y - 1 >= 0 and x + 1 < rows:
            empty_list.append([x + 1, y - 1])
        if y - 1 >= 0 and x - 1 >= 0:
            empty_list.append([x - 1, y - 1])
        if y + 1 < col and x + 1 < rows:
            empty_list.append([x + 1, y + 1])
        if y + 1 < col and x - 1 >= 0:
            empty_list.append([x - 1, y + 1])
        while bees_left > 0:
            while True:
                print(x, y)
                rand_x = random.randrange(rows)
                rand_y = random.randrange(col)
                if _grid[rand_x][rand_y] != 9 and ([rand_x, rand_y] not in empty_list):
                    _grid[rand_x][rand_y] = 9
                    print(rand_x, rand_y)
                    break
                else:
                    continue
            bees_left -= 1
        for i,j in empty_list:
            if _grid[i][j] == 9:
                _grid[i][j] = 0
        print(empty_list)


first_click = True

_grid = create_grid(rows, col)
bees = math.ceil(0.1466666 * rows * col)
bee_list = []
for i in range(bees):

    while True:
        rand_col = random.randint(0, col - 1)
        rand_rows = random.randint(0, rows - 1)
        if [rand_rows, rand_col] not in bee_list:
            bee_list.append([rand_rows, rand_col])
            break
        else:
            continue
for i in range(bees):
    _grid[bee_list[i][0]][bee_list[i][1]] = 9

print(_grid)

for r in range(rows):
    for c in range(col):
        bee_count(r, c)

height = col * pix_size
width = rows * pix_size

size = (height, width)
screen = pygame.display.set_mode(size)


def draw_grid():
    for c in range(col):
        for r in range(rows):
            pygame.draw.rect(screen, WHITE, (c * pix_size, r * pix_size, pix_size, pix_size))
    for _ in range(rows):
        pygame.draw.line(screen, BLACK, (0, _ * pix_size), (col * pix_size, _ * pix_size))
    for _ in range(col):
        pygame.draw.line(screen, BLACK, (_ * pix_size, 0), (_ * pix_size, rows * pix_size))


draw_grid()

print(_grid)
game_over = False
while not game_over:  # main game loop
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            x_cood = event.pos[1]
            y_cood = event.pos[0]
            if event.button == 1:
                if first_click:
                    coordinate_assign(x_cood // pix_size, y_cood // pix_size)
                    for a in range(rows):
                        for b in range(col):
                            bee_count(a, b)
                    print(_grid)
                    first_click = False

                elif _grid[x_cood // pix_size][y_cood // pix_size] == 9:
                    sys.exit()
                screen.blit(png_dict[_grid[x_cood // pix_size][y_cood // pix_size]],
                            ((y_cood // pix_size) * pix_size, (x_cood // pix_size) * pix_size))
            if event.button == 3:
                screen.blit(png_dict[9],
                            ((y_cood // pix_size) * pix_size, (x_cood // pix_size) * pix_size))

            # print(x_cood, y_cood , end=" ###")
            # print(_grid[x_cood//100][y_cood//100])

            # pygame.draw.rect(screen, RED, (y_cood* pix_size, x_cood * pix_size, pix_size, pix_size))
        pygame.display.update()
        # if _grid[x_cood//100][y_cood] == 9:
        #     print("")
    # enter_row = int(input()) - 1
    # enter_col = int(input()) - 1
    # if _grid[enter_row][enter_col] == 1:
    #     break
    # else:
    #     pass
