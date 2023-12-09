import pygame


class Sprite(pygame.sprite.Sprite):
    def __init__(self, image_path, scale_by):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale_by(self.image, scale_by)
        self.rect = self.image.get_rect()