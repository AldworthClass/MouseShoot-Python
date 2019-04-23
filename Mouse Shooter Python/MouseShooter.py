import pygame
import math



# Define some colors, you may want to add more
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

#Other Game Constants
WIDTH = 800
HEIGHT = 600

def draw_crosshair(screen, pos):
    pygame.draw.circle(screen, BLACK, pos, 11, 1)
    pygame.draw.circle(screen, BLACK, pos, 6,1)
    pygame.draw.line(screen, RED, [pos[0], pos[1] - 10], [pos[0], pos[1] + 10])
    pygame.draw.line(screen, RED, [pos[0] - 10, pos[1]], [pos[0] + 10, pos[1]])



#Class for ship
class Ship():
    def __init__(self):
        self.color = BLUE
        self.ship_rect = pygame.Rect(WIDTH/2-10, HEIGHT/2-10, 20, 20)
        self.x_vel = 0
        self.y_vel = 0
    #Moves Ship by speed
    def update(self):
        #self.ship_rect.move_ip(self.x_vel,self.y_vel)
        self.ship_rect=self.ship_rect.move(self.x_vel, self.y_vel)
    #Draws Ship on screen
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.ship_rect)

#Class for projectile
class Projectile():
    def __init__(self, ship):
        self.Dest = pygame.mouse.get_pos()
        self.color = RED
        self.radius = 2
        #Starts projectile in centre of ship
        self.loc = [ship.ship_rect.x + ship.ship_rect.width/2, ship.ship_rect.y + ship.ship_rect.height/2]

        #Determine appropriate speed to move projectiles based on slope and distance

        #Change in x between ship centre and mouse location
        self.run = self.Dest[0] - self.loc[0]
        #Change in y between ship centre and mouse location
        self.rise = self.Dest[1] - self.loc[1]


        distance = math.sqrt(self.run*self.run + self.rise*self.rise)
        #Normalizes speed by dividing out distance from rise and run and uses multiplyer to set speed
        self.x_speed = self.run / distance * 2
        self.y_speed = self.rise / distance * 2

    def move(self):
        self.loc[0] += self.x_speed
        self.loc[1] += self.y_speed

    def draw(self, screen):
        pygame.draw.circle(screen,self.color,[int(self.loc[0]), int(self.loc[1])],self.radius)


pygame.init()
#Makes cursor invisible
pygame.mouse.set_visible(False)
# Set the width and height of the screen [width, height]
size = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("My Game")
# Loop until the user clicks the close button.
done = False
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
hero_ship = Ship()
projectiles = []
# -------- Main Program Loop -----------
while not done:
    # --- Main event loop

    # --- All events are detected here
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            # Figure out if it was an arrow key. If so
            # adjust speed.
            if event.key == pygame.K_LEFT:
                hero_ship.x_vel += -2
            elif event.key == pygame.K_RIGHT:
                hero_ship.x_vel += 2
            elif event.key == pygame.K_UP:
                hero_ship.y_vel += -2
            elif event.key == pygame.K_DOWN:
                hero_ship.y_vel += 2


        elif event.type == pygame.KEYUP:
            # Figure out if it was an arrow key. If so
            # adjust speed.
            if event.key == pygame.K_LEFT:
                hero_ship.x_vel -= -2
            elif event.key == pygame.K_RIGHT:
                hero_ship.x_vel -= 2
            elif event.key == pygame.K_UP:
                hero_ship.y_vel -= -2
            elif event.key == pygame.K_DOWN:
                hero_ship.y_vel -= 2

        elif event.type == pygame.MOUSEBUTTONDOWN:
            projectiles.append(Projectile(hero_ship))



    # --- Game logic should go here
    hero_ship.update()
    for projectile in projectiles:
        projectile.move()
        #removes projectile once it leaves the screen
        if not pygame.Rect(0, 0, WIDTH, HEIGHT).collidepoint(projectile.loc):
            projectiles.remove(projectile)
            print("projectile removed")

    # --- Screen-clearing code goes here
    #  Here, we clear the screen to white.
    screen.fill(WHITE)

    # --- Drawing code should go here
    draw_crosshair(screen, pygame.mouse.get_pos())

    hero_ship.draw(screen)
    for projectile in projectiles:
        projectile.draw(screen)
    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # --- Limit to 60 frames per second
    clock.tick(60)

# Close the window and quit.
pygame.quit()