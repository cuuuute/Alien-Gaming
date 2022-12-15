import pygame


class Ship:
    def __init__(self, ai_settings, screen):
        # 参数screen用于指定飞船绘制到什么地方
        # 参数ai_settings让飞船获取速度位置
        self.screen = screen
        self.ai_settings = ai_settings
        # 加载飞船图像并获取其外接矩形
        self.image = pygame.image.load('C:/Users/lenovo/Desktop/外星人入侵/images/ship.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (90, 110))
        # 图片路径不能用反斜杠！！
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # 将每艘新飞船放在屏幕中央
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        # 由于centerx只能存储整数值，因此另设center存储飞船目前像素位置的小数值
        self.center = float(self.rect.centerx)

        # 移动标志，玩家按下某个方向，将标志设为true，松开时重新设为false
        self.moving_right = False
        self.moving_left = False

    # 方法 update 检查标志状态，标志为true时调整飞船位置
    def update(self):
        # 保证飞船不飞出屏幕
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed
        elif self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed
        # 根据self.center更新rect对象
        self.rect.centerx = self.center

    def blitme(self):
        # 在指定位置绘制飞船
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        self.center = self.screen_rect.centerx
