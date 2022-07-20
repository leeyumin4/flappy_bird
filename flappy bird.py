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

# Images
bg_image = pygame.image.load('flappy bird/Assets/Background/background.png').convert_alpha()
bg_image = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
mountain_image = pygame.image.load('flappy bird/Assets/Background/mountain.png').convert_alpha()
mountain_image = pygame.transform.scale(mountain_image, (SCREEN_WIDTH, SCREEN_HEIGHT // 3))
bird_image = pygame.image.load('flappy bird/Assets/Bird/icon-32.png').convert_alpha()

def draw_bg(bg_scroll):
    screen.blit(bg_image, (0 + bg_scroll, 0))
    screen.blit(bg_image, (SCREEN_WIDTH + bg_scroll, 0))
    screen.blit(mountain_image, (0 + bg_scroll, 350))
    screen.blit(mountain_image, (SCREEN_WIDTH + bg_scroll, 350))

class Player():
    def __init__(self, x, y):
        self.image = bird_image
        self.rect = self.image.get_rect(topleft = (0, SCREEN_HEIGHT // 2))
        self.rect.center = (x, y)

    def move(self):
        # movement variables
        scroll = 0
        dx = 3 # change of movement on x axis
        dy = 0 # change of movement on y axis

        key = pygame.key.get_pressed()
        if key[pygame.K_w]:
            dy = -5
        if key[pygame.K_s]:
            dy = 5

        if self.rect.right <= SCROLL_THRESHOLD:
            scroll = -dx

        self.rect.x += dx + scroll
        self.rect.y += dy
        
        return scroll

    def draw(self):
        screen.blit(self.image, self.rect)


bird = Player(50,SCREEN_HEIGHT // 2)

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

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()