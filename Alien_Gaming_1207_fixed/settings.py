# 存储外星人入侵小游戏所有设置的类

class Setting:
    def __init__(self):
        # 窗口屏幕设置
        self.frames = 100
        self.screen_width = 1000
        self.screen_height = 850
        self.bg_color = (230, 230, 230)
        # 飞船设置
        self.ship_speed = 600 / self.frames  # 设置飞船速度（移动像素）
        self.ship_broken = False  # 设置飞船状态
        self.ship_limit = 5  # 飞船最大生命条数
        # 子弹设置
        self.bullet_speed = 1000 / self.frames  # 己方飞船子弹速度
        self.enemy_bullet_speed = -160 / self.frames  # 敌方飞船子弹速度
        self.bullet_width = 6  # 子弹大小
        self.bullet_height = 20  # 子弹大小
        self.bullets_allowed = 10  # 屏幕最多子弹数（限制子弹发射速率）
        self.bullet_condition = 1  # 子弹类型
        self.bullet_harm = 1  # 威力
        # 上次增益效果开始时间
        self.last_time_buffed = 0
        # 外星人生成设置
        self.alien_width = None  # 外星人的宽度
        self.number_aliens_x = None  # 每行最多数量
        self.number_rows = None  # 一次生成最多列数
        # 声音设置
        self.init_sound = 0.33  # 声音初始值
