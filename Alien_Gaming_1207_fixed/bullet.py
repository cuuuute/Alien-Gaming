import pygame
from pygame.sprite import Sprite
# 通过使用精灵类，可将游戏中相关的元素编组，进而可以同时操作编组中的元素


from global_var import ai_settings


class Bullet(Sprite):
    def __init__(self, screen, y, x, bullet_images, is_alien_bullet=0):
        super().__init__()  # 继承Sprite类
        self.screen = screen  # 设置屏幕
        self.bullet_type = None
        if is_alien_bullet:  # 是外星人Boss发射的子弹
            self.bullet_type = 5  # 子弹类型为5
        else:  # 是己方飞船的子弹，不是外星人Boss发射的子弹
            self.bullet_type = ai_settings.bullet_condition  # 1、普通；2、冰；3、火；4、双发；5、boss子弹

        self.color = None  # 声明颜色
        self.shoot_once = 1  # 默认射击模式为单发
        ai_settings.bullet_harm = 1  # 默认伤害为1
        self.rect = None  # 声明大小
        self.image = None  # 声明图片资源
        # 声明加速度 用于实现类型5（Boss子弹）自动追踪目标的效果
        self.x_acceleration = None
        self.y_acceleration = None
        # 声明速度
        self.x_speed = None
        self.y_speed = None
        self.exist_time = None  # 声明存在时间
        # 加载子弹图片资源，并设置大小和出射坐标
        # 寒冰子弹
        if self.bullet_type == 2:
            self.image = bullet_images[0]
            self.rect = self.image.get_rect()
            self.rect.centerx = x
            self.rect.top = y  # 子弹从飞船顶部射出
        # 火焰子弹
        elif self.bullet_type == 3:
            self.image = bullet_images[1]
            self.rect = self.image.get_rect()
            self.rect.centerx = x
            self.rect.top = y  # 子弹从飞船顶部射出
            ai_settings.bullet_harm = 2
        # Boss子弹
        elif self.bullet_type == 5:
            self.image = bullet_images[2]
            self.rect = self.image.get_rect()
            self.rect.centerx = x
            self.rect.bottom = y  # 子弹从boss底部射出
            self.x_acceleration = 0
            self.y_acceleration = 0
            self.x_speed = 0
            self.exist_time = 0
        # 普通子弹
        else:
            # 在（0,0）处创建一个表示子弹的矩形，再设置正确位置
            self.rect = pygame.Rect(0, 0, ai_settings.bullet_width, ai_settings.bullet_height)
            self.rect.centerx = x
            self.rect.top = y  # 子弹从飞船顶部射出
            self.color = 60, 60, 60

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        # 设置己方飞船子弹的竖直速度始终为定值ai_settings.bullet_speed
        if self.bullet_type <= 4:
            self.y_speed = ai_settings.bullet_speed
        # 设置Boss子弹的初始竖直速度为0，之后会在update函数中进行修改，以便实现自动追踪目标的效果
        else:
            self.y_speed = 0

    # 更新子弹位置
    def update(self, screen, ship):
        # 己方飞船的四种类型子弹，只需要更新位置即可
        if self.bullet_type <= 4:
            self.y -= self.y_speed
            self.rect.y = self.y
        # Boss发射的子弹实现子弹自动追踪效果
        elif self.bullet_type == 5:
            self.exist_time += 1
            # Boss的子弹存在时间为5秒，若子弹未超出存在时间
            if self.exist_time < ai_settings.frames * 5:
                # 子弹中心点的横坐标与飞船中心点的横坐标之差大于0，即子弹在飞船的右半侧
                if self.rect.centerx - ship.rect.centerx > 0:
                    self.x_acceleration -= 1 / ai_settings.frames  # 给子弹施加一个向左的加速度
                # 子弹中心点的横坐标与飞船中心点的横坐标之差小于0，即子弹在飞船的左半侧
                else:
                    self.x_acceleration += 1 / ai_settings.frames  # 给子弹施加一个向右的加速度

                # 消除“逐帧更新”的强滞后性和延迟，根据加速度方向将子弹加速度直接提升至游戏设置中的子弹速度
                if self.x_acceleration < ai_settings.enemy_bullet_speed:
                    self.x_acceleration = ai_settings.enemy_bullet_speed
                elif self.x_acceleration > -ai_settings.enemy_bullet_speed:
                    self.x_acceleration = -ai_settings.enemy_bullet_speed

                # 根据子弹上一帧的x轴速度和子弹加速度，更新子弹当前的x轴速度
                self.x_speed += self.x_acceleration
                if self.x_speed < ai_settings.enemy_bullet_speed:
                    self.x_speed = ai_settings.enemy_bullet_speed
                elif self.x_speed > -ai_settings.enemy_bullet_speed:
                    self.x_speed = -ai_settings.enemy_bullet_speed

                # 子弹中心点的纵坐标与飞船中心点的纵坐标之差大于0，即子弹在飞船的下半侧
                if self.rect.centery - ship.rect.centery > 0:
                    self.y_acceleration -= 1.5 / ai_settings.frames  # 给子弹施加一个向上的加速度
                # 子弹中心点的纵坐标与飞船中心点的纵坐标之差小于0，即子弹在飞船的上半侧
                else:
                    self.y_acceleration += 1.5 / ai_settings.frames  # 给子弹施加一个向下的加速度

                # 消除“逐帧更新”的强滞后性和延迟，根据加速度方向将子弹加速度直接提升至游戏设置中的子弹速度
                if self.y_acceleration < ai_settings.enemy_bullet_speed:
                    self.y_acceleration = ai_settings.enemy_bullet_speed
                elif self.y_acceleration > -ai_settings.enemy_bullet_speed:
                    self.y_acceleration = -ai_settings.enemy_bullet_speed

                # 根据子弹上一帧的y轴速度和子弹加速度，更新子弹当前的y轴速度
                self.y_speed += self.y_acceleration
                if self.y_speed < ai_settings.enemy_bullet_speed:
                    self.y_speed = ai_settings.enemy_bullet_speed
                elif self.y_speed > -ai_settings.enemy_bullet_speed:
                    self.y_speed = -ai_settings.enemy_bullet_speed

            # 根据子弹的速度，更新子弹位置和中心点坐标
            self.x += self.x_speed
            self.y += self.y_speed
            self.rect.y = self.y
            self.rect.x = self.x

    # 绘制子弹
    def draw_bullet(self):
        # 普通子弹或双发子弹，由pygame进行绘制
        if self.bullet_type == 1 or self.bullet_type == 4:
            pygame.draw.rect(self.screen, self.color, self.rect)
        # 其余子弹类型由图片资源加载
        else:
            self.screen.blit(self.image, self.rect)
