import random
import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    def __init__(self, ai_settings, screen, types):
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        self.types = types
        self.direct = random.choice([1, -1])
        self.relative_position = 0

        if self.types == 1:
            self.image = pygame.image.load('./images/alien1.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (60, 60))
            self.hp = 1
            self.alien_speed = 1.2
            self.moving_range = 300
        elif self.types == 2:
            self.image = pygame.image.load('./images/alien2.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (1.5 * 60, 80))
            self.hp = 2
            self.alien_speed = 0.9
            self.moving_range = 200
        elif self.types == 3:
            self.image = pygame.image.load('./images/alien3.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (3.5 * 60, 100))
            self.hp = 4
            self.alien_speed = 0.5
            self.moving_range = 100

        self.rect = self.image.get_rect()

        # 每个外星人最初都在屏幕左上角
        self.rect.x = self.rect.width / 2  # 每个外星人的左边距都设置为外星人的宽度
        self.rect.y = self.rect.height / 2  # 每个外星人的上边距都设置为外星人的高度

        # 存储外星人准确位置
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def update(self):
        self.x += self.alien_speed * self.direct
        self.relative_position += self.alien_speed * self.direct
        self.rect.x = self.x

    # 检查是否撞到边缘
    def check_edges(self):
        # 如果撞到了，就返回true
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True
        else:
            return False
