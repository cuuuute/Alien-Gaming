from pygame import time
from pygame.sprite import Sprite


class Explosion(Sprite):
    def __init__(self, center, imgs):
        super().__init__()
        self.imgs = imgs
        self.image = imgs[0]  # 爆炸特效的首帧
        self.rect = self.image.get_rect()  # 获取资源图片大小
        self.rect.center = center
        self.frame = 0
        self.last_update = time.get_ticks()  # 获取最近刷新时间
        self.frame_rate = 40  # 设定爆炸图片显示的间隔时间

    def update(self):
        now = time.get_ticks()  # 获取当前时间
        if now - self.last_update > self.frame_rate:  # 本帧与上一帧的时间差达到fram_rate时，显示1帧爆炸图片
            self.last_update = now  # 记录最近刷新时间
            self.frame += 1  # 帧数+1，这样下次才会调用下一张图片
            if self.frame == len(self.imgs):  # 当爆炸图片到达最后一帧时，爆炸对象自杀(不再占用内存)
                self.kill()
            else:
                self.image = self.imgs[self.frame]  # 指定要显示的爆炸图片(Surface对象)
