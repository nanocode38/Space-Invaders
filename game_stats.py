"""管理游戏统计信息的模块"""
class GameStats():
    """跟踪游戏的统计数据。"""
    
    def __init__(self, settings):
        """初始化数据。"""
        self.settings = settings
        self.reset_stats()
        is_FileNotFoundError = False
        
        # 读取最高分数
        with open("high_score.txt") as scf:
            try:
                self.high_score = int(scf.read())
            except ValueError:
                self.high_score = 0
            except FileNotFoundError:
                is_FileNotFoundError = True

        with open("high_score.txt","w") as scf:
            scf.write(str(0))
            self.high_score = 0
        
    def reset_stats(self):
        """初始化在游戏过程中可能改变的统计数据。"""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1
