from pygame.sprite import Sprite
from global_var import ai_settings


class Gift(Sprite):
    def __init__(self, gift_type, x, gift_image):
        super().__init__()
        self.gift_type = gift_type  # 设置类型
        self.image = gift_image[gift_type - 1]  # 载入图片资源

        self.rect = self.image.get_rect()  # 获取资源图片大小
        self.speed = 300 / ai_settings.frames  # 设置速度

        self.rect.x = x
        self.rect.y = -80
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def update(self):
        self.y += self.speed  # 根据速度更新y轴位置，增益包移动路线为直线
        self.rect.y = self.y
