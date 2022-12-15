import random
from pygame.sprite import Sprite
from global_var import ai_settings
import pygame


class Alien(Sprite):
    def __init__(self, screen, stats, types, alien_image):
        super().__init__()
        self.screen = screen
        self.types = types
        self.direct = random.choice([1, -1])
        self.relative_position = 0
        self.image = alien_image[types - 1]
        self.is_frozen = 0
        if self.types == 1:
            self.hp = 1
            self.alien_speed = 200 * (1 + stats.game_difficulty * 0.02) / ai_settings.frames
            self.moving_range = 300
            self.drop_speed = 170 * (1 + stats.game_difficulty * 0.005) / ai_settings.frames
        elif self.types == 2:
            self.hp = 2
            self.alien_speed = 160 * (1 + stats.game_difficulty * 0.02) / ai_settings.frames
            self.moving_range = 220
            self.drop_speed = 170 * (1 + stats.game_difficulty * 0.005) / ai_settings.frames
        elif self.types == 3:
            self.hp = 4
            self.alien_speed = 100 * (1 + stats.game_difficulty * 0.02) / ai_settings.frames
            self.moving_range = 120
            self.drop_speed = 170 * (1 + stats.game_difficulty * 0.005) / ai_settings.frames
        elif self.types == 4:
            self.hp = 80
            self.alien_speed = 0
            self.moving_range = 0
            self.drop_speed = 170 / ai_settings.frames
            pygame.time.set_timer(pygame.USEREVENT + 6, ai_settings.frames * 13 / (1 + stats.game_difficulty * 0.005))

        self.rect = self.image.get_rect()

        # 每个外星人最初都在屏幕左上角
        self.rect.x = self.rect.width / 2  # 每个外星人的左边距都设置为外星人的宽度
        self.rect.y = self.rect.height / 2  # 每个外星人的上边距都设置为外星人的高度

        # 存储外星人准确位置
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

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
