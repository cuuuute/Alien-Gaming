# 存储外星人入侵小游戏所有设置的类

class Setting:
    def __init__(self):
        self.screen_width = 1000
        self.screen_height = 800
        self.bg_color = (230, 230, 230)
        self.ship_speed = 0.5  # 飞船速度（移动像素）
        # 飞船生命数
        self.ship_limit = 3
        # 子弹设置
        self.bullet_speed = 1
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 60, 60, 60
        self.bullets_allowed = 10
        # 外星人速度
        self.alien_speed = 0.07
        # fleet_drop_speed表示外星人撞到屏幕边缘，向下移动的速度
        self.fleet_drop_speed = 0.05
        # fleet_direction为正负一表示向右/左移动
        self.fleet_direction = 1

