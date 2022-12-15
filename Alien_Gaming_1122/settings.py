# 存储外星人入侵小游戏所有设置的类

class Setting:
    def __init__(self):
        self.frames = 100

        self.screen_width = 1000
        self.screen_height = 850
        self.bg_color = (230, 230, 230)
        self.ship_speed = 600 / self.frames  # 飞船速度（移动像素）
        self.ship_broken = False
        # 飞船生命数
        self.ship_limit = 3
        # 子弹设置
        self.bullet_speed = 1000 / self.frames
        self.bullet_width = 6
        self.bullet_height = 20
        self.bullets_allowed = 10
        self.bullet_condition = 1
        self.bullet_harm = 1
        # 上次增益效果开始时间
        self.last_time_buffed = 0
        # 外星人的宽度、每行最多数量、一次生成最多列数
        self.alien_width = None
        self.number_aliens_x = None
        self.number_rows = None
        # 声音初始值
        self.init_sound = 0.33
