import pygame,math
import random
from random import randint

pygame.init()
screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
Screen_Width,Screen_Height = screen.get_size()
running = True
FPS = pygame.time.Clock()

bullets=[]
e_bullets = []
enemies = []

class ball:
    global Screen_Height,Screen_Width
    def __init__(self,x , y, v_x, v_y,color,radius = 40):
        self.x = x
        self.y = y
        self.v_x = v_x
        self.v_y = v_y
        self.color = color
        self.radius = radius 

    def draw(self):
        pygame.draw.circle(screen,self.color,(self.x,self.y),30)

    def collison_with_window(self):
        if self.x + self.radius  <= 70 or self.x + self.radius  >= Screen_Width  - 30 :
            self.v_x *= -1
        if self.y + self.radius  <= 70 or self.y + self.radius >= Screen_Height  - 30 :
            self.v_y *= -1

    def movement(self):
        self.x += self.v_x
        self.y += self.v_y

    def move(self,key):
        if key[pygame.K_w] or key[pygame.K_UP]:
            self.y -= self.v_y
        if key[pygame.K_a] or key[pygame.K_LEFT]:
            self.x -= self.v_x
        if key[pygame.K_s]or key[pygame.K_DOWN]:
            self.y += self.v_y
        if key[pygame.K_d]or key[pygame.K_RIGHT]:
            self.x += self.v_x
        
    def bullet_data(self):
        bullet_pos = pygame.Vector2(self.x,self.y)
        target_x , target_y = pygame.mouse.get_pos()
        target_pos = pygame.Vector2(target_x,target_y)
        bullets.append({'bullet_pos':bullet_pos,'direction':(target_pos-bullet_pos).normalize(),'speed':5 , 'target_pos':target_pos,
                        'bounciness':randint(1,5),'bounced':0,'radius':10})
        
    def enemy_ball_bullet_collision(self,ball):
        ball_pos = pygame.Vector2(self.x,self.y)
        for bullet in bullets[:]:
            if bullet['radius'] + self.radius >= bullet['bullet_pos'].distance_to(ball_pos):
                enemies.remove(ball)
                bullets.remove(bullet)


        
def bounce_check():
    for bullet in bullets[:]:
        bullet['bullet_pos'] += bullet['direction'] * bullet['speed']
        if bullet['bounciness'] < bullet['bounced']:
            bullets.remove(bullet)
        else:
            pygame.draw.circle(screen, (255, 0, 0), bullet['bullet_pos'], bullet['radius'])
        if bullet['bullet_pos'][0] + bullet['radius']  <= 70 or bullet['bullet_pos'][0] + bullet['radius']  >= Screen_Width  - 30 :
            bullet['direction'][0] *= -1
            bullet["bounced"] += 1
        if bullet['bullet_pos'][1] + bullet['radius']  <= 70 or bullet['bullet_pos'][1] + bullet['radius'] >= Screen_Height  - 30 :
            bullet['direction'][1] *= -1
            bullet["bounced"] += 1
        
def enemy_creation():
    x = random.randint(50, Screen_Width - 50)
    y = random.randint(50, Screen_Height - 50)
    vx = random.choice([-1, 1]) * random.uniform(1, 3)
    vy = random.choice([-1, 1]) * random.uniform(1, 3)
    color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    enemies.append(ball(x, y,vx, vy, color))


player_data = ball(Screen_Width/2,Screen_Height/2,5,5,"blue")
for _ in range(5):
    enemy_creation()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            player_data.bullet_data()

    screen.fill("black")

    bounce_check()
    
    for _ in enemies[:]:
        _.enemy_ball_bullet_collision(_)

    for aball in enemies:
        aball.draw()
        aball.movement()
        aball.collison_with_window()
    
    KEYS = pygame.key.get_pressed()
    player_data.move(KEYS)
    player_data.draw()

    pygame.display.flip()
    FPS.tick(60)

pygame.quit()