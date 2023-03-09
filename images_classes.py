"""含有纯粹图像及显示的类的模块"""
import pygame


class ProtectingCover:
    """表示防护罩图像的类"""

    def __init__(self, settings, screen, ship):
        """初始化属性"""
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


class GameOverStr:
    def __init__(self, settings, screen, ship):
        """初始化基础数据"""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.settings = settings
        self.ship = ship

        self.color = (250, 10, 20)
        self.font = pygame.font.SysFont(None, 120)
        self.is_hidden = True

        self.image = self.font.render("Game Over!",
            True, self.color)
        self.rect = self.image.get_rect()
        self.rect.center = self.screen_rect.center
        self.rect.x += 10

    def draw(self):
        """画出Game Over"""
        if self.is_hidden == False:
            self.screen.blit(self.image, self.rect)

    def show(self):
        """显示Game Over"""
        self.is_hidden = False
        return

    def hidden(self):
        """隐藏GameOver"""
        self.is_hidden = True
        return
