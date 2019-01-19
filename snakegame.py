import pygame
import sys
import time
import random

from pygame.locals import *


# Define Size
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
GRID_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH / GRID_SIZE
GRID_HEIGHT = WINDOW_HEIGHT / GRID_SIZE

# Define Color
WHITE = (255, 255, 255)
GREEN = (0, 100, 0)
RED = (255, 0, 0)
GRAY = (100, 100, 100)
ORANGE = (255, 165, 0)

# Define Direction
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Frame Per Sec
FPS = 10

# Snake
class Python(object):
    def __init__(self):
        self.create()
        self.color = GREEN

    def create(self):
        self.length = 2
        self.positions = [((WINDOW_WIDTH / 2), (WINDOW_HEIGHT / 2))]
        self.Direction = random.choice([UP, DOWN, LEFT, RIGHT])

    def move(self):
        cur = self.positions[0]
        x, y = self.Direction
        new = (((cur[0] + (x * GRID_SIZE)) % WINDOW_WIDTH), (cur[1] + (y * GRID_SIZE)) % WINDOW_HEIGHT)
        if new in self.positions[2:]:
            self.create()
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()
    
    def eat(self):
        self.length += 1

    def draw(self, surface):
        for p in self.positions:
            draw_object(surface, self.color, p)

# Feed
class Feed(object):
    def __init__(self):
        self.position = (0, 0)
        self.color = ORANGE
        self.create()

    def create(self):
        self.position = (random.randint(0, GRID_WIDTH - 1) * GRID_SIZE, random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE)

    def draw(self, surface):
        #draw_object(surface, self.color, self.position)
        display_image(surface, self.position)




def draw_object(surface, color, pos):
    r = pygame.Rect((pos[0], pos[1]), (GRID_SIZE, GRID_SIZE))
    pygame.draw.rect(surface, color, r)

def display_image(surface, pos):
    apple = pygame.image.load('apple.png')
    apple = pygame.transform.scale(apple, (GRID_SIZE, GRID_SIZE))
    surface.blit(apple, pos)


def check_eat(python, feed):
    if python.positions[0] == feed.position:
        python.eat()
        feed.create()

def show_info(length, speed, surface):
    font = pygame.font.Font(None, 34)
    text = font.render("Length: " + str(length) + "    Speed: " + str(round(speed, 2)), 1, GRAY)
    pos = text.get_rect()
    pos.centerx = 150
    surface.blit(text, pos)



if __name__ == '__main__':
    python = Python()
    feed = Feed()


    pygame.init()
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), 0, 32)
    pygame.display.set_caption('Snake Game')
    surface = pygame.Surface(window.get_size())
    surface = surface.convert()
    surface.fill(WHITE)
    clock = pygame.time.Clock()
    pygame.key.set_repeat(1,40)
    window.blit(surface, (0, 0))


    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_UP:
                    python.Direction = UP
                elif event.key == K_DOWN:
                    python.Direction = DOWN
                elif event.key == K_LEFT:
                    python.Direction = LEFT
                elif event.key == K_RIGHT:
                    python.Direction = RIGHT
                
        
        surface.fill(WHITE)
        python.move()
        check_eat(python, feed)
        speed = (FPS + python.length) / 2
        show_info(python.length, speed, surface)
        python.draw(surface)
        feed.draw(surface)
        window.blit(surface, (0, 0))
        pygame.display.flip()
        pygame.display.update()
        clock.tick(speed)
        
