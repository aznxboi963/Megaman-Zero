""" Alex Fang's Megaman Zero Program, Main Game File """
 
import pygame, os, random, time, math
from Player import *
from Levels import *
from Enemy import *
from pygame.locals import *

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0,255,255)

FRAMERATE = 60
 
# Screen dimensions
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600

def terminate():
    """ This function is called when the user closes the window or presses ESC """
    pygame.quit()
    os._exit(1)
    
def drawText(text, font, surface, x, y, textcolour):
    """ Draws the text on the surface at the location specified """
    textobj = font.render(text, 1, textcolour)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def display_menu(screen,clock,music):
    """ Displays the menu so the user can choose what to do """
    chosen = False #Boolean variable for if the player chose yet
    #Loading all menu images
    screens = [pygame.image.load('Resources\Menu1.png'), pygame.image.load('Resources\Menu2.png'),
               pygame.image.load('Resources\Menu3.png'), pygame.image.load('Resources\Menu4.png')]
    controlscreens =[pygame.image.load('Resources\Controls.png'),pygame.image.load('Resources\Controls.png'),
                     pygame.image.load('Resources\Controls.png'),pygame.image.load('Resources\Controls2.png')]
    #Setting up variables for cycling through the screen animation
    screenCount = 0
    change = 1
    screenrect = screens[0].get_rect()
    
    controls = False #Boolean variable for if the player is in the menu screen
    
    musicPlaying = music #Music variable for if it's active
    if musicPlaying:
        pygame.mixer.music.load('Music\IntroScreen.mp3') #Loading the intro music
        pygame.mixer.music.play(-1, 0.0) #Playing the intro music
    
    #While loop that loops through the menu animations and checks for player input
    while not chosen:
        #Changing the direction of the screenCount to loop animation
        if screenCount+1 >= 60 and change == 1:
            change = change*-1
        elif screenCount-1 <= 0 and change == -1:
            change = change*-1
        #Initial menu showing which tracks for 1,2,quit and mute
        if not controls:
            screen.blit(screens[int(screenCount/15)],screenrect)
            screenCount += change
            for event in pygame.event.get():
                if event.type == QUIT:
                    terminate()
                elif event.type== KEYDOWN:
                    if event.key == ord('1'):
                        chosen = True
                        Health = 100
                        pygame.mixer.music.stop()
                    elif event.key == ord('2'):
                        controls = True
                    elif event.key == ord('m'):
                        if musicPlaying:
                            pygame.mixer.music.stop()
                        else:
                            pygame.mixer.music.play(-1, 0.0)
                        musicPlaying = not musicPlaying
                    elif event.key == ord('o'):
                        chosen = True
                        Health = 1000
                        pygame.mixer.music.stop()
        #Control menu which tracks for b,quit and mute
        else:
            screen.blit(controlscreens[int(screenCount/15)],screenrect)
            screenCount += change
            for event in pygame.event.get():
                if event.type == QUIT:
                    terminate()
                elif event.type== KEYDOWN:
                    if event.key == ord('b'):
                        controls = False
                    if event.key == ord('m'):
                        if musicPlaying:
                            pygame.mixer.music.stop()
                        else:
                            pygame.mixer.music.play(-1, 0.0)
                        musicPlaying = not musicPlaying

        #Going through a frame
        clock.tick(FRAMERATE)
 
        #Updating the screen
        pygame.display.flip()
    #Returning the variables needed to start the game
    info=[Health,musicPlaying]
    return info

class Game():
    def __init__(self, info): 
        #Creates the player with the health
        self.health = info[0]
        self.musicPlaying = info[1]
        self.player = Player(self.health)

        #Loading all the images and doubling the sprites that are too small
        self.bullets = [pygame.image.load('Sprites\Bullet.png'),pygame.image.load('Sprites\BulletBig.png'),
                        pygame.image.load('Sprites\BulletBig2.png')]
        self.EnemyBullet = pygame.image.load('Enemies\BasicBullet.png')
        self.statuses = [pygame.transform.scale2x(pygame.image.load('Resources\Health.png')),
                         pygame.transform.scale2x(pygame.image.load('Resources\Health2.png')),
                         pygame.transform.scale2x(pygame.image.load('Resources\Health3.png')),
                         pygame.transform.scale2x(pygame.image.load('Resources\BossHealth.png'))]
        self.BulletHit = [pygame.transform.scale2x(pygame.image.load('Sprites\BulletBlow2.png')),
                          pygame.transform.scale2x(pygame.image.load('Sprites\BulletBlow.png')),
                          pygame.transform.scale2x(pygame.image.load('Sprites\BulletBlow1.png'))]

        #Setting up the player status bar
        self.statusrect = self.statuses[0].get_rect()
        self.statusrect.x = 50
        self.statusrect.y = 50

        #Setting up the bosses status bar
        self.bossstatrect = self.statuses[3].get_rect()
        self.bossstatrect.x = 820
        self.bossstatrect.y = 50
        
        #Create all the levels and adding it to a level list
        self.level_list = []
        self.level_list.append(Level_01(self.player))
        self.level_list.append(Level_02(self.player))
        self.level_list.append(BossLvl(self.player))

        #Setting up the players initial position and music for each level
        self.level_pos = [[150,SCREEN_HEIGHT - self.player.rect.height - 210, "Music\Stage.mp3"],
                          [15,405 - self.player.rect.height,"Music\Level2.mp3"],[60,450,"Music\Boss.mp3"]]

        #Setup the current level with the variables required for the game
        self.game_over = False
        self.starttime = 0 #Start time to allow for the charging of the gun
        self.current_level_no = 0 #Current level number
        self.current_level = self.level_list[self.current_level_no]
        self.active_sprite_list = pygame.sprite.Group() #Player's active sprite list group
        self.player.level = self.current_level
        self.explodelist = [] #List of bullet explosions

        #Setting up the players position and adding him to the active sprite list
        self.player.rect.x = self.level_pos[self.current_level_no][0]
        self.player.rect.y = self.level_pos[self.current_level_no][1]
        self.active_sprite_list.add(self.player)

        #Setting up music and sound effects
        pygame.mixer.music.load(self.level_pos[self.current_level_no][2])
        self.shoot = pygame.mixer.Sound('Music\Shot1.wav')
        self.sabre = pygame.mixer.Sound('Music\Sabre1.wav')
        self.dead = pygame.mixer.Sound('Music\Death.wav')
        self.hit = pygame.mixer.Sound('Music\Hit1.wav')

        #Check if music should be playing
        if self.musicPlaying:
            pygame.mixer.music.play(-1, 0.0)
        

    def process_events(self):
        """Processing all the key inputs from the user"""
        #Not allowing the player to move if they are on the boss level and the timer is more than zero
        if self.player.bosswait>0 and self.current_level_no == 2:
            self.player.bosswait-=1
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == pygame.KEYDOWN:
                    #Check if the player is using the sabre
                    if not self.player.sabrecheck():
                        #Check for keydown on movement and attacks
                        if event.key == pygame.K_LEFT or event.key == ord('a'):
                            self.player.go_left()
                        if event.key == pygame.K_RIGHT or event.key == ord('d'):
                            self.player.go_right()
                        if event.key == pygame.K_UP or event.key == ord('w') or event.key == pygame.K_SPACE:
                            #Check if he's in hitstun before jumping
                            if self.player.hurt < 60:
                                self.player.jump()
                        if event.key == ord('t'):
                            #Start charging the gun
                            self.starttime=time.time()
                            self.player.charging(self.starttime)
                        if event.key == ord('y'):
                            #Sabre activates and plays the sound effect if not hit stunned
                            if self.player.hurt < 60:
                                self.player.shotduration = 0
                                if self.player.change_y ==0:
                                    #Stop player movement if they are on the ground
                                    self.player.stop()
                                    self.player.sabre()
                                    if self.musicPlaying:
                                        self.sabre.play()
                                else:
                                    self.player.sabre()
                                    if self.musicPlaying:
                                        self.sabre.play()
                        if event.key == ord('m'):
                            # toggles the background music
                            if self.musicPlaying:
                                pygame.mixer.music.stop()
                            else:
                                pygame.mixer.music.play(-1, 0.0)
                            self.musicPlaying = not self.musicPlaying
     
                if event.type == pygame.KEYUP:
                    #Check for letting go of a movement key and stopping the player
                    if (event.key == pygame.K_LEFT or event.key == ord('a')) and self.player.change_x < 0:
                        if self.player.swordcount <15:
                            #Reset sword if cancel sword animation midair
                            self.player.swordcount = 1
                        self.player.stop()
                    if (event.key == pygame.K_RIGHT or event.key == ord('d')) and self.player.change_x > 0:
                        self.player.stop()
                        if self.player.swordcount <15:
                            #Reset sword if cancel sword animation midair
                            self.player.swordcount = 1
                    #Shooting with the amount of charge they charged up
                    if event.key == ord('t'):
                        #Check the cooldown for the gun and hitstun
                        if self.player.shotduration <= 45 and self.player.chargingbool == True and self.player.hurt < 60:
                            self.player.shoot()
                            #Assigning bullet type based on charge time
                            if self.chargingtime < 1:
                                self.bullettype = 0
                                self.bulspeed = 12
                                self.chargingtime = 0
                                self.buldmg = 18
                            elif self.chargingtime == 1:
                                self.bullettype = 1
                                self.bulspeed = 14
                                self.chargingtime = 0
                                self.buldmg = 50
                            else:
                                self.bullettype = 2
                                self.bulspeed = 16
                                self.chargingtime = 0
                                self.buldmg = 100
                            #Set the direction of the bullet
                            if self.player.facing == "Left":
                                self.starting = self.player.rect.left-5
                            else:
                                self.starting = self.player.rect.right-5
                            #Creating the bullet and adding it to the sprite list
                            self.bullet = Projectile(self.starting, self.player.rect.y+25, self.chargingtime,
                                                   self.bullets[self.bullettype], self.player.facing, self.bulspeed, self.buldmg)
                            self.current_level.bullet_list.add(self.bullet)
                            #Reset the charge time and play the sound effect
                            self.chargingtime = 0
                            if self.musicPlaying:
                                self.shoot.play()
            

    def run_logic(self,screen):
        #Update the player.
        self.active_sprite_list.update()
 
        #Update items in the level
        self.current_level.update()

        #Running the logic for the basic enemy
        for enemy in self.current_level.enemy_list:
            #Checking if the basic enemy is on the screen
            if enemy.rect.right > 0 and enemy.rect.x < SCREEN_WIDTH:
                #Check for collision between my bullets and the enemy
                attack = pygame.sprite.spritecollide(enemy, self.current_level.bullet_list, True)
                for myhits in attack:
                    #Make the enemy take damage for an attack and have a chance to drop health if killed
                    if enemy.takedmg(myhits.dmg):
                        randomchance = random.randrange(0,6)
                        if randomchance%3 == 0:
                            Pickup = HealthPick(enemy.rect.centerx, enemy.rect.centery, 0)
                            self.current_level.healths_list.add(Pickup)
                        elif randomchance == 5:
                            Pickup = HealthPick(enemy.rect.centerx, enemy.rect.centery, 1)
                            self.current_level.healths_list.add(Pickup)
                        enemy.kill()
                    #Add the bullet explosion where the bullet hit
                    self.explodelist.append([self.BulletHit,myhits.rect.right, myhits.rect.y, 6])
                #Shoot if the cooldown is over
                if self.player.rect.bottom >= enemy.rect.top and self.player.rect.top <= enemy.rect.bottom:
                    if enemy.shotduration <= 0:
                        enemy.shoot()
                #Change the way the enemy is facing
                if enemy.rect.x > self.player.rect.x:
                    enemy.facing = "Left"
                else:
                    enemy.facing = "Right"
                #Shoot when the cooldown matches the animation of the enemy shooting which is frame 15
                if enemy.shotduration == 15:
                    if enemy.facing == "Left":
                        starting = enemy.rect.left-5
                    else:
                        starting = enemy.rect.right-5
                    #Adding the enemy bullet
                    enemybullet = Projectile(starting, enemy.rect.y+15, 0 ,self.EnemyBullet, enemy.facing, 10, 10)
                    self.current_level.enemybullet_list.add(enemybullet)

        #Running the logic for the fly
        for fly in self.current_level.fly_list:
            #Checking if the fly is on the screen
            if fly.rect.right > 0 and fly.rect.x < SCREEN_WIDTH:
                #Check for collision between my bullets and the enemy
                attack = pygame.sprite.spritecollide(fly, self.current_level.bullet_list, True)
                for myhits in attack:
                    #Make the enemy take damage for an attack and have a chance to drop health if killed
                    if fly.takedmg(myhits.dmg):
                        randomchance = random.randrange(0,6)
                        if randomchance%3 == 0:
                            Pickup = HealthPick(fly.rect.centerx, fly.rect.centery, 0)
                            self.current_level.healths_list.add(Pickup)
                        elif randomchance == 5:
                            Pickup = HealthPick(fly.rect.centerx, fly.rect.centery, 1)
                            self.current_level.healths_list.add(Pickup)
                        fly.kill()
                    #Add the bullet explosion where the bullet hit
                    self.explodelist.append([self.BulletHit,myhits.rect.right, myhits.rect.y, 6])
                #Shoot if the cooldown is over
                if fly.shotduration <= 0:
                    fly.shoot()
                    xdiff = (self.player.rect.centerx - fly.rect.centerx-10)
                    ydiff = (self.player.rect.centery - fly.rect.centery+10)
                    #Calculating the angle of tragectory for the bullet to hit near the player and adding the bullet to the projectile list.
                    if abs(xdiff)<ydiff:
                        xratio = xdiff/(abs(ydiff)+abs(xdiff))
                        yratio = ydiff/(abs(ydiff)+abs(xdiff))
                        #Calculating the speed of the bullet and creating it (10 speed)
                        flyspeed = math.sqrt(xratio**2+yratio**2)*10
                        flybullet = Projectile(fly.rect.centerx-10, fly.rect.centery+10, 0 ,self.EnemyBullet, [xratio,yratio] , flyspeed, 10)
                        self.current_level.enemybullet_list.add(flybullet)
                    else:
                        yratio = ydiff/(abs(ydiff)+abs(xdiff))
                        xratio = xdiff/(abs(ydiff)+abs(xdiff))
                        #Calculating the speed of the bullet and creating it (10 speed)
                        flyspeed = math.sqrt(xratio**2+yratio**2)*10
                        flybullet = Projectile(fly.rect.centerx-10, fly.rect.centery+10, 0 ,self.EnemyBullet, [xratio,yratio] , flyspeed, 10)
                        self.current_level.enemybullet_list.add(flybullet)

        for roller in self.current_level.roller_list:
            #Checking if the roller is on the screen
            if roller.rect.right > 0 and roller.rect.x < SCREEN_WIDTH:
                #Check for collision between my bullets and the enemy
                attack = pygame.sprite.spritecollide(roller, self.current_level.bullet_list, True)
                for myhits in attack:
                    #Make the enemy take damage for an attack and have a chance to drop health if killed
                    if roller.takedmg(myhits.dmg):
                        randomchance = random.randrange(0,6)
                        if randomchance%3 == 0:
                            Pickup = HealthPick(roller.rect.centerx, roller.rect.centery, 0)
                            self.current_level.healths_list.add(Pickup)
                        elif randomchance == 5:
                            Pickup = HealthPick(roller.rect.centerx, roller.rect.centery, 1)
                            self.current_level.healths_list.add(Pickup)
                        roller.kill()
                    #Add the bullet explosion where the bullet hit
                    self.explodelist.append([self.BulletHit,myhits.rect.right, myhits.rect.y, 6])

        for guards in self.current_level.guarders_list:
            #Checking if the guard is on the screen
            if guards.rect.right > 0 and guards.rect.x < SCREEN_WIDTH:
                #Check for collision between my bullets and the enemy
                attack = pygame.sprite.spritecollide(guards, self.current_level.bullet_list, False)
                for myhits in attack:
                    #Make the enemy take damage for an attack if their not guarding and have a chance to drop health if killed
                    if not guards.guard:
                        if guards.takedmg(myhits.dmg):
                            randomchance = random.randrange(0,6)
                            if randomchance%3 == 0:
                                Pickup = HealthPick(guards.rect.centerx, guards.rect.centery, 0)
                                self.current_level.healths_list.add(Pickup)
                            elif randomchance == 5:
                                Pickup = HealthPick(guards.rect.centerx, guards.rect.centery, 1)
                                self.current_level.healths_list.add(Pickup)
                            guards.kill()
                        myhits.kill()
                        self.explodelist.append([self.BulletHit,myhits.rect.right, myhits.rect.y, 6])
                    elif myhits.facing == guards.facing:
                        #Make the enemy take damage if they geet hit from behind and have a chance to drop health if killed
                        if guards.takedmg(myhits.dmg):
                            randomchance = random.randrange(0,6)
                            if randomchance%3 == 0:
                                Pickup = HealthPick(guards.rect.centerx, guards.rect.centery, 0)
                                self.current_level.healths_list.add(Pickup)
                            elif randomchance == 5:
                                Pickup = HealthPick(guards.rect.centerx, guards.rect.centery, 1)
                                self.current_level.healths_list.add(Pickup)
                            guards.kill()
                        myhits.kill()
                        self.explodelist.append([self.BulletHit,myhits.rect.right, myhits.rect.y, 6])
                    else:
                        #If the bullet is guarded then reflect it and make it an enemy bullet
                        myhits.velx = myhits.velx*-1
                        myhits.image = pygame.transform.flip(myhits.image,True,False)
                        myhits.remove(self.current_level.bullet_list)
                        myhits.add(self.current_level.enemybullet_list)

        #Check if they are at the boss level
        if self.current_level_no == 2:
            #Check if the boos is on the screen
            if self.current_level.boss.rect.right > 0 and self.current_level.boss.rect.x < SCREEN_WIDTH:
                #Check if any player bullets hit the boss
                for myhits in self.current_level.bullet_list:
                    if pygame.Rect.colliderect(self.current_level.boss.hitboxrect, myhits.rect):
                        self.current_level.boss.takedmg(myhits.dmg)
                        myhits.kill()
                #Check if the idle duration of the boss is over
                if self.current_level.boss.idlecount == 120 and self.current_level.boss.action == "Idle":
                    #If it is randomly choose either to shoot bullets or summon enemies
                    self.current_level.boss.idlecount = 0
                    bossattack = random.randrange(0,2)
                    #Set the action of the boss and the action count
                    if bossattack == 0:
                        self.current_level.boss.action = "Bullet"
                        self.current_level.boss.bulletcount = 159
                    else:
                        self.current_level.boss.action = "Summon"
                        self.current_level.boss.summoncount = 59
                #Check if the action count has ending and switch the boss back to idle
                elif self.current_level.boss.bulletcount == 0 and self.current_level.boss.action == "Bullet":
                    self.current_level.boss.action = "Idle"
                elif self.current_level.boss.summoncount == 0 and self.current_level.boss.action == "Summon":
                    self.current_level.boss.action = "Idle"

                #IF the action is bullet, every 20 frame the bossshoots a bullet from both it's hands
                if self.current_level.boss.action == "Bullet" and self.current_level.boss.bulletcount < 120:
                    if self.current_level.boss.bulletcount%20 == 0:
                        #Calculating the distance between the player and the initial shot
                        xdiff = (self.player.rect.centerx - self.current_level.boss.rect.centerx+60)
                        ydiff = (self.player.rect.centery - self.current_level.boss.rect.centery)
                        #Calculating the angle of tragectory for the bullet to hit near the player and adding the bullet to the projectile list.
                        if abs(xdiff)<ydiff:
                            xratio = xdiff/(abs(ydiff)+abs(xdiff))
                            yratio = ydiff/(abs(ydiff)+abs(xdiff))
                            #Calculating the speed of the bullet and creating it (15 speed)
                            bossspeed = math.sqrt(xratio**2+yratio**2)*15
                            bossbullet = Projectile(self.current_level.boss.rect.centerx-60, self.current_level.boss.rect.centery, 0 ,self.EnemyBullet, [xratio,yratio] , bossspeed, 10)
                            self.current_level.enemybullet_list.add(bossbullet)
                        else:
                            yratio = ydiff/(abs(ydiff)+abs(xdiff))
                            xratio = xdiff/(abs(ydiff)+abs(xdiff))
                            #Calculating the speed of the bullet and creating it (15 speed)
                            bossspeed = math.sqrt(xratio**2+yratio**2)*15
                            bossbullet = Projectile(self.current_level.boss.rect.centerx-60, self.current_level.boss.rect.centery, 0 ,self.EnemyBullet, [xratio,yratio] , bossspeed, 10)
                            self.current_level.enemybullet_list.add(bossbullet)
                        #Calculating the distance between the player and the initial shot
                        xdiff = (self.player.rect.centerx - self.current_level.boss.rect.centerx-60)
                        ydiff = (self.player.rect.centery - self.current_level.boss.rect.centery)
                        #Calculating the angle of tragectory for the bullet to hit near the player and adding the bullet to the projectile list.
                        if abs(xdiff)<ydiff:
                            xratio = xdiff/(abs(ydiff)+abs(xdiff))
                            yratio = ydiff/(abs(ydiff)+abs(xdiff))
                            #Calculating the speed of the bullet and creating it (15 speed)
                            bossspeed = math.sqrt(xratio**2+yratio**2)*15
                            bossbullet = Projectile(self.current_level.boss.rect.centerx+60, self.current_level.boss.rect.centery, 0 ,self.EnemyBullet, [xratio,yratio] , bossspeed, 10)
                            self.current_level.enemybullet_list.add(bossbullet)
                        else:
                            yratio = ydiff/(abs(ydiff)+abs(xdiff))
                            xratio = xdiff/(abs(ydiff)+abs(xdiff))
                            #Calculating the speed of the bullet and creating it (15 speed)
                            bossspeed = math.sqrt(xratio**2+yratio**2)*15
                            bossbullet = Projectile(self.current_level.boss.rect.centerx+60, self.current_level.boss.rect.centery, 0 ,self.EnemyBullet, [xratio,yratio] , bossspeed, 10)
                            self.current_level.enemybullet_list.add(bossbullet)

                #Summoning 2 mobs at the last 20 frames of the animation
                elif self.current_level.boss.action == "Summon" and self.current_level.boss.summoncount <= 20:
                    if self.current_level.boss.summoncount%10 == 0:
                        #Random chance to summon a rolle or a fly mob
                        summon = random.randrange(0,2)
                        if summon == 0:
                            rollmob = Roller(self.current_level.boss.rect.centerx,500)
                            self.current_level.roller_list.add(rollmob)
                        else:
                            flymob = Fly(random.randrange(100,700),150) #Random x position for the fly
                            self.current_level.fly_list.add(flymob)
                            self.current_level.normalenemies.add(flymob)
                            

        #Check if enemy or player bullets collide with the platforms
        for platform in self.current_level.platform_list:
            hits = pygame.sprite.spritecollide(platform, self.current_level.bullet_list, True)
            ehits = pygame.sprite.spritecollide(platform, self.current_level.enemybullet_list, True)

        #If the player is not in sabre mode, take damage from enemy collisions
        if not self.player.sabrecheck():
            
            rollercollide = pygame.sprite.spritecollide(self.player, self.current_level.roller_list, False)
            basiccollide = pygame.sprite.spritecollide(self.player, self.current_level.normalenemies, False)
            #Take damage for collisions and play the damage sound effect if not in hit cooldown
            
            for rcollide in rollercollide:
                if self.player.hurt<=0:
                    if self.musicPlaying:
                        self.hit.play()
                    self.player.takedmg(20)
                    
            for bcollide in basiccollide:
                if self.player.hurt<=0:
                    if self.musicPlaying:
                        self.hit.play()
                    self.player.takedmg(20)
                    
            if self.current_level_no == 2:
                if pygame.Rect.colliderect(self.player.rect, self.current_level.boss.hitboxrect):
                    if self.player.hurt<=0:
                        if self.musicPlaying:
                            self.hit.play()
                        self.player.takedmg(20)

        else:
            #If the player is in sabre, it can cut enemy bullets
            if self.player.swordcount >25:
                for enemybullet in self.current_level.enemybullet_list:
                    if pygame.Rect.colliderect(self.player.sabrerect, enemybullet.rect):
                        enemybullet.kill()
            #Check for collision between enemies and the sabre rectangle, takes damage when hit and has a chance to drop health
            for enemy in self.current_level.enemy_list:
                if pygame.Rect.colliderect(self.player.sabrerect, enemy.rect):
                    if enemy.takedmg(100):
                        randomchance = random.randrange(0,6)
                        if randomchance%3 == 0:
                            Pickup = HealthPick(enemy.rect.centerx, enemy.rect.centery, 0)
                            self.current_level.healths_list.add(Pickup)
                        elif randomchance == 5:
                            Pickup = HealthPick(enemy.rect.centerx, enemy.rect.centery, 1)
                            self.current_level.healths_list.add(Pickup)
                        enemy.kill()
            for fly in self.current_level.fly_list:
                if pygame.Rect.colliderect(self.player.sabrerect, fly.rect):
                    if fly.takedmg(100):
                        randomchance = random.randrange(0,6)
                        if randomchance%3 == 0:
                            Pickup = HealthPick(fly.rect.centerx, fly.rect.centery, 0)
                            self.current_level.healths_list.add(Pickup)
                        elif randomchance == 5:
                            Pickup = HealthPick(fly.rect.centerx, fly.rect.centery, 1)
                            self.current_level.healths_list.add(Pickup)
                        fly.kill()
            for roller in self.current_level.roller_list:
                if pygame.Rect.colliderect(self.player.sabrerect, roller.rect):
                    if roller.takedmg(100):
                        randomchance = random.randrange(0,6)
                        if randomchance%3 == 0:
                            Pickup = HealthPick(roller.rect.centerx, roller.rect.centery, 0)
                            self.current_level.healths_list.add(Pickup)
                        elif randomchance == 5:
                            Pickup = HealthPick(roller.rect.centerx, roller.rect.centery, 1)
                            self.current_level.healths_list.add(Pickup)
                        roller.kill()
            for guards in self.current_level.guarders_list:
                if pygame.Rect.colliderect(self.player.sabrerect, guards.rect):
                    #Take damage only when off guard or when the player is behind them
                    if not guards.guard:
                        if guards.takedmg(100):
                            randomchance = random.randrange(0,6)
                            if randomchance%3 == 0:
                                Pickup = HealthPick(guards.rect.centerx, guards.rect.centery, 0)
                                self.current_level.healths_list.add(Pickup)
                            elif randomchance == 5:
                                Pickup = HealthPick(guards.rect.centerx, guards.rect.centery, 1)
                                self.current_level.healths_list.add(Pickup)
                            guards.kill()
                    elif self.player.facing == guards.facing:
                        if guards.takedmg(100):
                            randomchance = random.randrange(0,6)
                            if randomchance%3 == 0:
                                Pickup = HealthPick(guards.rect.centerx, guards.rect.centery, 0)
                                self.current_level.healths_list.add(Pickup)
                            elif randomchance == 5:
                                Pickup = HealthPick(guards.rect.centerx, guards.rect.centery, 1)
                                self.current_level.healths_list.add(Pickup)
                            guards.kill()
            if self.current_level_no == 2:
                if pygame.Rect.colliderect(self.player.sabrerect, self.current_level.boss.hitboxrect):
                    self.current_level.boss.takedmg(100)

        #Checking for collisions between the player and enemy bullets
        damage = pygame.sprite.spritecollide(self.player, self.current_level.enemybullet_list, True)
        for hits in damage:
            #Take damage and play the sound if they are not on hit cooldown
            if self.player.hurt<=0:
                if self.musicPlaying:
                    self.hit.play()
                self.player.takedmg(hits.dmg)
            self.explodelist.append([self.BulletHit,hits.rect.x , hits.rect.y, 6])

        #Checking for collisions between the player and health packs
        heals = pygame.sprite.spritecollide(self.player, self.current_level.healths_list, True)
        for heal in heals:
            #Heals depending on the size and can't go past 100 health
            if heal.size == 0:
                self.player.health += 10
            else:
                self.player.health += 30
            if self.player.health > self.player.totalhealth:
                self.player.health = self.player.totalhealth
            
        #If the player gets near the right side, shift the world left (-x)
        if self.player.rect.right >= 400 and self.current_level.world_shift > self.current_level.level_limit:
            self.diff = self.player.rect.right - 400
            self.player.rect.right = 400
            self.current_level.shift_world(-self.diff)
            self.current_level.backrect = [self.current_level.backrect[0]-self.diff,self.current_level.backrect[1]]

        #If the player gets near the left side, shift the world right (+x)
        if self.player.rect.left <= 100 and self.current_level.world_shift <0:
            self.diff = 100 - self.player.rect.left
            self.player.rect.left = 100
            self.current_level.shift_world(self.diff)
            self.current_level.backrect = [self.current_level.backrect[0]+self.diff,self.current_level.backrect[1]]
 
        #If the player gets to the end of the level, go to the next level and set his position
        self.current_position = self.player.rect.x
        if self.current_position >= SCREEN_WIDTH:
            if self.current_level_no < len(self.level_list)-1:
                self.current_level_no += 1
                self.player.stop()
                self.player.rect.x = self.level_pos[self.current_level_no][0]
                self.player.rect.y = self.level_pos[self.current_level_no][1]
                self.current_level = self.level_list[self.current_level_no]
                self.player.level = self.current_level
                #Change and play music for the next level
                pygame.mixer.music.load(self.level_pos[self.current_level_no][2])
                if self.musicPlaying:
                    pygame.mixer.music.play(-1, 0.0)
                    
        #If the player walks to the back end of the level dont let him
        if self.player.rect.left < 10:
            self.player.rect.x = 10

        #Kill the player if they fall out
        if self.player.rect.bottom >= SCREEN_HEIGHT:
            self.player.health = 0

        #Set gameover to true and win to false and play the death music if the player has no health
        if self.player.health <= 0:
            if self.musicPlaying:
                self.dead.play()
            self.game_over = True
            self.win = False

        #Set game over to true and win to true and plays the winning music if the boss reaches it's last death frame
        if self.current_level_no == 2:
            if self.current_level.boss.deathcount == 1 :
                self.game_over = True
                self.win = True
                if self.musicPlaying:
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load("Win.mp3")
                    pygame.mixer.music.play(-1, 0.0)
            
        #Update charging time if the player is charging his gun
        if self.player.chargingbool:
            self.chargingtime = int(time.time()-self.starttime)
        else:
            self.chargingtime = 0

    def statusdraw(self,screen):
        """Function to draw the player status"""
        #Show the charge of the bullet
        if self.chargingtime < 1:
            screen.blit(self.statuses[0], self.statusrect)
        elif self.chargingtime == 1:
            screen.blit(self.statuses[1], self.statusrect)
        else:
            screen.blit(self.statuses[2], self.statusrect)
        #Calculate the damage taken and drawing the red health bar
        self.damage = 88-round(88*(self.player.health/self.player.totalhealth))
        self.healthrect = (56,56+self.damage,12,88-self.damage)
        if self.player.health >0:
            pygame.draw.rect(screen,RED,self.healthrect)
        if self.current_level_no == 2:
            self.bossdamage = 88-round(88*(self.current_level.boss.health/self.current_level.boss.totalhealth))
            self.bosshealthrect = (826,56+self.bossdamage,12,88-self.bossdamage)
            screen.blit(self.statuses[3], self.bossstatrect)
            if self.current_level.boss.health >0:
                pygame.draw.rect(screen,BLUE,self.bosshealthrect)

    def explode(self,screen):
        """Function to blit the explosion of the bullet"""
        if len(self.explodelist)> 0:
            count = 0
            #Running through the explosions and blitting it
            for explode in self.explodelist:
                screen.blit(explode[0][int(explode[3]/3)],(explode[1],explode[2]))
                if explode[3] == 0:
                    self.explodelist.pop(count)
                else:
                    explode[3] -=1
                count += 1

    def display_frame(self, screen):
        """Displaying the frame"""
        
        if self.game_over:
            #draws all entities and draws the gameover display or draws winning display if they won
            if self.win:
                winner = pygame.image.load('Win.png')
                screen.blit(winner,winner.get_rect())
                x = SCREEN_WIDTH / 2 - 300
                y = 50
                basicFont = pygame.font.Font("Mega-Man-ZX.ttf", 20)
                drawText("Mission Complete, press R to restart", basicFont, screen, x ,y, GREEN)
            else:
                self.current_level.draw(screen)
                self.active_sprite_list.draw(screen)
                self.statusdraw(screen)
                x = SCREEN_WIDTH / 2 - 240
                y = SCREEN_HEIGHT / 2 - 30
                basicFont = pygame.font.Font("Mega-Man-ZX.ttf", 20)
                drawText("Game Over, press R to restart", basicFont, screen, x ,y, GREEN)
                #terminate()
        else:
            # draws the level and the active sprites onto the surface
            self.current_level.draw(screen)
            self.active_sprite_list.draw(screen)
            self.statusdraw(screen)
            
def main():
    """ Main Program """
    pygame.init()
 
    # Set the height and width of the screen
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)
 
    pygame.display.set_caption("Megaman Zero Advent")

    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()
    chosen = False
    music = True
    # -------- Main Program Loop -----------
    while True:
        if not chosen:
            #Let the player access the menu if not chosen
            
            stats = display_menu(screen,clock,music)
            game = Game(stats)
            chosen = True
        else:
            #Run if the player isn't dead
            if not game.game_over:
                #Running the game
                game.process_events()
                game.run_logic(screen)
          
                #Drawing images
                game.display_frame(screen)
                game.explode(screen)
            else:
                #Set chosen to false and reset the game if the player presses r when dead
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        terminate()
                    if event.type == pygame.KEYDOWN:
                        if event.key == ord('r'):
                            chosen = False
                music = game.musicPlaying #Passing the music value
                #Drawing images
                game.display_frame(screen)
            
        #Going through a frame
        clock.tick(FRAMERATE)
        #Updating the screen
        pygame.display.flip()
    
    pygame.quit() 
 
if __name__ == "__main__":
    main()
