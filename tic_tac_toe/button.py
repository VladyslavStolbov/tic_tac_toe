import pygame


class Button(pygame.sprite.Sprite):
    def __init__(self, image_path, position):
        super().__init__()
        self.image = pygame.image.load(image_path).convert()
        self.image = pygame.transform.scale_by(self.image, 5)
        self.x = position[0]
        self.y = position[1]
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def update(self, screen):
        screen.blit(self.image, self.rect)

    def is_clicked(self, mouse_position):
        return self.rect.collidepoint(mouse_position)


