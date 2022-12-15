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
        if event.key == pygame.K_RIGHT:  # 右方向键被按下
            ship.key_down(pygame.K_RIGHT)
        elif event.key == pygame.K_LEFT:  # 左方向键被按下
            ship.key_down(pygame.K_LEFT)
        elif event.key == pygame.K_UP:  # 上方向键被按下
            ship.key_down(pygame.K_UP)
        elif event.key == pygame.K_DOWN:  # 下方向键被按下
            ship.key_down(pygame.K_DOWN)
        elif event.key == pygame.K_SPACE:  # 空格键被按下
            fire_bullets(screen, ship, bullets, shoot_sound, bullet_images)  # 执行一次射击开火函数
    if event.key == pygame.K_q:  # 退出
        sys.exit()  # 快捷退出


def check_keyup_events(event, ship, stats):
    # 飞船未被破坏且游戏状态激活的前提下：
    if not ai_settings.ship_broken and stats.game_active:
        if event.key == pygame.K_RIGHT:  # 右方向键被松开
            ship.key_up(pygame.K_RIGHT)
        elif event.key == pygame.K_LEFT:  # 左方向键被松开
            ship.key_up(pygame.K_LEFT)
        elif event.key == pygame.K_UP:  # 上方向键被松开
            ship.key_up(pygame.K_UP)
        elif event.key == pygame.K_DOWN:  # 下方向键被松开
            ship.key_up(pygame.K_DOWN)


def check_events(stats, screen, buttons, ship, aliens, bullets, gifts, explosions, shoot_sound, bullet_images):
    for event in pygame.event.get():
        # 监听键盘和鼠标事件
        if event.type == pygame.QUIT:  # 退出quit
            sys.exit()  # 游戏退出
        elif event.type == pygame.KEYDOWN:  # 按键按下，上下左右移动
            check_keydown_events(event, stats, screen, ship, bullets, shoot_sound, bullet_images)  # 响应按键函数
        elif event.type == pygame.KEYUP:  # 按键松开，停止上下左右移动
            check_keyup_events(event, ship, stats)  # 响应按键函数
        elif event.type == pygame.USEREVENT:
            ai_settings.bullet_condition = 1  # 普通子弹类型
        elif event.type == pygame.USEREVENT + 1 and ai_settings.ship_broken:
            ship_hit(stats, ship, aliens, bullets, gifts, explosions)  # 执行一次飞船被击中的函数
        elif event.type == pygame.USEREVENT + 2 and (not stats.game_active):
            msg = event.__dict__['msg']
            if msg == 'move':  # 鼠标移动到按钮上，按钮会变色
                buttons['start'].status = 1
            elif msg == 'click':  # 鼠标点击按钮，游戏开始
                stats.game_active = True
                for button in buttons.values():
                    if button.text != 'exit':
                        button.status = -1
        elif event.type == pygame.USEREVENT + 5:  # 退出按钮的事件侦听
            msg = event.__dict__['msg']
            if msg == 'move':  # 鼠标移动到按钮上，按钮会变色
                buttons['exit'].status = 1
            elif msg == 'click':  # 鼠标点击按钮，游戏退出
                sys.exit()
        elif event.type == pygame.USEREVENT + 3 and (not stats.game_active):  # 音量调节按钮的事件侦听
            msg = event.__dict__['msg']
            if msg == 'click':  # 鼠标点击按钮，音量调节
                buttons['volume_button_image'].status = (buttons['volume_button_image'].status + 1) % 4
        elif event.type == pygame.USEREVENT + 4:  # 游戏重新开始
            stats.reset_stats()
            for button in buttons.values():
                if button.status < 0:
                    if button.text == 'start':
                        button.status = 0
                    elif button.text == 'volume_button_image':
                        button.status = 1
        elif event.type == pygame.USEREVENT + 6:  # Boss附加额外效果
            for alien in aliens:
                if alien.types == 4:
                    new_bullet = Bullet(screen, alien.rect.bottom, alien.rect.centerx, bullet_images, is_alien_bullet=1)
                    bullets.add(new_bullet)
        elif event.type == pygame.MOUSEMOTION and (not stats.game_active):  # 指针移动到按钮上，更新按钮形态
            for button in buttons.values():
                button.update(event, 'move')
        elif event.type == pygame.MOUSEMOTION and stats.game_active:  # 指针移动到按钮上，更新按钮形态
            buttons['exit'].update(event, 'move')
        elif event.type == pygame.MOUSEBUTTONDOWN and (not stats.game_active):  # 指针点击按钮，更新按钮状态
            for button in buttons.values():
                button.update(event, 'click')
        elif event.type == pygame.MOUSEBUTTONDOWN and stats.game_active:  # 指针点击按钮，更新按钮状态
            buttons['exit'].update(event, 'click')


def update_screen(stats, screen, all_sounds, title_image, buttons, ship, aliens, bullets,
                  explosions, gifts, background, move_keyboard, space_keyboard, font):
    # screen.fill(ai_settings.bg_color)  # 每次循环时均重新绘制屏幕
    screen.blit(background, (0, 0))
    for bullet in bullets:  # 重新绘制每颗子弹
        bullet.draw_bullet()
    ship.blitme()  # 每次循环时重新绘制飞船
    aliens.draw(screen)  # 在屏幕上绘制外星人
    gifts.draw(screen)  # 在屏幕上绘制增益包
    explosions.draw(screen)  # 在屏幕上绘制爆炸特效
    # 得分板显示
    text = font.render('Score: ' + str(stats.score), True, (255, 58, 0))
    screen.blit(text, (30, 10))
    ship_left_image = pygame.transform.scale(ship.image, (60, 90))
    # 按钮和插图的渲染
    for button in buttons.values():
        button.render(screen, all_sounds)
    for i in range(0, stats.ship_left):
        screen.blit(ship_left_image, (screen.get_rect().left + 20 + i * 70, screen.get_rect().bottom - 110))
    # 游戏未开始时，游戏插图的绘制
    if not stats.game_active:
        screen.blit(title_image[0], (screen.get_rect().centerx - 400, screen.get_rect().centery - 250))
        screen.blit(title_image[1], (screen.get_rect().centerx + 170, screen.get_rect().centery - 10))
        screen.blit(title_image[2], (screen.get_rect().centerx - 240, screen.get_rect().centery - 310))
        screen.blit(title_image[3], (screen.get_rect().centerx - 40, screen.get_rect().centery - 10))
    # 游戏未开始时，游戏说明的绘制
    elif stats.game_active:
        screen.blit(move_keyboard, (screen.get_rect().centerx + 250, screen.get_rect().centery + 190))
        screen.blit(space_keyboard, (screen.get_rect().centerx + 242, screen.get_rect().centery + 310))
    pygame.display.flip()  # 让绘制屏幕可见


def create_gifts(gifts, gift_image):
    r = random.random()  # 随机决策值
    x_place = random.uniform(5, ai_settings.screen_width - 125)
    if r <= 0.25:  # 寒冰Buff增益包
        gift = Gift(1, x_place, gift_image)
        gifts.add(gift)
    elif r <= 0.5:  # 火焰Buff增益包
        gift = Gift(2, x_place, gift_image)
        gifts.add(gift)
    elif r <= 0.75:  # 双发Buff增益包
        gift = Gift(3, x_place, gift_image)
        gifts.add(gift)
    else:  # 加血Buff增益包
        gift = Gift(4, x_place, gift_image)
        gifts.add(gift)


def update_gifts(stats, gifts, ship, screen, gift_image, get_buff_sound):
    for gift in gifts:  # 对列表中的每一个gift进行更新
        # 若gift到达屏幕最底部
        if gift.rect.bottom >= screen.get_rect().bottom:
            gifts.remove(gift)
        # 飞船碰撞到增益包时
        elif abs(gift.rect.y - ship.rect.y) < max(gift.rect.height, ship.rect.height) \
                and abs(gift.rect.x - ship.rect.x) < max(gift.rect.width, ship.rect.width) \
                and pygame.sprite.collide_mask(ship, gift):
            if gift.gift_type <= 3:  # 获取子弹类buff增益包
                ai_settings.bullet_condition = gift.gift_type + 1
            elif gift.gift_type == 4:  # 获取加血类buff增益包
                if stats.ship_left < ai_settings.ship_limit:
                    stats.ship_left += 1
            gifts.remove(gift)
            pygame.time.set_timer(pygame.USEREVENT, 5000)
            get_buff_sound.play()
    if len(gifts) == 0:
        now = time.get_ticks()
        if now - ai_settings.last_time_buffed >= 7000 or ai_settings.last_time_buffed == 0:
            ai_settings.last_time_buffed = now
            create_gifts(gifts, gift_image)  # 增益包生成
    gifts.update()  # 调用增益包更新函数


def update_bullets(screen, stats, ship, aliens, bullets, explosions, explosion_sm, bomb_sound):
    bullets.update(screen, ship)
    # 删除子弹
    for bullet in bullets:
        if bullet.bullet_type <= 4:
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
                elif bullet.bullet_type == 2 and (not alien.is_frozen):
                    alien.alien_speed /= 2
                    alien.drop_speed /= 2
                    alien.is_frozen = 1
        elif bullet.bullet_type == 5:
            if bullet.rect.top >= screen.get_rect().bottom or bullet.rect.bottom <= 0 or \
                    bullet.rect.left <= 5 or bullet.rect.right >= screen.get_rect().width - 5:
                bullets.remove(bullet)
            collision_ship = pygame.sprite.collide_mask(ship, bullet)
            if collision_ship:
                bullets.remove(bullet)
                explosion = Explosion(ship.rect.center, explosion_sm)  # 实例化爆炸对象，爆炸中心=敌人中心位置
                explosions.add(explosion)
                bomb_sound.play()
                ship.key_list.clear()
                pygame.time.set_timer(pygame.USEREVENT + 1, ai_settings.frames * 3)
                ai_settings.ship_broken = True


def fire_bullets(screen, ship, bullets, shoot_sound, bullet_images):
    # 限制屏幕上最多子弹数量
    if len(bullets) < ai_settings.bullets_allowed:
        # 创建子弹
        if ai_settings.bullet_condition == 4:  # 双发子弹
            new_bullet1 = Bullet(screen, ship.rect.top, ship.rect.centerx - 30, bullet_images)
            new_bullet2 = Bullet(screen, ship.rect.top, ship.rect.centerx + 30, bullet_images)
            bullets.add(new_bullet1)
            bullets.add(new_bullet2)
        else:  # 非 双发类型的 子弹
            new_bullet = Bullet(screen, ship.rect.top, ship.rect.centerx, bullet_images)
            bullets.add(new_bullet)
        shoot_sound.play()


def check_alien_num(screen, stats, aliens, bullets, alien_image):
    if len(aliens) == 0:
        # 若外星人均消灭，重新创建外星人，游戏难度上升
        stats.game_difficulty += 1
        create_fleet(screen, stats, aliens, alien_image)
    # elif stats.game_difficulty % 5 == 0:
    #     if len(aliens) == 1:
    #         for alien in aliens:
    #             if alien.types == 4:
    #                 for i in range(0, 4):
    #                     create_alien(screen, stats, aliens, random.randrange(0, ai_settings.number_aliens_x),
    #                                  random.randrange(0, ai_settings.number_rows), 1, alien_image)


def get_aliens_x_and_rows(screen, stats, ship, alien_image):
    alien = Alien(screen, stats, 1, alien_image)
    alien_width = alien.rect.width
    number_aliens_x = get_number_aliens_x(alien_width)
    number_rows = get_number_rows(ship.rect.height, alien.rect.height)
    return alien_width, number_aliens_x, number_rows


def create_fleet(screen, stats, aliens, alien_image):
    if stats.game_difficulty % 5:
        for row_number in range(ai_settings.number_rows):
            alien_number = 0
            # 外星人数量小于每行最大外星人数量时生成
            while alien_number < ai_settings.number_aliens_x:
                r = random.random()  # 随机决策值
                if r >= 0.90 - stats.game_difficulty * 0.015 and r >= 0.75:
                    types = 3
                    create_alien(screen, stats, aliens, alien_number, row_number, types, alien_image)
                    alien_number += 3
                elif r >= 0.70 - stats.game_difficulty * 0.015 and r >= 0.65:
                    types = 2
                    create_alien(screen, stats, aliens, alien_number, row_number, types, alien_image)
                    alien_number += 2
                elif r >= 0.5 - stats.game_difficulty * 0.015 and r >= 0.2:
                    types = 1
                    create_alien(screen, stats, aliens, alien_number, row_number, types, alien_image)
                    alien_number += 1
                else:
                    alien_number += 1
    else:
        create_alien(screen, stats, aliens, 0, 0, 4, alien_image)  # 完成生成


def get_number_aliens_x(alien_width):
    # 计算一行可以放置外星人的宽度
    available_space_x = ai_settings.screen_width - 2 * alien_width
    # 计算一行可以放置外星人的个数
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def create_alien(screen, stats, aliens, alien_number, row_number, types, alien_image):
    alien = Alien(screen, stats, types, alien_image)
    if types <= 3:  # 普通外星小怪兽、中级外星乌龟人、高级外星飞船人三类
        alien.x = ai_settings.alien_width + 2 * ai_settings.alien_width * alien_number
        alien.y = 2 * alien.rect.height * (row_number - ai_settings.number_rows) / alien.types * 1.5
    elif types == 4:  # 外星Boss
        alien.x = screen.get_rect().centerx - alien.rect.width / 2
        alien.y = screen.get_rect().top - alien.rect.height
    alien.rect.x = alien.x
    alien.rect.y = alien.y
    aliens.add(alien)  # 添加alien实例


# 计算容纳多少行外星人
def get_number_rows(ship_height, alien_height):
    available_space_y = ai_settings.screen_height - (5 * alien_height) - ship_height
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def update_aliens(stats, screen, ship, aliens, bullets, explosions, explosion_sm, alien_image, bomb_sound):
    for alien in aliens.sprites():
        if alien.types == 4 and alien.y >= screen.get_rect().top + 30:
            alien.drop_speed = 0
        alien.y += alien.drop_speed
        alien.rect.y = alien.y
    # 对外星人列表中的每个外星人
    for alien in aliens:
        if alien.rect.right >= screen.get_rect().width - 25 or \
                alien.rect.x <= 25 or \
                abs(alien.relative_position) >= alien.moving_range:
            alien.direct *= -1
        # 碰撞检测
        if abs(alien.rect.y - ship.rect.y) < max(alien.rect.height, ship.rect.height) \
                and abs(alien.rect.x - ship.rect.x) < max(alien.rect.width, ship.rect.width) \
                and pygame.sprite.collide_mask(ship, alien) and (not ai_settings.ship_broken):
            # 实例化爆炸对象，爆炸中心=敌人中心位置
            explosion = Explosion(ship.rect.center, explosion_sm)
            explosions.add(explosion)
            bomb_sound.play()
            ship.key_list.clear()
            pygame.time.set_timer(pygame.USEREVENT + 1, ai_settings.frames * 3)
            ai_settings.ship_broken = True  # 飞船被摧毁
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
    if stats.game_difficulty >= 1:
        stats.game_difficulty -= 1
    if stats.ship_left > 0:  # 玩家有生命值剩余
        ai_settings.ship_broken = False  # 重置飞船摧毁标记
        stats.ship_left -= 1  # 扣除一条生命值
    if stats.ship_left == 0:
        stats.game_active = False  # 结束游戏
        data = {'msg': 'reset'}
        ev = pygame.event.Event(pygame.USEREVENT + 4, data)
        pygame.event.post(ev)


def check_aliens_bottom(stats, screen, aliens):
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            stats.score -= alien.types  # 不同等级的外星人扣分值不同
            if stats.score < 0:  # 不足扣分则分数清零
                stats.score = 0
            aliens.remove(alien)  # 移除该外星人


def init_explosion():
    # 载入爆炸图片
    explosion_image = []  # 初始化爆炸特效资源列表
    for i in range(14):  # 一共载入14张图片
        # 用f-string将文件名格式化，:04指定了宽度为4位数字，左侧以0补齐
        image = pygame.image.load(f'./images/explosion/explosion{i:04}.png').convert_alpha()  # 载入图片，返回Surface对象
        image = pygame.transform.scale(image, (200, 200))  # 设置大小
        explosion_image.append(image)  # 将Surface对象添加到列表中备用
    return explosion_image  # 返回爆炸特效资源列表


def init_gift():
    gift_image = []  # 初始化增益包资源列表
    image1 = pygame.image.load('./images/ice_buff.png').convert_alpha()  # 载入寒冰buff
    image2 = pygame.image.load('./images/fire_buff.png').convert_alpha()  # 载入火焰buff
    image3 = pygame.image.load('./images/double_shoot_buff.png').convert_alpha()  # 载入双发buff
    image4 = pygame.image.load('./images/add_heart.png').convert_alpha()  # 载入增加生命值buff
    image1 = pygame.transform.scale(image1, (80, 80))  # 设置图像大小
    image2 = pygame.transform.scale(image2, (80, 80))  # 设置图像大小
    image3 = pygame.transform.scale(image3, (80, 80))  # 设置图像大小
    image4 = pygame.transform.scale(image4, (115, 70))  # 设置图像大小
    gift_image.append(image1)  # 将本图像添加到增益包资源列表
    gift_image.append(image2)  # 将本图像添加到增益包资源列表
    gift_image.append(image3)  # 将本图像添加到增益包资源列表
    gift_image.append(image4)  # 将本图像添加到增益包资源列表
    return gift_image  # 返回加载完毕的增益包资源列表


def init_alien():
    alien_image = []  # 初始化敌方外星人资源列表
    image1 = pygame.image.load('./images/alien1.png').convert_alpha()  # 载入外星小怪（lv=1）
    image2 = pygame.image.load('./images/alien2.png').convert_alpha()  # 载入外星乌龟（lv=2）
    image3 = pygame.image.load('./images/alien3.png').convert_alpha()  # 载入外星飞碟（lv=3）
    image4 = pygame.image.load('./images/alien_boss.png').convert_alpha()  # 载入外星Boss（lv=∞）
    image1 = pygame.transform.scale(image1, (60, 60))  # 设置图像大小
    image2 = pygame.transform.scale(image2, (1.5 * 60, 80))  # 设置图像大小
    image3 = pygame.transform.scale(image3, (3.5 * 60, 120))  # 设置图像大小
    image4 = pygame.transform.scale(image4, (500, 150))  # 设置图像大小
    alien_image.append(image1)  # 将本图像添加到增益包资源列表
    alien_image.append(image2)  # 将本图像添加到增益包资源列表
    alien_image.append(image3)  # 将本图像添加到增益包资源列表
    alien_image.append(image4)  # 将本图像添加到增益包资源列表
    return alien_image  # 返回加载完毕的敌方外星人列表
