import pygame


class Sprite(pygame.sprite.Sprite):
    def __init__(self, image_path, position=(0,0)):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale_by(self.image, 5)
        self.rect = self.image.get_rect(center=position)
