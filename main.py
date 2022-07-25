#import libraries
# 
from platform import platform
import pygame
import random

#initialize pygame
pygame.init()

#game window

SCREEN_WIDTH = 400
SCREEN_HIGHT = 600

#create game window

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HIGHT))

pygame.display.set_caption("Lumpy Jumpy")

#set frame rate
clock = pygame.time.Clock()

#framerate is set to 60 frames per second
FPS = 60

#GameVariables
GRAVITY = 1
MAX_PLATFORMS = 10 


#define colours
WHITE = (255,255,255)

#load images
player_image = pygame.image.load("Assets/Doodler_char.png").convert_alpha()
bg_image = pygame.image.load("Assets/el-capitan.png").convert_alpha()
platform_image = pygame.image.load("Assets/cucumber_platform.png").convert_alpha()



#player class 
class Player(): 
    
    def __init__(self,x,y):
        self.image = pygame.transform.scale(player_image, (45,45))
       
        # variables to create a "customized" (collision) rectangle
        self.width = 35
        self.height = 40
        #get_rect function nochmal nachschauen/verstehen
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = (x,y)
        #gives the velocity of the player on the y axis
        self.vel_y = 0
         #flip method ensures that char looks in the direction of movement
        self.flip = False

    def move(self):
        #here you can change the move speed

        # reset variables
        # these extra positional variables are introduced to simplify collision checks
        # and control that player does not leave the screen
        # "d" stands for delta. It symbolizes the change in the x and y coordinate respectively
        dx = 0
        dy = 0
        
        # which keypresses are present
        key = pygame.key.get_pressed()
        
        #checks if Key a is pressed
        #tweeking with dx changes movement speed
       
        
        if key[pygame.K_a]: 
            dx = - 10
            self.flip = True
        
        # checks if key d is pressed
        if key[pygame.K_d]:
            dx = 10
            self.flip = False

        #gravity
        #every interation of the gameloop, gravity is increasing
        self.vel_y += GRAVITY
        dy += self.vel_y


        #ensure player doesn't go off the edge of the screen
        #maybe this can be a seperate function
        #checks if player goes over left edge of the screen
        #gives the distance bewtween the players lefthand side and edge of the screen
        if self.rect.left +dx < 0: 
            dx = 0 - self.rect.left

        #checks if player goes over right edge of the screen    
        if self.rect.right + dx > SCREEN_WIDTH:
            dx = SCREEN_WIDTH - self.rect.right

        #check collision with platforms
        for platform in platform_group:
            #collision in the y direction
            if platform.rect.colliderect(self.rect.x,self.rect.y + dy, self.width, self.height):
                #check if above platfrom
                if self.rect.bottom < platform.rect.centery: 
                    if self.vel_y > 0:
                        self.rect.bottom = platform.rect.top
                        dy = 0 
                        self.vel_y = -20
                
                
                
        # check collision with ground
        if self.rect.bottom + dy > SCREEN_HIGHT:
            dy = 0 
            self.vel_y = -20

        #update rectangle position
        self.rect.x += dx
        self.rect.y += dy

    def draw(self):
        # coordinates are in relation to position of player rectangle -> self.rect
        #flip method ensures that char looks in the direction of movement
        screen.blit(pygame.transform.flip(self.image, self.flip, False), (self.rect.x -3, self.rect.y - 4))
        #screen.blit(self.image, self.rect)
        
        #shows me the "collision" rectangle
        #pygame.draw.rect(screen, WHITE,self.rect, 2)


#we are using a sprite class for more functionality
class Platform(pygame.sprite.Sprite):

    def __init__(self, x, y, width):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(platform_image,(width,10))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


#player instance
# sets Player coordinates in middle bottom part of the screen
jumpy = Player(SCREEN_WIDTH // 2, SCREEN_HIGHT - 150 )

#create sprite groups
platform_group = pygame.sprite.Group()

#create temporary platfroms
#for ramdonmization we import the module "random"
for p in range(MAX_PLATFORMS):
    p_width = random.randint(40,60)
    p_x = random.randint(0, SCREEN_WIDTH - p_width)
    p_y = p* random.randint(80,120)
    platform = Platform(p_x,p_y,p_width)
    platform_group.add(platform)

#game loop
# game runs as long as run = true
run = True

while run : 

    #ensures that gameplay is 60 frames per second
    clock.tick(FPS)

    #enables movement of the player
    jumpy.move()

    #draw backgound image
    #-100 auf der x achse damit der Bildausschnitt passt. 
    screen.blit(bg_image, (-100,0))

    #draw sprites 
    platform_group.draw(screen)
    jumpy.draw()


    #event handler (python function)
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            run = False


    #update display window

    pygame.display.update()

pygame.quit()
