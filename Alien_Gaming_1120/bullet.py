import pygame
from pygame.sprite import Sprite
# 通过使用精灵类，可将游戏中相关的元素编组，进而可以同时操作编组中的元素


class Bullet(Sprite):
    def __init__(self, ai_settings, screen, ship):
        super().__init__()  # 继承Sprite类
        self.screen = screen
        # 在（0,0）处创建一个表示子弹的矩形，再设置正确位置
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width, ai_settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top  # 子弹从飞船顶部射出
        self.y = float(self.rect.y)
        self.color = ai_settings.bullet_color
        self.speed = ai_settings.bullet_speed

    # 更新子弹位置
    def update(self):
        self.y -= self.speed
        self.rect.y = self.y

    # 绘制子弹
    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
