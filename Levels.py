""" Alex Fang's Megaman Zero Program, Level Game File """
import pygame, os, random, time
from pygame.locals import *
from Enemy import *

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

FRAMERATE = 40

# Screen dimensions
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600

def load_image(filename):
    """ Load an image from a file.  Return the image and corresponding rectangle """
    image = pygame.image.load(filename)
    image = image.convert_alpha() 
    return image, image.get_rect()    

class Projectile(pygame.sprite.Sprite):
    #Projectile class
    def __init__(self,x,y,charge,image,facing,speed,dmg):
        super().__init__()

        #Setting up the bullet variables for movement, hitbox, and bullet properties
        self.image = pygame.transform.scale2x(image)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.dmg = dmg
        self.charge = charge
        self.angled = False
        self.facing = facing
        self.vely = 0

        #Setting up the velocities depending on where it's facing
        if self.facing == "Left":
            self.image = pygame.transform.flip(self.image,True,False)
            self.velx = speed*-1
        elif self.facing == "Right":
            self.velx = speed
        else:
            #Diagonal movement if facing is a list
            self.velx = int(speed * facing[0])
            self.vely = int(speed * facing[1])
            self.angled = True

    def update(self):
        """Checking if the bullet if off screen and updating it"""
        #Updating the bullets position when it's angled or not and killing it if its off the screen
        if self.angled:
            if self.rect.x < 900 and self.rect.x >0:
                # Moves the bullet by its velocity
                self.rect.x += self.velx 
                self.rect.y += self.vely
            else:
                self.kill()
        else:
            if self.rect.x < 900 and self.rect.x >0:
                # Moves the bullet by its velocity
                self.rect.x += self.velx  
                self.rect.y += self.vely  
            else:
                self.kill()
                
class HealthPick(pygame.sprite.Sprite):
    #Health pickup class
    def __init__(self,x,y,size):
        super().__init__()
        #Setting up the images for the health
        self.sizes = [pygame.transform.scale2x(pygame.image.load('Resources\SmallHealth.png')),
                      pygame.transform.scale2x(pygame.image.load('Resources\BigHealth.png'))]
        self.image = self.sizes[size]
        #Set up the variables for the hitbox and the size of health pickup
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.size = size
        self.change_y = -8 #Initial droping jump height

    def update(self,platform_list):
        #Calculate gravity for the Health
        self.change_y += .35
        self.rect.y += self.change_y
        #Kill it if it's off the level
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

        #Checking if the health hits a block top or bottom
        block_hit_list = pygame.sprite.spritecollide(self, platform_list, False)
        for block in block_hit_list:
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom
            self.change_y = 0
    
class Platform(pygame.sprite.Sprite):
    """ Platform the player can interact with """
    def __init__(self, image):
        """ Platform constructor. Assumes constructed with user passing in
            an image """
        super().__init__()
        #To construct invisible platforms if the image is a list and visible ones if not
        if isinstance(image, list):
            self.image = image[2]
            self.rect = Rect(0,0,image[0],image[1])
        else:
            self.image = image
            self.rect = self.image.get_rect()
        

class Level():
    def __init__(self, player):
        """ Constructor. Pass in a handle to player. Needed for when moving
            platforms collide with the player. """
        #Setting up item groups, enemies, player, sidescrolling variable and the background image
        self.platform_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.bullet_list = pygame.sprite.Group()
        self.enemybullet_list = pygame.sprite.Group()
        self.fly_list = pygame.sprite.Group()
        self.roller_list = pygame.sprite.Group()
        self.healths_list = pygame.sprite.Group()
        self.guarders_list = pygame.sprite.Group()
        self.normalenemies = pygame.sprite.Group()
        self.player = player
        self.boss = False #Initially set the boss as false until he exists

        self.world_shift = 0
 
    def update(self):
        """ Update everything in this level."""
        self.platform_list.update()
        self.normalenemies.update()
        self.bullet_list.update()
        self.enemybullet_list.update()
        self.roller_list.update(self.platform_list)
        self.healths_list.update(self.platform_list)
        #Update the boss if it exists
        if self.boss != False:
            self.boss.update()
 
    def draw(self, screen):
        """Draw all platforms, enemies and bullets"""
        screen.blit(self.backimage,self.backrect)
        self.platform_list.draw(screen)
        self.normalenemies.draw(screen)
        self.roller_list.draw(screen)
        self.healths_list.draw(screen)
        #Draw the boss if he exists and his wings if it is fighting
        if self.boss != False:
            if self.boss.spawncount == 0 and self.boss.deathcount == 0:
                screen.blit(self.boss.wings[int(self.boss.wingcount/10)],self.boss.wingrect)
            screen.blit(self.boss.image,self.boss.rect)
        self.bullet_list.draw(screen)
        self.enemybullet_list.draw(screen)
        
    def shift_world(self, shift_x):
        """Shift every sprite and playfor in the level"""
        # Keep track of the shift amount
        self.world_shift += shift_x
        
        # Go through all the sprite lists and shift
        for platform in self.platform_list:
            platform.rect.x += shift_x
 
        for enemy in self.enemy_list:
            enemy.rect.x += shift_x

        for fly in self.fly_list:
            fly.rect.x += shift_x

        for bullet in self.bullet_list:
            bullet.rect.x += shift_x

        for ebullet in self.enemybullet_list:
            ebullet.rect.x += shift_x

        for roller in self.roller_list:
            roller.rect.x += shift_x

        for healths in self.healths_list:
            healths.rect.x += shift_x

        for guard in self.guarders_list:
            guard.truex += shift_x
            guard.rect.x += shift_x
            
        
# Create platforms for the level
class Level_01(Level):
    """ Definition for level 1. """
 
    def __init__(self, player):
        """ Create level 1. """
        # Call the parent constructor
        Level.__init__(self, player)
        #Setting up level limit and all the images for the level
        self.level_limit = -7500
        self.backimage, self.backrect = load_image("Resources\BackStart.png")
        self.platimages = [pygame.transform.scale2x(pygame.image.load('Resources\Platform160x32.png')),
                           pygame.transform.scale2x(pygame.image.load('Resources\Platform1.png')),
                           pygame.transform.scale2x(pygame.image.load('Resources\Platform2.png')),
                           pygame.transform.scale2x(pygame.image.load('Resources\Platform3.png')),
                           pygame.transform.scale2x(pygame.image.load('Resources\Platform4.png'))]
 
        #Arrays with the enemies, platforms and health for the level
        
        level = [[1,0,390], [2,1500,300],[3,3200,350], [3,3500,400], [3,3800,300],  [3,4100,350],
                [3,4450,420], [2,4800,300], [2,6300,400] , [4,7578,400]]
        Basicenemies = [[950,SCREEN_HEIGHT - 275],[1600,SCREEN_HEIGHT - 365],
                        [2500,SCREEN_HEIGHT - 365],[5100,SCREEN_HEIGHT - 365],[5500,SCREEN_HEIGHT - 365],
                        [6500,SCREEN_HEIGHT - 265],[8000,SCREEN_HEIGHT - 265],[8500,SCREEN_HEIGHT - 265]]
        Flys = [[2000, 70],[2700,60],[3350,45],[3700,30],[4275,55],[5275,85],[7000,100],[7500,100]]
        Rollers = [[1600,SCREEN_HEIGHT - 350],[2300, SCREEN_HEIGHT - 350],[2900,SCREEN_HEIGHT - 350],
                   [5000,SCREEN_HEIGHT - 350],[7000,SCREEN_HEIGHT - 250],[7500,SCREEN_HEIGHT - 250]]
        Healths = [[800,300,0]]
        
        #Go through the arrays above and adding platforms, enemies and health
        for platform in level:
            block = Platform(self.platimages[platform[0]])
            block.rect.x = platform[1]
            block.rect.y = platform[2]
            block.player = self.player
            self.platform_list.add(block)
        
        for enemy in Basicenemies:
            botmob = Basicenemy(enemy[0],enemy[1])
            self.enemy_list.add(botmob)
            self.normalenemies.add(botmob)

        for fly in Flys:
            flymob = Fly(fly[0],fly[1])
            self.fly_list.add(flymob)
            self.normalenemies.add(flymob)

        for roller in Rollers:
            rollmob = Roller(roller[0],roller[1])
            self.roller_list.add(rollmob)

        for hp in Healths:
            drop = HealthPick(hp[0],hp[1],hp[2])
            self.healths_list.add(drop)


# Create platforms for the level
class Level_02(Level):
    """ Definition for level 2. """
 
    def __init__(self, player):
        """ Create level 1. """
        # Call the parent constructor
        Level.__init__(self, player)
        #Setting up level limit and all the images for the level
        self.level_limit = -5945
        self.backimage, self.backrect = load_image("Resources\Level2.png")
        self.platimages = [pygame.image.load('Resources\Empty.png')]
        
        #Arrays with the enemies, invisible platforms and health for the level
        
        level = [[[788,413,self.platimages[0]],0,413],[[306,300,self.platimages[0]],788,300],
                 [[295,375,self.platimages[0]],1089,225],[[227,260,self.platimages[0]],1384,340],
                 [[226,185,self.platimages[0]],1611,415],[[190,185,self.platimages[0]],1950,415],
                 [[265,185,self.platimages[0]],2260,415],[[145,261,self.platimages[0]],2525,339],
                 [[302,147,self.platimages[0]],2670,453],[[223,300,self.platimages[0]],2975,300],
                 [[680,185,self.platimages[0]],3197,415],[[295,260,self.platimages[0]],3877,340],
                 [[145,255,self.platimages[0]],4555,345],[[145,255,self.platimages[0]],5083,345],
                 [[85,180,self.platimages[0]],5000,420],[[330,220,self.platimages[0]],5685,380],
                 [[330,220,self.platimages[0]],6815,380],[[2700,145,self.platimages[0]],4172,455],
                 
                 [[6600,32,self.platimages[0]],0,0],[[105,300,self.platimages[0]],0,0],
                 [[145,225,self.platimages[0]],105,0],[[225,150,self.platimages[0]],255,0],
                 [[225,70,self.platimages[0]],480,0],[[70,75,self.platimages[0]],4292,153],
                 [[940,32,self.platimages[0]],4365,191],[[110,265,self.platimages[0]],5912,0],
                 [[110,265,self.platimages[0]],6815,0]]
        
        Basicenemies = [[836,235],[2000,350],[3017,238],[4050,273],[4600,273],[5100,122],[5090,273]]
        Flys = [[1890, 110],[2400,100],[3520,106],[5620,90]]
        Rollers = [[975,215],[2550, 250],[3050,225],[3900,255],[5200,105],[5800,290]]
        Healths = [[4585,160,1],[4710,160,1],[4840,160,1],[6450,400,1]]
        Guarders = [[650,320],[1250,132],[1525,245],[2375,320],[4450,360],[5775,282]]

        #Go through the arrays above and adding the invisible platforms, enemies and health
        for platform in level:
            block = Platform(platform[0])
            block.rect.x = platform[1]
            block.rect.y = platform[2]
            block.player = self.player
            self.platform_list.add(block)
            
        for enemy in Basicenemies:
            botmob = Basicenemy(enemy[0],enemy[1])
            self.enemy_list.add(botmob)
            self.normalenemies.add(botmob)

        for fly in Flys:
            flymob = Fly(fly[0],fly[1])
            self.fly_list.add(flymob)
            self.normalenemies.add(flymob)

        for roller in Rollers:
            rollmob = Roller(roller[0],roller[1])
            self.roller_list.add(rollmob)

        for hp in Healths:
            drop = HealthPick(hp[0],hp[1],hp[2])
            self.healths_list.add(drop)

        for guard in Guarders:
            guardman = Guarder(guard[0],guard[1])
            self.guarders_list.add(guardman)
            self.normalenemies.add(guardman)
            
class BossLvl(Level):
    """Definition for boss level."""
    def __init__(self, player):
        # Call the parent constructor
        Level.__init__(self, player)
        #Setting up level limit and all the images for the level
        self.level_limit = 0
        self.backimage, self.backrect = load_image("Resources\Bosslvl.png")
        self.platimages = [pygame.image.load('Resources\Empty.png'),pygame.image.load('Resources\Platform160x32.png')]
        
        #Arrays with the enemies, invisible platforms and health for the level
        
        level = [[[900,22,self.platimages[0]],0,578],[[900,23,self.platimages[0]],0,0],
                [[25,600,self.platimages[0]],0,0],[[28,600,self.platimages[0]],872,0],
                [self.platimages[1],125,400],[self.platimages[1],615,400]]

        #Go through the arrays above and adding the invisible platforms, platforms, and the boss
        for platform in level:
            block = Platform(platform[0])
            block.rect.x = platform[1]
            block.rect.y = platform[2]
            block.player = self.player
            self.platform_list.add(block)

        self.boss = Boss(450,0)
