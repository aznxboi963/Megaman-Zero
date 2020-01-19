""" Alex Fang's Megaman Zero Program, Enemy Game File """
import pygame, os, random, time
from pygame.locals import *

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

FRAMERATE = 60
 
# Screen dimensions
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600

class Basicenemy(pygame.sprite.Sprite):
    #Class for the most basic enemy
    def __init__(self, x, y):
        super().__init__()
        #Setting up all his images
        self.TrueIdle = pygame.transform.scale2x(pygame.image.load('Enemies\BasicEnemy1.png'))
        #True Idle is his idle when not activated (seen the player atleast once)
        self.Idle = pygame.transform.scale2x(pygame.image.load('Enemies\BasicShot3.png'))
        self.IdleShot = [pygame.image.load('Enemies\BasicShot5.png'), pygame.image.load('Enemies\BasicShot4.png'),
                         pygame.image.load('Enemies\BasicShot3.png'), pygame.image.load('Enemies\BasicShot2.png'),
                         pygame.image.load('Enemies\BasicShot1.png')]
        self.image = self.TrueIdle

        #Doubling the scale of all images
        for z in range(len(self.IdleShot)):
            self.IdleShot[z] = pygame.transform.scale2x(self.IdleShot[z])

        #Setting up the rect for the enemy and variables for animation,attack,health
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.rect.width -= 10
        self.health = 100
        self.shotduration = 0
        self.facing = "Left"
        self.action = "TrueIdle"
        self.first = False

    def shoot(self):
        """Shooting function, changes the action variable to shoot and starts the
        duration of the shot is set"""
        if not self.first:
            self.action = "Shoot"
            self.shotduration = 60
            self.first = True
        else:
            self.action = "Shoot"
            self.shotduration = 44

    def takedmg(self,dmg):
        """Function to take damage and returns a boolean variable for if it dies"""
        self.health -= dmg
        if self.health <= 0:
            return(True)
        else:
            return(False)
            
    def update(self):
        """Updating the enemy if it is within the screen"""
        if self.rect.right > 0 and self.rect.x < SCREEN_WIDTH:
            #Changing the animation to Idle if the shooting duration is over
            if self.shotduration-1 <= 0 and self.action == "Shoot" and self.first:
                self.shotduration = 0
                self.action = "Idle"
                if self.facing == "Right":
                    self.image = self.Idle
                else:
                    self.image = pygame.transform.flip(self.Idle,True,False)
            #Updating the animation depending on his action and direction
            #Reducing shot duration by 1 every frame if he is shooting
            if self.facing == "Left" and self.action == "Shoot":
                self.image = pygame.transform.flip(self.IdleShot[int(self.shotduration/15)],True,False)
                self.shotduration -=1
            elif self.facing == "Right" and self.action == "Shoot":
                self.image = self.IdleShot[int(self.shotduration/15)]
                self.shotduration -=1
            elif self.facing == "Right" and self.action == "TrueIdle":
                self.image = pygame.transform.flip(self.TrueIdle,True,False)
            elif self.facing == "Left" and self.action == "TrueIdle":
                self.image = self.TrueIdle

class Fly(pygame.sprite.Sprite):
    def __init__(self, x, y):
        #Class for the flying enemy
        super().__init__()
        #Loading all idle images and doubling their size
        self.Idle = [pygame.image.load('Enemies\Fly.png'), pygame.image.load('Enemies\Fly2.png'),
                     pygame.image.load('Enemies\Fly3.png'), pygame.image.load('Enemies\Fly4.png')]
        for z in range(len(self.Idle)):
            self.Idle[z] = pygame.transform.scale2x(self.Idle[z])
        #Setting up variables for the animation, health, and attack
        self.image = self.Idle[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.shotduration = 0
        self.spriteCount = 0
        self.health = 50
        
    def shoot(self):
        """Shooting function that sets the shot duration/cooldown"""
        self.shotduration = 60

    def takedmg(self,dmg):
        """Function to take damage and returns a boolean variable for if it dies"""
        self.health -= dmg
        if self.health <= 0:
            return(True)
        else:
            return(False)
        
    def update(self):
        """Updating the sprite animation and the shot duration/cooldown if it is in the screen"""
        if self.rect.right > 0 and self.rect.x < SCREEN_WIDTH:
            if self.spriteCount+1 >= 35:
                self.spriteCount = 0
            self.spriteCount +=1
            self.image = self.Idle[int(self.spriteCount/10)]
            self.shotduration -=1

class Roller(pygame.sprite.Sprite):
    def __init__(self, x, y):
        #Class for the rolling blockade enemy
        super().__init__()
        #Loading all idle images and doubling their size
        self.Roll = [pygame.image.load('Enemies\Ball.png'), pygame.image.load('Enemies\Ball2.png'),
                     pygame.image.load('Enemies\Ball3.png')]
        for z in range(len(self.Roll)):
            self.Roll[z] = pygame.transform.scale2x(self.Roll[z])
        self.image = self.Roll[0]
        #Setting up variables for the animation, health, attack and movement
        self.rect = self.image.get_rect()
        self.facing = "Left"
        self.rect.x = x
        self.rect.y = y
        self.spriteCount = 0
        self.health = 150
        self.change_x = -4
        self.change_y = 0
        self.spawn = False
        self.hurt = 0

    def takedmg(self,dmg):
        """Function to take damage and returns a boolean variable for if it dies"""
        #includes hurt cooldown so the player can't oneshot it with the sabre
        if self.hurt <= 0:
            self.health -= dmg
            self.hurt = 30
            if self.health <= 0:
                return(True)
            else:
                return(False)

    def calc_grav(self):
        """Function to alculate gravity."""
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .35

    def update(self, platform_list):
        """Updating the sprite animation and the shot duration/cooldown if it is in the screen"""
        if self.rect.right > 0 and self.rect.x < SCREEN_WIDTH:
            #Gravity
            self.calc_grav()
            #Moving the sprite left or right
            self.rect.x += self.change_x
            #Killing the sprite if he moves off screen
            if self.rect.right < 0 or self.rect.x >= SCREEN_WIDTH or self.rect.top >= SCREEN_HEIGHT:
                self.kill()
            #Counting down the hit cooldown
            if self.hurt > 0:
                self.hurt -= 1
                
            #Check and see if we hit anything and reverse direction if we do
            block_hit_list = pygame.sprite.spritecollide(self, platform_list, False)
            for block in block_hit_list:
                # Set our right side to the left side of the item we hit
                if block.rect.top+13 <= self.rect.bottom:
                    if self.change_x > 0:
                        self.rect.right = block.rect.left
                        self.change_x = self.change_x *-1
                        self.facing = "Left"
                    elif self.change_x < 0:
                        # Otherwise if we are moving left, do the opposite.
                        self.rect.left = block.rect.right
                        self.change_x = self.change_x *-1
                        self.facing = "Right"

            #Moving the sprite up or down
            self.rect.y += self.change_y

            #Check and see if we hit anything top and the bottom
            block_hit_list = pygame.sprite.spritecollide(self, platform_list, False)
            for block in block_hit_list:
                # Reset our position based on the top/bottom of the object.
                if self.change_y > 0:
                    self.rect.bottom = block.rect.top
                elif self.change_y < 0:
                    self.rect.top = block.rect.bottom
                self.change_y = 0

            #Updating the animation of the sprite
            if self.spriteCount+1 >= 25:
                self.spriteCount = 0
            self.spriteCount +=1
            if self.facing == "Left":
                self.image = self.Roll[int(self.spriteCount/10)]
            elif self.facing == "Right":
                self.image = pygame.transform.flip(self.Roll[int(self.spriteCount/10)], True, False)
                
class Guarder(pygame.sprite.Sprite):
    def __init__(self, x, y):
        #Class for the Guarder enemy with a sheild
        super().__init__()
        #Loading all idle images and doubling their size
        self.Guardmove = [pygame.image.load('Enemies\Tank.png'),pygame.image.load('Enemies\Tank2.png'),
                          pygame.image.load('Enemies\Tank3.png'),pygame.image.load('Enemies\Tank4.png'),
                          pygame.image.load('Enemies\Tank5.png'),pygame.image.load('Enemies\Tank6.png'),
                          pygame.image.load('Enemies\Tank7.png'),pygame.image.load('Enemies\Tank8.png'),
                          pygame.image.load('Enemies\Tank9.png'),pygame.image.load('Enemies\Tank10.png')]
        
        for z in range(len(self.Guardmove)):
            self.Guardmove[z] = pygame.transform.flip(pygame.transform.scale2x(self.Guardmove[z]), True, False)
        #Setting up variables for the animation, health, guard and attack
        self.image = self.Guardmove[0]
        self.rect = self.image.get_rect()
        self.facing = "Left"
        self.guard = True
        self.rect.x = x
        self.rect.y = y
        self.truex = self.rect.right #True variable to make sure the enemy stays in place when animating
        self.truey = y #True variable to make sure the enemy stays in place when animating
        self.spriteCount = 1
        self.health = 200
        self.spritechange = 1 #Variable to allow the back and forth cycling of the animation
        self.hurt = 0
        
    def takedmg(self,dmg):
        """Function to take damage and returns a boolean variable for if it dies"""
        #includes hurt cooldown so the player can't oneshot it with the sabre
        if self.hurt <= 0:
            self.health -= dmg
            self.hurt = 30
            if self.health <= 0:
                return(True)
            else:
                return(False)
    
    def update(self):
        """Updating the sprite animation and guarding stance if it is in the screen"""
        if self.rect.right > 0 and self.rect.left < SCREEN_WIDTH:
            if self.spriteCount+1 > 114 or self.spriteCount-1 < 0:
                self.spritechange = self.spritechange * -1
            self.spriteCount += self.spritechange
            #Counting down the hit cooldown
            if self.hurt > 0:
                self.hurt -= 1
            self.image = self.Guardmove[int(self.spriteCount/12)]
            self.rect = self.image.get_rect()
            #Setting the rect of the sprite to its true position
            self.rect.right = self.truex
            self.rect.y = self.truey

            #Setting the guard boolean to be true if they are in a certain position
            if self.spriteCount > 60:
                self.guard = False
            else:
                self.guard = True

class Boss(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        #Setting up variables for the animation, if the boss through all his actions and doubling the size of them all
        self.spawnimage = [pygame.image.load('Enemies\BOss\BossSpawn13.png'),pygame.image.load('Enemies\BOss\BossSpawn12.png'),
                      pygame.image.load('Enemies\BOss\BossSpawn11.png'),pygame.image.load('Enemies\BOss\BossSpawn10.png'),
                      pygame.image.load('Enemies\BOss\BossSpawn9.png'),pygame.image.load('Enemies\BOss\BossSpawn8.png'),
                      pygame.image.load('Enemies\BOss\BossSpawn7.png'),pygame.image.load('Enemies\BOss\BossSpawn6.png'),
                      pygame.image.load('Enemies\BOss\BossSpawn5.png'),pygame.image.load('Enemies\BOss\BossSpawn4.png'),
                      pygame.image.load('Enemies\BOss\BossSpawn3.png'),pygame.image.load('Enemies\BOss\BossSpawn2.png'),
                      pygame.image.load('Enemies\BOss\BossSpawn.png')]
        self.deathimage = [pygame.image.load('Enemies\BOss\Death8.png'),pygame.image.load('Enemies\BOss\Death7.png'),
                           pygame.image.load('Enemies\BOss\Death6.png'),pygame.image.load('Enemies\BOss\Death5.png'),
                           pygame.image.load('Enemies\BOss\Death4.png'),pygame.image.load('Enemies\BOss\Death3.png'),
                           pygame.image.load('Enemies\BOss\Death2.png'),pygame.image.load('Enemies\BOss\Death.png')]
        self.bulletimg = [pygame.image.load('Enemies\BOss\Bullet3.png'),pygame.image.load('Enemies\BOss\Bullet3.png'),
                          pygame.image.load('Enemies\BOss\Bullet3.png'),pygame.image.load('Enemies\BOss\Bullet3.png'),
                          pygame.image.load('Enemies\BOss\Bullet3.png'),pygame.image.load('Enemies\BOss\Bullet3.png'),
                          pygame.image.load('Enemies\BOss\Bullet2.png'),pygame.image.load('Enemies\BOss\Bullet.png')]
        self.summonimg = [pygame.image.load('Enemies\BOss\Summon2.png'),pygame.image.load('Enemies\BOss\Summon.png')]
        #Images for his wing animation
        self.wings =  [pygame.image.load('Enemies\BOss\Wings.png'),pygame.image.load('Enemies\BOss\Wings2.png'),
                       pygame.image.load('Enemies\BOss\Wings3.png'),pygame.image.load('Enemies\BOss\Wings4.png'),
                       pygame.image.load('Enemies\BOss\Wings5.png'),pygame.image.load('Enemies\BOss\Wings6.png'),
                       pygame.image.load('Enemies\BOss\Wings7.png')]
        self.Idle = pygame.transform.scale2x(pygame.image.load('Enemies\BOss\BossIdle.png'))
        for z in range(len(self.spawnimage)):
            self.spawnimage[z] = pygame.transform.scale2x(self.spawnimage[z])
        for z in range(len(self.bulletimg)):
            self.bulletimg[z] = pygame.transform.scale2x(self.bulletimg[z])
        for z in range(len(self.summonimg)):
            self.summonimg[z] = pygame.transform.scale2x(self.summonimg[z])
        for z in range(len(self.wings)):
            self.wings[z] = pygame.transform.scale2x(self.wings[z])
        for z in range(len(self.deathimage)):
            self.deathimage[z] = pygame.transform.scale2x(self.deathimage[z])
            
        #Setting up variables for the spawn,death and fighting animations
        self.spriteCount = 0
        self.image = self.Idle
        self.action = "Spawn"
        self.totalhealth = 1500
        self.health = 1500
        self.spawncount = 200
        self.deathcount = 0

        #Setting up his action and action counts
        self.action = "Idle"
        self.bulletcount = 0
        self.summoncount = 0
        self.idlecount = 0

        #Setting up his hitstun variable
        self.hurt = 0

        #Setting up his image rect
        self.rect = self.spawnimage[12].get_rect()
        self.rect.centerx = x

        #His actual hitbox rect
        self.hitboxrect = Rect(x-15,y+245,30,100)

        #Setting up his wing animation variables
        self.wingcount = 0
        self.wingrect = self.wings[0].get_rect()
        self.wingrect.x = 320
        self.wingrect.y = 200

    def takedmg(self,dmg):
        """Function to take damage and returns a boolean variable for if it dies"""
        #includes hurt cooldown so the player can't oneshot it with the sabre
        if self.hurt <= 0:
            self.health -= dmg
            self.hurt = 40
            if self.health <= 0:
                return(True)
            else:
                return(False)

    def update(self):
        """Updating the sprite animation if it is in the screen"""
        if self.rect.right > 0 and self.rect.left < SCREEN_WIDTH:
            #Increasing or reseting the wingcount
            if self.wingcount+1 >= 70:
                self.wingcount = 0
            else:
                self.wingcount +=1

            #Going through spawn animation if it hasn't been done yet
            if self.spawncount >0:
                self.image = self.spawnimage[int(self.spawncount/16)]
                self.rect = self.image.get_rect()
                self.rect.centerx = 450
                self.rect.y = 200-self.spawncount #Slowly moving him down 
                self.spawncount -=1
            #Going through death animaion if he is dead
            elif self.deathcount >0:
                self.image = self.deathimage[int(self.deathcount/20)]
                self.rect = self.image.get_rect()
                self.rect.centerx = 450
                self.rect.y = 470-int(self.deathcount*1.6875)  #Slowly moving him down 
                self.deathcount -=1
            else:
                #Counting down the hit cooldown
                if self.hurt > 0:
                    self.hurt -= 1
                #Going through the animation for each action
                if self.action == "Idle":
                    self.image = self.Idle
                    self.rect = self.image.get_rect()
                    self.rect.centerx = 450
                    self.rect.y = 250
                    self.idlecount += 1
                elif self.action == "Bullet":
                    self.image = self.bulletimg[int(self.bulletcount/20)]
                    self.rect = self.image.get_rect()
                    self.rect.centerx = 450
                    self.rect.y = 250
                    self.bulletcount -= 1
                elif self.action == "Summon":
                    self.image = self.summonimg[int(self.bulletcount/30)]
                    self.rect = self.image.get_rect()
                    self.rect.centerx = 450
                    self.rect.y = 250
                    self.summoncount -= 1
                #If the boss is dead, activate the death count
                if self.health <= 0:
                    self.deathcount = 159



        

