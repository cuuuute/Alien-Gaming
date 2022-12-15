import sys
# sys用于退出游戏
import pygame
from settings import Setting
from ship import Ship
import game_functions as gf
from pygame.sprite import Group  # Group类似列表
from alien import Alien
from game_stats import GameStats


def run_game():
    pygame.init()    # 初始化屏幕对象
    ai_settings = Setting()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))    # 创建显示窗口
    pygame.display.set_caption("外星人入侵")
    stats = GameStats(ai_settings)
    ship = Ship(ai_settings, screen)    # 绘制一艘飞船
    bullets = Group()  # 创建一个存储子弹的编组
    aliens = Group()  # 创建一个外星人编组
    gf.create_fleet(ai_settings, screen, ship, aliens)  # 创建外星人群

    # 开始游戏主循环
    while True:
        gf.check_events(ai_settings, screen, ship, bullets)

        if stats.game_active:
            ship.update()
            gf.update_aliens(ai_settings, stats, screen, ship, aliens, bullets)
            gf.update_bullets(aliens, bullets)

        gf.update_screen(ai_settings, screen, ship, aliens, bullets)


run_game()


