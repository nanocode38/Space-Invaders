import os
import sys
from time import sleep
import threading
import random as rd

import pygame
from pygame.locals import *
import win32api  
import win32con
import win32

from bullet import Bullet
from alien import Alien
from meteorolite import Meteorolite
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from images_classes import ProtectingCover, GameOverStr

class SpaceInvaders(object):
    """管理资产和行为的游戏整体类"""
    def __init__(self):
        """初始化游戏,创建游戏资源"""
        os.system("cls")
        pygame.init()
        pygame.mixer.init()
        self.计时器 = pygame.time.Clock()
        self.settings = Settings()
        icon = pygame.image.load("images\\Logo.bmp")

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height - 60
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("太空入侵者")
        pygame.display.set_icon(icon)
        self.background = pygame.image.load('images\\sceen.bmp').convert()
        # 制作按钮.
        self.play_button = Button(self.settings, self.screen, 
            "Play", (0,0,255), 0, -30)
        self.help_button = Button(self.settings, self.screen, 
            "Help", (255,0,0), 0, 30)
        
        # 创建一个实例来存储游戏统计数据和记分牌.
        self.stats = GameStats(self.settings)
        self.sb = Scoreboard(self.settings, self.screen, self.stats)

        self.game_active = False
        
        # 制作一艘飞船船,一个子弹编组,一群外星人.  
        self.ship = Ship(self.settings, self.screen)
        self.cover = ProtectingCover(self.settings, 
            self.screen, self.ship)      
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.meteorolites = pygame.sprite.Group()
        self.gameover = GameOverStr(self.settings, self.screen, self.ship)
        
        # 创建的外星人
        self._create_fleet()
    def run_game(self):
        """开始游戏主循环"""
        while True:
            self.screen.blit(self.background, (0, 0))
            self._check_events()
            
            if self.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
                self._update_meteorolite()
                self._add_meteorolites()
                self._update_cover()
            
            self._update_screen(False)
            self.计时器.tick(130)


    def _exit(self):
        """退出游戏"""
        pygame.mouse.set_visible(True)
        sl = win32api.MessageBox(0, "确定退出游戏吗？", "退出确认", win32con.MB_OKCANCEL)
        if  sl == 1:
            with open("high_score.txt","w") as scf:
                scf.write(str(self.sb.high_score))
                sys.exit()
        else:
            pygame.mouse.set_visible(False)



    def _check_events(self):
        """响应按键和鼠标事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                self._check_play_button(mouse_x, mouse_y)
                self._check_help_button(mouse_x, mouse_y)        


    def _check_keydown_events(self, event):
        """响应按键"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == 27:#ESC
            self._exit()  
        elif event.key == 1073742048:#Ctrl
            self.settings.shield = True      
    
    def _check_keyup_events(self, event):
        """相应松开按键"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == 1073742048:#Ctrl
            self.settings.shield = False

    def _check_aliens_bottom(self):
        """检查是否有外星人到达屏幕底部。"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                return

    def _check_high_score(self):
        """检查有没有新的高分"""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.sb.prep_high_score()
                 
    def _check_bullet_alien_collisions(self):
        """对子弹-外星人碰撞做出反应"""
        # 移除所有碰撞过的子弹和外星人.
        color = "red"
        points = 0
        if len(self.sb.ships) == 0:
            collisions = pygame.sprite.groupcollide(self.bullets,
                self.aliens, False, True)
        else:
            collisions = pygame.sprite.groupcollide(self.bullets,
                self.aliens, True, True)
        
        if collisions:
            for aliens in collisions.values():
                for alien in aliens:
                    color = alien.color
                    if color == "blue":
                        points = self.settings.blue_alien_points
                    elif color == "purple":
                        points = self.settings.purple_alien_points
                    elif color == "orange":
                        points = self.settings.orange_alien_points
                    elif color == "red":
                        points = self.settings.red_alien_points              
                    self.stats.score += points
                self.sb.prep_score()
            self._check_high_score()
        
        if len(self.aliens) == 0:
            # 如果整个舰队被摧毁,开始一个新的关卡.
            self.bullets.empty()
            self.settings.increase_speed()
            
            # 提高水平.
            self.stats.level += 1
            self.sb.prep_level()
            
            self._create_fleet()
    def _check_fleet_edges(self):
        """如果有任何外星人到达边缘,应作相应"""
        for alien1 in self.aliens.sprites():
            if alien1.check_edges():
                self._change_fleet_direction()
                break          

    def _check_play_button(self, mouse_x, mouse_y):
        """当玩家点击Play按钮开始一个新的游戏"""
        button_clicked = self.play_button.rect.collidepoint(mouse_x, mouse_y)
        if button_clicked and not self.game_active:
            pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
            # 重置游戏设置.
            self.settings.initialize_dynamic_settings()
            
            # 隐藏光标.
            pygame.mouse.set_visible(False)
            
            # 重置游戏统计数据.
            self.stats.reset_stats()
            self.game_active = True
            
            # 重置记分板图片.
            self.sb.prep_score()
            self.sb.prep_high_score()
            self.sb.prep_level()
            self.sb.prep_ships()
            
            # 清空外星人、子弹和陨石的列表.
            self.aliens.empty()
            self.bullets.empty()
            self.meteorolites.empty()
            
            #创建一个新的.
            self._create_fleet()
            self.ship.center_ship()

    def _check_help_button(self, mouse_x, mouse_y):
        """游戏帮助按钮响应"""
        button_clicked = self.help_button.rect.collidepoint(mouse_x, mouse_y)
        if button_clicked and not self.game_active:
            help_text =  "太空入侵者玩法说明：\n"
            help_text += "1.游戏目标: 躲避或防御陨石," \
                         "在外星人达到屏幕低端或撞上飞船之前杀掉所以外星人\n"
            help_text += "2.操作方法: 按左右方向键控制飞船移动,按空格键发射子弹," \
                         "按下Ctrl键防御,"
            help_text += "松开Ctrl键停止防御\n"
            help_text += "3.游戏细节: 防御状态无法发射子弹," \
                         "红色外星人点数最多,其次橙色外星人"
            help_text += ",再次紫色外星人,最后蓝色外星人\n"
            sl = win32api.MessageBox(0, help_text, "太空入侵者--help", 
                win32con.MB_OK)
         
            
    def _fire_bullet(self):
        """如果没有达到子弹发射极限,发射一颗子弹"""
        # 创建一个新的子弹,并添加到子弹群.
        if not self.settings.shield:
            if len(self.bullets) < self.settings.bullets_allowed:
                new_bullet = Bullet(self.settings, self.screen, self.ship)
                self.bullets.add(new_bullet)
                self.settings.bulletsound.play()


    def _draw_button(self):
        """画出两个按钮"""
        self.help_button.draw_button()
        self.play_button.draw_button()
    def _update_screen(self, gameoveris):
        """在屏幕上更新图像,绘制到新屏幕"""
        # 通过循环每个重绘屏幕
        
        # 重画所有的子弹,飞船和外星人.
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        for meteorolite in self.meteorolites.sprites():
            meteorolite.blitme()    
        self.ship.blitme()
        self.aliens.draw(self.screen)
        
        # 绘制得分信息
        self.sb.show_score()
        self.gameover.draw()
        
        # 如果游戏处于非活动状态,则绘制Play按钮.
        if not self.game_active and not gameoveris:
            self.help_button.draw_button()
            self.play_button.draw_button()
        # 使最近绘制的屏幕可见.
        pygame.display.flip()
    def _update_bullets(self):
        """更新子弹位置,清除旧子弹"""
        # 更新子弹位置
        self.bullets.update()

        # 处理掉已经消失的子弹
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
                
        self._check_bullet_alien_collisions()

    def _add_a_meteorolite(self):
        """添加一个陨石"""
        if len(self.meteorolites) < self.settings.meteorolite_allowed:
            new_meteorolite = Meteorolite(self.settings, self.screen)
            self.meteorolites.add(new_meteorolite)

    def _add_meteorolites(self):
        """添加所有陨石"""
        s = threading.Timer(rd.randint(1,6), 
            self._add_a_meteorolite)
        s.start()    

    def _update_meteorolite(self):
        """更新陨石位置"""
        for meteorolite in self.meteorolites.sprites():
                meteorolite.update()
                meteorolite.blitme()

        for meteorolite in self.meteorolites.copy().sprites():
            if meteorolite.rect.top >= self.settings.screen_height:
                self.meteorolites.remove(meteorolite)
            if pygame.sprite.spritecollideany(self.ship, self.meteorolites):
                if not self.settings.shield:
                    self._ship_hit()
                else:
                    self.meteorolites.remove(meteorolite)

        
    def _change_fleet_direction(self):
        """检查是否碰到屏幕边缘,并改变外星人队的方向"""
        for alien1 in self.aliens.sprites():
            alien1.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _ship_hit(self):
        """飞船坠毁时做出响应"""
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            sleep(0.2)
            self.settings.shiphitsound.play()
            sleep(4)
            # 更新记分板
            self.sb.prep_ships()
            
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)
            sleep(0.5)
            self.settings.gameoversound1.play()
            self.settings.gameoversound2.play()
            self.gameover.show()
            self._update_screen(True)
            sleep(2)
            self.gameover.hidden()

        self.aliens.empty()
        self.bullets.empty()
        self.meteorolites.empty()
        
        # 创建一个新的舰队，并局中飞船。
        self._create_fleet()
        self.ship.center_ship()
        
        # 暂停.
        sleep(0.8)



    def _update_aliens(self):
        """
        检查舰队是否在边缘，
        然后更新舰队中所有外星人的位置。
        """
        self._check_fleet_edges()
        for alien1 in self.aliens.sprites():
            alien1.update()
        
        # 外星人与飞船的碰撞。
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # 撞击屏幕底部的外星人。
        self._check_aliens_bottom()
                
    def _get_number_aliens_x(self, alien_width):
        """确定能排成一行的外星人的数量。"""
        available_space_x = self.settings.screen_width - 2 * alien_width
        number_aliens_x = int(available_space_x / (2 * alien_width))
        return number_aliens_x
        
    def _get_number_rows(self, ship_height, alien_height):
        """确定能在屏幕上显示的外星人的行数。"""
        available_space_y = (self.settings.screen_height -
                                (3 * alien_height) - ship_height)
        number_rows = int(available_space_y / (2 * alien_height))
        return number_rows
        
    def _create_alien(self, alien_number, row_number):
        """创造一个外星人，并把它放在这一行"""
        alien = Alien(self.settings, self.screen)
        alien_width = alien.rect.width
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _create_fleet(self):
        """创建一个完整的外星人."""
        # 创建一个外星人,发现外星人在一行的数量.
        alien = Alien(self.settings, self.screen)
        number_aliens_x = self._get_number_aliens_x(alien.rect.width)
        number_rows = self._get_number_rows(self.ship.rect.height, alien.rect.height)
        
        # 建造外星人舰队。
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)
        self._add_meteorolites()

    def _update_cover(self):
        """更新防御盾图像"""
        self.cover.update()
        self.cover.blitme()

if __name__ == '__main__':
    # 创建一个游戏实例，并运行游戏.
    si = SpaceInvaders()
    si.run_game()