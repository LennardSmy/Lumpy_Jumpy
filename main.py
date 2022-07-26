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

#defines the threshhold at which when the player reaches it, 
#the screen starts scrolling
SCROLL_THRESH = 200

GRAVITY = 1
#the max number of platforms is limited to 10
MAX_PLATFORMS = 10


#this variable is gonna change during the game
scroll = 0

# sets the background scroll speed
bg_scroll = 0

#define colours
WHITE = (255,255,255)

#load images
player_image = pygame.image.load("Assets/Doodler_char.png").convert_alpha()
bg_image = pygame.image.load("Assets/el-capitan_croped.png").convert_alpha()
platform_image = pygame.image.load("Assets/cucumber_platform.png").convert_alpha()


#function for drawing the background
def draw_bg(bg_scroll):
    #-100 auf der x achse damit der Bildausschnitt passt. 
    screen.blit(bg_image, (0,0 + bg_scroll))
    screen.blit(bg_image, (0,-600 + bg_scroll))



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
        #scroll variable is resetet every time move is called
        scroll = 0
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
            #colliderect() checks if platform rectangle collides with player rectangle
            if platform.rect.colliderect(self.rect.x,self.rect.y + dy, self.width, self.height):
                #check if player is above platfrom
                if self.rect.bottom < platform.rect.centery: 
                    #should only collide when falling -> velocity needs do be larger than 0
                    if self.vel_y > 0:
                        #ensures that player bounces off the top of the plattform
                        self.rect.bottom = platform.rect.top
                        dy = 0 
                        self.vel_y = -20
                
                
                
        # check collision with ground
        if self.rect.bottom + dy > SCREEN_HIGHT:
            dy = 0 
            self.vel_y = -20


        # check if the player has bounced to the top of the screen
        if self.rect.top <= SCROLL_THRESH:
            #once the player has reached the threshold it stops moving 
            # and the screen moves relative to it
            #player velocity is dy , so scroll variable needs to be negative dy
            #if player is jumping
            if self.vel_y < 0:
                scroll = -dy 

        #update rectangle position
        self.rect.x += dx
        #adding the scroll variable here makes the player freeze on y position when hitting SCROLL_THRESH
        #dy and scroll cancel each other out    

        self.rect.y += dy + scroll

        return scroll

    def draw(self):
        # coordinates are in relation to position of player rectangle -> self.rect
        #flip method ensures that char looks in the direction of movement
        screen.blit(pygame.transform.flip(self.image, self.flip, False), (self.rect.x -3, self.rect.y - 4))
        #screen.blit(self.image, self.rect)
        
        #shows me the "collision" rectangle
        #pygame.draw.rect(screen, WHITE,self.rect, 2)

#platform class
#we are using a sprite class for more and easier functionality

class Platform(pygame.sprite.Sprite):
    #we leave width undefined so we can tweek with it later
    def __init__(self, x, y, width):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(platform_image,(width,10))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self,scroll):
        
        #update platform's vertical position
        self.rect.y += scroll



#player instance
# sets Player coordinates in middle bottom part of the screen
jumpy = Player(SCREEN_WIDTH // 2, SCREEN_HIGHT - 150 )

#create sprite groups
# platforms are stored in this group
platform_group = pygame.sprite.Group()

#create temporary platfroms
#for ramdonmization of platform location and width we import the module "random"
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
    scroll = jumpy.move()
    

    #draw backgound image
    bg_scroll += scroll
    #if background scroll reaches top of second bg image it is reset to 0 -> endless scroll
    #image height is 600 pixels
    if bg_scroll >= 600: 
        bg_scroll = 0

    draw_bg(bg_scroll)

    #draw temporary scrollthreshhold
    pygame.draw.line(screen,WHITE,(0,SCROLL_THRESH), (SCREEN_WIDTH, SCROLL_THRESH))

    #update platforms
    platform_group.update(scroll)

    #draw sprites 
    #draw method of platform_groups comes with sprite groups
    platform_group.draw(screen)
    jumpy.draw()


    #event handler (python function)
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            run = False


    #update display window

    pygame.display.update()

pygame.quit()
