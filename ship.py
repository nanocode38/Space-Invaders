"""含有飞船类的模块"""
import pygame
from pygame.sprite import Sprite

class Ship(Sprite):

    def __init__(self, settings, screen):
        """初始化飞船，并设置它的起始位置。"""
        super(Ship, self).__init__()
        self.screen = screen
        self.settings = settings

        # 加载飞船的图像，并获得它的外接矩形。
        self.image = pygame.image.load('images\\ship.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.image.set_colorkey((230, 230, 230))
        self.image = self.image.convert()
        self.image = self.image.convert_alpha()

        # 在屏幕底部中央启动每艘飞船。
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        
        # 为船的中心存储一个实数值。
        self.center = float(self.rect.centerx)
        
        # 旗帜。
        self.moving_right = False
        self.moving_left = False
        
    def center_ship(self):
        """将船置于屏幕中央。"""
        self.center = self.screen_rect.centerx
        
    def update(self):
        """根据移动旗帜更新飞船的位置。"""
        # 更新船的中心值，而不是矩形。
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.settings.ship_speed_factor
        # 从self.center更新rect对象。
        self.rect.centerx = self.center


    def blitme(self):
        """在屏幕上绘制飞船"""
        self.screen.blit(self.image, self.rect)
