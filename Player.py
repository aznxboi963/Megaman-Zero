""" Alex Fang's Megaman Zero Program, Player Game File """
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

class Player(pygame.sprite.Sprite):
    """ This class represents the bar at the bottom that the player controls. """
 
    # -- Methods
    def __init__(self, health):
        super().__init__()
        #Loading in all the images
        self.spriteIdle = [pygame.image.load('Sprites\Idle1.png'), pygame.image.load('Sprites\Idle2.png'), pygame.image.load('Sprites\Idle3.png'), pygame.image.load('Sprites\Idle4N.png')]
        self.spriteWalk = [pygame.image.load('Sprites\Walking1.png'), pygame.image.load('Sprites\Walking2.png'), pygame.image.load('Sprites\Walking3.png'), pygame.image.load('Sprites\Walking4.png'),
                           pygame.image.load('Sprites\Walking5.png'), pygame.image.load('Sprites\Walking6.png'), pygame.image.load('Sprites\Walking7.png'), pygame.image.load('Sprites\Walking8.png'),
                           pygame.image.load('Sprites\Walking9.png'), pygame.image.load('Sprites\Walking10.png'), pygame.image.load('Sprites\Walking11.png')]
        self.spriteJump = [pygame.image.load('Sprites\Jump1.png'), pygame.image.load('Sprites\Jump2.png'), pygame.image.load('Sprites\Jump3.png'), pygame.image.load('Sprites\Jump4.png'),
                           pygame.image.load('Sprites\Jump5.png'), pygame.image.load('Sprites\Jump6.png'), pygame.image.load('Sprites\Jump7.png'), pygame.image.load('Sprites\Jump8.png'),
                           pygame.image.load('Sprites\Jump9.png'), pygame.image.load('Sprites\Jump10.png')]
        self.IdleShot = [pygame.image.load('Sprites\IdleShot.png'), pygame.image.load('Sprites\IdleShot.png'),
                         pygame.image.load('Sprites\IdleShot.png'),pygame.image.load('Sprites\IdleShot.png'),
                         pygame.image.load('Sprites\IdleShot2.png'),pygame.image.load('Sprites\IdleShot3.png')]
        self.ShotWalk = [pygame.image.load('Sprites\ShotWalk.png'), pygame.image.load('Sprites\ShotWalk2.png'), pygame.image.load('Sprites\ShotWalk3.png'), pygame.image.load('Sprites\ShotWalk4.png'),
                         pygame.image.load('Sprites\ShotWalk5.png'), pygame.image.load('Sprites\ShotWalk6.png'), pygame.image.load('Sprites\ShotWalk7.png'), pygame.image.load('Sprites\ShotWalk8.png'),
                         pygame.image.load('Sprites\ShotWalk9.png'), pygame.image.load('Sprites\ShotWalk10.png'), pygame.image.load('Sprites\ShotWalk11.png')]
        self.LoadWalk = [pygame.image.load('Sprites\LoadWalk.png'), pygame.image.load('Sprites\LoadWalk2.png'), pygame.image.load('Sprites\LoadWalk3.png'), pygame.image.load('Sprites\LoadWalk4.png'),
                         pygame.image.load('Sprites\LoadWalk5.png'), pygame.image.load('Sprites\LoadWalk6.png'), pygame.image.load('Sprites\LoadWalk7.png'), pygame.image.load('Sprites\LoadWalk8.png'),
                         pygame.image.load('Sprites\LoadWalk9.png'), pygame.image.load('Sprites\LoadWalk10.png'), pygame.image.load('Sprites\LoadWalk11.png')]
        self.GunWalk =  [pygame.image.load('Sprites\GunWalk.png'), pygame.image.load('Sprites\GunWalk2.png'), pygame.image.load('Sprites\GunWalk3.png'), pygame.image.load('Sprites\GunWalk4.png'),
                         pygame.image.load('Sprites\GunWalk5.png'), pygame.image.load('Sprites\GunWalk6.png'), pygame.image.load('Sprites\GunWalk7.png'), pygame.image.load('Sprites\GunWalk8.png'),
                         pygame.image.load('Sprites\GunWalk9.png'), pygame.image.load('Sprites\GunWalk10.png'), pygame.image.load('Sprites\GunWalk11.png')]
        self.JumpShot = [pygame.image.load('Sprites\JumpShot.png'), pygame.image.load('Sprites\JumpShot2.png'), pygame.image.load('Sprites\JumpShot3.png')]
        self.SwordIdle =[pygame.image.load('Sprites\SwordIdle.png'), pygame.image.load('Sprites\SwordIdle2.png'), pygame.image.load('Sprites\SwordIdle3.png'), pygame.image.load('Sprites\SwordIdle4.png'),
                         pygame.image.load('Sprites\SwordIdle5.png'), pygame.image.load('Sprites\SwordIdle6.png'), pygame.image.load('Sprites\SwordIdle7.png'), pygame.image.load('Sprites\SwordIdle8.png')]
        self.SwordAir =[pygame.image.load('Sprites\SwordAir.png'), pygame.image.load('Sprites\SwordAir2.png'), pygame.image.load('Sprites\SwordAir3.png'), pygame.image.load('Sprites\SwordAir4.png'),
                         pygame.image.load('Sprites\SwordAir5.png'), pygame.image.load('Sprites\SwordAir6.png'), pygame.image.load('Sprites\SwordAir7.png'), pygame.image.load('Sprites\SwordAir8.png')]
        self.HurtImg = [pygame.image.load('Sprites\Hurt4.png'),pygame.image.load('Sprites\Hurt3.png'),pygame.image.load('Sprites\Hurt2.png'),pygame.image.load('Sprites\Hurt.png')]
        
        #Doubling the size of all the images
        for x in range(len(self.spriteIdle)):
            self.spriteIdle[x] = pygame.transform.scale2x(self.spriteIdle[x])
        for x in range(len(self.spriteWalk)):
            self.spriteWalk[x] = pygame.transform.scale2x(self.spriteWalk[x])
        for x in range(len(self.spriteJump)):
            self.spriteJump[x] = pygame.transform.scale2x(self.spriteJump[x])
        for x in range(len(self.IdleShot)):
            self.IdleShot[x] = pygame.transform.scale2x(self.IdleShot[x])
        for x in range(len(self.ShotWalk)):
            self.ShotWalk[x] = pygame.transform.scale2x(self.ShotWalk[x])
        for x in range(len(self.LoadWalk)):
            self.LoadWalk[x] = pygame.transform.scale2x(self.LoadWalk[x])
        for x in range(len(self.GunWalk)):
            self.GunWalk[x] = pygame.transform.scale2x(self.GunWalk[x])
        for x in range(len(self.JumpShot)):
            self.JumpShot[x] = pygame.transform.scale2x(self.JumpShot[x])
        for x in range(len(self.SwordIdle)):
            self.SwordIdle[x] = pygame.transform.scale2x(self.SwordIdle[x])
        for x in range(len(self.SwordAir)):
            self.SwordAir[x] = pygame.transform.scale2x(self.SwordAir[x])
        for x in range(len(self.HurtImg)):
            self.HurtImg[x] = pygame.transform.scale2x(self.HurtImg[x])

        #Reversing the lists of backwards animations
        self.ShotWalk.reverse()
        self.LoadWalk.reverse()
        self.GunWalk.reverse()
        self.SwordIdle.reverse()
        self.SwordAir.reverse()

        #Setting up the sequence of animation for shooting while moving (reversed)
        self.ShotAni = [self.IdleShot, self.GunWalk, self.GunWalk, self.GunWalk, self.GunWalk, self.LoadWalk, self.ShotWalk, self.JumpShot]

        #Setting up initial positions and sizes
        self.image = self.spriteIdle[0]
        self.facing = "Right"
        self.rect = self.spriteIdle[0].get_rect()
        self.rect.width -= 10

        #Setting up required variables for animation and player movement/actions
        self.spriteCount = 0
        self.LRCount = 0
        self.shotduration = 0
        self.swordcount = 0
        self.hurt = 0

        #Setting up variables for player attacks
        self.sabrerect = self.SwordIdle[6].get_rect()
        self.sabrerect.width -= 80
        self.chargingbool = False
        self.animation = "Idle"
        self.action = "None"

        # Set up player stats
        self.totalhealth = health
        self.health = health
        
        # Set speed vector of player
        self.change_x = 0
        self.change_y = 0
 
        # List of sprites we can bump against
        self.level = None

        #Setting up the players waiting timer when he enters the boss room
        self.bosswait = 200
        
    def sprite(self):

        #Resetting sprite animations if they cycle past the limit
        if self.spriteCount+1 >= 60:
            self.spriteCount = 0
        if self.LRCount+1 >= 60:
            #Checking whether they are directionally moving in the air or on the ground
            if self.animation != "BAir" and self.animation != "FAir" and self.animation != "NAir":
                self.LRCount = 0
            elif self.rect.y < SCREEN_HEIGHT - self.rect.height:
                self.LRCount = 48
            else:
                self.LRCount = 0

        #Resetting actions variables and counts when the action is over
        if self.shotduration-1 <= 0 and self.action == "Shoot":
            self.action = "None"
        elif self.swordcount-1 <= 0 and self.action == "Sabre":
            self.action = "None"
        elif self.action == "None":
            self.swordcount = 0
            self.shotduration = 0

        #Animations for every possible movement
        if self.facing == "Left":
            #Left sabre animations
            if self.action == "Sabre":
                #Updating the hitbox of the sabre
                self.sabrerect.x = self.rect.x - 25
                self.sabrerect.y = self.rect.y
                if self.animation == "Idle":
                    self.image = pygame.transform.flip(self.SwordIdle[int(self.swordcount/5)],True,False)
                    self.LRCount +=1
                    self.swordcount -=1
                else:
                    self.image = pygame.transform.flip(self.SwordAir[int(self.swordcount/5)],True,False)
                    self.LRCount +=1
                    self.swordcount -=1
            #Left shooting animations
            elif self.action == "Shoot":
                if self.animation == "Idle":
                    self.image = pygame.transform.flip(self.ShotAni[0][int(self.shotduration/10)],True,False)
                    self.shotduration -=1
                elif self.animation == "BAir" or self.animation == "NAir":
                    self.image = pygame.transform.flip(self.JumpShot[int(self.shotduration/20)],True,False)
                    self.LRCount +=1
                    self.shotduration -=4
                else:
                    self.image = pygame.transform.flip(self.ShotAni[int(self.shotduration/10)+1][int(self.LRCount/6)],True,False)
                    self.shotduration -=1
                    self.LRCount +=1
            #Left idle animations
            else:
                if self.animation == "Idle":
                    self.image = self.spriteIdle[int(self.spriteCount/15)]
                    self.spriteCount +=1
                elif self.animation == "Left":
                    self.image = self.spriteWalk[int(self.LRCount/6)]
                    self.LRCount +=1
                    if self.swordcount > 15:
                        #Cancelling sword animation if landing mid action
                        self.swordcount = 1
                else:
                    self.image = self.spriteJump[int(self.LRCount/6)]
                    self.LRCount +=1
                
        else:
            #Right sabre animations
            if self.action == "Sabre":
                #Updating the hitbox of the sabre
                self.sabrerect.x = self.rect.x + 60
                self.sabrerect.y = self.rect.y
                if self.animation == "Idle":
                    self.image = self.SwordIdle[int(self.swordcount/5)]
                    self.swordcount -=1
                else:
                    self.image = self.SwordAir[int(self.swordcount/5)]
                    self.LRCount +=1
                    self.swordcount -=1
            #Right shooting animations
            elif self.action == "Shoot":
                if self.animation == "Idle":
                    self.image = self.ShotAni[0][int(self.shotduration/10)]
                    self.shotduration -=1
                elif self.animation == "FAir" or self.animation == "NAir":
                    self.image = self.JumpShot[int(self.shotduration/20)]
                    self.LRCount +=1
                    self.shotduration -=4
                else:
                    self.image = self.ShotAni[int(self.shotduration/10)+1][int(self.LRCount/6)]
                    self.shotduration -=1
                    self.LRCount +=1
            #Right idle animations
            else:
                if self.animation == "Idle":
                    self.image = pygame.transform.flip(self.spriteIdle[int(self.spriteCount/15)],True,False)
                    self.spriteCount +=1
                elif self.animation == "Right":
                    self.image = pygame.transform.flip(self.spriteWalk[int(self.LRCount/6)],True,False)
                    self.LRCount +=1
                    if self.swordcount > 15:
                        #Cancelling sword animation if landing mid action
                        self.swordcount = 1
                else:
                    self.image = pygame.transform.flip(self.spriteJump[int(self.LRCount/6)],True,False)
                    self.LRCount +=1

        
    def update(self):
        """ Update the player. """
        #Update gravity
        self.calc_grav()
        #Countdown hit cooldown
        if self.hurt >0:
            self.hurt -= 1
        # Move left/right if the player isn't in hit stun animation
        if self.hurt > 60:
            #Play the hit animation
            if self.facing == "Left":
                self.image = pygame.transform.flip(self.HurtImg[int((self.hurt-60)/8)],True,False)
                self.change_x = 1
            else:
                self.image = self.HurtImg[int((self.hurt-60)/8)]
                self.change_x = -1
            self.swordcount = 0
            self.shotduration = 0
            self.action == "None"
            self.rect.x += self.change_x
        else:
            self.rect.x += self.change_x
            self.sprite() #Update the player sprite
            
        #See if we hit any platform
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            # If we are moving right,
            # set our right side to the left side of the item we hit
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = block.rect.right

        # Move up/down
        self.rect.y += self.change_y
    
        #Check and see if we hit any platform
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
 
            # Reset our position based on the top/bottom of the object.
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom
            self.change_y = 0
        #Updatting the direction and animation type of the player
        #If changes are made, reset the movement animation and sword animation counts
        if self.hurt < 60:
            if self.animation!= "FAir" and self.change_x >0 and self.change_y!=0:
                self.animation = "FAir"
                self.facing = "Right"
                spriteCount = 0
            elif self.animation!= "BAir" and self.change_x <0 and self.change_y!=0:
                self.animation = "BAir"
                self.facing = "Left"
                spriteCount = 0
            elif self.animation!= "NAir" and self.change_x ==0 and self.change_y!=0:
                self.animation = "NAir"
                spriteCount = 0
            elif self.animation!= "Idle" and self.change_x == 0 and self.change_y==0:
                self.animation = "Idle"
                self.spriteCount = 0
                self.LRCount = 0
            elif self.animation!= "Right" and self.change_x >0 and self.change_y==0:
                self.animation = "Right"
                self.facing = "Right"
                self.spriteCount = 0
                self.LRCount = 0
                self.swordcount = 1
            elif self.animation!= "Left" and self.change_x <0 and self.change_y==0:
                self.animation = "Left"
                self.facing = "Left"
                self.spriteCount = 0
                self.LRCount = 0
                self.swordcount = 1

        if self.hurt > 60:
            self.change_x = 0

    def calc_grav(self):
        """ Calculate effect of gravity. """
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .35
 
        # See if we are on the ground.
        if self.rect.y >= SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = SCREEN_HEIGHT - self.rect.height
 
    def jump(self):
        """ Called when user hits 'jump' button. """
 
        # move down a bit and see if there is a platform below us.
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 2
 
        # If it is ok to jump, set our speed upwards
        if len(platform_hit_list) > 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.change_y = -12
 
    # Player-controlled movement:
    def go_left(self):
        """ Called when the user hits the left arrow. """
        self.change_x = -6
        #If a change is made, reset the sprite and sword counts and change the animations
        if self.animation!= "Left" and self.change_x <0 and self.change_y==0:
            self.animation = "Left"
            self.facing = "Left"
            self.spriteCount = 0
            self.swordcount = 0
            
    def go_right(self):
        """ Called when the user hits the right arrow. """
        self.change_x = 6
        #If a change is made, reset sprite and sword counts and change the animations
        if self.animation!= "Right" and self.change_x >0 and self.change_y==0:
            self.animation = "Right"
            self.facing = "Right"
            self.spriteCount = 0
            self.swordcount = 0

    def stop(self):
        """ Called when the user lets off the keyboard. """
        self.change_x = 0
        #If stopped, reset the counts and change the animations
        if self.animation!= "Idle" and self.change_x == 0 and self.change_y==0:
            self.animation = "Idle"
            self.spriteCount = 0
            self.LRCount = 0

    def shoot(self):
        """ Called when shooting a bullet """
        #Setting up variables for the shooting animation if called
        self.charged = self.startchar-time.time()
        self.chargingbool = False
        self.action = "Shoot"
        self.shotduration = 58

    def charging(self,starttime):
        """ Called to start charging the gun"""
        #Keep track of charging
        self.startchar = starttime
        self.chargingbool = True

    def sabre(self):
        """ Called to set up the sabre"""
        #Setting up variables for the sabre animation if called
        self.action = "Sabre"
        self.swordcount = 35

    def sabrecheck(self):
        """Check if the sabre is active"""
        #Checking if sabre is still in use
        if self.swordcount > 15:
            return(True)
        else:
            self.swordcount = 1
            return(False)
        
    def takedmg(self,dmg):
        """ Called to make the player take damage"""
        #If there is no hit cooldown then take damage
        if self.hurt <= 0:
            self.health -= dmg
            self.hurt = 90
