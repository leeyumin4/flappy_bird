import pygame
import random

pygame.init()

# Game window
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 500
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Flappy Bird')

# FPS
clock = pygame.time.Clock()
FPS = 60

# VARIABLES
YELLOW = (255,255,0)
SCROLL_THRESHOLD = SCREEN_WIDTH - 200
scroll = 0
bg_scroll = 0 # background scroll variable
ob_gap = 150 # gap between two obstacles
ob_frequency = 1500 # ms
last_ob = pygame.time.get_ticks() - ob_frequency

# Images
bg_image = pygame.image.load('flappy bird/Assets/Background/background.png').convert_alpha()
bg_image = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
mountain_image = pygame.image.load('flappy bird/Assets/Background/mountain.png').convert_alpha()
mountain_image = pygame.transform.scale(mountain_image, (SCREEN_WIDTH, SCREEN_HEIGHT // 3))
bird_image = pygame.image.load('flappy bird/Assets/Bird/icon-32.png').convert_alpha()
obstacle_image = pygame.image.load('flappy bird/Assets/Background/obstacle.png').convert_alpha()
obstacle_image = pygame.transform.scale(obstacle_image, (50, 300))
def draw_bg(bg_scroll):
    screen.blit(bg_image, (0 + bg_scroll, 0))
    screen.blit(bg_image, (SCREEN_WIDTH + bg_scroll, 0))
    screen.blit(mountain_image, (0 + bg_scroll, 350))
    screen.blit(mountain_image, (SCREEN_WIDTH + bg_scroll, 350))

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self.image = bird_image
        self.rect = self.image.get_rect(topleft = (0, SCREEN_HEIGHT // 2))
        self.rect.center = (x, y)
        self.gravity = 0

    def move(self):
        # movement variables
        scroll = 0
        dx = 3 # change of movement on x axis
        dy = 0 # change of movement on y axis

        key = pygame.key.get_pressed()
        if key[pygame.K_w]:
            self.gravity -= 2
        # if key[pygame.K_s]:
        #     dy = 5

        if self.rect.right <= SCROLL_THRESHOLD:
            scroll = -dx

        self.rect.x += dx + scroll
        self.rect.y += dy
        
        return scroll

    def draw(self):
        screen.blit(self.image, self.rect)

    def player_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        # if self.rect.y  SCREEN_HEIGHT:
        #     self.rect.y = SCREEN_HEIGHT

    def update(self):
        self.move()
        # self.player_gravity()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y,position):
        super().__init__()
        self.image = obstacle_image
        self.rect = self.image.get_rect()
        # position is to split the pipe from top and bottom, 1 = top -1 = bottom
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x , y - ob_gap // 2]
        if position == -1:
            self.rect.topleft = [x , y + ob_gap // 2]

    def update(self):
        self.rect.x -= 3
        if self.rect.right < 0:
            self.kill()



bird = Player(50,SCREEN_HEIGHT // 2)
obstacle = pygame.sprite.Group()



run = True
while run:
    
    clock.tick(FPS)
    screen.blit(mountain_image,(0,0))

    scroll = bird.move()

    # blit and scroll background
    bg_scroll += scroll
    if bg_scroll >= SCREEN_WIDTH:
        bg_scroll = 0
    draw_bg(bg_scroll)

    # sprites
    bird.draw()
    bird.update()
    obstacle.draw(screen)
    obstacle.update()

    # make new obstacles
    time = pygame.time.get_ticks()
    if time - last_ob > ob_frequency:
        ob_height = random.randint(-100 , 100)
        bottom_ob = Obstacle(SCREEN_WIDTH,SCREEN_HEIGHT // 2 + ob_height, -1)
        top_ob = Obstacle(SCREEN_WIDTH,SCREEN_HEIGHT // 2 + ob_height, 1)
        obstacle.add(bottom_ob)
        obstacle.add(top_ob)
        last_ob = time

    # Need to make collision

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()