import pygame
import random


#this is a Sprite class 
class Enemy(pygame.sprite.Sprite):
    #scale : for different bird sizes
    def __init__(self, SCREEN_WIDTH, y, sprite_sheet, scale):
        pygame.sprite.Sprite.__init__(self)
        
        
        #define variables
        # will store the stil images of the bird image
        self.animation_list = []
        #0 so that animation starts at the first frame
        self.frame_index = 0
        #ensures that the animation only lasts a limited time
        self.update_time = pygame.time.get_ticks()
        #direction of bird movement
        self.direction = random.choice([-1, 1])
        
        #esures that the bird is facing the right way 
        if self.direction == 1:
            self.flip = True
        
        
        else:
            self.flip = False
        
        #load images from spritesheet
        #there are 8 still images in the image
        animation_steps = 8
        
        for animation in range(animation_steps):
            
            #extract an image from the SpriteSheet image with the "get_image" function of spritesheet class
            #arguments see spritesheet class
            image = sprite_sheet.get_image(animation, 32, 32, scale, (0, 0, 0))
            image = pygame.transform.flip(image, self.flip, False)
            #setting color key to black ensures transparency for the image
            image.set_colorkey((0, 0, 0))
            self.animation_list.append(image)
        
        #select starting image and create rectangle from it
        self.image = self.animation_list[self.frame_index]
        #getting a rectangle from the image
        self.rect = self.image.get_rect()


        #to ensure that the bird doesnt go off the screen when direction is -1
        #we check it and place it so that has to cross the screen to go off it. 
        if self.direction == 1:
            self.rect.x = 0
        else:
            self.rect.x = SCREEN_WIDTH
        self.rect.y = y

    def update(self, scroll, SCREEN_WIDTH):
   
        #update animation
        #animation cooldown defines how fast the animation is happening
        ANIMATION_COOLDOWN = 50

        #update image depending on current frame in the animation list

        self.image = self.animation_list[self.frame_index]

        #check if enough time has passed since the last update in order to skip to the next frame / still image
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            #by setting update time to the current time, we reset the counter for the next frame
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        #if the animation has run out of frames then reset back to the starting frame
        if self.frame_index >= len(self.animation_list):
            self.frame_index = 0

        #move enemy
        #2 defines the speed of the bird - speed is fixed - could be made into a random speed variable
        self.rect.x += self.direction * 2
        self.rect.y += scroll

        #check if gone off screen
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()