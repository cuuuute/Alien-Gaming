import random
from pygame.sprite import Sprite
from global_var import ai_settings
import pygame


class Alien(Sprite):
    def __init__(self, screen, stats, types, alien_image):
        super().__init__()
        self.screen = screen  # 设置屏幕
        self.types = types  # 设置外星人种类
        self.direct = random.choice([1, -1])  # 设置移动方向为随机
        self.relative_position = 0  # 初始化相对位置
        self.image = alien_image[types - 1]  # 载入外星人图片资源
        self.is_frozen = 0  # 冰冻减速效果标记，是否被寒冰子弹击中
        # 普通外星小怪兽
        if self.types == 1:
            self.hp = 1  # 设置血量
            self.alien_speed = 200 * (1 + stats.game_difficulty * 0.02) / ai_settings.frames  # 设置水平移动速度
            self.moving_range = 300  # 设置移动范围
            self.drop_speed = 170 * (1 + stats.game_difficulty * 0.005) / ai_settings.frames  # 设置向下移动速度
        # 中级外星乌龟人
        elif self.types == 2:
            self.hp = 2  # 设置血量
            self.alien_speed = 160 * (1 + stats.game_difficulty * 0.02) / ai_settings.frames  # 设置水平移动速度
            self.moving_range = 220  # 设置移动范围
            self.drop_speed = 170 * (1 + stats.game_difficulty * 0.005) / ai_settings.frames  # 设置向下移动速度
        # 高级外星飞船人
        elif self.types == 3:
            self.hp = 4  # 设置血量
            self.alien_speed = 100 * (1 + stats.game_difficulty * 0.02) / ai_settings.frames  # 设置水平移动速度
            self.moving_range = 120  # 设置移动范围
            self.drop_speed = 170 * (1 + stats.game_difficulty * 0.005) / ai_settings.frames  # 设置向下移动速度
        # 外星Boss飞碟
        elif self.types == 4:
            self.hp = 80  # 设置血量
            self.alien_speed = 0  # 设置水平移动速度
            self.moving_range = 0  # 设置移动范围
            self.drop_speed = 170 / ai_settings.frames  # 设置向下移动速度
            pygame.time.set_timer(pygame.USEREVENT + 6, ai_settings.frames * 13)  # Boss附加额外效果

        self.rect = self.image.get_rect()  # 获取资源图片大小

        # 每个外星人最初都在屏幕左上角
        self.rect.x = self.rect.width / 2  # 每个外星人的左边距都设置为外星人的宽度
        self.rect.y = self.rect.height / 2  # 每个外星人的上边距都设置为外星人的高度

        # 存储外星人准确位置
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def update(self):
        self.x += self.alien_speed * self.direct  # 计算当前外星人的左边距
        self.relative_position += self.alien_speed * self.direct  # 更新相对位置
        self.rect.x = self.x  # 更新外星人的左边距

    # 检查是否撞到边缘
    def check_edges(self):
        # 如果撞到了，就返回true
        screen_rect = self.screen.get_rect()  # 获取屏幕大小
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:  # 超出屏幕右边缘或左边距小于0
            return True
        else:
            return False
