import sys

import pygame
from pygame.locals import (
    KEYDOWN,
    MOUSEBUTTONDOWN,
    BUTTON_LEFT,
    K_ESCAPE,
    QUIT,
)

from button import Button

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 320
SCREEN_HEIGHT = 565
FPS = 60
GRID_SIZE = 3
RECT_SIZE = 90
SPACE_BETWEEN = 5
HORIZONTAL_OFFSET = 5
VERTICAL_OFFSET = 37.5


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
start_menu = pygame.image.load("assets/start_menu.PNG").convert()
start_menu = pygame.transform.scale_by(start_menu, 5)
grid = pygame.image.load("assets/grid.PNG").convert()
grid = pygame.transform.scale_by(grid, 5)
x_image = pygame.image.load("assets/x.PNG").convert_alpha()
x_image = pygame.transform.scale_by(x_image, 5)
o_image = pygame.image.load("assets/o.PNG").convert_alpha()
o_image = pygame.transform.scale_by(o_image, 5)
play_button_image = pygame.image.load("assets/play_button.PNG").convert_alpha()
play_button_image = pygame.transform.scale_by(play_button_image, 5)
quit_button_image = pygame.image.load("assets/quit_button.PNG").convert_alpha()
quit_button_image = pygame.transform.scale_by(quit_button_image, 5)
clock = pygame.time.Clock()
turn = 'X'

# Constants related to the game board
TOTAL_WIDTH = GRID_SIZE * RECT_SIZE + (GRID_SIZE - 1) * SPACE_BETWEEN
TOTAL_HEIGHT = GRID_SIZE * RECT_SIZE + (GRID_SIZE - 1) * SPACE_BETWEEN
START_X = (screen.get_width() - TOTAL_WIDTH) // 2 + HORIZONTAL_OFFSET
START_Y = (screen.get_height() - TOTAL_HEIGHT) // 2 + VERTICAL_OFFSET


def create_board(start_x, start_y):
    board = {}
    for row in range(GRID_SIZE):
        for column in range(GRID_SIZE):
            x = start_x + column * (RECT_SIZE + SPACE_BETWEEN)
            y = start_y + row * (RECT_SIZE + SPACE_BETWEEN)
            board[(x, y)] = ""
    return board


def switch_turn():
    return "O" if turn == "X" else "X"


def check_game_state(board, start_x, start_y, turn):
    lines = [
        [(start_x + c * 95, start_y + r * 95) for c in range(3)] for r in range(3)
    ] + [
        [(start_x + c * 95, start_y + r * 95) for r in range(3)] for c in range(3)
    ] + [
        [(start_x + i * 95, start_y + i * 95) for i in range(3)],
        [(start_x + i * 95, start_y + (2 - i) * 95) for i in range(3)],
    ]

    for line in lines:
        if all(board[pos] == turn for pos in line):
            return "win"

    if all(symbol != "" for symbol in board.values()):
        return "draw"

    return "ongoing"


def minimax(board, depth, maximizing_player):
    pass


def find_best_move(board):
    pass


def main_menu():

    quit_button = Button(image=quit_button_image, position=(162, 337))
    play_button = Button(image=play_button_image, position=(162, 287))

    while True:

        mouse_x, mouse_y = pygame.mouse.get_pos()

        screen.blit(start_menu, (0, 0))
        quit_button.update(screen)
        play_button.update(screen)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.is_clicked((mouse_x, mouse_y)):
                    play()
                if quit_button.is_clicked((mouse_x, mouse_y)):
                    pygame.quit()
                    sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            elif event.type == QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()


board = create_board(START_X, START_Y)

screen.blit(grid, (0, 0))


def play():
    while True:

        # Input handler
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            elif event.type == QUIT:
                running = False

            elif event.type == MOUSEBUTTONDOWN:
                if event.button == BUTTON_LEFT:
                    # Placing image and switch turn
                    x, y = pygame.mouse.get_pos()
                    for position, symbol in board.items():
                        rect = pygame.Rect(position[0], position[1], RECT_SIZE, RECT_SIZE)
                        if rect.collidepoint(x, y) and symbol == "":
                            if turn == "X":
                                screen.blit(x_image, rect)
                                board[position] = "X"
                            else:
                                screen.blit(o_image, rect)
                                board[position] = "O"
                            # Check game state
                            game_state = check_game_state(board, START_X, START_Y, turn)
                            if game_state != "ongoing":
                                print(f"{turn} wins!" if game_state == "win" else "It's a draw!")
                                running = False  # or take other actions based on game state
                            else:
                                turn = switch_turn()

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

main_menu()
