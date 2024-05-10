import pygame
import random
import time
from constants_for_floppy_bird import *
count = 0
score_count = 1


class Bird:
    def __init__(self, bird_screen: pygame.surface):
        self.screen = bird_screen
        self.life = 1
        self.x = 50
        self.y = 300
        self.r = 20
        self.vy = 5
        self.gravity = 0.45
        self.color = RED
        self.orig_image = pygame.image.load('download-removebg-preview.png').convert_alpha()
        self.image = pygame.transform.scale(self.orig_image, (70, 70))
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def move(self):
        self.y += self.vy
        if self.y != 0:
            self.vy += self.gravity
        if self.y + self.r > HEIGHT:
            self.vy = 0
            self.y = HEIGHT - self.r
        self.rect.center = (self.x, self.y)

    def draw(self):
        self.screen.blit(self.image, self.rect.topleft)

    def jump(self):
        self.vy = -8

    def fast_fall(self):
        self.vy = 8

    def hit_test(self, obj):
        global count
        if (obj.x <= self.x <= (obj.x + obj.width)) and ((obj.h - obj.d) >= self.y or self.y >= obj.h):
            return True
        elif (obj.x <= self.x <= (obj.x + obj.width)) and ((obj.h - obj.d) <= self.y <= obj.h):
            count += 1


class Column:
    def __init__(self, column_screen: pygame.surface, x):
        self.screen = column_screen
        self.h = random.randint(260, 550)
        self.d = random.randint(150, 250)
        self.width = 80
        self.x = x
        self.orig_column_up = pygame.image.load('column-removebg-preview1.png').convert_alpha()
        self.image = pygame.transform.scale(self.orig_column_up, (self.width, self.h-self.d))
        # self.rect = self.image.get_rect()
        self.orig_column_down = pygame.image.load('column-removebg-preview.png').convert_alpha()
        self.image2 = pygame.transform.scale(self.orig_column_down, (self.width, HEIGHT-self.h))

    def draw(self):
        # pygame.draw.rect(self.screen, GREY, (self.x, self.h, self.width, HEIGHT - self.h))
        screen.blit(self.image2, (self.x, self.h))
        # pygame.draw.rect(self.screen, GREY, (self.x, 0, self.width, self.h - self.d))
        screen.blit(self.image, (self.x, 0))

    def move(self):
        self.x -= 5


def reset_game():
    global count, score_count
    text_file = open('score.txt', 'a')
    text_file.write(f'On your try nr. {score_count}, you scored: {count//17}\n')
    text_file.close()
    count = 0
    score_count += 1
    main_game_loop()


def main_game_loop():
    finished = False
    bird = Bird(screen)
    columns = []
    a = 1
    column_timer = 0
    column_interval = 50
    font = pygame.font.Font('Minecraft.ttf', size=50)

    while not finished:
        bg_image_orig = pygame.image.load('bg.jpg').convert_alpha()
        bg_image = pygame.transform.scale(bg_image_orig, (WIDTH, HEIGHT))
        screen.blit(bg_image, (0, 0))
        text_surface = font.render(str(count//17), True, BLACK)
        screen.blit(text_surface, (10, 10))

        bird.move()
        bird.draw()
        for c in columns:
            c.draw()

        clock.tick(FPS)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                bird.jump()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                bird.fast_fall()

        for column in columns:
            column.move()
            if bird.hit_test(column):
                finished = True
                bg_image_orig = pygame.image.load('bgdark.png').convert_alpha()
                bg_image = pygame.transform.scale(bg_image_orig, (WIDTH, HEIGHT))
                screen.blit(bg_image, (0, 0))
                b_font = pygame.font.Font('Minecraft.ttf', size=100)
                lose_text = b_font.render('You lost!', True, CYAN)
                count_text = b_font.render(f'Your score: {count//17}', True, CYAN)
                screen.blit(lose_text, (190, 100))
                screen.blit(count_text, (60, 300))
                pygame.display.update()
                time.sleep(1.5)
                reset_game()

        column_timer += a
        a += 0.00005
        if column_timer >= column_interval:
            columns.append(Column(screen, WIDTH))
            column_timer = 0


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Floppy Bird')
    clock = pygame.time.Clock()
    main_game_loop()
    pygame.quit()
    print(count//17)

text = open('score.txt', 'a')
text.write('-----------------------------\n')
text.close()
