"""管理按钮模块"""
import pygame.font

class Button():
    """创建单个按钮"""
    def __init__(self, settings, screen, msg, button_color, x, y):
        """初始化按钮属性。"""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        
        # 设置按钮的尺寸和属性。
        self.width, self.height = 200, 50
        self.button_color = button_color
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)
        
        # 创建按钮的rect对象，并居中按钮。
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center
        self.rect.x += x
        self.rect.y += y        
        # 按钮消息只需要准备一次。
        self.prep_msg(msg)

    def prep_msg(self, msg):
        """将msg转换为渲染的图像，并在按钮上居中显示文本"""
        self.msg_image = self.font.render(msg, True, self.text_color,
            self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center
        
    def draw_button(self):
        """绘制空白按钮，然后绘制消息。"""
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
