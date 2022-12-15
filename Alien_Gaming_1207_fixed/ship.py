import pygame
from global_var import ai_settings


class Ship:
    def __init__(self, screen):
        # 参数screen用于指定飞船绘制到什么地方
        # 参数ai_settings让飞船获取速度位置
        self.screen = screen
        self.ai_settings = ai_settings
        # 加载飞船图像并获取其外接矩形
        self.image = pygame.image.load('./images/ship.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (60, 90))
        # 图片路径不能用反斜杠！！
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # 将每艘新飞船放在屏幕中央
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        # 由于centerx只能存储整数值，因此另设center存储飞船目前像素位置的小数值
        self.centerx = float(self.rect.centerx)
        self.centery = float(self.rect.centery)
        self.init_x = self.centerx
        self.init_y = self.centery

        # 移动标志，玩家按下某个方向，将其添加至key_list
        self.key_list = []

    # 按键按下时将监听到的键值加入列表
    def key_down(self, key):
        self.key_list.append(key)

    # 按键松开时将监听到的键值从列表中删除
    def key_up(self, key):
        if len(self.key_list) != 0 and (key in self.key_list):
            self.key_list.remove(key)

    # 方法 update 检查标志状态，调整飞船位置
    def update(self):
        # 保证飞船不飞出屏幕
        if len(self.key_list) != 0:
            # 同时按下两个键时进行判断
            if len(self.key_list) == 2:
                if (self.key_list[0] == pygame.K_UP and self.key_list[1] == pygame.K_LEFT) or (self.key_list[0] == pygame.K_LEFT and self.key_list[1] == pygame.K_UP):
                    if self.rect.left > 0:
                        self.centerx -= self.ai_settings.ship_speed
                    if self.rect.top > 0:
                        self.centery -= self.ai_settings.ship_speed
                elif (self.key_list[0] == pygame.K_UP and self.key_list[1] == pygame.K_RIGHT) or (self.key_list[0] == pygame.K_RIGHT and self.key_list[1] == pygame.K_UP):
                    if self.rect.right < self.screen_rect.right - 25:
                        self.centerx += self.ai_settings.ship_speed
                    if self.rect.top > 0:
                        self.centery -= self.ai_settings.ship_speed
                elif (self.key_list[0] == pygame.K_DOWN and self.key_list[1] == pygame.K_RIGHT) or (self.key_list[0] == pygame.K_RIGHT and self.key_list[1] == pygame.K_DOWN):
                    if self.rect.right < self.screen_rect.right - 25:
                        self.centerx += self.ai_settings.ship_speed
                    if self.rect.bottom < self.screen_rect.bottom:
                        self.centery += self.ai_settings.ship_speed
                elif (self.key_list[0] == pygame.K_DOWN and self.key_list[1] == pygame.K_LEFT) or (self.key_list[0] == pygame.K_LEFT and self.key_list[1] == pygame.K_DOWN):
                    if self.rect.left > 0:
                        self.centerx -= self.ai_settings.ship_speed
                    if self.rect.bottom < self.screen_rect.bottom:
                        self.centery += self.ai_settings.ship_speed

            # 按下一个键时进行判断
            else:
                if self.key_list[0] == pygame.K_LEFT and self.rect.left > 0:
                    self.centerx -= self.ai_settings.ship_speed
                elif self.key_list[0] == pygame.K_RIGHT and self.rect.right < self.screen_rect.right - 25:
                    self.centerx += self.ai_settings.ship_speed
                elif self.key_list[0] == pygame.K_UP and self.rect.top > 0:
                    self.centery -= self.ai_settings.ship_speed
                elif self.key_list[0] == pygame.K_DOWN and self.rect.bottom < self.screen_rect.bottom:
                    self.centery += self.ai_settings.ship_speed

        # 根据self.center更新rect对象
        self.rect.centerx = self.centerx
        self.rect.centery = self.centery

    def blitme(self):
        # 在指定位置绘制飞船
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        self.centerx = self.init_x
        self.centery = self.init_y
