#import libraries
# 
import pygame

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

#define colours
WHITE = (255,255,255)

#load images
player_image = pygame.image.load("Assets/Doodler_char.png").convert_alpha()
bg_image = pygame.image.load("Assets/el-capitan.png").convert_alpha()

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
        self.flip = False

    def move(self):
        #here you can change the move speed

        # reset variables
        # these extra positional variables are introduced to simplify collision checks
        # and control that player does not leave the screen
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


        #ensure player doesn't go off the edge of the screen
        #maybe this can be a seperate function
        if self.rect.left +dx < 0: 
            dx = 0 - self.rect.left


            
        if self.rect.right + dx > SCREEN_WIDTH:
            dx = SCREEN_WIDTH - self.rect.right

        #update rectangle position
        self.rect.x += dx
        self.rect.y += dy

    def draw(self):
        # coordinates are in relation to position of player rectangle -> self.rect
        screen.blit(pygame.transform.flip(self.image, self.flip, False), (self.rect.x -3, self.rect.y - 4))
        #screen.blit(self.image, self.rect)
        
        #shows me the "collision" rectangle
        pygame.draw.rect(screen, WHITE,self.rect, 2)


# sets Player coordinates in middle bottom part of the screen
jumpy = Player(SCREEN_WIDTH // 2, SCREEN_HIGHT - 150 )


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
    jumpy.draw()


    #event handler (python function)
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            run = False


    #update display window

    pygame.display.update()

pygame.quit()
