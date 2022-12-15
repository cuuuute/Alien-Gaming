import pygame
from ship import Ship
import game_functions as gf
from pygame.sprite import Group  # Group类似列表
from game_stats import GameStats
from global_var import ai_settings
from button import Button


def run_game():
    pygame.init()  # 初始化屏幕对象
    stats = GameStats()
    screen = pygame.display.set_mode((1024, 768), pygame.FULLSCREEN, 256)
    background = pygame.image.load('./images/background.png')
    background = pygame.transform.scale(background, (ai_settings.screen_width, ai_settings.screen_height))
    move_keyboard = pygame.image.load('images/keyboard_move.png')
    move_keyboard = pygame.transform.scale(move_keyboard, (220, 130))
    space_keyboard = pygame.image.load('images/keyboard_space.png')
    space_keyboard = pygame.transform.scale(space_keyboard, (230, 90))
    pygame.display.set_caption("外星人入侵")

    title_word_image = pygame.image.load('./images/title.png')
    title_word_image = pygame.transform.scale(title_word_image, (800, 260))
    title_alien_image1 = pygame.image.load('./images/alien1_rotated.png')
    title_alien_image1 = pygame.transform.scale(title_alien_image1, (220, 160))
    title_alien_image2 = pygame.image.load('./images/alien2_rotated.png')
    title_alien_image2 = pygame.transform.scale(title_alien_image2, (120, 100))
    title_alien_image3 = pygame.image.load('./images/alien1.png')
    title_alien_image3 = pygame.transform.scale(title_alien_image3, (80, 80))
    title_images = [title_word_image, title_alien_image1, title_alien_image2, title_alien_image3]

    bullet_snow = pygame.image.load('./images/bullet_snow.png').convert_alpha()
    bullet_snow = pygame.transform.scale(bullet_snow, (50, 50))
    bullet_fire = pygame.image.load('./images/bullet_fire.png').convert_alpha()
    bullet_fire = pygame.transform.scale(bullet_fire, (35, 60))
    bullet_alien = pygame.image.load('./images/bullet_alien.png').convert_alpha()
    bullet_alien = pygame.transform.scale(bullet_alien, (120, 100))
    bullet_images = [bullet_snow, bullet_fire, bullet_alien]
    explosion_image = gf.init_explosion()
    gift_image = gf.init_gift()
    alien_image = gf.init_alien()
    all_images = {'explosion': explosion_image, 'gift': gift_image, 'alien': alien_image, 'bullet': bullet_images}

    shoot_sound = pygame.mixer.Sound('./music/shoot.wav')
    bomb_sound = pygame.mixer.Sound('./music/bomb.wav')
    get_buff_sound = pygame.mixer.Sound('./music/get_buff.mp3')
    all_sounds = {'shoot': shoot_sound, 'bomb': bomb_sound, 'get_buff': get_buff_sound}

    font = pygame.font.SysFont('Times', 60, bold=True)

    btn_start_image_width = 200
    btn_start_image_height = 180
    btn_start_image1 = pygame.image.load('images/start_button_image/button_1.png')
    btn_start_image1 = pygame.transform.scale(btn_start_image1, (btn_start_image_width, btn_start_image_height))
    btn_start_image2 = pygame.image.load('images/start_button_image/button_2.png')
    btn_start_image2 = pygame.transform.scale(btn_start_image2, (btn_start_image_width, btn_start_image_height))
    btn_start_images = [btn_start_image1, btn_start_image2]
    btn_start_rect = pygame.Rect(screen.get_rect().centerx - btn_start_image_width / 2,
                                 screen.get_rect().centery - btn_start_image_height / 2 + 150,
                                 btn_start_image_width, btn_start_image_height)
    start_button = Button(btn_start_rect, 2, btn_start_images, 'start', None, pygame.USEREVENT + 2)

    btn_exit_image_width = 80
    btn_exit_image_height = 80
    btn_exit_image1 = pygame.image.load('images/exit_button_image/exit_1.png')
    btn_exit_image1 = pygame.transform.scale(btn_exit_image1, (btn_exit_image_width, btn_exit_image_height))
    btn_exit_image2 = pygame.image.load('images/exit_button_image/exit_2.png')
    btn_exit_image2 = pygame.transform.scale(btn_exit_image2, (btn_exit_image_width, btn_exit_image_height))
    btn_exit_images = [btn_exit_image1, btn_exit_image2]
    btn_exit_rect = pygame.Rect(screen.get_rect().centerx + 350,
                                screen.get_rect().centery - 350,
                                btn_exit_image_width, btn_exit_image_height)
    exit_button = Button(btn_exit_rect, 2, btn_exit_images, 'exit', None, pygame.USEREVENT + 5)

    btn_volume_image_width = 50
    btn_volume_image_height = 50
    volume_image = pygame.image.load('images/volume_button_image/volume_image.png')
    volume_image = pygame.transform.scale(volume_image, (50, 50))
    btn_volume_image1 = pygame.image.load('images/volume_button_image/1.png')
    btn_volume_image1 = pygame.transform.scale(btn_volume_image1, (btn_volume_image_width, btn_volume_image_height))
    btn_volume_image2 = pygame.image.load('images/volume_button_image/2.png')
    btn_volume_image2 = pygame.transform.scale(btn_volume_image2, (btn_volume_image_width, btn_volume_image_height))
    btn_volume_image3 = pygame.image.load('images/volume_button_image/3.png')
    btn_volume_image3 = pygame.transform.scale(btn_volume_image3, (btn_volume_image_width, btn_volume_image_height))
    btn_volume_image4 = pygame.image.load('images/volume_button_image/4.png')
    btn_volume_image4 = pygame.transform.scale(btn_volume_image4, (btn_volume_image_width, btn_volume_image_height))
    btn_volume_rect = pygame.Rect(screen.get_rect().centerx - btn_volume_image_width / 2 + 390,
                                  screen.get_rect().centery - btn_volume_image_height / 2 + 340,
                                  btn_volume_image_width, btn_volume_image_height)
    btn_volume_images = [volume_image, btn_volume_image1, btn_volume_image2, btn_volume_image3, btn_volume_image4]
    volume_button = Button(btn_volume_rect, 5, btn_volume_images, 'volume_button_image', None, pygame.USEREVENT + 3)
    volume_button.status = 1

    buttons = {'start': start_button, 'volume_button_image': volume_button, 'exit': exit_button}

    ship = Ship(screen)  # 绘制一艘飞船
    bullets = Group()  # 创建一个存储子弹的编组
    aliens = Group()  # 创建一个外星人编组
    explosions = Group()  # 创建一个爆炸效果组
    gifts = Group()  # 创建一个掉落奖励组
    ai_settings.alien_width, ai_settings.number_aliens_x, ai_settings.number_rows = \
        gf.get_aliens_x_and_rows(screen, stats, ship, alien_image)
    clock = pygame.time.Clock()

    # 开始游戏主循环
    while True:
        clock.tick(ai_settings.frames)
        gf.check_events(stats, screen, buttons, ship, aliens, bullets, gifts, explosions,
                        all_sounds['shoot'], all_images['bullet'])

        if stats.game_active:
            ship.update()
            gf.update_aliens(stats, screen, ship, aliens, bullets, explosions, all_images['explosion'],
                             all_images['alien'], all_sounds['bomb'])
            gf.update_bullets(screen, stats, ship, aliens, bullets, explosions,
                              all_images['explosion'], all_sounds['bomb'])
            gf.update_gifts(stats, gifts, ship, screen, all_images['gift'], all_sounds['get_buff'])
            explosions.update()
        # elif stats.game_active and ai_settings.ship_broken:
        #     explosions.update()

        gf.update_screen(stats, screen, all_sounds, title_images, buttons, ship, aliens, bullets,
                         explosions, gifts, background, move_keyboard, space_keyboard, font)


run_game()
