#! /usr/bin/env python
import pygame
from random import uniform

black = 0, 0, 0
white = 255, 255, 255
green = 0, 80, 0

game_end = False
screen_size = 800, 600
game_screen = pygame.display.set_mode(screen_size)
game_rect_screen = game_screen.get_rect()
game_time = pygame.time.Clock()
pygame.display.set_caption('Pong')

pygame.mixer.init()
racket_tap_sound = pygame.mixer.Sound('./sounds/bounce.wav')
bounce_wall_sound = pygame.mixer.Sound('./sounds/tap1.wav')
lose_point_sound = pygame.mixer.Sound('./sounds/losepoint.wav')


class Racket:
    def __init__(self, size):
        self.image = pygame.Surface(size)
        self.image.fill(green)
        self.image_rect = self.image.get_rect()
        self.speed = 15
        self.image_rect[0] = 12

    def move(self, x, y):
        self.image_rect[0] += x * self.speed
        self.image_rect[1] += y * self.speed

    def refresh(self, key_pressed):
        if key_pressed[pygame.K_UP]:
            self.move(0, -1)
        if key_pressed[pygame.K_DOWN]:
            self.move(0, 1)
        self.image_rect.clamp_ip(game_rect_screen)

    def realize(self):
        game_screen.blit(self.image, self.image_rect)


class Ball:
    def __init__(self, size):
        self.height, self.width = size
        self.image = pygame.Surface(size)
        self.image.fill(white)
        self.image_rect = self.image.get_rect()
        self.speed = 15
        self.set_ball()

    def random_number(self):
        while True:
            num = uniform(-1.0, 1.0)
            if num > -.5 and num < .5:
                continue
            else:
                return num

    def set_ball(self):
        x = self.random_number()
        y = self.random_number()
        self.image_rect.x = game_rect_screen.centerx
        self.image_rect.y = game_rect_screen.centery
        self.spd = [x, y]
        self.position = list(game_rect_screen.center)

    def wall_bounce(self):
        if self.image_rect.y < 0 or self.image_rect.y > game_rect_screen.bottom - self.height:
            self.spd[1] *= -1
            bounce_wall_sound.play()

        if self.image_rect.x < 0 or self.image_rect.x > game_rect_screen.right - self.width:
            self.spd[0] *= -1
            if self.image_rect.x < 0:
                scoreboard1.points -= 1
                lose_point_sound.play()
                self.speed -= 3
            if self.image_rect.x > game_rect_screen.right - self.width:
                bounce_wall_sound.play()

    def racket_bounce(self, racket):
        if self.image_rect.colliderect(racket):
            self.spd[0] *= -1
            scoreboard1.points += 1
            self.speed += 3
            racket_tap_sound.play()

    def move(self):
        self.position[0] += self.spd[0] * self.speed
        self.position[1] += self.spd[1] * self.speed
        self.image_rect.center = self.position

    def refresh(self, racket):
        self.wall_bounce()
        self.racket_bounce(racket)
        self.move()

    def realize(self):
        game_screen.blit(self.image, self.image_rect)


class Scoreboard:
    def __init__(self):
        pygame.font.init()
        self.header = pygame.font.Font(None, 36)
        self.points = 5

    def counting(self):
        self.text = self.header.render("Points - " + str(self.points), 1, (255, 255, 255))
        self.text_position = self.text.get_rect()
        self.text_position.centerx = game_screen.get_width() / 2
        game_screen.blit(self.text, self.text_position)
        game_screen.blit(game_screen, (0, 0))


racket = Racket((15, 100))
ball = Ball((15, 15))
scoreboard1 = Scoreboard()

while not game_end:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_end = True
    key_press = pygame.key.get_pressed()
    game_screen.fill(black)
    racket.realize()
    racket.refresh(key_press)
    ball.realize()
    ball.refresh(racket.image_rect)
    game_time.tick(60)
    scoreboard1.counting()
    pygame.display.update()
    if scoreboard1.points == 0:
        print('You Lose!')
        print('Game Over!')
        game_end = True
    elif scoreboard1.points == 10:
        print('You Win!')
        print('Game Over!')
        game_end = True
