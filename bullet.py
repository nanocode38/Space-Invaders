"""管理飞船子弹的模块"""
import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """管理飞船子弹的一个类"""

    def __init__(self, settings, screen, ship):
        """在船的当前位置,创建一个子弹对象"""
        super(Bullet, self).__init__()
        self.screen = screen

        # 先在(0,0)创建子弹矩形,然后设置正确的位置
        self.rect = pygame.Rect(0, 0, settings.bullet_width,
            settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top
        
        # 存储一个小数值子弹的位置
        self.y = float(self.rect.y)

        self.color = settings.bullet_color
        self.speed_factor = settings.bullet_speed_factor

    def update(self):
        """更新子弹在屏幕上的移动"""
        # 子弹的小数点位置更新
        self.y -= self.speed_factor
        # 矩形的位置更新
        self.rect.y = self.y

    def draw_bullet(self):
        """在屏幕上绘制子弹"""
        pygame.draw.rect(self.screen, self.color, self.rect)
