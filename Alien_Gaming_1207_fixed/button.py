import pygame
from global_var import ai_settings


class Button(object):
    def __init__(self, rect, image_num, btn_start_images, text, font_info, event_id):
        self.status = 0  # 设置状态
        self.rect = rect  # 设置大小
        self.text = text  # 设置文本
        self.image_num = image_num  # 设置图片数量
        self.font_info = font_info  # 设置字体信息
        self.event_id = event_id  # 设置事件id

        # 设定底图，每一种 status 一张。
        self.image = []
        # 获取底图资源大小并设置
        img_rect = btn_start_images[0].get_rect()
        self.img_width = img_rect.width
        self.image = btn_start_images

        # # 设定 Label 对象
        # if text == "":
        #     self.label = None
        # else:
        #     self.label = Label(rect.left, rect.top, text, font_info)

    def render(self, screen, all_sounds):
        if self.status >= 0:
            # 开始按钮或退出按钮
            if self.text == 'start' or self.text == 'exit':
                # 绘制按钮封面和底图，可以根据光标移动至按钮上，来切换按钮的图标
                screen.blit(self.image[self.status], (self.rect.left, self.rect.top))
            # 音量调节按钮
            elif self.text == 'volume_button_image':
                # 绘制音量按钮，根据载入按钮不同形态时的图片资源来绘制
                screen.blit(self.image[0], (self.rect.left, self.rect.top))
                screen.blit(self.image[self.status + 1], (self.rect.left + 40, self.rect.top - 1))
                # 设置音量值
                for sound in all_sounds.values():
                    sound.set_volume(ai_settings.init_sound * self.status)
            # if self.label is not None:
            #     self.label.render(surface)

    # 检查鼠标位置，以此来实现光标移动到按钮上时按钮会改变形态，实现交互
    def check_mouse_place(self, event):
        if self.status < 0:
            flag = False  # disabled
        else:
            flag = self.rect.collidepoint(event.pos)
        return flag

    # 链接按钮与鼠标事件，实现按钮功能的响应
    def update(self, event, msg):
        if self.check_mouse_place(event):
            data = {'msg': msg}
            # 执行事件id对应的事件
            ev = pygame.event.Event(self.event_id, data)
            pygame.event.post(ev)
        elif self.text == 'start' or self.text == 'exit':
            self.status = 0
