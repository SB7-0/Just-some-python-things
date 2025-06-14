import pygame
import random
import asyncio


pygame.init()
screen=pygame.display.set_mode((0,0),pygame.FULLSCREEN)
Screen_Width,Screen_Height = screen.get_size()
FPS = pygame.time.Clock()
running = True
choice_for_velocity = [1,-1]

class ball:
    def __init__(self,x,y,v_x,v_y,color,radius = 20 ):
        self.x = x
        self.y = y
        self.v_x = v_x
        self.v_y = v_y
        self.color = color
        self.radius = radius 

    def movement(self):
        self.x += self.v_x
        self.y += self.v_y

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
        pygame.draw.polygon(screen,color="white",points=[(0,0),(0,Screen_Height),(Screen_Width,Screen_Height),(Screen_Width,0)],width=30)

    def collison_with_window(self):
        if self.x + self.radius  <= 70 or self.x + self.radius  >= Screen_Width  - 30 :
            self.v_x *= -1 
        if self.y + self.radius  <= 70 or self.y + self.radius >= Screen_Height  - 30 :
            self.v_y *= -1


def create_random_ball():
    x = random.randint(30, Screen_Width - 30)
    y = random.randint(30, Screen_Height - 30)
    vx = random.choice([-1, 1]) * random.uniform(1, 3)
    vy = random.choice([-1, 1]) * random.uniform(1, 3)
    color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
    return ball(x, y,vx, vy, color)

balls = [create_random_ball() for _ in range(10)]

def Ball_2_Ball_COllision_Handeling():
    for i in range(len(balls)):
        for j in range(i + 1, len(balls)):
            ball1 = balls[i]
            ball2 = balls[j]

            dx = ball2.x - ball1.x
            dy = ball2.y - ball1.y

            distance = (dx**2 + dy**2)**(1/2)

            if distance > 40:
                continue 
            else:
                ball1.v_x *= random.choice(choice_for_velocity)
                ball2.v_x *=  random.choice(choice_for_velocity)
                ball1.v_y *= random.choice(choice_for_velocity)
                ball2.v_y *=  random.choice(choice_for_velocity)

                size = random.choice([-1,1,2,-2])


                if ball1.v_x < 0 :
                    ball1.v_x += -1
                else:
                    ball1.v_x += 1

                if ball1.v_y < 0 :
                    ball1.v_y += -1 
                else:
                    ball1.v_y += 1

                if ball2.v_x < 0 :
                    ball2.v_x += -1 
                else:
                    ball2.v_x += 1

                if ball2.v_y < 0 :
                    ball2.v_y += -1 
                else:
                    ball2.v_y += 1

async def cd_reset():
    while running:
        await asyncio.sleep(5)
        for _ in balls:
            if _.v_x < 0:
                _.v_x = -1* random.uniform(1, 3)
            else:
                _.v_x = 1* random.uniform(1, 3)
            
            if _.v_y<0:
                _.v_y = -1 * random.uniform(1, 3)
            else:
                _.v_y = 1 * random.uniform(1, 3)

        print("Velocity reset")

async def main():
    global running
    asyncio.create_task(cd_reset())
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill("black")

        for aball in balls:
            aball.draw(screen)
            aball.movement()
            aball.collison_with_window()
        
        Ball_2_Ball_COllision_Handeling()

        pygame.display.flip()
        await asyncio.sleep(0)
        FPS.tick(60)

    pygame.quit()

asyncio.run(main())

    
