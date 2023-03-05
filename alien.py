"""外星人模块"""
import pygame
import random as rd
from pygame.sprite import Sprite

class Alien(Sprite):
    """代表单个外星人的类。"""

    def __init__(self, settings, screen):
        """初始化外星人,并设置其起始位置。"""
        Sprite.__init__(self)
        super(Alien, self).__init__()
        self.screen = screen
        self.settings = settings
        self.color = "blue"

        # 加载外星人图像，并设置其rect属性。
        rand = rd.randint(1,10)
        if rand >= 1 and rand <= 4:
            self.image = pygame.image.load('images\\alien1.bmp')
        elif rand >= 5 and rand <= 7:
            self.image = pygame.image.load('images\\alien3.bmp')
            self.color = "purple"
        elif rand == 8 or rand == 9:
            self.image = pygame.image.load('images\\alien2.bmp')
            self.color = "orange"  
        elif rand == 10:
            self.color = "red"
            self.image = pygame.image.load('images\\alien.bmp')    
        self.image.set_colorkey((230, 230, 230))#RGB(230,230,230)
        self.image = self.image.convert()
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()

        # 在屏幕左上角附近启动每个新外星人。
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        

        # 储存外星人的确切位置。
        self.x = float(self.rect.x)
        
    def check_edges(self):
        """如果外星人位于屏幕边缘则返回true。"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True
        
    def update(self):
        """向右或向左移动外星人。"""
        self.x += (self.settings.alien_speed_factor *
                        self.settings.fleet_direction)
        self.rect.x = self.x

    def blitme(self):
        """把外星人画在它的位置。"""
        self.screen.blit(self.image, self.rect)

if __name__ == '__main__':
    # 创建一个游戏实例，并运行游戏.
    si = SpaceInvaders()
    si.run_game()