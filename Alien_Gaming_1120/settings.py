# 存储外星人入侵小游戏所有设置的类

class Setting:
    def __init__(self):
        self.screen_width = 1000
        self.screen_height = 850
        self.bg_color = (230, 230, 230)
        self.ship_speed = 4  # 飞船速度（移动像素）
        self.ship_broken = 0
        # 飞船生命数
        self.ship_limit = 3
        # 子弹设置
        self.bullet_speed = 5
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 60, 60, 60
        self.bullets_allowed = 10
        # 外星人速度
        # fleet_drop_speed表示外星人向下移动的速度
        self.fleet_drop_speed = 1

