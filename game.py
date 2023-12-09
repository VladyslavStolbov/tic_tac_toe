import sys

import pygame
from pygame.locals import (
    KEYDOWN,
    MOUSEBUTTONDOWN,
    BUTTON_LEFT,
    K_ESCAPE,
    QUIT,
)

from sprite import Sprite
from button import Button

class TicTacToe:
    def __init__(self):
        # Initialize pygame
        pygame.init()

        # Constants
        self.SCREEN_WIDTH = 320
        self.SCREEN_HEIGHT = 565
        self.FPS = 60
        self.GRID_SIZE = 3
        self.RECT_SIZE = 90
        self.SPACE_BETWEEN = 5
        self.HORIZONTAL_OFFSET = 5
        self.VERTICAL_OFFSET = 37.5
        self.TOTAL_WIDTH = self.GRID_SIZE * self.RECT_SIZE + (self.GRID_SIZE - 1) * self.SPACE_BETWEEN
        self.TOTAL_HEIGHT = self.GRID_SIZE * self.RECT_SIZE + (self.GRID_SIZE - 1) * self.SPACE_BETWEEN

        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.start_menu = pygame.image.load("assets/start_menu.PNG").convert()
        self.start_menu = pygame.transform.scale_by(self.start_menu, 5)
        self.grid = pygame.image.load("assets/grid.PNG").convert()
        self.grid = pygame.transform.scale_by(self.grid, 5)
        self.x_image = Sprite("assets/x.PNG", 5)
        self.o_image = Sprite("assets/o.PNG", 5)
        self.play_button_image = pygame.image.load("assets/play_button.PNG").convert_alpha()
        self.play_button_image = pygame.transform.scale_by(self.play_button_image, 5)
        self.quit_button_image = pygame.image.load("assets/quit_button.PNG").convert_alpha()
        self.quit_button_image = pygame.transform.scale_by(self.quit_button_image, 5)
        self.pvp_button = pygame.image.load("assets/pvp_button.PNG").convert()
        self.pvp_button = pygame.transform.scale_by(self.pvp_button, 5)
        self.vs_ai_button = pygame.image.load("assets/vs_ai.PNG").convert()
        self.vs_ai_button = pygame.transform.scale_by(self.vs_ai_button, 5)
        self.play_window = pygame.image.load("assets/play_window.png").convert()
        self.play_window = pygame.transform.scale_by(self.play_window, 5)
        self.x_turn_image = Sprite("assets/x_turn.PNG", 5)
        self.o_turn_image = Sprite("assets/o_turn.PNG", 5)
        self.clock = pygame.time.Clock()
        self.turn = 'X'

        self.START_X = (self.screen.get_width() - self.TOTAL_WIDTH) // 2 + self.HORIZONTAL_OFFSET
        self.START_Y = (self.screen.get_height() - self.TOTAL_HEIGHT) // 2 + self.VERTICAL_OFFSET

        self.turn_images_group = pygame.sprite.Group()
        self.marks_group = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.turn_images_group, self.marks_group)
        self.board = self.create_board()

    def create_board(self):
        board = {}
        for row in range(self.GRID_SIZE):
            for column in range(self.GRID_SIZE):
                x = self.START_X + column * (self.RECT_SIZE + self.SPACE_BETWEEN)
                y = self.START_Y + row * (self.RECT_SIZE + self.SPACE_BETWEEN)
                board[(x, y)] = ""
        return board

    def switch_turn(self):
        return "O" if self.turn == "X" else "X"

    def display_turn(self):
        if self.turn == "X":
            self.turn_images_group.empty()
            self.turn_images_group.add(self.x_turn_image)
            self.turn_images_group.update()
            self.x_turn_image.rect.center = (160, 120)
        else:
            self.turn_images_group.empty()
            self.turn_images_group.add(self.o_turn_image)
            self.turn_images_group.update()
            self.o_turn_image.rect.center = (160, 120)

        self.turn_images_group.draw(self.screen)

    def check_game_state(self):
        lines = [
                    [(self.START_X + c * 95, self.START_Y + r * 95) for c in range(3)] for r in range(3)
                ] + [
                    [(self.START_X + c * 95, self.START_Y + r * 95) for r in range(3)] for c in range(3)
                ] + [
                    [(self.START_X + i * 95, self.START_Y + i * 95) for i in range(3)],
                    [(self.START_X + i * 95, self.START_Y + (2 - i) * 95) for i in range(3)],
                ]

        for line in lines:
            if all(self.board[pos] == self.turn for pos in line):
                return "win"

        if all(symbol != "" for symbol in self.board.values()):
            return "draw"

        return "ongoing"

    def minimax(self):
        pass

    def find_best_move(self):
        pass

    def main_menu(self):

        quit_button = Button(image=self.quit_button_image, position=(162, 337))
        play_button = Button(image=self.play_button_image, position=(162, 287))

        while True:

            mouse_position = pygame.mouse.get_pos()

            self.screen.blit(self.start_menu, (0, 0))
            quit_button.update(self.screen)
            play_button.update(self.screen)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if play_button.is_clicked(mouse_position):
                        self.game_mode()
                    if quit_button.is_clicked(mouse_position):
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

    def game_mode(self):

        vs_ai_button = Button(image=self.vs_ai_button, position=(162, 337))
        pvp_button = Button(image=self.pvp_button, position=(162, 287))

        while True:
            mouse_position = pygame.mouse.get_pos()

            self.screen.blit(self.play_window, (25, 210))
            pvp_button.update(self.screen)
            vs_ai_button.update(self.screen)
            # Input handler
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONDOWN:
                    if pvp_button.is_clicked(mouse_position):
                        self.play()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                elif event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()

    def play(self):

        while True:
            # Input handler
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                elif event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == MOUSEBUTTONDOWN:
                    if event.button == BUTTON_LEFT:
                        # Placing image and switch turn
                        x, y = pygame.mouse.get_pos()
                        for position, symbol in self.board.items():
                            rect = pygame.Rect(position[0], position[1], self.RECT_SIZE, self.RECT_SIZE)
                            if rect.collidepoint(x, y) and symbol == "":
                                if self.turn == "X":
                                    x_mark = Sprite("assets/x.PNG", 5)
                                    x_mark.rect.topleft = rect.topleft
                                    self.marks_group.add(x_mark)
                                    self.board[position] = "X"
                                else:
                                    o_mark = Sprite("assets/o.PNG", 5)
                                    o_mark.rect.topleft = rect.topleft
                                    self.marks_group.add(o_mark)
                                    self.board[position] = "O"
                                # Check game state
                                game_state = self.check_game_state()
                                if game_state != "ongoing":
                                    print(f"{self.turn} wins!" if game_state == "win" else "It's a draw!")
                                    pygame.quit()
                                    sys.exit()
                                else:
                                    self.turn = self.switch_turn()

            self.marks_group.update()
            self.all_sprites.update()

            self.screen.blit(self.grid, (0, 0))
            self.marks_group.draw(self.screen)
            self.display_turn()

            pygame.display.flip()
            self.clock.tick(self.FPS)


if __name__ == "__main__":
    game = TicTacToe()
    game.main_menu()
