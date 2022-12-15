import pygame
from pygame.sprite import Sprite
# 通过使用精灵类，可将游戏中相关的元素编组，进而可以同时操作编组中的元素


from global_var import ai_settings


class Bullet(Sprite):
    def __init__(self, screen, ship_top, x, bullet_images):
        super().__init__()  # 继承Sprite类
        self.screen = screen
        self.bullet_type = ai_settings.bullet_condition   # 1、普通；2、冰；3、火；4、双发

        self.color = None
        self.shoot_once = 1
        ai_settings.bullet_harm = 1
        self.rect = None
        self.image = None
        if self.bullet_type == 2:
            self.image = bullet_images[0]
            self.rect = self.image.get_rect()
            self.rect.centerx = x
            self.rect.top = ship_top  # 子弹从飞船顶部射出
        elif self.bullet_type == 3:
            self.image = bullet_images[1]
            self.rect = self.image.get_rect()
            self.rect.centerx = x
            self.rect.top = ship_top  # 子弹从飞船顶部射出
            ai_settings.bullet_harm = 2
        else:
            # 在（0,0）处创建一个表示子弹的矩形，再设置正确位置
            self.rect = pygame.Rect(0, 0, ai_settings.bullet_width, ai_settings.bullet_height)
            self.rect.centerx = x
            self.rect.top = ship_top  # 子弹从飞船顶部射出
            self.color = 60, 60, 60

        self.y = float(self.rect.y)
        self.speed = ai_settings.bullet_speed

    # 更新子弹位置
    def update(self):
        self.y -= self.speed
        self.rect.y = self.y

    # 绘制子弹
    def draw_bullet(self):
        if self.bullet_type == 1 or self.bullet_type == 4:
            pygame.draw.rect(self.screen, self.color, self.rect)
        else:
            self.screen.blit(self.image, self.rect)
