""""含有游戏设置类的模块"""
import pygame
class Settings:
    """存储游戏所有设置的类。"""
    
    def __init__(self):
        """初始化游戏设置"""
        # 场景设置。
        self.screen_width = 1290
        self.sceen_height = 660

        # 飞船设置。
        self.ship_speed_factor = 1.5
        self.ship_limit = 0

        # 子弹设置。
        self.bullet_speed_factor = 5
        self.bullet_width = 2
        self.bullet_height = 15   
        self.bullet_color = (200, 255, 200)
        self.bullets_allowed = 10
        self.shield = False

        # 外星人设置。
        self.alien_speed_factor = 1
        self.fleet_drop_speed = 10

        # 陨石设置
        self.meteorolite_allowed = 3
        self.meteorolite_speed = 2

        # 声音设置
        self.gameoversound1 = pygame.mixer.Sound("sounds\\GameOver1.wav")
        self.gameoversound2 = pygame.mixer.Sound("sounds\\gameover2.wav")
        self.shiphitsound = pygame.mixer.Sound("sounds\\crash.wav")
        self.bulletsound = pygame.mixer.Sound("sounds\\bullet.wav")   
        
        # 游戏速度设置
        # 游戏速度增加速度
        self.speedup_scale = 1.1
        # 游戏点值增加速度。
        self.score_scale = 1.5
     
    
        self.initialize_dynamic_settings()
  
    def initialize_dynamic_settings(self):
        """初始化在游戏中不断变化的设置。"""
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 4
        self.alien_speed_factor = 1
        
        # 外星人得分
        self.blue_alien_points = 10
        self.purple_alien_points = 20
        self.orange_alien_points = 30
        self.red_alien_points = 40
    
        # fleet_direction为1表示右，为-1表示左。
        self.fleet_direction = 1
        self.vieit_time = 0

    def increase_speed(self):
        """增加速度设置和点值。"""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale

        self.red_alien_points = int(self.red_alien_points * self.score_scale)
        self.blue_alien_points = int(self.blue_alien_points 
            * self.score_scale)
        self.orange_alien_points = int(self.orange_alien_points 
            * self.score_scale)
        self.purple_alien_points = int(self.purple_alien_points
            * self.score_scale)
