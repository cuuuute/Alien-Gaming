import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    def __init__(self, ai_settings, screen):
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        self.image = pygame.image.load('C:/Users/lenovo/Desktop/外星人入侵/images/alien.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (80, 60))
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
        self.x += self.ai_settings.alien_speed * self.ai_settings.fleet_direction
        self.rect.x = self.x

    # 检查是否撞到边缘
    def check_edges(self):
        # 如果撞到了，就返回true
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True
        else:
            return False
