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
ob_gap = 150 # gap between two obstacles
ob_frequency = 1500 # ms
last_ob = pygame.time.get_ticks() - ob_frequency
flying = False
game_over = False

# Images
bg_image = pygame.image.load('flappy bird/Assets/Background/background.png').convert_alpha()
bg_image = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
mountain_image = pygame.image.load('flappy bird/Assets/Background/mountain.png').convert_alpha()
mountain_image = pygame.transform.scale(mountain_image, (SCREEN_WIDTH, SCREEN_HEIGHT // 3))
bird_image = pygame.image.load('flappy bird/Assets/Bird/icon-32.png').convert_alpha()
obstacle_image = pygame.image.load('flappy bird/Assets/Background/obstacle.png').convert_alpha()
obstacle_image = pygame.transform.scale(obstacle_image, (50, 300))

bg1 = 0
bg2 = SCREEN_WIDTH

def draw():
    screen.blit(bg_image, (bg1, 0))
    screen.blit(bg_image, (bg2, 0))
    screen.blit(mountain_image, (bg1, 350))
    screen.blit(mountain_image, (bg2, 350))


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self.image = bird_image
        self.rect = self.image.get_rect(topleft = (0, SCREEN_HEIGHT // 2))
        self.rect.center = (x, y)
        self.gravity = 0
        self.pressed = False
        

    def move(self):

        key = pygame.key.get_pressed()
        if key[pygame.K_w] == 1 and self.pressed == False:
            self.pressed = True
            self.gravity -= 13
        if key[pygame.K_w] == 0:
            self.pressed = False
        

    def player_gravity(self):
        self.gravity += 0.4
        if self.gravity > 8:
            self.gravity = 8
        if self.gravity < -15:
            self.gravity = -8
        if self.rect.bottom < 500:
            self.rect.y += self.gravity
        # if self.rect.top < 0:
        #     self.rect.y -= self.gravity

        

        print(self.gravity)


    def draw(self):
        screen.blit(self.image, self.rect)
        self.rect.x += 0.9

    


    def update(self):
        self.move()
        if flying == True:
            self.player_gravity()

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
obstacle_group = pygame.sprite.Group()
bird_group = pygame.sprite.Group()




run = True
while run:
    
    clock.tick(FPS)

    draw()

    # sprites
    bird.draw()
    bird.update()
    if flying == True and game_over == False:
        obstacle_group.draw(screen)
        obstacle_group.update()
        # moved background scrolling, so that when bird dies, the background and obstascle stops running.
        bg1 -= 2
        bg2 -= 2
        if bg1 < bg_image.get_width() * -1:
            bg1 = bg_image.get_width()
        if bg2 < bg_image.get_width() * -1:
            bg2 = bg_image.get_width()

        # make new obstacles
        
        time = pygame.time.get_ticks()
        if time - last_ob > ob_frequency:
            ob_height = random.randint(-100 , 100)
            bottom_ob = Obstacle(SCREEN_WIDTH,SCREEN_HEIGHT // 2 + ob_height, -1)
            top_ob = Obstacle(SCREEN_WIDTH,SCREEN_HEIGHT // 2 + ob_height, 1)
            obstacle_group.add(bottom_ob)
            obstacle_group.add(top_ob)
            last_ob = time


    # check if bird hits the ground or ceiling
    if bird.rect.bottom > 500 or bird.rect.top < 0:
        game_over = True
        flying = False

    # Need to make collision

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN and flying == False and game_over == False:
            flying = True


    pygame.display.update()

pygame.quit()