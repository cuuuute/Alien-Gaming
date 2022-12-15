import pygame
from ship import Ship
import game_functions as gf
from pygame.sprite import Group  # Group类似列表
from game_stats import GameStats
from global_var import ai_settings
from button import Button


def run_game():
    pygame.init()  # 初始化屏幕对象
    stats = GameStats()  # 初始化游戏状态
    screen = pygame.display.set_mode((1024, 768), pygame.FULLSCREEN, 256)  # 设定游戏分辨率，并设置全屏化游戏模式
    background = pygame.image.load('./images/background.png')  # 加载地图背景资源
    background = pygame.transform.scale(background, (ai_settings.screen_width, ai_settings.screen_height))  # 加载全局设置
    move_keyboard = pygame.image.load('images/keyboard_move.png')  # 加载移动按键说明
    move_keyboard = pygame.transform.scale(move_keyboard, (220, 130))  # 调整图像大小
    space_keyboard = pygame.image.load('images/keyboard_space.png')  # 加载开火按键说明
    space_keyboard = pygame.transform.scale(space_keyboard, (230, 90))  # 调整图像大小
    pygame.display.set_caption("外星人入侵")  # 设置窗口标题

    title_word_image = pygame.image.load('./images/title.png')  # 加载游戏标题
    title_word_image = pygame.transform.scale(title_word_image, (800, 260))  # 设置标题图像大小
    title_alien_image1 = pygame.image.load('./images/alien1_rotated.png')  # 加载插图资源1
    title_alien_image1 = pygame.transform.scale(title_alien_image1, (220, 160))  # 设置图像大小
    title_alien_image2 = pygame.image.load('./images/alien2_rotated.png')  # 加载插图资源2
    title_alien_image2 = pygame.transform.scale(title_alien_image2, (120, 100))  # 设置图像大小
    title_alien_image3 = pygame.image.load('./images/alien1.png')  # 加载插图资源3
    title_alien_image3 = pygame.transform.scale(title_alien_image3, (80, 80))  # 设置图像大小
    title_images = [title_word_image, title_alien_image1, title_alien_image2, title_alien_image3]  # 游戏插图资源列表

    bullet_snow = pygame.image.load('./images/bullet_snow.png').convert_alpha()  # 加载寒冰子弹资源
    bullet_snow = pygame.transform.scale(bullet_snow, (50, 50))  # 设置图像大小
    bullet_fire = pygame.image.load('./images/bullet_fire.png').convert_alpha()  # 加载火焰子弹资源
    bullet_fire = pygame.transform.scale(bullet_fire, (35, 60))  # 设置图像大小
    bullet_alien = pygame.image.load('./images/bullet_alien.png').convert_alpha()  # 加载Boss子弹资源
    bullet_alien = pygame.transform.scale(bullet_alien, (120, 100))  # 设置图像大小
    bullet_images = [bullet_snow, bullet_fire, bullet_alien]  # 游戏内子弹资源列表
    explosion_image = gf.init_explosion()  # 加载爆炸特效
    gift_image = gf.init_gift()  # 加载增益包Buff资源
    alien_image = gf.init_alien()  # 加载敌方外星人资源
    all_images = {'explosion': explosion_image, 'gift': gift_image, 'alien': alien_image,
                  'bullet': bullet_images}  # 游戏内所有插图资源

    shoot_sound = pygame.mixer.Sound('./music/shoot.wav')  # 载入射击音效
    bomb_sound = pygame.mixer.Sound('./music/bomb.wav')  # 载入爆炸音效
    get_buff_sound = pygame.mixer.Sound('./music/get_buff.mp3')  # 载入获取buff的音效
    all_sounds = {'shoot': shoot_sound, 'bomb': bomb_sound, 'get_buff': get_buff_sound}  # 游戏内所有音效资源

    font = pygame.font.SysFont('Times', 60, bold=True)  # 设置字体

    btn_start_image_width = 200  # 设置按钮的宽
    btn_start_image_height = 180  # 设置按钮的高
    btn_start_image1 = pygame.image.load('images/start_button_image/button_1.png')  # 载入开始按钮的形态1插图
    btn_start_image1 = pygame.transform.scale(btn_start_image1,
                                              (btn_start_image_width, btn_start_image_height))  # 设置按钮大小
    btn_start_image2 = pygame.image.load('images/start_button_image/button_2.png')  # 载入开始按钮的形态2插图
    btn_start_image2 = pygame.transform.scale(btn_start_image2,
                                              (btn_start_image_width, btn_start_image_height))  # 设置按钮大小
    btn_start_images = [btn_start_image1, btn_start_image2]  # 开始按钮的游戏资源列表
    btn_start_rect = pygame.Rect(screen.get_rect().centerx - btn_start_image_width / 2,
                                 screen.get_rect().centery - btn_start_image_height / 2 + 150, btn_start_image_width,
                                 btn_start_image_height)  # 创建矩形对象
    start_button = Button(btn_start_rect, 2, btn_start_images, 'start', None, pygame.USEREVENT + 2)  # 创建按钮用户事件

    btn_exit_image_width = 80  # 设置按钮的宽
    btn_exit_image_height = 80  # 设置按钮的高
    btn_exit_image1 = pygame.image.load('images/exit_button_image/exit_1.png')  # 载入退出按钮的形态1插图
    btn_exit_image1 = pygame.transform.scale(btn_exit_image1, (btn_exit_image_width, btn_exit_image_height))  # 设置按钮大小
    btn_exit_image2 = pygame.image.load('images/exit_button_image/exit_2.png')  # 载入退出按钮的形态2插图
    btn_exit_image2 = pygame.transform.scale(btn_exit_image2, (btn_exit_image_width, btn_exit_image_height))  # 设置按钮大小
    btn_exit_images = [btn_exit_image1, btn_exit_image2]  # 退出按钮的游戏资源列表
    btn_exit_rect = pygame.Rect(screen.get_rect().centerx + 350, screen.get_rect().centery - 350, btn_exit_image_width,
                                btn_exit_image_height)  # 创建矩形对象
    exit_button = Button(btn_exit_rect, 2, btn_exit_images, 'exit', None, pygame.USEREVENT + 5)  # 创建按钮用户事件

    btn_volume_image_width = 50  # 设置按钮的宽
    btn_volume_image_height = 50  # 设置按钮的高
    volume_image = pygame.image.load('images/volume_button_image/volume_image.png')  # 载入音量小喇叭按钮的插图
    volume_image = pygame.transform.scale(volume_image, (50, 50))
    btn_volume_image1 = pygame.image.load('images/volume_button_image/1.png')  # 载入音量的插图
    btn_volume_image1 = pygame.transform.scale(btn_volume_image1, (btn_volume_image_width, btn_volume_image_height))
    btn_volume_image2 = pygame.image.load('images/volume_button_image/2.png')  # 载入音量小的插图
    btn_volume_image2 = pygame.transform.scale(btn_volume_image2, (btn_volume_image_width, btn_volume_image_height))
    btn_volume_image3 = pygame.image.load('images/volume_button_image/3.png')  # 载入音量中等的插图
    btn_volume_image3 = pygame.transform.scale(btn_volume_image3, (btn_volume_image_width, btn_volume_image_height))
    btn_volume_image4 = pygame.image.load('images/volume_button_image/4.png')  # 载入音量响的插图
    btn_volume_image4 = pygame.transform.scale(btn_volume_image4, (btn_volume_image_width, btn_volume_image_height))
    btn_volume_rect = pygame.Rect(screen.get_rect().centerx - btn_volume_image_width / 2 + 390,
                                  screen.get_rect().centery - btn_volume_image_height / 2 + 340, btn_volume_image_width,
                                  btn_volume_image_height)  # 创建矩形对象
    btn_volume_images = [volume_image, btn_volume_image1, btn_volume_image2, btn_volume_image3,
                         btn_volume_image4]  # 音量调节按钮的游戏资源列表
    volume_button = Button(btn_volume_rect, 5, btn_volume_images, 'volume_button_image', None,
                           pygame.USEREVENT + 3)  # 创建按钮用户事件
    volume_button.status = 1  # 将音量调节按钮状态置为1

    buttons = {'start': start_button, 'volume_button_image': volume_button, 'exit': exit_button}  # 所有按钮的游戏资源列表

    ship = Ship(screen)  # 绘制一艘飞船
    bullets = Group()  # 创建一个存储子弹的编组
    aliens = Group()  # 创建一个外星人编组
    explosions = Group()  # 创建一个爆炸效果组
    gifts = Group()  # 创建一个掉落奖励组
    ai_settings.alien_width, ai_settings.number_aliens_x, ai_settings.number_rows = \
        gf.get_aliens_x_and_rows(screen, stats, ship, alien_image)  # 加载游戏设置
    clock = pygame.time.Clock()  # 创建clock对象，设置帧速率

    # 开始游戏主循环
    while True:
        clock.tick(ai_settings.frames)  # 设置帧数
        # 检查游戏资源完整性
        gf.check_events(stats, screen, buttons, ship, aliens, bullets, gifts, explosions,all_sounds['shoot'], all_images['bullet'])
        # 游戏状态被激活（游戏启动）
        if stats.game_active:
            ship.update()  # 更新飞船
            gf.update_aliens(stats, screen, ship, aliens, bullets, explosions, all_images['explosion'],all_images['alien'], all_sounds['bomb'])  # 更新外星人
            gf.update_bullets(screen, stats, ship, aliens, bullets, explosions,all_images['explosion'], all_sounds['bomb'])  # 更新子弹
            gf.update_gifts(stats, gifts, ship, screen, all_images['gift'], all_sounds['get_buff'])  # 更新增益包
            explosions.update()  # 更新爆炸
        # elif stats.game_active and ai_settings.ship_broken:
        #     explosions.update()

        # 刷新游戏画面
        gf.update_screen(stats, screen, all_sounds, title_images, buttons, ship, aliens, bullets,explosions, gifts, background, move_keyboard, space_keyboard, font)


run_game()
