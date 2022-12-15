import pygame
from pygame.sprite import Sprite
# 通过使用精灵类，可将游戏中相关的元素编组，进而可以同时操作编组中的元素


from global_var import ai_settings


class Bullet(Sprite):
    def __init__(self, screen, y, x, bullet_images, is_alien_bullet=0):
        super().__init__()  # 继承Sprite类
        self.screen = screen
        self.bullet_type = None
        if is_alien_bullet:
            self.bullet_type = 5
        else:
            self.bullet_type = ai_settings.bullet_condition   # 1、普通；2、冰；3、火；4、双发；5、boss子弹

        self.color = None
        self.shoot_once = 1
        ai_settings.bullet_harm = 1
        self.rect = None
        self.image = None
        self.x_acceleration = None
        self.y_acceleration = None
        self.x_speed = None
        self.y_speed = None
        self.exist_time = None
        if self.bullet_type == 2:
            self.image = bullet_images[0]
            self.rect = self.image.get_rect()
            self.rect.centerx = x
            self.rect.top = y  # 子弹从飞船顶部射出
        elif self.bullet_type == 3:
            self.image = bullet_images[1]
            self.rect = self.image.get_rect()
            self.rect.centerx = x
            self.rect.top = y  # 子弹从飞船顶部射出
            ai_settings.bullet_harm = 2
        elif self.bullet_type == 5:
            self.image = bullet_images[2]
            self.rect = self.image.get_rect()
            self.rect.centerx = x
            self.rect.bottom = y  # 子弹从boss底部射出
            self.x_acceleration = 0
            self.y_acceleration = 0
            self.x_speed = 0
            self.exist_time = 0
        else:
            # 在（0,0）处创建一个表示子弹的矩形，再设置正确位置
            self.rect = pygame.Rect(0, 0, ai_settings.bullet_width, ai_settings.bullet_height)
            self.rect.centerx = x
            self.rect.top = y  # 子弹从飞船顶部射出
            self.color = 60, 60, 60

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        if self.bullet_type <= 4:
            self.y_speed = ai_settings.bullet_speed
        else:
            self.y_speed = 0

    # 更新子弹位置
    def update(self, screen, ship):
        if self.bullet_type <= 4:
            self.y -= self.y_speed
            self.rect.y = self.y
        elif self.bullet_type == 5:
            self.exist_time += 1
            if self.exist_time < ai_settings.frames * 5:
                if self.rect.centerx - ship.rect.centerx > 0:
                    self.x_acceleration -= 1 / ai_settings.frames
                else:
                    self.x_acceleration += 1 / ai_settings.frames

                if self.x_acceleration < ai_settings.enemy_bullet_speed:
                    self.x_acceleration = ai_settings.enemy_bullet_speed
                elif self.x_acceleration > -ai_settings.enemy_bullet_speed:
                    self.x_acceleration = -ai_settings.enemy_bullet_speed

                self.x_speed += self.x_acceleration
                if self.x_speed < ai_settings.enemy_bullet_speed:
                    self.x_speed = ai_settings.enemy_bullet_speed
                elif self.x_speed > -ai_settings.enemy_bullet_speed:
                    self.x_speed = -ai_settings.enemy_bullet_speed

                if self.rect.centery - ship.rect.centery > 0:
                    self.y_acceleration -= 1.5 / ai_settings.frames
                else:
                    self.y_acceleration += 1.5 / ai_settings.frames

                if self.y_acceleration < ai_settings.enemy_bullet_speed:
                    self.y_acceleration = ai_settings.enemy_bullet_speed
                elif self.y_acceleration > -ai_settings.enemy_bullet_speed:
                    self.y_acceleration = -ai_settings.enemy_bullet_speed

                self.y_speed += self.y_acceleration
                if self.y_speed < ai_settings.enemy_bullet_speed:
                    self.y_speed = ai_settings.enemy_bullet_speed
                elif self.y_speed > -ai_settings.enemy_bullet_speed:
                    self.y_speed = -ai_settings.enemy_bullet_speed

            self.x += self.x_speed
            self.y += self.y_speed
            self.rect.y = self.y
            self.rect.x = self.x

    # 绘制子弹
    def draw_bullet(self):
        if self.bullet_type == 1 or self.bullet_type == 4:
            pygame.draw.rect(self.screen, self.color, self.rect)
        else:
            self.screen.blit(self.image, self.rect)
