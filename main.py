#import libraries
# 
from platform import platform
from turtle import update
from scipy import rand

from sqlalchemy import false, true
import pygame
import random
import os
from pygame import mixer
from spritesheet import SpriteSheet
from enemy import Enemy




#initialize pygame 
mixer.init()
pygame.init()


#game window

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

#create game window

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

pygame.display.set_caption("Lumpy Jumpy")

#set frame rate
clock = pygame.time.Clock()

#framerate is set to 60 frames per second
FPS = 60

#load music and sounds
pygame.mixer.music.load("Assets/music.mp3")
#60 percent volume
pygame.mixer.music.set_volume(0.6)

#first arg = how many times it should play -> -1 is infinite loop 
#second arg = starting point in the track
pygame.mixer.music.play(-1,0.0)

jump_effect = pygame.mixer.Sound("Assets/jump.mp3")
jump_effect.set_volume(0.6) 

death_effect = pygame.mixer.Sound("Assets/death.mp3")
death_effect.set_volume(0.6) 


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

game_over = False

score = 0

#variable for screen transition
fade_counter = 0 

if os.path.exists("score.txt"):
    with open("score.txt","r") as file:
        high_score = int(file.read())
else:
	high_score = 0



#define colours
WHITE = (255,255,255)
BLACK = (0,0,0)
PANEL =(153,217,234)


#define font for on screen text
font_small = pygame.font.SysFont("Lucida Sans", 20)

font_big = pygame.font.SysFont("Lucida Sans", 24)


#load images
player_image = pygame.image.load("Assets/ninja_char.png").convert_alpha()
bg_image = pygame.image.load("Assets/fruit_bg.png").convert_alpha()
platform_image = pygame.image.load("Assets/cucumber_platform.png").convert_alpha()
#bird spritesheet - basis for enemy animation
bird_sheet_img = pygame.image.load("Assets/bird.png").convert_alpha()
bird_sheet = SpriteSheet(bird_sheet_img)





#function for outputting text onto the screen
#
def draw_text(text,font,text_col,x,y):
    img = font.render(text,True,text_col)
    screen.blit(img,(x,y))

#function for drawing info panel
def draw_panel():

    #setting background colour for panel
    pygame.draw.rect(screen, PANEL, (0, 0, SCREEN_WIDTH, 30))
    #draw a line to seperate panel from the rest
    pygame.draw.line(screen,WHITE,(0,30),(SCREEN_WIDTH, 30),2)
    #draw the score on the top left corner
    draw_text('SCORE: ' + str(score),font_small,WHITE,0,0)
    #draw the high score on the top right corner
    draw_text('HIGH SCORE: ' + str(high_score),font_small,WHITE,SCREEN_WIDTH - 200,0)
    

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
                        #insert jumping sound after player is moving back up again
                        jump_effect.play()
                
        # we dont need this anymore        
        '''        
        # check collision with ground
        if self.rect.bottom + dy > SCREEN_HEIGHT:
            dy = 0 
            self.vel_y = -20
        '''

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
    #moving argument for extra difficulty
    def __init__(self, x, y, width, moving):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(platform_image,(width,10))
        #adjustments for moving platforms
        self.moving = moving
        self.move_counter = random.randint(0,50)
        self.direction = random.choice([-1,1])
        self.speed = random.randint(1,2)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self,scroll):
        
        #move platform side to side if it is a moving platform
        if self.moving == True:
            self.move_counter += 1
            self.rect.x += self.direction * self.speed


        #change platform directio if it has moved fully or hits a wall

        if self.move_counter >= 100 or self.rect.left < 0 or self.rect.right > SCREEN_WIDTH: 
            self.direction *= -1
            self.move_counter = 0 

        #update platform's vertical position
        self.rect.y += scroll
        
        # check if platform has gone off the screen
        #if it has, we delete this platform
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()



#player instance
# sets Player coordinates in middle bottom part of the screen
jumpy = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150 )

#create sprite groups
# platforms are stored in this group
platform_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()


'''
#create temporary platfroms
#for ramdonmization of platform location and width we import the module "random"
for p in range(MAX_PLATFORMS):
    p_width = random.randint(40,60)
    p_x = random.randint(0, SCREEN_WIDTH - p_width)
    p_y = p* random.randint(80,120)
    platform = Platform(p_x,p_y,p_width)
    platform_group.add(platform)
'''
#create starting platform
platform = Platform(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT -50, 100, False )
platform_group.add(platform)
#game loop
# game runs as long as run = True
run = True

while run : 

    #ensures that gameplay is 60 frames per second
    clock.tick(FPS)
    #print(high_score)


    if game_over == False:
        #enables movement of the player
        scroll = jumpy.move()
        

        #draw backgound image
        bg_scroll += scroll
        #if background scroll reaches top of second bg image it is reset to 0 -> endless scroll
        #image height is 600 pixels
        if bg_scroll >= 600: 
            bg_scroll = 0

        draw_bg(bg_scroll)


        '''
        #draw temporary scrollthreshhold from which screen starts scrolling
        pygame.draw.line(screen,WHITE,(0,SCROLL_THRESH), (SCREEN_WIDTH, SCROLL_THRESH))
        '''
        #generate platforms
        if len(platform_group) < MAX_PLATFORMS:
            p_width = random.randint(40,60)
            p_x = random.randint(0, SCREEN_WIDTH - p_width)
            p_y = platform.rect.y - random.randint(80,120)
            #we are adding another type (moving) of platform to increase difficulty
            p_type = random.randint(1,2)
            #second condition ensures that moving platforms only start after score of 500 
            if p_type == 1 and score > 500: 
                p_moving = True
            else:
                p_moving = False
            platform = Platform(p_x,p_y,p_width,p_moving)
            platform_group.add(platform)
            


        #update platforms
        platform_group.update(scroll)

        #generate enemies
        #only create one enemy at a time and only when score passes certain number
        if len(enemy_group) == 0 and score > 1000:
            enemy = Enemy(SCREEN_WIDTH,100,bird_sheet,1.5)
            enemy_group.add(enemy)

        
        #update enemies
        enemy_group.update(scroll, SCREEN_WIDTH)



        #update score
        #update of score variable is dependent on scroll variable
        if scroll > 0:
            score += scroll
            #print(score)
        
        #draw line at previous high score

        pygame.draw.line(screen,WHITE,(0,score - high_score + SCROLL_THRESH),(SCREEN_WIDTH,score - high_score + SCROLL_THRESH), 3)
        draw_text("HIGH SCORE",font_small,WHITE,SCREEN_WIDTH - 130, score - high_score + SCROLL_THRESH )


        #draw sprites 
        #draw method of platform_groups comes with sprite groups
        platform_group.draw(screen)
        enemy_group.draw(screen)
        jumpy.draw()


        #draw panel
        draw_panel()


        #check if game over
        # if the top of the player instance is higher than the screenheight (600p) than player has fallen off the screen

        if jumpy.rect.top > SCREEN_HEIGHT: 
            game_over = True
            death_effect.play()
        
        #check for collision with enemies
        #pygame method that checks for collision between two instance rectangles
        if pygame.sprite.spritecollide(jumpy, enemy_group, False):
            game_over = true
            death_effect.play()

    
    else:
        #if statement to start the fade effect when game over
        if fade_counter < SCREEN_WIDTH:
            # by incrementally increasing fade counter seemingly continuous movement is possible , the increment is the movement speed
            fade_counter += 5
            # here we make a fancy transition into black screen with each 3 Black bars coming in from left and right respectively
            for y in range(0,6,2):
                pygame.draw.rect(screen,BLACK,(0,y * 100,fade_counter, SCREEN_HEIGHT / 6))
                pygame.draw.rect(screen,BLACK,(SCREEN_WIDTH - fade_counter,(y+1) * 100 ,SCREEN_WIDTH, SCREEN_HEIGHT/6))
        
        #else statement so that the text is only shown once the fade is complete
        else:

            #if game_over == True it outputs a text saying "GAME OVER!"
            draw_text("GAME OVER!",font_big,WHITE,130,200)
            draw_text("SCORE:" + str(score),font_big, WHITE,130,150)
            draw_text("PRESS SPACE TO PLAY AGAIN",font_big,WHITE,40,300)

            #update high score: 
            if score > high_score:
                high_score = score
                with open("score.txt", "w") as file:
                    file.write(str(high_score))  

            key = pygame.key.get_pressed()
            
            if key[pygame.K_SPACE]:
                #reset variables
                game_over = False
                score = 0
                scroll = 0
                fade_counter = 0
                #reposition jumpy
                jumpy.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150)
                
                #reset enemies
                enemy_group.empty()
                
                #reset platforms
                platform_group.empty()

                #create starting platform
                platform = Platform(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT - 50, 100, False)
                platform_group.add(platform)
            


    #event handler (python function)
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:

            #update high score: 
            if score > high_score:
                high_score = score
                with open("score.txt", "w") as file:
                    file.write(str(high_score))  
            run = False
            





    #update display window

    pygame.display.update()

pygame.quit()
