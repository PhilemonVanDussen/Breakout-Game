import pygame
import random


# SCREEN
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TITLE = 'Breakout'
FPS = 30

# COLORS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)


# FONT
FONT = 'arial'
FONT_SIZE_SCORE = 36
FONT_SIZE_START = 36
FONT_SIZE_INSTRUCTIONS = 24
FONT_SIZE_GAMEOVER_TITLE = 48
FONT_SIZE_GAMEOVER_SCORE = 36
FONT_SIZE_GAMEOVER_RESTART = 26

# PLAYER
PLAYER_WIDTH = 90
PLAYER_HEIGHT = 20
PLAYER_START_X = SCREEN_WIDTH //2
PLAYER_START_Y = SCREEN_HEIGHT - 40
PLAYER_MOVEMENT_SPEED = 30

# BALL 
BALL_RADIUS = 10
BALL_DIAMETER = BALL_RADIUS*2
BALL_START_X = SCREEN_HEIGHT //2
BALL_START_Y = SCREEN_HEIGHT //2
BALL_INITIAL_X_SPEED = 8
BALL_INITIAL_Y_SPEED = 12

# BRICK
BRICK_WIDTH = 100
BRICK_HEIGHT = 30
BRICK_HORIZONTAL_PADDING = 50
BRICK_VERTICAL_PADDING = 20
BRICK_ROWS = 6
BRICK_COLUMNS = 8


class Player(pygame.sprite.Sprite):
    

    def __init__(self, color):
        super().__init__()
        self.color = color
        self.image = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
        self.image.fill(color)
        self.rect = self.image.get_rect()

        # Position
        self.x = PLAYER_START_X
        self.y = PLAYER_START_Y
        self.rect.center = (self.x, self.y)

    def update(self):


        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] and self.x <= SCREEN_WIDTH - PLAYER_WIDTH // 2 and self.y > SCREEN_HEIGHT - 100:
            self.x += PLAYER_MOVEMENT_SPEED
        if keys[pygame.K_LEFT] and self.x >= PLAYER_WIDTH // 2 and self.y > SCREEN_HEIGHT - 100:
            self.x -= PLAYER_MOVEMENT_SPEED
        
        self.rect.center = (self.x, self.y)


class Ball(pygame.sprite.Sprite):


    def __init__(self):
        super().__init__()
        ball_image = pygame.Surface((BALL_DIAMETER, BALL_DIAMETER))
        pygame.draw.circle(ball_image, ball_color, (BALL_RADIUS, BALL_RADIUS), BALL_RADIUS)

        self.image = ball_image
        self.rect = self.image.get_rect()

        # Position
        self.x = BALL_START_X
        self.y = BALL_START_Y
        self.x_vel = BALL_INITIAL_X_SPEED
        self.y_vel = BALL_INITIAL_Y_SPEED
        self.rect.center = (self.x, self.y)

    def update(self):

        self.x += self.x_vel
        self.y += self.y_vel

        if self.x <= BALL_RADIUS or self.x > SCREEN_WIDTH - BALL_RADIUS:
            self.x_vel *= -1 # reverse horizontal direction

        if self.y <= BALL_RADIUS:
            self.y_vel *= -1 #Reverse vertical direction
        
        self.rect.center = (self.x, self.y)


class Brick(pygame.sprite.Sprite):


    def __init__(self, x, y, color):
        super().__init__()
        self.image = pygame.Surface((BRICK_WIDTH, BRICK_HEIGHT))
        self.image.fill(ball_color)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)


class Game:


    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.font_name = pygame.font.match_font(FONT)

    def new(self):
        # new game set up

        self.all_sprites = pygame.sprite.Group()
        self.players = pygame.sprite.Group()
        self.bricks = pygame.sprite.Group()
        self.score = 0

        self.ball = Ball()
        self.player = Player(WHITE)
        self.all_sprites.add(self.ball)
        self.all_sprites.add(self.player)
        self.players.add(self.player)

        # creat bricks
        for col in range(BRICK_COLUMNS):
            for row in range(BRICK_ROWS):
                brick_x = BRICK_HORIZONTAL_PADDING + col * (BRICK_WIDTH + BRICK_HORIZONTAL_PADDING)
                brick_y = BRICK_VERTICAL_PADDING + row * (BRICK_HEIGHT + BRICK_VERTICAL_PADDING)
                brick = Brick(brick_x, brick_y, BLUE)
                self.all_sprites.add(brick)
                self.bricks.add(brick)
        

        self.main()
    
    def main(self):


        self.playing = True
        while self.playing:
            
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
    
    def events(self):


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

    def update(self):


        self.all_sprites.update()

        # Paddle check collision
        hit_paddle = pygame.sprite.spritecollide(self.ball, self.players, False)
        if hit_paddle and self.ball.y_vel > 0:
            self.ball.y = self.player.rect.top - BALL_RADIUS # prevents ball from going into paddle
            self.ball.y_vel *= -1
        
        # Brick check collision
        hit_brick = pygame.sprite.spritecollide(self.ball, self.bricks, True)
        if hit_brick:
            self.ball.y_vel *= -1
            self.score += len(hit_brick) # Increase score by the number of bricks hit

        # Game over coditions
        if self.ball.rect.top > SCREEN_HEIGHT: # Ball went off the bottom of the screen
            self.playing = False
        if not self.bricks: # No more bricks left
                self.playing = False
        
    def draw(self):


        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen) # draw all sprites
        self.draw_text(f'Score: {self.score}', FONT_SIZE_SCORE, RED, SCREEN_WIDTH * 3/4, SCREEN_HEIGHT - 50) # display score

        pygame.display.flip()

    def show_start_screen(self):


        self.screen.fill(BLACK)
        self.draw_text('Breakout Game!', FONT_SIZE_START, RED, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)
        self.draw_text('Press any key to begin...',FONT_SIZE_INSTRUCTIONS, WHITE, SCREEN_WIDTH /2, SCREEN_HEIGHT /2)
        pygame.display.flip()
        self.wait_for_key()

    def show_game_over_screen(self):


        if not self.running:
            return
        self.screen.fill(BLACK)
        self.draw_text('GAME OVER', FONT_SIZE_GAMEOVER_TITLE, RED, SCREEN_WIDTH /2, SCREEN_HEIGHT /4)
        self.draw_text(f'Score: {self.score}', FONT_SIZE_INSTRUCTIONS, WHITE, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.draw_text('Press any key to play again...', FONT_SIZE_GAMEOVER_RESTART, WHITE, SCREEN_WIDTH / 2, SCREEN_HEIGHT * 3/4)
        pygame.display.flip()
        self.wait_for_key()

    def wait_for_key(self):


        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pygame.KEYUP:
                    waiting = False

    def draw_text(self, text, size, color, x, y):


        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)



game = Game()  
game.show_start_screen()

while game.running:
    ball_color = (random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255))
    game.new()
    game.show_game_over_screen()

pygame.quit()





