import pygame
import random

RUNNING = [pygame.image.load('./assets/Dino/DinoRun1.png'),
           pygame.image.load('./assets/Dino/DinoRun2.png')]

JUMPING = pygame.image.load('./assets/Dino/DinoJump.png')

WIDTH = 1100
JUMP_VEL = 8.5
X_POS = 80
Y_POS = 310 

class Obstacle:
    def __init__(self, image, n_cacti):
        self.image = image
        self.type = n_cacti
        self.rect = self.image[self.type].get_rect()
        self.rect.x = WIDTH

    def update(self, game_speed, obstacles):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()

    def draw(self, screen):
        screen.blit(self.image[self.type], self.rect)

class SmallCactus(Obstacle):
    def __init__(self, image, n_cacti):
        super().__init__(image, n_cacti)
        self.rect.y = 325

class LargeCactus(Obstacle):
    def __init__(self, image, n_cacti):
        super().__init__(image, n_cacti)
        self.rect.y = 300

class Dinosaur:
    X_POS = 80
    Y_POS = 310

    def __init__(self, img=RUNNING[0]):
        self.image = img
        self.dino_run = True
        self.dino_jump = False
        self.jump_vel = JUMP_VEL
        self.rect = pygame.Rect(X_POS, Y_POS, img.get_width(), img.get_height())
        self.step_index = 0
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    def update(self):
        if self.dino_run:
            self.run()
        if self.dino_jump:
            self.jump()
        if self.step_index >= 10:
            self.step_index = 0

    def jump(self):
        if self.dino_jump:
            self.image = JUMPING
            self.rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8

        if self.jump_vel < -JUMP_VEL:
            self.dino_jump = False
            self.dino_run = True
            self.jump_vel = JUMP_VEL
            self.rect.y = Y_POS

    def run(self):
        self.image = RUNNING[self.step_index // 5]
        self.rect.x = X_POS
        self.rect.y = Y_POS
        self.step_index += 1

    def draw(self, screen, obstacles):
        screen.blit(self.image, (self.rect.x, self.rect.y))
        pygame.draw.rect(screen, self.color, (self.rect.x, self.rect.y, self.rect.width, self.rect.height), 2)

        for obstacle in obstacles:
            pygame.draw.line(screen, self.color, self.rect.center, obstacle.rect.center, 2)
