class Button():
    def __init__(self, image, position):
        self.image = image
        self.x = position[0]
        self.y = position[1]
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def update(self, screen):
        screen.blit(self.image, self.rect)

    def is_clicked(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False
