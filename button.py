import pygame.sprite


class Button(pygame.sprite.Sprite):
    def __init__(self, image, position):
        super().__init__()
        self.image = image
        self.x = position[0]
        self.y = position[1]
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def update(self, screen):
        screen.blit(self.image, self.rect)

    def is_clicked(self, mouse_position):
        return self.rect.collidepoint(mouse_position)


