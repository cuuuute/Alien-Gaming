import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep
import random


# 响应按键函数
def check_keydown_events(event, ai_settings, screen, ship, bullets):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullets(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()  # 快捷退出


def check_keyup_events(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_events(ai_settings, screen, ship, bullets):
    for event in pygame.event.get():
        # 监听键盘和鼠标事件
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:  # 上下左右移动
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)


def update_screen(ai_settings, screen, ship, aliens, bullets):
    screen.fill(ai_settings.bg_color)  # 每次循环时均重新绘制屏幕
    for bullet in bullets:  # 重新绘制每颗子弹
        bullet.draw_bullet()
    ship.blitme()  # 每次循环时重新绘制飞船
    aliens.draw(screen)
    pygame.display.flip()  # 让绘制屏幕可见


def update_bullets(aliens, bullets):
    bullets.update()
    # 删除子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    pygame.sprite.groupcollide(bullets, aliens, True, True)


def fire_bullets(ai_settings, screen, ship, bullets):
    # 限制屏幕上最多子弹数量
    if len(bullets) < ai_settings.bullets_allowed:
        # 创建子弹
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def check_alien_num(ai_settings, screen, ship, aliens, bullets):
    if len(aliens) == 0:
        # 若外星人均消灭，重新创建外星人
        bullets.empty()
        create_fleet(ai_settings, screen, ship, aliens)


def create_fleet(ai_settings, screen, ship, aliens):
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    number_aliens_x = get_number_aliens_x(ai_settings, alien_width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            if random.random() >= 0.5:
                create_alien(ai_settings, screen, aliens, alien_number, alien_width, row_number)


def get_number_aliens_x(ai_settings, alien_width):
    # 计算一行可以放置外星人的宽度
    available_space_x = ai_settings.screen_width - 2 * alien_width
    # 计算一行可以放置外星人的个数
    number_aliens_x = int(available_space_x / (1.5 * alien_width))
    return number_aliens_x


def create_alien(ai_settings, screen, aliens, alien_number, alien_width, row_number):
    alien = Alien(ai_settings, screen)
    alien.x = alien_width + 1.5 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.y = alien.rect.height / 2 + 1.5 * alien.rect.height * row_number
    alien.rect.y = alien.y
    aliens.add(alien)


# 计算容纳多少行外星人
def get_number_rows(ai_settings, ship_height, alien_height):
    available_space_y = ai_settings.screen_height - (4.5 * alien_height) - ship_height
    number_rows = int(available_space_y / (1.5 * alien_height))
    return number_rows


def update_aliens(ai_settings, stats, screen, ship, aliens, bullets):
    for alien in aliens.sprites():
        alien.y += ai_settings.fleet_drop_speed
        alien.rect.y = alien.y
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
    check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets)
    check_alien_num(ai_settings, screen, ship, aliens, bullets)
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    # 对编组update，相当于对每个外星人update
    # 检查外星人与飞船的碰撞


def check_fleet_edges(ai_settings, aliens):
    for alien in aliens.sprites():
        if alien.check_edges():
            ai_settings.fleet_direction *= -1
            break


def ship_hit(ai_settings, stats, screen, ship, aliens, bullets):
    if stats.ship_left > 0:
        stats.ship_left -= 1
        aliens.empty()
        bullets.empty()
        # 重建飞船
        ship.center_ship()
        sleep(0.5)
    else:
        stats.game_active = False


def check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets):
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            aliens.remove(alien)



