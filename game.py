import sys
import time
import os
import pygame
from pygame.locals import KEYDOWN, MOUSEBUTTONDOWN, BUTTON_LEFT, K_ESCAPE, QUIT

from sprite import Sprite
from button import Button
from ai import AI

# Change the current working directory to the directory of the script
os.chdir(os.path.dirname(os.path.abspath(__file__)))


class TicTacToe:
    """A simple implementation of the Tic Tac Toe game using Pygame."""
    def __init__(self):
        """Initialize the game."""
        # Initialize pygame
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption("Tic-Tac-Toe")

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

        # Variables
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.start_menu = pygame.image.load("assets/start_menu.PNG").convert()
        self.start_menu = pygame.transform.scale_by(self.start_menu, 5)
        self.grid = pygame.image.load("assets/grid.PNG").convert()
        self.grid = pygame.transform.scale_by(self.grid, 5)
        self.play_window = pygame.image.load("assets/play_window.png").convert()
        self.play_window = pygame.transform.scale_by(self.play_window, 5)
        self.x_turn_sprite = Sprite("assets/x_turn.PNG", (160, 120))
        self.o_turn_sprite = Sprite("assets/o_turn.PNG", (160, 120))
        self.x_won_sprite = Sprite("assets/x_won.png", (160, 310))
        self.o_won_sprite = Sprite("assets/o_won.png", (160, 310))
        self.draw_sprite = Sprite("assets/draw.png", (160, 310))

        self.click_sound = pygame.mixer.Sound("sounds/click.wav")
        self.win_sound = pygame.mixer.Sound("sounds/win.wav")
        self.lose_sound = pygame.mixer.Sound("sounds/lose.wav")
        self.draw_sound = pygame.mixer.Sound("sounds/draw.wav")
        self.background_music = pygame.mixer.Sound("sounds/background.wav")
        self.background_music.set_volume(0.3)
        self.ai = AI()
        self.game_mode = "pvp"
        self.clock = pygame.time.Clock()
        self.turn = 'X'

        self.START_X = (self.screen.get_width() - self.TOTAL_WIDTH) // 2 + self.HORIZONTAL_OFFSET
        self.START_Y = (self.screen.get_height() - self.TOTAL_HEIGHT) // 2 + self.VERTICAL_OFFSET

        # Groups
        self.turn_images_group = pygame.sprite.Group()
        self.marks_group = pygame.sprite.Group()
        self.buttons_group = pygame.sprite.Group()
        self.game_end_states_group = pygame.sprite.Group()
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

    def quit_game(self):
        pygame.quit()
        sys.exit()

    def handle_exit_input(self, event):
        if event.type == KEYDOWN and event.key == K_ESCAPE:
            self.quit_game()
        elif event.type == QUIT:
            self.quit_game()

    def switch_turn(self):
        return "O" if self.turn == "X" else "X"

    def display_turn(self):
        sprite = self.x_turn_sprite if self.turn == "X" else self.o_turn_sprite
        self.turn_images_group.empty()
        self.turn_images_group.add(sprite)
        self.turn_images_group.update()
        self.turn_images_group.draw(self.screen)

    def update_display(self):
        self.marks_group.update()
        self.all_sprites.update()
        self.screen.blit(self.grid, (0, 0))
        self.marks_group.draw(self.screen)
        self.display_turn()
        pygame.display.flip()

    def place_image(self):
        x, y = pygame.mouse.get_pos()
        for position, symbol in self.board.items():
            rect = pygame.Rect(position[0], position[1], self.RECT_SIZE, self.RECT_SIZE)
            if rect.collidepoint(x, y) and symbol == "":
                mark_type = "x" if self.turn == "X" else "o"
                mark = Sprite(f"assets/{mark_type}.PNG")
                mark.rect.topleft = rect.topleft
                self.marks_group.add(mark)
                self.board[position] = self.turn
                self.click_sound.play()
                self.update_display()
                return True
        return False

    def return_game_state(self):
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
                return f"{self.turn} win"

        if all(symbol != "" for symbol in self.board.values()):
            return "draw"

        return "ongoing"

    def show_end_game_window(self, game_state):
        self.game_end_states_group.empty()
        if game_state == "X win":
            self.background_music.stop()
            self.win_sound.play()
            self.game_end_states_group.add(self.x_won_sprite)
        elif game_state == "O win":
            self.background_music.stop()
            self.lose_sound.play()
            self.game_end_states_group.add(self.o_won_sprite)
        elif game_state == "draw":
            self.background_music.stop()
            self.draw_sound.play()
            self.game_end_states_group.add(self.draw_sprite)

    def end_game_state(self):
        game_state = self.return_game_state()
        if game_state != 'ongoing':
            self.game_end_menu(game_state)
            return True  # Indicate that the game has ended
        return False  # Indicate that the game is still ongoing

    def reset_game(self):
        self.turn = "X"
        self.turn_images_group.empty()
        self.marks_group.empty()
        self.board = self.create_board()

    def main_menu(self):

        self.background_music.play(loops=-1)

        play_button = Button("assets/play_button.PNG", position=(162, 287))
        quit_button = Button("assets/quit_button.PNG", position=(162, 337))

        while True:

            mouse_position = pygame.mouse.get_pos()

            self.screen.blit(self.start_menu, (0, 0))
            quit_button.update(self.screen)
            play_button.update(self.screen)
            for event in pygame.event.get():
                self.handle_exit_input(event)
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == BUTTON_LEFT:
                    if play_button.is_clicked(mouse_position):
                        self.click_sound.play()
                        self.game_mode_menu()
                    if quit_button.is_clicked(mouse_position):
                        self.click_sound.play()
                        time.sleep(0.3)
                        pygame.quit()
                        sys.exit()

            pygame.display.update()

    def game_mode_menu(self):

        pvp_button = Button("assets/pvp_button.PNG", position=(162, 287))
        vs_ai_button = Button("assets/vs_ai_button.PNG", position=(162, 337))

        while True:
            mouse_position = pygame.mouse.get_pos()

            self.screen.blit(self.play_window, (25, 210))
            pvp_button.update(self.screen)
            vs_ai_button.update(self.screen)
            # Input handler
            for event in pygame.event.get():
                self.handle_exit_input(event)
                if event.type == MOUSEBUTTONDOWN and event.button == BUTTON_LEFT:
                    if pvp_button.is_clicked(mouse_position):
                        self.click_sound.play()
                        self.game_mode = "pvp"
                        self.start_game()
                    if vs_ai_button.is_clicked(mouse_position, ):
                        self.click_sound.play()
                        self.game_mode = "ai"
                        self.start_game()

            pygame.display.update()

    def game_end_menu(self, game_state):
        again_button = Button("assets/again_button.png", position=(162, 287))
        quit_button = Button("assets/quit_button.PNG", position=(162, 337))
        self.buttons_group.add(again_button, quit_button)
        self.show_end_game_window(game_state)
        running = True
        while running:
            mouse_position = pygame.mouse.get_pos()

            again_button.update(self.screen)
            quit_button.update(self.screen)

            for event in pygame.event.get():
                self.handle_exit_input(event)
                if event.type == MOUSEBUTTONDOWN and event.button == BUTTON_LEFT:
                    if again_button.is_clicked(mouse_position):
                        self.click_sound.play()
                        self.reset_game()
                        self.main_menu()
                        running = False
                    elif quit_button.is_clicked(mouse_position):
                        self.click_sound.play()
                        time.sleep(0.3)
                        pygame.quit()
                        sys.exit()

            self.game_end_states_group.update()
            self.buttons_group.update(self.screen)
            self.game_end_states_group.draw(self.screen)
            self.buttons_group.draw(self.screen)

            pygame.display.update()

    def start_game(self):
        running = True
        while running:
            for event in pygame.event.get():
                self.handle_exit_input(event)
                if event.type == MOUSEBUTTONDOWN and event.button == BUTTON_LEFT:
                    if self.place_image():
                        game_state = self.return_game_state()
                        if game_state != 'ongoing':
                            running = False
                            self.game_end_menu(game_state)
                        else:
                            self.turn = self.switch_turn()

                            if self.game_mode == 'ai' and self.turn == 'O':
                                ai_position = self.ai.move(self.board)
                                self.board[ai_position] = self.turn
                                ai_mark = Sprite("assets/o.PNG")
                                ai_mark.rect.topleft = ai_position
                                self.marks_group.add(ai_mark)
                                self.update_display()
                                game_state = self.return_game_state()
                                if game_state != 'ongoing':
                                    running = False
                                    self.game_end_menu(game_state)
                                self.turn = self.switch_turn()

            self.update_display()
            self.clock.tick(self.FPS)
