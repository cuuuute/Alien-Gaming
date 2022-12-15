import sys
import pygame
from bullet import Bullet
from alien import Alien
from gift import Gift
from pygame import time
import random
from explosion import Explosion
from global_var import ai_settings


# 响应按键函数
def check_keydown_events(event, stats, screen, ship, bullets, shoot_sound, bullet_images):
    if not ai_settings.ship_broken and stats.game_active:
        if event.key == pygame.K_RIGHT:
            ship.key_down(pygame.K_RIGHT)
        elif event.key == pygame.K_LEFT:
            ship.key_down(pygame.K_LEFT)
        elif event.key == pygame.K_UP:
            ship.key_down(pygame.K_UP)
        elif event.key == pygame.K_DOWN:
            ship.key_down(pygame.K_DOWN)
        elif event.key == pygame.K_SPACE:
            fire_bullets(screen, ship, bullets, shoot_sound, bullet_images)
    if event.key == pygame.K_q:
        sys.exit()  # 快捷退出


def check_keyup_events(event, ship, stats):
    if not ai_settings.ship_broken and stats.game_active:
        if event.key == pygame.K_RIGHT:
            ship.key_up(pygame.K_RIGHT)
        elif event.key == pygame.K_LEFT:
            ship.key_up(pygame.K_LEFT)
        elif event.key == pygame.K_UP:
            ship.key_up(pygame.K_UP)
        elif event.key == pygame.K_DOWN:
            ship.key_up(pygame.K_DOWN)


def check_events(stats, screen, buttons, ship, aliens, bullets, gifts, explosions, shoot_sound, bullet_images):
    for event in pygame.event.get():
        # 监听键盘和鼠标事件
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:  # 上下左右移动
            check_keydown_events(event, stats, screen, ship, bullets, shoot_sound, bullet_images)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship, stats)
        elif event.type == pygame.USEREVENT:
            ai_settings.bullet_condition = 1
        elif event.type == pygame.USEREVENT + 1 and ai_settings.ship_broken:
            ship_hit(stats, ship, aliens, bullets, gifts, explosions)
        elif event.type == pygame.USEREVENT + 2 and (not stats.game_active):
            msg = event.__dict__['msg']
            if msg == 'move':
                buttons['start'].status = 1
            elif msg == 'click':
                stats.game_active = True
                for button in buttons.values():
                    button.status = -1
        elif event.type == pygame.USEREVENT + 3 and (not stats.game_active):
            msg = event.__dict__['msg']
            if msg == 'click':
                buttons['volume_button_image'].status = (buttons['volume_button_image'].status + 1) % 4
        elif event.type == pygame.USEREVENT + 4:
            stats.reset_stats()
            for button in buttons.values():
                if button.status < 0:
                    if button.text == 'start':
                        button.status = 0
                    elif button.text == 'volume_button_image':
                        button.status = 1
        elif event.type == pygame.MOUSEMOTION and (not stats.game_active):
            for button in buttons.values():
                button.update(event, 'move')
        elif event.type == pygame.MOUSEBUTTONDOWN and (not stats.game_active):
            for button in buttons.values():
                button.update(event, 'click')


def update_screen(stats, screen, all_sounds, title_image, buttons, ship, aliens, bullets,
                  explosions, gifts, background, move_keyboard, space_keyboard, font):
    # screen.fill(ai_settings.bg_color)  # 每次循环时均重新绘制屏幕
    screen.blit(background, (0, 0))
    for bullet in bullets:  # 重新绘制每颗子弹
        bullet.draw_bullet()
    ship.blitme()  # 每次循环时重新绘制飞船
    aliens.draw(screen)
    gifts.draw(screen)
    explosions.draw(screen)
    text = font.render('Score: ' + str(stats.score), True, (255, 58, 0))
    screen.blit(text, (30, 10))
    ship_left_image = pygame.transform.scale(ship.image, (60, 90))
    for button in buttons.values():
        button.render(screen, all_sounds)
    for i in range(0, stats.ship_left):
        screen.blit(ship_left_image, (screen.get_rect().left + 20 + i * 70, screen.get_rect().bottom - 110))
    if not stats.game_active:
        screen.blit(title_image[0], (screen.get_rect().centerx - 400, screen.get_rect().centery - 250))
        screen.blit(title_image[1], (screen.get_rect().centerx + 170, screen.get_rect().centery - 10))
        screen.blit(title_image[2], (screen.get_rect().centerx - 240, screen.get_rect().centery - 310))
        screen.blit(title_image[3], (screen.get_rect().centerx - 40, screen.get_rect().centery - 10))
    elif stats.game_active:
        screen.blit(move_keyboard, (screen.get_rect().centerx + 250, screen.get_rect().centery + 190))
        screen.blit(space_keyboard, (screen.get_rect().centerx + 242, screen.get_rect().centery + 310))
    pygame.display.flip()  # 让绘制屏幕可见


def create_gifts(gifts, gift_image):
    r = random.random()
    x_place = random.uniform(0, ai_settings.screen_width - 80)
    if r <= 0.333:
        gift = Gift(2, x_place, gift_image)
        gifts.add(gift)
    elif r <= 0.666:
        gift = Gift(3, x_place, gift_image)
        gifts.add(gift)
    else:
        gift = Gift(4, x_place, gift_image)
        gifts.add(gift)


def update_gifts(gifts, ship, screen, gift_image, get_buff_sound):
    for gift in gifts:
        if gift.rect.bottom >= screen.get_rect().bottom:
            gifts.remove(gift)
        elif abs(gift.rect.y - ship.rect.y) < max(gift.rect.height, ship.rect.height) \
                and abs(gift.rect.x - ship.rect.x) < max(gift.rect.width, ship.rect.width) \
                and pygame.sprite.collide_mask(ship, gift):
            ai_settings.bullet_condition = gift.gift_type
            gifts.remove(gift)
            pygame.time.set_timer(pygame.USEREVENT, 5000)
            get_buff_sound.play()
    if len(gifts) == 0:
        now = time.get_ticks()
        if now - ai_settings.last_time_buffed >= 7000 or ai_settings.last_time_buffed == 0:
            ai_settings.last_time_buffed = now
            create_gifts(gifts, gift_image)
    gifts.update()


def update_bullets(stats, aliens, bullets, explosions, explosion_sm, bomb_sound):
    bullets.update()
    # 删除子弹
    for bullet in bullets:
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
        collision_alien = pygame.sprite.spritecollide(bullet, aliens, False)
        if len(collision_alien) != 0:
            bullets.remove(bullet)
        for alien in collision_alien:
            alien.hp -= ai_settings.bullet_harm
            if alien.hp <= 0:
                explosion = Explosion(alien.rect.center, explosion_sm)  # 实例化爆炸对象，爆炸中心=敌人中心位置
                explosions.add(explosion)
                stats.score += alien.types * 2
                aliens.remove(alien)
                bomb_sound.play()
            elif bullet.bullet_type == 2:
                alien.alien_speed /= 2
                alien.drop_speed /= 2


def fire_bullets(screen, ship, bullets, shoot_sound, bullet_images):
    # 限制屏幕上最多子弹数量
    if len(bullets) < ai_settings.bullets_allowed:
        # 创建子弹
        if ai_settings.bullet_condition == 4:
            new_bullet1 = Bullet(screen, ship.rect.top, ship.rect.centerx - 30, bullet_images)
            new_bullet2 = Bullet(screen, ship.rect.top, ship.rect.centerx + 30, bullet_images)
            bullets.add(new_bullet1)
            bullets.add(new_bullet2)
        else:
            new_bullet = Bullet(screen, ship.rect.top, ship.rect.centerx, bullet_images)
            bullets.add(new_bullet)
        shoot_sound.play()


def check_alien_num(screen, stats, aliens, bullets, alien_image):
    if len(aliens) == 0:
        # 若外星人均消灭，重新创建外星人，游戏难度上升
        stats.game_difficulty += 1
        create_fleet(screen, stats, aliens, alien_image)


def get_aliens_x_and_rows(screen, stats, ship, alien_image):
    alien = Alien(screen, stats, 1, alien_image)
    alien_width = alien.rect.width
    number_aliens_x = get_number_aliens_x(alien_width)
    number_rows = get_number_rows(ship.rect.height, alien.rect.height)
    return alien_width, number_aliens_x, number_rows


def create_fleet(screen, stats, aliens, alien_image):
    for row_number in range(ai_settings.number_rows):
        alien_number = 0
        while alien_number < ai_settings.number_aliens_x:
            r = random.random()
            if r >= 0.90 - stats.game_difficulty * 0.03 and r >= 0.75:
                types = 3
                create_alien(screen, stats, aliens, alien_number, row_number, types, alien_image)
                alien_number += 3
            elif r >= 0.70 - stats.game_difficulty * 0.06 and r >= 0.65:
                types = 2
                create_alien(screen, stats, aliens, alien_number, row_number, types, alien_image)
                alien_number += 2
            elif r >= 0.5 - stats.game_difficulty * 0.09 and r >= 0.2:
                types = 1
                create_alien(screen, stats, aliens, alien_number, row_number, types, alien_image)
                alien_number += 1
            else:
                alien_number += 1


def get_number_aliens_x(alien_width):
    # 计算一行可以放置外星人的宽度
    available_space_x = ai_settings.screen_width - 2 * alien_width
    # 计算一行可以放置外星人的个数
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def create_alien(screen, stats, aliens, alien_number, row_number, types, alien_image):
    alien = Alien(screen, stats, types, alien_image)
    alien.x = ai_settings.alien_width + 2 * ai_settings.alien_width * alien_number
    alien.rect.x = alien.x
    alien.y = 2 * alien.rect.height * (row_number - ai_settings.number_rows)
    alien.rect.y = alien.y
    aliens.add(alien)


# 计算容纳多少行外星人
def get_number_rows(ship_height, alien_height):
    available_space_y = ai_settings.screen_height - (4 * alien_height) - ship_height
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def update_aliens(stats, screen, ship, aliens, bullets, explosions, explosion_sm, alien_image, bomb_sound):
    for alien in aliens.sprites():
        alien.y += alien.drop_speed
        alien.rect.y = alien.y
    for alien in aliens:
        if alien.check_edges() or abs(alien.relative_position) >= alien.moving_range:
            alien.direct *= -1
        if abs(alien.rect.y - ship.rect.y) < max(alien.rect.height, ship.rect.height) \
                and abs(alien.rect.x - ship.rect.x) < max(alien.rect.width, ship.rect.width) \
                and pygame.sprite.collide_mask(ship, alien) and (not ai_settings.ship_broken):
            explosion = Explosion(ship.rect.center, explosion_sm)  # 实例化爆炸对象，爆炸中心=敌人中心位置
            explosions.add(explosion)
            bomb_sound.play()
            ship.key_list.clear()
            pygame.time.set_timer(pygame.USEREVENT + 1, ai_settings.frames * 3)
            ai_settings.ship_broken = True
    check_aliens_bottom(stats, screen, aliens)
    check_alien_num(screen, stats, aliens, bullets, alien_image)
    aliens.update()
    # 对编组update，相当于对每个外星人update
    # 检查外星人与飞船的碰撞


def ship_hit(stats, ship, aliens, bullets, gifts, explosions):
    aliens.empty()
    bullets.empty()
    gifts.empty()
    explosions.empty()
    # 重建飞船
    ship.center_ship()
    ship.update()
    if stats.ship_left > 0:
        ai_settings.ship_broken = False
        stats.ship_left -= 1
    if stats.ship_left == 0:
        stats.game_active = False
        data = {'msg': 'reset'}
        ev = pygame.event.Event(pygame.USEREVENT + 4, data)
        pygame.event.post(ev)


def check_aliens_bottom(stats, screen, aliens):
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            stats.score -= alien.types
            if stats.score < 0:
                stats.score = 0
            aliens.remove(alien)


def init_explosion():
    # 载入爆炸图片
    explosion_image = []
    for i in range(14):  # 一共载入14张图片
        # 用f-string将文件名格式化，:04指定了宽度为4位数字，左侧以0补齐
        image = pygame.image.load(f'./images/explosion/explosion{i:04}.png').convert_alpha()  # 载入图片，返回Surface对象
        image = pygame.transform.scale(image, (200, 200))
        explosion_image.append(image)  # 将Surface对象添加到列表中备用
    return explosion_image


def init_gift():
    gift_image = []
    image1 = pygame.image.load('./images/ice_buff.png').convert_alpha()
    image2 = pygame.image.load('./images/fire_buff.png').convert_alpha()
    image3 = pygame.image.load('./images/double_shoot_buff.png').convert_alpha()
    image1 = pygame.transform.scale(image1, (80, 80))
    image2 = pygame.transform.scale(image2, (80, 80))
    image3 = pygame.transform.scale(image3, (80, 80))
    gift_image.append(image1)
    gift_image.append(image2)
    gift_image.append(image3)
    return gift_image


def init_alien():
    alien_image = []
    image1 = pygame.image.load('./images/alien1.png').convert_alpha()
    image2 = pygame.image.load('./images/alien2.png').convert_alpha()
    image3 = pygame.image.load('./images/alien3.png').convert_alpha()
    image1 = pygame.transform.scale(image1, (60, 60))
    image2 = pygame.transform.scale(image2, (1.5 * 60, 80))
    image3 = pygame.transform.scale(image3, (3.5 * 60, 120))
    alien_image.append(image1)
    alien_image.append(image2)
    alien_image.append(image3)
    return alien_image
