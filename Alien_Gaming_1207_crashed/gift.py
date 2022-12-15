from pygame.sprite import Sprite
from global_var import ai_settings


class Gift(Sprite):
    def __init__(self, gift_type, x, gift_image):
        super().__init__()
        self.gift_type = gift_type
        self.image = gift_image[gift_type - 1]

        self.rect = self.image.get_rect()
        self.speed = 300 / ai_settings.frames

        self.rect.x = x
        self.rect.y = -80

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def update(self):
        self.y += self.speed
        self.rect.y = self.y
