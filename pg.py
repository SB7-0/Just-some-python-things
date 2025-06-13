import pygame
import random

pygame.init()
screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
clock = pygame.time.Clock()
running = True

screen_width, screen_height = screen.get_size()
center_x = screen_width // 2
center_y = screen_height // 2

def create_random_ball():
    color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
    speed_x = random.choice([-1, 1]) * random.uniform(2, 5)
    speed_y = random.choice([-1, 1]) * random.uniform(2, 5)
    return {
        'x': center_x,
        'y': center_y,
        'color': color,
        'speed_x': speed_x,
        'speed_y': speed_y
    }
balls = [create_random_ball() for _ in range(10)]

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("white")

    for ball in balls:
        ball['x'] += ball['speed_x']
        ball['y'] += ball['speed_y']
        
        if ball['x'] - 30 <= 0 or ball['x'] + 30 >= screen_width:
            ball['speed_x'] *= -1
        if ball['y'] - 30 <= 0 or ball['y'] + 30 >= screen_height:
            ball['speed_y'] *= -1

    for ball in balls:
        pygame.draw.circle(screen, ball['color'], (int(ball['x']), int(ball['y'])), 30)


    pygame.display.flip()

    clock.tick(60)

pygame.quit()
