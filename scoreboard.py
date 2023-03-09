"""关于记分牌的类"""
import pygame.font
from pygame.sprite import Group

from ship import Ship

class Scoreboard():
    """显示得分信息的类。"""

    def __init__(self, settings, screen, stats):
        """初始化记分属性。"""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.settings = settings
        self.stats = stats
        
        # 得分信息的字体设置。
        self.text_color = (250, 250, 250)
        self.font = pygame.font.SysFont(None, 48)

        # 准备初始得分图像。
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_score(self):
        """将分数转换为渲染图像。"""
        rounded_score = int(round(self.stats.score, -1))
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render("Score:" + score_str, True,
                self.text_color)
            
        # 在屏幕的右上方显示分数。
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20
        
    def prep_high_score(self):
        """将高分转换为渲染图像。"""
        high_score = int(round(self.stats.high_score, -1))
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render("High Score:" + high_score_str, True, self.text_color)
                
        # 在屏幕上方居中显示最高分。
        self.high_score = high_score
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top
    
    def prep_level(self):
        """将等级转换为渲染图像。"""
        self.level_image = self.font.render("Level:"+str(self.stats.level), True, self.text_color)   
        
        # 将等级置于分数下方。
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10
        
    def prep_ships(self):
        """显示还有多少艘飞船。"""
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.settings, self.screen)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)
        
    def show_score(self):
        """在屏幕上绘制分数。"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)
