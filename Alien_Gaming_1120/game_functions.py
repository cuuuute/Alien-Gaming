import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep
import random
from explosion import Explosion


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


def update_screen(ai_settings, screen, ship, aliens, bullets, explosions):
    screen.fill(ai_settings.bg_color)  # 每次循环时均重新绘制屏幕
    for bullet in bullets:  # 重新绘制每颗子弹
        bullet.draw_bullet()
    ship.blitme()  # 每次循环时重新绘制飞船
    aliens.draw(screen)
    explosions.draw(screen)
    pygame.display.flip()  # 让绘制屏幕可见


def update_bullets(aliens, bullets, explosions, explosion_sm):
    bullets.update()
    # 删除子弹
    for bullet in bullets:
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
        collision_alien = pygame.sprite.spritecollide(bullet, aliens, False)
        if len(collision_alien) != 0:
            bullets.remove(bullet)
        for alien in collision_alien:
            alien.hp -= 1
            if alien.hp == 0:
                explosion = Explosion(alien.rect.center, explosion_sm)  # 实例化爆炸对象，爆炸中心=敌人中心位置
                explosions.add(explosion)
                aliens.remove(alien)


def fire_bullets(ai_settings, screen, ship, bullets):
    # 限制屏幕上最多子弹数量
    if len(bullets) < ai_settings.bullets_allowed:
        # 创建子弹
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def check_alien_num(ai_settings, screen, aliens, bullets, alien_width, number_aliens_x, number_rows):
    if len(aliens) == 0:
        # 若外星人均消灭，重新创建外星人
        bullets.empty()
        create_fleet(ai_settings, screen, aliens, alien_width, number_aliens_x, number_rows)


def get_aliens_x_and_rows(ai_settings, screen, ship):
    alien = Alien(ai_settings, screen, 1)
    alien_width = alien.rect.width
    number_aliens_x = get_number_aliens_x(ai_settings, alien_width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)
    return alien_width, number_aliens_x, number_rows


def create_fleet(ai_settings, screen, aliens, alien_width, number_aliens_x, number_rows):
    for row_number in range(number_rows):
        alien_number = 0
        while alien_number < number_aliens_x:
            r = random.random()
            if r >= 0.85:
                types = 3
                create_alien(ai_settings, screen, aliens, alien_number, alien_width, row_number, types, number_rows)
                alien_number += 3
            elif r >= 0.65:
                types = 2
                create_alien(ai_settings, screen, aliens, alien_number, alien_width, row_number, types, number_rows)
                alien_number += 2
            elif r >= 0.3:
                types = 1
                create_alien(ai_settings, screen, aliens, alien_number, alien_width, row_number, types, number_rows)
                alien_number += 1
            else:
                alien_number += 1


def get_number_aliens_x(ai_settings, alien_width):
    # 计算一行可以放置外星人的宽度
    available_space_x = ai_settings.screen_width - 2 * alien_width
    # 计算一行可以放置外星人的个数
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def create_alien(ai_settings, screen, aliens, alien_number, alien_width, row_number, types, number_rows):
    alien = Alien(ai_settings, screen, types)
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.y = 2 * alien.rect.height * (row_number - number_rows)
    alien.rect.y = alien.y
    aliens.add(alien)


# 计算容纳多少行外星人
def get_number_rows(ai_settings, ship_height, alien_height):
    available_space_y = ai_settings.screen_height - (4 * alien_height) - ship_height
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def update_aliens(ai_settings, stats, screen, ship, aliens,
                  bullets, alien_width, number_aliens_x, number_rows, explosions, explosion_sm):
    for alien in aliens.sprites():
        alien.y += ai_settings.fleet_drop_speed
        alien.rect.y = alien.y
    for alien in aliens:
        if alien.check_edges() or abs(alien.relative_position) >= alien.moving_range:
            alien.direct *= -1
        if alien.rect.bottom > screen.get_rect().bottom - 90 \
                and abs(alien.rect.x - ship.rect.x) < max(alien.rect.width, ship.rect.width) \
                and pygame.sprite.collide_mask(ship, alien):
            explosion = Explosion(ship.rect.center, explosion_sm)  # 实例化爆炸对象，爆炸中心=敌人中心位置
            explosions.add(explosion)
            ai_settings.ship_broken = 1
            # ship_hit(ai_settings, stats, ship, aliens, bullets)
    check_aliens_bottom(screen, aliens)
    check_alien_num(ai_settings, screen, aliens, bullets, alien_width, number_aliens_x, number_rows)
    aliens.update()
    # 对编组update，相当于对每个外星人update
    # 检查外星人与飞船的碰撞


def ship_hit(ai_settings, stats, ship, aliens, bullets):
    ai_settings.ship_broken = 0
    if stats.ship_left > 0:
        stats.ship_left -= 1
        aliens.empty()
        bullets.empty()
        # 重建飞船
        ship.center_ship()
    else:
        stats.game_active = False


def check_aliens_bottom(screen, aliens):
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            aliens.remove(alien)


def init_explosion():
    # 载入爆炸图片
    explosion_sm = []
    for i in range(14):  # 一共载入14张图片
        # 用f-string将文件名格式化，:04指定了宽度为4位数字，左侧以0补齐
        image = pygame.image.load(f'./images/explosion/explosion{i:04}.png').convert_alpha()  # 载入图片，返回Surface对象
        image = pygame.transform.scale(image, (200, 200))
        explosion_sm.append(image)            # 将Surface对象添加到列表中备用
    return explosion_sm
