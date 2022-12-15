import pygame
from global_var import ai_settings


class Button(object):
    def __init__(self, rect, image_num, btn_start_images, text, font_info, event_id):
        self.status = 0
        self.rect = rect
        self.text = text
        self.image_num = image_num
        self.font_info = font_info
        self.event_id = event_id

        # 设定底图，每一种 status 一张。
        self.image = []

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
            if self.text == 'start':
                screen.blit(self.image[self.status], (self.rect.left, self.rect.top))
            elif self.text == 'volume_button_image':
                screen.blit(self.image[0], (self.rect.left, self.rect.top))
                screen.blit(self.image[self.status + 1], (self.rect.left + 40, self.rect.top - 1))
                for sound in all_sounds.values():
                    sound.set_volume(ai_settings.init_sound * self.status)
            # if self.label is not None:
            #     self.label.render(surface)

    def check_mouse_place(self, event):
        if self.status < 0:
            flag = False  # disabled
        else:
            flag = self.rect.collidepoint(event.pos)
        return flag

    def update(self, event, msg):
        if self.check_mouse_place(event):
            data = {'msg': msg}
            ev = pygame.event.Event(self.event_id, data)
            pygame.event.post(ev)
        elif self.text == 'start':
            self.status = 0

