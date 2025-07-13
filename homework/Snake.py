import pygame
import random
import time
import sys

# 初始化pygame
pygame.init()

# 游戏常量
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
SNAKE_SPEED = 10

# 颜色定义
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (100, 100, 100)

# 方向常量
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

class Snake:
    def __init__(self):
        # 初始化蛇身，初始长度为4节
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        for i in range(1, 4):
            self.positions.append((GRID_WIDTH // 2 - i, GRID_HEIGHT // 2))
        self.direction = RIGHT
        self.next_direction = RIGHT
        self.grow = False
        self.color_head = (0, 200, 0)  # 深绿色头部
        self.color_body = (0, 255, 0)  # 浅绿色身体
        
    def get_head_position(self):
        return self.positions[0]
    
    def update(self):
        # 更新蛇的位置
        if self.next_direction != self.get_opposite_direction(self.direction):
            self.direction = self.next_direction
        
        head_x, head_y = self.get_head_position()
        dir_x, dir_y = self.direction
        new_position = ((head_x + dir_x) % GRID_WIDTH, (head_y + dir_y) % GRID_HEIGHT)
        
        # 检查是否撞到自己
        if new_position in self.positions[1:]:
            return False  # 游戏结束
        
        self.positions.insert(0, new_position)
        if not self.grow:
            self.positions.pop()
        else:
            self.grow = False
        return True  # 游戏继续
    
    def get_opposite_direction(self, direction):
        # 获取相反方向，用于防止180度转向
        if direction == UP:
            return DOWN
        elif direction == DOWN:
            return UP
        elif direction == LEFT:
            return RIGHT
        else:
            return LEFT
    
    def render(self, surface):
        # 绘制蛇身
        for i, pos in enumerate(self.positions):
            rect = pygame.Rect(pos[0] * GRID_SIZE, pos[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            if i == 0:  # 头部使用不同颜色
                pygame.draw.rect(surface, self.color_head, rect)
                pygame.draw.rect(surface, WHITE, rect, 1)  # 白色边框
            else:
                pygame.draw.rect(surface, self.color_body, rect)
                pygame.draw.rect(surface, WHITE, rect, 1)  # 白色边框

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.color = RED
        self.randomize_position()
        
    def randomize_position(self):
        # 随机生成食物位置
        self.position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
        
    def render(self, surface):
        # 绘制食物
        rect = pygame.Rect(self.position[0] * GRID_SIZE, self.position[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(surface, self.color, rect)
        pygame.draw.rect(surface, WHITE, rect, 1)  # 白色边框

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('贪吃蛇')
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('arial', 30)
        self.snake = Snake()
        self.food = Food()
        self.score = 0
        self.game_over = False
        self.paused = False
        self.speed_increase = 0  # 速度增加量
        self.background = BLACK
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.paused = not self.paused
                elif not self.paused and not self.game_over:
                    if event.key == pygame.K_UP:
                        self.snake.next_direction = UP
                    elif event.key == pygame.K_DOWN:
                        self.snake.next_direction = DOWN
                    elif event.key == pygame.K_LEFT:
                        self.snake.next_direction = LEFT
                    elif event.key == pygame.K_RIGHT:
                        self.snake.next_direction = RIGHT
                elif self.game_over and event.key == pygame.K_r:
                    self.__init__()  # 重置游戏
    
    def update(self):
        if self.paused or self.game_over:
            return
            
        # 更新蛇的位置
        if not self.snake.update():
            self.game_over = True
            return
            
        # 检查是否吃到食物
        if self.snake.get_head_position() == self.food.position:
            self.snake.grow = True
            self.food.randomize_position()
            self.score += 1
            
            # 确保食物不会出现在蛇身上
            while self.food.position in self.snake.positions:
                self.food.randomize_position()
            
            # 每得5分增加速度
            if self.score % 5 == 0:
                self.speed_increase += 1
    
    def render(self):
        self.screen.fill(self.background)
        
        # 绘制网格线
        for x in range(0, SCREEN_WIDTH, GRID_SIZE):
            pygame.draw.line(self.screen, GRAY, (x, 0), (x, SCREEN_HEIGHT))
        for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
            pygame.draw.line(self.screen, GRAY, (0, y), (SCREEN_WIDTH, y))
        
        # 绘制蛇和食物
        self.snake.render(self.screen)
        self.food.render(self.screen)
        
        # 显示分数
        score_text = self.font.render(f'分数: {self.score}', True, WHITE)
        self.screen.blit(score_text, (10, 10))
        
        # 暂停提示
        if self.paused:
            pause_text = self.font.render('游戏暂停 - 按P继续', True, WHITE)
            text_rect = pause_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(pause_text, text_rect)
        
        # 游戏结束提示
        if self.game_over:
            game_over_text = self.font.render('游戏结束! 按R重新开始', True, WHITE)
            text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(game_over_text, text_rect)
        
        pygame.display.update()
    
    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(SNAKE_SPEED + self.speed_increase)

if __name__ == '__main__':
    game = Game()
    game.run()