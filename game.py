import pygame
from pygame.locals import (
    KEYDOWN,
    MOUSEBUTTONDOWN,
    BUTTON_LEFT,
    K_ESCAPE,
    QUIT,
)

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
grid = pygame.image.load("assets/grid.PNG").convert_alpha()
grid = pygame.transform.scale_by(grid, 5)
x_image = pygame.image.load("assets/x.PNG").convert_alpha()
x_image = pygame.transform.scale_by(x_image, 5)
o_image = pygame.image.load("assets/o.PNG").convert_alpha()
o_image = pygame.transform.scale_by(o_image, 5)
clock = pygame.time.Clock()
turn = 'X'
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


board = create_board(START_X, START_Y)

screen.blit(grid, (0, 0))

running = True

while running:

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
                        if not game_state == "ongoing":
                            print(f"{turn} win!")
                            running = False  # or take other actions based on game state
                        turn = switch_turn()


    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
