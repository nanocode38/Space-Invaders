"""
存储meteorolite类
"""
import pygame
from pygame.sprite import Sprite
from pygame import image
import random as rd
class Meteorolite(Sprite):
    """表示单个陨石的类"""
    def __init__(self, settings, screen):
        """初始化数据"""
        super(Meteorolite, self).__init__()
        rand = rd.randint(1, 3)
        if rand == 1:
            self.image = image.load('images\\meteorolite1.bmp')
        if rand == 2:
            self.image = image.load("images\\meteorolite2.bmp")
        if rand == 3:  
            self.image = image.load("images\\meteorolite3.bmp")
        self.rect = self.image.get_rect()
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.image.set_colorkey((241,251,252))
        self.image = self.image.convert()
        self.image = self.image.convert_alpha()
        a = []
        for i in range(0,2):
            for j in range(0,9):
                a.append(i+j/10.0) 
        self.speed_factor = rd.choice(a)
        self.rect.x = rd.randint(40, settings.screen_width-40)
        self.rect.bottom = self.screen_rect.top
        self.y = self.rect.y
        
    def update(self):
        """更新陨石位置"""
        self.y += self.speed_factor
        self.rect.y = self.y  

    def blitme(self):
        """在指定位置绘制陨石"""
        self.screen.blit(self.image, self.rect)              