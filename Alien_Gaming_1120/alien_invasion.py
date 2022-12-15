import sys
# sys用于退出游戏
import pygame
from settings import Setting
from ship import Ship
import game_functions as gf
from pygame.sprite import Group  # Group类似列表
from game_stats import GameStats
from pygame import time


def run_game():
    pygame.init()    # 初始化屏幕对象
    ai_settings = Setting()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))    # 创建显示窗口
    pygame.display.set_caption("外星人入侵")
    stats = GameStats(ai_settings)
    ship = Ship(ai_settings, screen)    # 绘制一艘飞船
    bullets = Group()  # 创建一个存储子弹的编组
    aliens = Group()  # 创建一个外星人编组
    explosions = Group()
    alien_width, number_aliens_x, number_rows = gf.get_aliens_x_and_rows(ai_settings, screen, ship)
    gf.create_fleet(ai_settings, screen, aliens, alien_width, number_aliens_x, number_rows)  # 创建外星人群
    clock = pygame.time.Clock()
    explosion_sm = gf.init_explosion()

    ship_broken_time_setter = 0
    ship_broken_time = 0

    # 开始游戏主循环
    while True:
        clock.tick(200)
        gf.check_events(ai_settings, screen, ship, bullets)

        if stats.game_active and ai_settings.ship_broken == 0:
            ship.update()
            gf.update_aliens(ai_settings, stats, screen, ship, aliens, bullets,
                             alien_width, number_aliens_x, number_rows, explosions, explosion_sm)
            gf.update_bullets(aliens, bullets, explosions, explosion_sm)
            explosions.update()
        else:
            if ship_broken_time_setter == 0:
                ship_broken_time_setter = 1
                ship_broken_time = time.get_ticks()  # 获取当前时间
            elif ship_broken_time_setter and time.get_ticks() - ship_broken_time > 280:
                ship_broken_time_setter = 0
                gf.ship_hit(ai_settings, stats, ship, aliens, bullets)
            explosions.update()

        gf.update_screen(ai_settings, screen, ship, aliens, bullets, explosions)


run_game()


