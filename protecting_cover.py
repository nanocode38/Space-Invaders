"""含有绘制防护罩的类ProtectingCover(settings, screen)"""
import pygame
from pygame.sprite import Sprite

class ProtectingCover(Sprite):
    """表示防护罩图像的类"""

    def __init__(self, settings, screen, ship):
        """初始化属性"""
        super(ProtectingCover, self).__init__()
        self.settings = settings
        self.screen = screen
        self.ship = ship

        self.image = pygame.image.load("images\\cover.bmp")
        self.image.set_colorkey((255, 255, 255))
        self.image = self.image.convert()
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = self.ship.rect.centerx
        self.rect.bottom = self.ship.rect.bottom

    def update(self):
        """更新防护罩位置"""
        self.rect.centerx = self.ship.rect.centerx
        self.rect.bottom = self.ship.rect.bottom    

    def blitme(self):
        """在指定位置画防护盾"""
        if self.settings.shield:
            self.screen.blit(self.image, self.rect)    