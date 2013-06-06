from time import *
import pygame
import pygame.mixer
from pygame.locals import *
import math
import random

ROMANBOATLIST = []
CARTHAGINIANBOATLIST = []
MISSILELIST = []
TERRAINLIST = []
MOVEX = 0
MOVEY = 0


class terrain():
   def __init__(self,name,(x,y),window):
      self.x = x
      self.y = y
      self.initx = x
      self.inity = y
      self.name = name

      # Determine image based on name
      if self.name == "rock":
         self.image = "rock"+str(random.randint(0,3))
         self.drawnimage = pygame.image.load("data/"+self.image+".gif")

      self.window = window
      TERRAINLIST.append(self)

   def update(self):

      # Check colissions with anything-- run ishit if they hit the terrain

      for b in ROMANBOATLIST:
         if b.x < self.x+(self.drawnimage.get_width() / 2) < (b.x + b.drawnimage.get_width()):
            if b.y < self.y+(self.drawnimage.get_height() / 2) < (b.y + b.drawnimage.get_height()):
               b.ishit(1,"obstacle")
      for b in CARTHAGINIANBOATLIST:
         if b.x < self.x+(self.drawnimage.get_width() / 2) < (b.x + b.drawnimage.get_width()):
            if b.y < self.y+(self.drawnimage.get_height() / 2) < (b.y + b.drawnimage.get_height()):
               b.ishit(1,"obstacle")
      for m in MISSILELIST:
         if m.x < self.x+(self.drawnimage.get_width() / 2) < (m.x + m.missileimage.get_width()):
            if m.y < self.y+(self.drawnimage.get_height() / 2) < (m.y + m.missileimage.get_height()):
               m.ishit(1,"obstacle")

      # Move self opposite the player's 'movement'

      self.x -= MOVEX
      self.y -= MOVEY 
      self.window.blit(self.drawnimage,(self.x,self.y))

class boat():

   # Set every single variable for the boat. If a 'c'
   # is before a word, it represents 'current', else
   # a 'c' after a word represents 'count'.

   def __init__(self,type,alliance,(x,y),window,(mapwidth,mapheight),isplayer = False, inactive = False):

      if type == "trireme":
         self.rowc = 3
         self.sailc = 2
         self.hull = 100
         self.sail = 35
         self.people = 100
         self.catapult = False
         self.rocks = 0
         self.set_images("tri")
         self.acceleration = .03
         self.deceleration = .03

      if type == "bireme":
         self.rowc = 2
         self.sailc = 1
         self.hull = 100
         self.sail = 25
         self.people = 50
         self.catapult = False
         self.rocks = 0
         self.set_images("bi")
         self.acceleration = .2
         self.deceleration = .2

      if type == "quadrireme":
         self.rowc = 4
         self.sailc = 2
         self.hull = 150
         self.sail = 35
         self.people = 125
         self.catapult = True
         self.rocks = 5
         self.set_images("quadri")
         self.acceleration = .02
         self.deceleration = .05

      if type == "quinquereme":
         self.rowc = 5
         self.sailc = 3
         self.hull = 175
         self.sail = 45
         self.people = 150
         self.catapult = True
         self.rocks = 8
         self.set_images("quinque")
         self.acceleration = .01
         self.deceleration = .04

      self.chull = self.hull
      self.csail = 0
      self.cpeople = self.people
      self.cmaxrows = self.rowc
      self.crows = 0
      self.cmaxsails = self.sailc
      self.csailsout = 0
      self.crowers = self.people / 2
      self.csailors = self.people / 4
      self.cfighters = self.people / 8
      self.cbailers = 0
      self.cdousers = 0
      self.cidlers = 0
      self.cfixers = self.people / 8
      self.arrows = self.people * 10
      self.carrows = self.arrows
      self.javelin = self.people 
      self.cjavelin = self.javelin
      self.crocks = self.rocks
      self.coil = self.people / 10
      self.cweapon = None
      self.angle = 0
      self.fixingsail = False
      self.firingside = None
      self.type = type
      self.alliance = alliance
      self.x = x
      self.y = y
      self.nonrelx = x
      self.nonrely = y
      self.initx = x
      self.inity = y
      self.mapwidth = mapwidth
      self.mapheight = mapheight
      self.rowname = ""
      self.sailname = self.saildownimage
      self.load_image()
      self.drawnimage = pygame.image.load("data/"+self.alliance+self.saildownimage+".gif")
      self.rect = self.baseimage.get_rect()
      self.imageangle = self.angle
      self.max_speed = None
      self.speed = 0
      self.window = window
      self.firedamage = 0
      self.onfire = False
      self.waterdamage = 0
      self.destroyed = False
      self.target = None
      self.targetAIdistance = 300
      self.inactive = inactive
      self.AInum = random.randint(0,1)

      # Initiates dictionary of variables which are rendered as text objects

      self.textvariables = {}
      self.set_text()

      if isplayer:
         self.isplayer = True
      else: self.isplayer = False

      if self.alliance == "Roman":
         ROMANBOATLIST.append(self)
      else:
         CARTHAGINIANBOATLIST.append(self)

   def set_text(self):
      #self.textvariables["self.speed"] = [self.speed, (self.x+30,self.y)]
      #self.textvariables["self.chull"] = [self.chull, (self.x,self.y)]
      #self.textvariables["self.csail"] = [self.csail, (self.x,self.y - 10)]
      #self.textvariables["self.cpeople"] = [self.cpeople, (5,5)]
      self.textvariables["self.crowers"] = [self.crowers, (121,529)]
      self.textvariables["self.cfixers"] = [self.cfixers, (2,529)]
      self.textvariables["self.cdousers"] = [self.cdousers, (2,481)]
      self.textvariables["self.cbailers"] = [self.cbailers, (2,433)]
      self.textvariables["self.csailors"] = [self.csailors, (121,433)]
      self.textvariables["self.cfighters"] = [self.cfighters, (121,481)]
      self.textvariables["self.carrows"] = [self.carrows, (483,531)]
      self.textvariables["self.crocks"] = [self.crocks, (603,531)]
      self.textvariables["self.cjavelin"] = [self.cjavelin, (543,531)]
      self.textvariables["self.firedamage"] = [self.firedamage, (2,490)]
      self.textvariables["self.waterdamage"] = [self.waterdamage, (2,442)]

   # Set default images as according to the boat's prefix

   def set_images(self, prefix):
      self.sailupimage = prefix + "sailup"
      self.saildownimage = prefix +"saildown"

      # Currently unused
      self.sinkimage = prefix + "sinkimage"

   # Creates appropriate count of missiles of appropriate kind
   # when the user fires out of either side of the boat.

   def fire(self, side,shift = False):
      self.firingside = side
      if self.coil < 1:
         shift = False

      # Checks to ensure there is a current weapon
      if self.cweapon != None:

         # Sets appropriate kind of weapon as internal variable
         # 'weapon'

         if self.cweapon == "arrows":
            weapon = self.carrows
         elif self.cweapon == "javelin":
            weapon = self.cjavelin
         elif self.cweapon == "rocks":
            weapon = self.crocks

         missilespawn = (self.x+(self.drawnimage.get_width() / 2),self.y+(self.drawnimage.get_height() / 2))
         # Checks what the current count of weapons is respective
         # to how many people are currently set to be shooting
         # weapons, 'self.cfighters'. Fires missile and reduces
         # weapon count by whatever number is able to be fired
         # up until 25 missiles as a maximum per shot. Only one
         # rock can be fired at a time.

         if weapon > self.cfighters:
            if self.cfighters > 25:
               ammo_fired = 25
            else: ammo_fired = self.cfighters
            if self.cweapon == "rocks":
               ammo_fired = 1
            new_missile = missile(self.cweapon,ammo_fired,self.window,self.angle,self.firingside,missilespawn,self.alliance,shift)
            weapon -= ammo_fired

         elif weapon == 0:
            return None

         elif weapon <= self.cfighters and self.cweapon != "rocks":
            new_missile = missile(self.cweapon,weapon,self.window,self.angle,self.firingside,missilespawn,self.alliance,shift)
            weapon = 0
         elif weapon <= self.cfighters and self.cweapon == "rocks":
            new_missile = missile(self.cweapon,1,self.window,self.angle,self.firingside,missilespawn,self.alliance,shift)
            weapon -= 1
            
         if shift:
            self.coil -= 1
         # Resets appropriate weapon to the changed value as per
         # ammo_fired
         if self.cweapon == "arrows":
            self.carrows = weapon
         elif self.cweapon == "javelin":
            self.cjavelin = weapon
         elif self.cweapon == "rocks":
            self.crocks = weapon

   # This function takes damage upon being hit by anything

   def ishit(self,count,weapon,onfire = False):

      if weapon == "arrows":
         damage = 1
         prime_target = "sail"

         # Recover a portion of the weapons thrown at you.

         self.carrows += int((1.0/random.randint(2,10))*count)
         if self.carrows > self.arrows:
            self.carrows = self.arrows

      elif weapon == "javelin":
         damage = 3

         #Targetting people currently nonfunctional
         prime_target = "people"

         self.cjavelin += int((1.0/random.randint(2,10))*count)
         if self.cjavelin > self.javelin:
            self.cjavelin = self.javelin

      elif weapon == "rocks":
         damage = 45
         prime_target = "hull"

      else:
         damage = 10
         prime_target = "hull"

      if onfire:
         dammod = 1.25
      else:
         dammod = 1

      tot_damage = count * damage * dammod

      # Start taking firedamage if whatever hit you was on fire.

      if onfire:
         self.firedamage += tot_damage / 10

      # If sail is being targetted, reduces sail until sail is at 0,
      # then moves damage past 0 onto the hull.

      if prime_target == "sail":
         self.csail -= tot_damage
         print "self.csail is" + str(self.csail)
         if self.csail < 0:
            self.chull += self.csail
            print "self.hull is" + str(self.chull)
            self.csail = 0
            self.csailsout = 0

      else:
         self.chull -= tot_damage

      if weapon == "obstacle":
         self.turnaround()

   # Removes and disposes of destroyed boats.
   # Will eventually use self.sinkimage

   def destroy(self):
      self.destroyed = True

      # Go away if not player

      if not self.isplayer:
         self.x = -50
         self.y = -50
         self.window.blit(self.drawnimage, (self.x,self.y))
         if self.alliance == "Roman":
            ROMANBOATLIST.remove(self)
         else:
            CARTHAGINIANBOATLIST.remove(self)

      # Stop moving the screen upon death if player.

      else:
         global MOVEX
         global MOVEY
         MOVEX = 0
         MOVEY = 0
         if self.alliance == "Roman":
            ROMANBOATLIST.remove(self)
         else:
            CARTHAGINIANBOATLIST.remove(self)
   
   # Turn around, get away from whatever made you turn around, and slow down.

   def turnaround(self):
      self.turn('clockwise',180)
      self.move()
      self.row_change('down','total')
      self.sail_change('down')

   def setweapon(self,weapon):
      self.cweapon = weapon
      
   def turn(self,direction,mod = 15):
      if direction == "clockwise":
         self.angle = self.angle + mod
      elif direction == "counterclockwise":
         self.angle = self.angle - mod
      if self.angle < 0:
         self.angle = self.angle + 360
      elif self.angle >= 360:
         self.angle = self.angle - 360
      while self.angle%15 != 0:
         self.angle +=1
         self.angle = int(self.angle)

   # CREDIT: Gummbum via pygame.org
   # This function copies the boat's image and roates it as needed by
   # self.angle
   def change_image(self,image,angle = None):
      rect = image.get_rect()
      rotated_image = pygame.transform.rotate(image, -angle)
      rotated_rect = rect.copy()
      rotated_rect.center = rotated_image.get_rect().center
      rotated_image = rotated_image.subsurface(rotated_rect).copy()
      return rotated_image
   
   # Drops sail and rows to 0 before repairing the sail until the sail is at full

   def fixsail(self):
      if self.csail < self.sail and self.fixingsail != True:   
         self.fixingsail = True

      # Abort fixing sail if called while fixing sail
      elif self.fixingsail == True:
         self.fixingsail = False


   # Increase or decrease current number of sails out

   def sail_change(self,direction,amount=1):

      # Check to make sure the boat has sails to put out

      if self.csail != 0:

         if amount == "total" and direction == "down":
            while self.csailsout != 0:
               self.csailsout -= 1
         elif amount == "total" and direction == "up":
            while self.csailsout != self.cmaxsails:
               self.csailsout += 1

         else:
            if self.csailsout < self.cmaxsails and direction == "up":
               self.csailsout += amount
            elif self.csailsout > 0 and direction == "down":
               self.csailsout -= amount

         # Update imagename based on whether or not boat has sails out

         if self.csailsout == 0:
            self.sailname = self.saildownimage
         else:
            self.sailname = self.sailupimage
   
   # Increase or decrease number of rows of oars out, mirrors previous function

   def row_change(self,direction,amount=1):
         
      if amount == "total" and direction == "down":
         while self.crows != 0:
            self.crows -= 1
      elif amount == "total" and direction == "up":
         while self.crows != self.cmaxrows:
            self.crows += 1

      else:
         if self.crows < self.cmaxrows and direction == "up":
            self.crows += amount
         elif self.crows > 0 and direction == "down":
            self.crows -= amount

      if self.crows != 0 and self.rowname != "_rowup":
         self.rowname = "_rowup"
      elif self.crows == 0:
         self.rowname = ""
   
   # Change the number of people are working some job

   def people_manage(self,person,direction,magnitude=5):
      # Increasing people on a job
      if direction == "up":

         if self.cidlers >= magnitude:
            change = magnitude
         else:
            change = self.cidlers

            if change == 0:
               print "cidlers = 0"
               # Abort if there are no people idle to assign a job
               return

         cperson = eval("self.c"+person)

         if cperson <= self.people - change:
            cperson += change
            self.cidlers -= change
            # Update the changed job
            self.update_person(person,cperson)
            print self.cidlers
            print eval("self.c"+person)
      # Decreasing people on a job
      else:

         if self.cidlers <= self.people - magnitude:
            cperson = eval("self.c"+person)

            if cperson == 0:
               print "cperson = 0"
               # Abort if there are no people to remove from the job
               return
            else:

               # Set the amount of people to remove either magnitude #
               # or however many are on the job, if less than magnitude #
               if cperson - magnitude < 0:
                  change = -(cperson - magnitude)
                  cperson = 0
               else:
                  change = magnitude
                  cperson -= change

               self.cidlers += change
               # Update the changed job
               self.update_person(person,cperson)

               print self.cidlers
               print eval("self.c"+person)
      self.update_max_speed()

   # When the player changes how many people are doing whatever job,
   # this function checks to see if the player has disabled his or 
   # her maximum rows of oars or sails. If so, they are reduced.

   def update_max_speed(self):
      rowscapable = self.crowers / 15
      sailscapable = self.csailors / 10

      if rowscapable <= self.rowc:
         self.cmaxrows = rowscapable
         if self.crows > self.cmaxrows and self.crows != 0:
            self.crows -= 1

      if sailscapable <= self.sailc:
         self.cmaxsails = sailscapable
         if self.csailsout > self.cmaxsails and self.csailsout != 0:
            self.csailsout -= 1

   def update_person(self,person,count):
      if person == "fixers":
         self.cfixers = count
      elif person == "dousers":
         self.cdousers = count
      elif person == "bailers":
         self.cbailers = count
      elif person == "sailors":
         self.csailors = count
      elif person == "fighters":
         self.cfighters = count
      elif person == "rowers":
         self.crowers = count
      
   # When loading an image, sailname and rowname are used to condense code
   # into not having a series of if statements here.

   def load_image(self):
      self.baseimage = pygame.image.load("data/"+self.alliance+self.sailname+self.rowname+".gif")
      
   def update(self):

      # Hull repair

      if 0 < self.chull < self.hull:
         self.chull += self.cfixers / float(200)
      if self.fixingsail == True:
         self.sail_change("down","total")
         self.row_change("down","total")
         self.csail += .5
         if self.csail == self.sail:
            self.fixingsail = False

      # Fire damage

      if self.firedamage > 0:
         self.firedamage -= self.cdousers / float(100)
         if self.csail > 0:
            self.csail -= self.firedamage
         else:
            self.csail = 0
         if self.csail == 0:
            self.chull -= self.firedamage / 4
      elif self.firedamage != 0:
         self.firedamage = 0
      if self.firedamage > 5:
         self.onfire = True

      # Water damage

      if self.chull < self.hull:
         self.waterdamage += (self.hull - self.chull) / 500
      if self.waterdamage > self.hull:
         self.destroy()
      if self.waterdamage < 0:
         self.waterdamage = 0
      elif self.waterdamage > 0:
         self.waterdamage -= self.cbailers / float(100)

      # Determine colissions with other boats-- no friendly colission currently allowed.

      if self.alliance != "Roman":
         for b in ROMANBOATLIST:
            if b.x < self.x+(self.drawnimage.get_width() / 2) < (b.x + b.drawnimage.get_width()):
               if b.y < self.y+(self.drawnimage.get_height() / 2) < (b.y + b.drawnimage.get_height()):
                  b.ishit(1,"obstacle",self.onfire)
      else:
         for b in CARTHAGINIANBOATLIST:
            if b.x < self.x+(self.drawnimage.get_width() / 2) < (b.x + b.drawnimage.get_width()):
               if b.y < self.y+(self.drawnimage.get_height() / 2) < (b.y + b.drawnimage.get_height()):
                  b.ishit(1,"obstacle",self.onfire)

      # Set max speed based on how many rows of oars and sails are out.
      if self.crows or self.csailsout:
         self.max_speed = (self.crows + (self.csailsout * 2)) * .75
         accelerating = True
      else:
         accelerating = False 

      # Set speed based on what the max speed is and momentum

      if self.max_speed:
         if self.speed <= self.max_speed and accelerating:
            self.speed += self.acceleration
         elif self.speed > 0 and not accelerating:
            self.speed -= self.deceleration
         elif self.speed > self.max_speed + self.deceleration:
            self.speed -= self.deceleration
         elif self.speed < 0:
            self.speed = 0

      self.move()

      if not -self.mapwidth < self.nonrelx < self.mapwidth:
         if self.x > self.mapwidth:
            self.x -= 20
         else:
            self.x += 20
         self.turnaround()
      if not -self.mapheight < self.nonrely < self.mapheight:
         if self.y > self.mapheight:
            self.y -= 20
         else:
            self.y += 20
         self.turnaround()

      # Runs functions to update boat image and boat text interfaces
         
      self.load_image()
      self.drawnimage = self.change_image(self.baseimage,self.angle)
      self.window.blit(self.drawnimage, (self.x,self.y))
      self.set_text()

      # Destroys boat if boat's hull at 0 or less  
      if self.chull <= 0:
         self.destroy()

      if not self.isplayer:
         if self.target == None:
            self.gettarget()
         self.AI()
      else:
         self.update_status_UI()

   def update_status_UI(self):
      top = self.y+self.drawnimage.get_height()

      # Outline
      if self.csail and self.chull and (self.waterdamage or self.firedamage):
         width, height = 34, 18
      elif self.chull and self.csail:
         width, height = 34, 10
      elif self.chull and self.waterdamage and not self.csail and not self.firedamage:
         width, height = 18, 18
      elif self.chull and not self.csail and not self.waterdamage and not self.firedamage:
         width, height = 18, 10
      else:
         width, height = 34, 18

      pygame.draw.rect(self.window,(0,0,0),pygame.Rect(self.x+7,top,width,height))
      # Hull
      pygame.draw.rect(self.window,(0,255,0),pygame.Rect(self.x+8,top,((self.chull)/self.hull)*16,8))
      # Sail
      if self.csail:
         pygame.draw.rect(self.window,(255,255,255),pygame.Rect(self.x+24,top,((self.csail)/self.sail)*16,8))
      # Water
      if self.waterdamage:
         pygame.draw.rect(self.window,(0,0,255),pygame.Rect(self.x+8,top+8,((self.waterdamage)/self.hull)*16,8))
      # Fire
      if self.firedamage:
         pygame.draw.rect(self.window,(255,0,0),pygame.Rect(self.x+24,top+8,((self.firedamage)/self.sail)*16,8))


   def move(self):
      self.nonrelx += math.cos(math.radians(self.angle)) * self.speed
      self.nonrely += math.sin(math.radians(self.angle)) * self.speed

      if self.isplayer:
         global MOVEX
         global MOVEY

         if -self.mapwidth + 328 < self.nonrelx < self.mapwidth - 328:
            MOVEX = math.cos(math.radians(self.angle)) * self.speed
         else:
            self.x += math.cos(math.radians(self.angle)) * self.speed
            MOVEX = 0
         
         if -self.mapheight + 192 < self.nonrely < self.mapheight - 192:
            MOVEY = math.sin(math.radians(self.angle)) * self.speed
         else:
            self.y += math.sin(math.radians(self.angle)) * self.speed
            MOVEY = 0

      else:
         self.x += math.cos(math.radians(self.angle)) * self.speed
         self.y += math.sin(math.radians(self.angle)) * self.speed
         self.x -= MOVEX
         self.y -= MOVEY 

   # This function selects a random target for AI boats for them
   # to chase after.

   def gettarget(self):
      if self.alliance == "Carthaginian":
         activelist = ROMANBOATLIST
      elif self.alliance == "Roman":
         activelist = CARTHAGINIANBOATLIST

      count = len(activelist)
      if count != 0:
         targetnum = random.randint(0,count-1)
         for j in range(count):
            if j == targetnum:
               self.target = activelist[j]
      else: self.inactive = True

   # If boat is not player, determine what you are going to do.
   # AInum, assigned on __init__, defines what sequence of AI the boat
   # will run through.

   def AIwater_damage(self):
      if self.cidlers > 0:
         self.people_manage('bailers','up')
      else:
         if self.cfixers > 0:
            self.people_manage('fixers','down')
         elif self.cdousers > 0 and self.firedamage < 1:
            self.people_manage('dousers','down')
         elif self.cfighters > 10:
            self.people_manage('fighters','down')
         elif self.crowers > self.crows * 15:
            self.people_manage('rowers','down')
         elif self.csailors > self.csailsout * 10:
            self.people_manage('sailors','down')

   def AIfire_damage(self):
      if self.cidlers > 0:
         self.people_manage('dousers','up')
      else:
         if self.cfixers > 0:
            self.people_manage('fixers','down')
         elif self.cbailers > 0 and self.waterdamage < 2:
            self.people_manage('bailers','down')
         elif self.cfighters > 10:
            self.people_manage('fighters','down')
         elif self.crowers > self.crows * 15:
            self.people_manage('rowers','down')
         elif self.csailors > self.csailsout * 10:
            self.people_manage('sailors','down')

   def AIreset_people(self):
      randinc = random.randint(0,3)
      if randinc == 0:
         self.people_manage('fighters','up')
      elif randinc == 1:
         self.people_manage('fixers','up')
      elif randinc == 2:
         self.people_manage('rowers','up')
      else:
         self.people_manage('sailors','up')

   def AI(self):
      out_of_ammo = False
      if self.AInum == 0:
         turndirection = "counterclockwise"
         flame = random.randint(0,5)
         if flame == 0:
            onfire = True
         else: onfire = False
      elif self.AInum == 1:
         turndirection = 'clockwise'
         flame = random.randint(0,11)
         if flame == 0:
            onfire = True
         else:
            onfire = False
      if self.inactive != True:
         if self.target.destroyed == True:
            self.gettarget()
         if self.csail == 0 and self.firedamage == 0:
            self.fixsail()
            return
         elif self.speed == 0:
            self.sail_change('up')
            self.row_change('up')
            return
         elif self.waterdamage > 10 and self.cbailers < 10:
            self.AIwater_damage()
            return
         elif self.firedamage > 5 and self.cdousers < 5:
            self.AIwater_damage()
            return
         elif self.firedamage > 1 and self.waterdamage > 1 and self.cidlers != 0:
            self.AIreset_people()
            return
         else:
            if self.cweapon == None or (self.cjavelin < 1 and self.cweapon != 'arrows'):
               self.setweapon('arrows')
               return
            elif self.target.speed < 1 and self.cjavelin > 1 and self.cweapon != 'javelin':
               self.setweapon('javelin')
               return
            elif self.target.speed < 1 and self.catapult == True and self.crocks > 1 and self.cweapon != 'rocks':
               self.setweapon('rocks')
               return
            if self.javelin == 0 and self.rocks == 0 and self.arrows == 0:
               out_of_ammo = True
            # Pythagorean theorem distance
            if math.sqrt(((self.target.nonrelx - self.nonrelx)**2) +((self.target.nonrely - self.nonrely)**2)) < self.targetAIdistance and not out_of_ammo:  
                  cycling = True
                  self.targetAIdistance = 500
                  if self.nonrelx > 310+self.target.nonrelx:
                     if self.angle != 270:
                        self.turn(turndirection)
                        return
                  elif self.nonrelx < self.target.nonrelx-310:
                     if self.angle != 90:
                        self.turn(turndirection)
                        return
                  elif self.nonrely < self.target.nonrely-145:
                     if self.angle != 180:
                        self.turn(turndirection)
                        return
                  elif self.nonrely > 145+self.target.nonrely:
                     if self.angle != 0:
                        self.turn(turndirection)
                        return
            else:
               advancing = True
               self.targetAIdistance = 300
               angle =  math.degrees(math.atan2(float(self.target.nonrely-self.nonrely),float(self.target.nonrelx-self.nonrelx)))
               if not angle+30 > self.angle > angle - 30:
                  self.angle = angle
                  return
            if self.alliance == "Carthaginian":
               activelist = ROMANBOATLIST
            else: activelist = CARTHAGINIANBOATLIST
            for b in activelist:
               if self.y - 5 < b.y < self.y + 5:
                  if self.angle == 270:
                     if b.x < self.x:
                        self.fire('left',onfire)
                     else: self.fire('right',onfire)
                     return
                  elif self.angle == 90:
                     if b.x < self.x:
                        self.fire('right',onfire)
                     else: self.fire('left',onfire)
                     return
               elif self.x - 5 < b.x < self.x + 5:
                  if self.angle == 180:
                     if b.y < self.y:
                        self.fire('right',onfire)
                     else: self.fire('left',onfire)
                     return
                  elif self.angle == 0:
                     if b.y < self.y:
                        self.fire('left',onfire)
                     else: self.fire('right',onfire)
                     return
               else:
                  if self.csail != self.cmaxsails or self.crows != self.cmaxrows:
                     self.sail_change('up')
                     self.row_change('up')
            
class missile(boat):

   # Missile inherits Boat solely so that missile can use boat's 
   # change_image function to rotate itself on being spawned.
   # Missile represents missiles like arrows and javelin.

   def __init__(self,weapon,count,window,angle,firingside,(x,y),alliance,flaming):
         
         # Determine which missile image to render based on how many missiles
         # are being fired and whether or not te missile(s) are on fire.

         self.num = count / 5

         if count < 26:
            self.count = count
         else:
            self.count = 25

         if self.num < 5:
            self.count = self.num * 5

         if flaming and weapon == "arrows":
            self.flamename = "onfire"
            self.onfire = True
         else:
            self.flamename = ""
            self.onfire = False

         if self.count == 0 or weapon == "rocks":
            self.count = 1
            if weapon == "arrows":
               self.missileimage = pygame.image.load("data/"+weapon+self.flamename+".gif")
            else:
               self.missileimage = pygame.image.load("data/"+weapon+".gif")
         else:
            if weapon == "arrows":
               self.missileimage = pygame.image.load("data/"+weapon+str(int(self.count))+self.flamename+".gif")
            else:
               self.missileimage = pygame.image.load("data/"+weapon+str(int(self.count))+".gif")

         #Determine angle by which side missile is being fired from.

         if firingside == "left":
             self.angle = angle - 90
         elif firingside == "right":
             self.angle = angle + 90

         #Shoot missile at that angle.  

         self.missileimage = self.change_image(self.missileimage,self.angle+180)

         self.weapon = weapon
         self.x,self.y = (x,y)
         self.window = window
         self.speed = None
         self.alliance = alliance

         # Set speed, amount of inaccuracy, and how long the missile
         # remains in the air based on the type of weapon.

         if self.weapon == "javelin":
             self.speed = 6
             self.error = 0
             self.maxdeathtoll = 50
         elif self.weapon == "arrows":
             self.speed = 8
             self.error = 2
             self.maxdeathtoll = 60
         else: 
             self.speed = 4
             self.error = 4
             self.maxdeathtoll = 60

         self.deathtoll = 0
         MISSILELIST.append(self)

   # If you are hit, kill yourself

   def ishit(self,count,weapon):
      if weapon == "obstacle":
         self.deathtoll = self.maxdeathtoll-1
         self.window.blit(self.missileimage, (-50,-50))

   def update(self):

         # Determines how considerably the missile will waver in its path, javelin
         # are perfectly accurate (don't try this in real life) and will not have inaccuracy.

         if self.weapon != "javelin":
             inaccuracy = float(random.randint(-(self.error*5),(self.error*5)))/20
         else: inaccuracy = 0

         # Moves the missile as according to its angle and inaccuracy

         self.x += (math.cos(math.radians(self.angle)) * self.speed) + inaccuracy
         self.y += (math.sin(math.radians(self.angle)) * self.speed) + inaccuracy
         self.x -= MOVEX
         self.y -= MOVEY 

         # Checks collision with boats as according to alliance-- missiles will only hit
         # boats of the opposing alliance compared to the missiles' alliance

         if self.alliance == "Roman":
            enemylist = CARTHAGINIANBOATLIST
         else:
            enemylist = ROMANBOATLIST

         for b in enemylist:
            if b.x < self.x+(self.missileimage.get_width() / 2) < (b.x + b.drawnimage.get_width()):
               if b.y < self.y+(self.missileimage.get_height() / 2) < (b.y + b.drawnimage.get_height()):

                  #Register a hit on the opposing boat
                  b.ishit(self.count,self.weapon,self.onfire)

                  # Kills missile upon contact
                  self.deathtoll = self.maxdeathtoll-1

         self.window.blit(self.missileimage, (self.x,self.y))
         
         # Remove and dispose of the missile upon the missile reaching its maximum range   
         self.deathtoll += 1
         if self.deathtoll == self.maxdeathtoll:
            self.window.blit(self.missileimage, (-50,-50))
            MISSILELIST.remove(self)

class interface():

   #This class represents clickable graphical user interfaces

    def __init__(self, (x,y), function, interfacelist, size=2, functional=True):
      self.x = x
      self.y = y
      self.functional = functional
      self.function = function
      self.size = size

      # Adds self to interface list along with self's size for click checking
      if size == 1 or size == 2:
         interfacelist[self]=[[x,x+60],[y,y+(24*size)]]
      else:
         interfacelist[self]=[[x,x+size[0]],[y,y+size[1]]]

      # Sets and loads proper image file as defined by interface's function
      self.image = function + ".gif"
      self.uniqueimagecheck()
      self.drawnimage = pygame.image.load("data/"+self.image)

    # CONSIDER CHANGING THIS: DOES NOT NEED TO USE GLOBAL VARIABLE AT ALL
    # On init, checks if the function of the boat is one of the functions
    # defined as a standard up / down arrow function. If it is, it replaces
    # the image of the function with the default arrow.

    def uniqueimagecheck(self):
            for i in range(len(STANDARDIMAGES)):
                if STANDARDIMAGES[i] == self.function:
                    if i%2 == 0:
                        self.image = "standard_up.gif"
                    else: self.image = "standard_down.gif"

    def update(self, window):

      # This prevents the player from existing within the interfaces.

       for b in ROMANBOATLIST:
         if b.isplayer == True:
            if b.x < self.x+(self.drawnimage.get_width() / 2) < (b.x + b.drawnimage.get_width()):
               if b.y < self.y+(self.drawnimage.get_height() / 2) < (b.y + b.drawnimage.get_height()):
                  b.ishit(0,"obstacle",False)
       for b in CARTHAGINIANBOATLIST:
         if b.isplayer == True:
            if b.x < self.x+(self.drawnimage.get_width() / 2) < (b.x + b.drawnimage.get_width()):
               if b.y < self.y+(self.drawnimage.get_height() / 2) < (b.y + b.drawnimage.get_height()):
                  b.ishit(0,"obstacle",False)

       window.blit(self.drawnimage, (self.x,self.y))

class minimap():

   # The minimap class renders a minimap of all the boats and terrain on the playing field
   # by converting their relative positions into positions for rectangles

   def __init__(self,window,(mapwidth,mapheight),(x,y),(width,height)):
      self.x = x
      self.y = y
      self.mapwidth = float(mapwidth)
      self.mapheight = float(mapheight)
      self.window = window
      self.width = float(width)
      self.height = float(height)

   # The math below draws a rectangle at the middle of the minimap (self.x/y+self.width/height/2),
   # ofsetting that value by the non-relative position of each boat or terrain object being drawn
   # (float(b.nonrelx/y or t.initx/y)) modified to be proportionate to the minimap's dimensions as if 
   # the minimap were the playing field ((self.mapwidth/height*2))*self.width/height)
   # --importantly here mapwidth and mapheight are augmented by 2 in order to compensate for them
   # representing the distance from the center of the map to the edges of the map. The rectangles
   # are given a default size of 4 width and height. Variables shortened to decrease line length.

   def update(self):
      x1 = (self.x+self.width/2)
      mw2 = (self.mapwidth*2)
      mh2 = (self.mapheight*2)
      w = self.width
      h = self.height

      for b in ROMANBOATLIST:
         if b.isplayer:
            pygame.draw.rect(self.window,(255,255,255),pygame.Rect(x1+((float(b.nonrelx)/mw2)*w),(self.y+h/2)+((float(b.nonrely)/mh2)*h),4,4))
         else: 
            pygame.draw.rect(self.window,(200,50,50),pygame.Rect(x1+((float(b.nonrelx)/mw2)*w),(self.y+h/2)+((float(b.nonrely)/mh2)*h),4,4))
      for b in CARTHAGINIANBOATLIST:
         if b.isplayer:
            pygame.draw.rect(self.window,(255,255,255),pygame.Rect(x1+((float(b.nonrelx)/mw2)*w),(self.y+h/2)+((float(b.nonrely)/mh2)*h),4,4))
         else:
            pygame.draw.rect(self.window,(50,200,50),pygame.Rect(x1+((float(b.nonrelx)/mw2)*w),(self.y+h/2)+((float(b.nonrely)/mh2)*h),4,4))
      for t in TERRAINLIST:
         pygame.draw.rect(self.window,(50,10,10),pygame.Rect(x1+((float(t.initx)/mw2)*w),(self.y+h/2)+((float(t.inity)/mh2)*h),4,4))

class event_handler():

   # This class acts with left clicks to run the function of an interface
   # when the interface is clicked given that 1) an interface is being clicked
   # and 2) the interface is "functional=True". for formatting of interface
   # (i.e. why item[#][#][#]) see interface class __init__.

   def check_interface(self,(x,y),interfacelist):
       interfaces = interfacelist.items()
       for item in interfaces:
           if item[0].functional:
               if item[1][0][0] <= x <= item[1][0][1]:
                   if item[1][1][0] <= y <= item[1][1][1]:
                       print item[0].function
                       return item[0].function, True
       return None, False

   # The highlight function mirrors check_interface, applying it to create a 
   # new nonfunctional highlight interface atop the interface currently at mousex/y. 
   # Future functionality will check the size of the interface to be 
   # highlighted and create a highlight of an appropriate size for the interface.

   def highlight_interface(self,(x,y),interfacelist,highlightlist):
      highlightlist = {}
      interfaces = interfacelist.items()
      for item in interfaces:
           if item[0].functional:
               if item[1][0][0] <= x <= item[1][0][1]:
                   if item[1][1][0] <= y <= item[1][1][1]:
                     highlight = interface((item[1][0][0],item[1][1][0]),'interfacehighlight',highlightlist,functional = False)
                     return highlightlist
                       

class naval_event_handler(event_handler):

   # The naval event handler handles events when the MODE = "Naval"

   def __init__(self,screen,fpsClock,boattype,scenario):
      #Initiate various states for function
      self.gameover = False
      running = True
      a_font = pygame.font.Font(None, 16)
      interfaces = self.init_naval_interface()
      bgcolor = pygame.Color(25,100,250)
      highlightlist = {}
      shift = False
      paused = False
      tutorial = False
      
      # Depending on scenario, create different objects and a different map size.

      if scenario == "1v1":
         aboat = boat(boattype, "Roman", (328,192), screen,(1000,1000), True)
         enemy_boat = boat("trireme","Carthaginian", (420,420), screen,(1000,1000))

         rock1 = terrain('rock',(250,250),screen)
         rock2 = terrain('rock',(120,120),screen)

         mini = minimap(screen,(1000,1000),(239,431),(240,144))

      elif scenario == "3v3":
         aboat = boat(boattype, "Roman", (328,192), screen,(1000,1000), True)

         ally_boat_1 = boat("bireme", "Roman", (-400,100), screen,(1000,1000))
         ally_boat_2 = boat("quadrireme", "Roman", (-400,180), screen,(1000,1000))

         enemy_boat_1 = boat("trireme", "Carthaginian", (720,20), screen,(1000,1000))
         enemy_boat_2 = boat("bireme", "Carthaginian", (720,100), screen,(1000,1000))
         enemy_boat_3 = boat("quadrireme", "Carthaginian", (720,180), screen,(1000,1000))

         mini = minimap(screen,(1000,1000),(239,431),(240,144))

      elif scenario == "2v6":
         aboat = boat(boattype, "Roman", (328,192), screen,(1000,1000), True)
         ally_boat_1 = boat(boattype, "Roman", (428,192), screen, (1000,1000))
         enemy_boat_1 = boat("trireme", "Carthaginian", (-400,20), screen,(1000,1000))
         enemy_boat_2 = boat("bireme", "Carthaginian", (-400,100), screen,(1000,1000))
         enemy_boat_3 = boat("quadrireme", "Carthaginian", (-400,180), screen,(1000,1000))
         enemy_boat_4 = boat("trireme", "Carthaginian", (-300,20), screen,(1000,1000))
         enemy_boat_5 = boat("quinquereme", "Carthaginian", (-300,100), screen,(1000,1000))
         enemy_boat_6 = boat("quadrireme", "Carthaginian", (-300,180), screen,(1000,1000))

         mini = minimap(screen,(1000,1000),(239,431),(240,144))

      elif scenario == "Tutorial":
         aboat = boat(boattype, "Roman", (328,192), screen,(1000,1000), True)
         enemy_boat = boat("trireme","Carthaginian", (420,420), screen,(1000,1000), inactive = True)

         rock1 = terrain('rock',(250,250),screen)
         rock2 = terrain('rock',(120,120),screen)

         tutorial = True

         print "This is the current tutorial! In order to tutorialize, you will see messages over here",
         print "as you try to do things. To begin the game, your sail is broken. To fix it, you can see",
         print "a button in the bottom right with a sail and a red patch on it. Either click that button",
         print "or to continue the tutorial, press the / or ? key."

         mini = minimap(screen,(1000,1000),(239,431),(240,144))

      while running:
         if not paused:
            for event in pygame.event.get():

               # If the player quits, remove everything from
               # the global update lists. Currently only semi
               # functional-- if there are too many boats, not
               # all of them are gone upon restarting the
               # scenario in Test_Arena.

               if event.type == pygame.QUIT:
                  print("User asked to quit.")
                  for b in ROMANBOATLIST:
                     ROMANBOATLIST.remove(b)
                  for b in CARTHAGINIANBOATLIST:
                     CARTHAGINIANBOATLIST.remove(b)
                  for m in MISSILELIST:
                     MISSILELIST.remove(m)
                  for t in TERRAINLIST:
                     TERRAINLIST.remove(t)
                  running = False

               # Shift allows for alternate functions to be run when
               # using the keyboard as an interface. Future functionality
               # should allow it to be functional for clicking the
               # interface as well.

               if pygame.key.get_mods() & KMOD_SHIFT:
                  shift = True
               else: shift = False 

               if event.type == pygame.MOUSEMOTION:
                  mousex, mousey = event.pos
                  highlightlist = self.highlight_interface((mousex, mousey),interfaces,highlightlist)

               # Act with left clicks

               if event.type == pygame.MOUSEBUTTONUP: 
                  mousex, mousey = event.pos

                  # If left-click, determine if interface is being clicked;
                  # run the interface's function if it is. Currently demands
                  # player boat be "aboat".

                  if event.button == 1:
                     function, isinterface = self.check_interface((mousex, mousey),interfaces)
                     if isinterface:
                        eval(("aboat." + function))

               # Determine what interface to run on keyboard input

               elif event.type == pygame.KEYUP and not tutorial:
                  if event.key == 117:
                     if shift:
                        aboat.row_change('up','total')
                     else:
                        aboat.row_change('up')
                  elif event.key == 105:
                     if shift:
                        aboat.turn('counterclockwise',30)
                     else:
                        aboat.turn('counterclockwise')
                  elif event.key == 111:
                     if shift:
                        aboat.turn('clockwise',30)
                     else:
                        aboat.turn('clockwise')
                  elif event.key == 112:
                     if shift:
                        aboat.sail_change('up','total')
                     else:
                        aboat.sail_change('up')
                  elif event.key == 106:
                     if shift:
                        aboat.row_change('down','total')
                     else:
                        aboat.row_change('down')
                  elif event.key == 107:
                     aboat.fire('left',shift)
                  elif event.key == 108:
                     aboat.fire('right',shift)
                  elif event.key == 59:
                     if shift:
                        aboat.sail_change('down',"total")
                     else:
                        aboat.sail_change('down')
                  elif event.key == 109:
                     aboat.setweapon('arrows')
                  elif event.key == 44:
                     aboat.setweapon('javelin')
                  elif event.key == ord("."):
                     aboat.setweapon('rocks')
                  elif event.key == ord("/"):
                     aboat.fixsail()

                  # If the player hits space, pause the game.
                  elif event.key == K_SPACE:
                     paused = True
               elif event.type == pygame.KEYUP and tutorial:
                  if event.key == 117:
                     print
                     print "This button will increase the number of rows of oars you have out by one."
                     print "If you hold shift while pressing this button, you will put all of your oars out.",
                     print "If you look on the left you can see a few guys holding oars-- they represent the number",
                     print "of people you have currently rowing. If you don't have at least 15 people rowing for each row of oars,",
                     print "your maximum number of oars will drop accordingly. The default maximum is represented by what boat you picked--",
                     print "Bireme - 2, Trireme - 3, Quadrireme - 4, Quinquereme - 5."
                     print "Oars are less useful than sails, as they don't intercept arrows and they provide less momentum in general."
                     if shift:
                        aboat.row_change('up','total')
                     else:
                        aboat.row_change('up')
                  elif event.key == 105:
                     print
                     print "This button will turn your boat 15 degrees counterclockwise."
                     print "If you hold shift while pressing this button, you will turn 30 degrees."
                     if shift:
                        aboat.turn('counterclockwise',30)
                     else:
                        aboat.turn('counterclockwise')
                  elif event.key == 111:
                     print
                     print "This button will turn your boat 15 degrees clockwise."
                     print "If you hold shift while pressing this button, you will turn 30 degrees."
                     if shift:
                        aboat.turn('clockwise',30)
                     else:
                        aboat.turn('clockwise')
                  elif event.key == 112:
                     print
                     print "This button will increase the number of sails you have out by one."
                     print "If you hold shift while pressing this button, you will put all of your sails out.",
                     print "Shift-button actions will only work when using the keyboard interface, however.",
                     print "The number of sails that you can have out is directly related to how many people you have manning the sails.",
                     print "In the third column, first row of the left interface, people pulling ropes to a sail represent",
                     print "the number of people you have manning sails currently.",
                     print "You need at least 10 people manning each sail that you have. If you have any less, your maximum",
                     print "number of sails that you can put out will be reduced."
                     print "You can control how many people are doing a job with the up and down arrows to the right of any particular person,",
                     print "but note that at default, you will have no people idling to give to any job, and will need to decrease a job before",
                     print "increasing another."
                     print
                     print "For information about all of the people on the left, press B for bailers, D for dousers, F for fixers,",
                     print "K for fighters, and U for rowers."
                     print 
                     print "Now that you are moving, if you want to not be moving, hit SPACE."
                     print
                     print "To see where you are, refer to the white square on the minimap at the center of the bottom of the screen."
                     if shift:
                        aboat.sail_change('up','total')
                     else:
                        aboat.sail_change('up')
                  elif event.key == 106:
                     print
                     print "This button will lower the number of rows of oars you have out by one."
                     print "To pull in all of your oars, hold shift while pressing the key for this button."
                     print "For more on oars, press the U key."
                     if shift:
                        aboat.row_change('down','total')
                     else:
                        aboat.row_change('down')
                  elif event.key == 107:
                     print
                     print "This button fires out of the port (left) side of your ship."
                     print "The number of missiles that you fire is directly related to how many people you have assigned to be fighting.",
                     print "As you can see on the left, in the third column from the left and the second row down, there are people holding javelin.",
                     print "The number they have is representative of how many missiles you will fire when you hit the key to shoot.",
                     print "You can control how many people are firing with the up and down arrows to the right of any particular person,",
                     print "but note that at default, you will have no people idling to give to any job, and will need to decrease a job before",
                     print "increasing another."
                     aboat.fire('left',shift)
                  elif event.key == 108:
                     print
                     print "This button fires out of the starboard (right) side of your ship."
                     print "For more on firing, hit K."
                     aboat.fire('right',shift)
                  elif event.key == 59:
                     print
                     print "This button will lower the number of sails you have out by one."
                     print "To drop all of your sails, hold shift while pressing the key for this button."
                     print "For more on sails, press the P key."
                     if shift:
                        aboat.sail_change('down',"total")
                     else:
                        aboat.sail_change('down')
                  elif event.key == 109:
                     print
                     print "This button sets your active weapon to be arrows.",
                     print "You have many arrows, and they are your primary weapon. They target your enemy's sails before",
                     print "hitting their hull, however, but in this sense they can also immobilize your opponent.",
                     print "If you hold shift while pressing the fire key and you have arrows equipped, you will shoot",
                     print "flaming arrows, which will actively damage your opponent's ship until they douse the flames."
                     print "For information on firing, hit K."
                     aboat.setweapon('arrows')
                  elif event.key == 44:
                     print
                     print "This button sets your active weapon to be javelin.",
                     print "You have far less javelin than you do arrows, but javelin do thrice as much damage as arrows",
                     print "and they directly target the hull of the ship you are attacking. Javelin move slower than arrows."
                     print "For information on firing, hit K."
                     aboat.setweapon('javelin')
                  elif event.key == ord("."):
                     print 
                     print "This button sets your active weapon to be boulders shot from catapults. Smaller boats like triremes",
                     print "cannot support catapults, and so have no boulders. Boulders are incredibly powerful",
                     print ", but they are also very slow. For information on firing, hit K."
                     aboat.setweapon('rocks')
                  elif event.key == ord("/"):
                     print 
                     print "This button will start fixing your sails."
                     print "As you can see, if you sails were broken, your white bar will now be filling up under your boat.",
                     print "This bar represents the condition of your sails. If it depletes fully,",
                     print "You will need to fix your sails if you want to use them. While fixing your sail,",
                     print "you cannot put up your sail or put out any oars. To stop fixing your sail prematurely, hit the fixsail button again."
                     print
                     print "Press the key of any other button as indicated by the lower-right interface in order to get a message on what it does",
                     print "You might want to start by hitting P."
                     aboat.fixsail()
                  elif event.key == ord("B"):
                     print
                     print "The bailers are the guys throwing water out of a filling-with-water boat."
                     print "If you start taking hull damage, water will start leaking into your boat, and these guys will remove that water.",
                     print "The amount of water in your boat is both represented by a blue bar underneath your hull bar and by the lower number",
                     print "on the bailers' picture. If it reaches your hull number, or if the blue bar reaches all the way to where your max hull would be",
                     print ", then you will sink from taking on too much water."
                  elif event.key == ord("D"):
                     print
                     print "The dousers are the guys throwing water onto a flaming sail.",
                     print "If you are hit by flaming arrows, you will start taking ongoing fire damage until someone douses the fire.",
                     print "Your current fire damage is represented both by a red bar that appears under your sail bar and by the lower number",
                     print "on the dousers' picture. If you have fire damage undoused, you will have a hard time fixing your sail!"
                  elif event.key == ord("F"):
                     print
                     print "The fixers are the guys hammering a ship with holes in it.",
                     print "If you take hull damage, these guys will immediately start working on patching those holes.",
                     print "They work slowly, but they are also necessary if you want to stop taking on water."

                  # If the player hits space, pause the game.
                  elif event.key == K_SPACE:
                     print
                     print "This button pauses the game! To unpause, hit space again."
                     print "The only thing you can do while paused is change how many people are on any particular job,",
                     print "although they won't move jobs until you unpause."
                     paused = True

                   
            #Draw sea
            screen.fill(bgcolor)
                      
            #Draw boats
            for b in ROMANBOATLIST:
               b.update()
            for b in CARTHAGINIANBOATLIST:
               b.update()

            #Draw missiles
            for m in MISSILELIST:
               m.update()

            # Draw terrain
            for t in TERRAINLIST:
               t.update()

            #Draw  Graphic Interfaces
            for i in interfaces:
               i.update(screen)

            if isinstance(highlightlist,dict):
               for h in highlightlist:
                  h.update(screen)

            mini.update()

            # Draw victory text if one side is out of boats

            if len(ROMANBOATLIST) == 0 and self.gameover == False:
               self.end_game('Roman',interfaces)
            elif len(CARTHAGINIANBOATLIST) == 0 and self.gameover == False:
               self.end_game('Carthaginian',interfaces)

            # Draw text interfaces. Currently demands player boat
            # be "aboat".
            self.update_text_interface(aboat, screen, a_font)

            # Render everything, impose fps limit
            pygame.display.flip()
            fpsClock.tick(25)
         else:
            for event in pygame.event.get():
               if event.type == pygame.MOUSEMOTION:
                  mousex, mousey = event.pos
                  highlightlist = self.highlight_interface((mousex, mousey),interfaces,highlightlist)

               #Determine mouse click

               if event.type == pygame.MOUSEBUTTONUP: 
                  mousex, mousey = event.pos

                  # If left-click, determine if interface is being clicked;
                  # run the interface's function if it is. While paused, the
                  # player can only use 'people_manage' functions.
                  if event.button == 1:
                     function, isinterface = self.check_interface((mousex, mousey),interfaces)
                     if isinterface and function[0] == 'p':
                        eval(("aboat." + function))

               # Unpause if space is hit again.

               if event.type == pygame.KEYUP:
                  if event.key == K_SPACE:
                     paused = False

   # This function initates the entire graphical user interface for the 
   # player. Each interface has a given string 'function', boolean functional,
   # and size (effectively height) default 2. If a tuple size is given, it is
   # interpreted as new width and height.

   def init_naval_interface(self):
       interfaces = {}
       turn_cclockwise_box = interface((539,431),"turn('counterclockwise')", interfaces)
       turn_clockwise_box = interface((599,431),"turn('clockwise')", interfaces)
       row_change_up_box = interface((479,431), "row_change('up')", interfaces)
       row_change_down_box = interface((479,479), "row_change('down')", interfaces)
       sail_change_up_box = interface((659,431), "sail_change('up')", interfaces)
       sail_change_down_box = interface((659,479), "sail_change('down')", interfaces)
       fire_left_box = interface((539,479), "fire('left')", interfaces)
       fire_right_box = interface((599,479), "fire('right')", interfaces)
       weapon_arrow_box = interface((479,527), "setweapon('arrows')", interfaces)
       weapon_javelin_box = interface((539,527), "setweapon('javelin')", interfaces)
       weapon_rocks_box = interface((599,527), "setweapon('rocks')", interfaces)
       fix_sail_box = interface((659,527), "fixsail()", interfaces)
       bailers_up_box = interface((59,431), "people_manage('bailers','up')", interfaces, 1)
       bailers_down_box = interface((59,455), "people_manage('bailers','down')", interfaces, 1)
       dousers_up_box = interface((59,479), "people_manage('dousers','up')", interfaces, 1)
       dousers_down_box = interface((59,503), "people_manage('dousers','down')", interfaces, 1)
       fixers_up_box = interface((59,527), "people_manage('fixers','up')", interfaces, 1)
       fixers_down_box = interface((59,551), "people_manage('fixers','down')", interfaces, 1)
       sailors_up_box = interface((179,431), "people_manage('sailors','up')", interfaces, 1)
       sailors_down_box = interface((179,455), "people_manage('sailors','down')", interfaces, 1)
       fighters_up_box = interface((179,479), "people_manage('fighters','up')", interfaces, 1)
       fighters_down_box = interface((179,503), "people_manage('fighters','down')", interfaces, 1)
       rowers_up_box = interface((179,527), "people_manage('rowers','up')", interfaces, 1)
       rowers_down_box = interface((179,551), "people_manage('rowers','down')", interfaces, 1)
       sailorimage = interface((119,431),"sailorimage", interfaces, functional=False)
       bailerimage = interface((0,431),"bailerimage", interfaces, functional=False)
       fighterimage = interface((119,479),"fighterimage",interfaces,functional=False)
       douserimage = interface((0,479),"douserimage",interfaces,functional=False)
       rowerimage = interface((119,527),"rowerimage",interfaces,functional=False)
       fixerimage = interface((0,527),"fixerimage",interfaces,functional=False)
       #bordertop = interface((1,1),"borderhorz",interfaces,(720,1),False)
       #borderleft = interface((1,1),"bordervert",interfaces,(1,430),False)
       #borderright = interface((717,0),"bordervert",interfaces,(1,430),False)
       #borderbottom = interface((0,430),"borderhorz",interfaces,(720,1),False)
       minimap = interface((239,431),"minimap",interfaces,(240,144),False)
       
       return interfaces

   # This function renders all the text objects for the player boat 
   # (currently aboat); for formatting of boat.textvariables, see
   # boat.set_text()

   def update_text_interface(self,aboat, window,a_font):
      items = aboat.textvariables.items()
      for item in items:
         image = a_font.render(str(item[1][0]),1,(255,255,255))
         window.blit(image,item[1][1])      

   def end_game(self,defeated,interfaces):
      self.gameover = True
      if defeated == "Carthaginian":
         vic_text = interface((210,41),"romanvictory",interfaces,(300,150),functional = False)
      else:
         vic_text = interface((210,41),"carthaginianvictory",interfaces,(300,150),functional = False)


   # This function is called to mirror menu_event_handler upon exiting
   # naval gameplay 

   def menu_done(self):
      global MODE
      MODE = "Menu"

class menu_event_handler(event_handler):

   # The menu event handler (expectedly) handles events when the MODE = "Menu"

   def __init__(self,screen,fpsClock):
      self.font = pygame.font.Font(None, 24)
      self.running = True
      self.menuplace = 1
      self.boattype = "quinquereme"
      self.scenario = "3v3"
      self.textlist = []
      while self.running:
         if MODE != "Menu":
            return
         if self.menuplace == 1:
            self.bgcolor = (30,10,10)
            interfaces = self.init_menu1_interface()
         elif self.menuplace == 3:
            interfaces = self.init_menu3_interface()
         elif self.menuplace == 2:
            interfaces = self.init_menu2_interface()
         elif self.menuplace == 4:
            interfaces = self.init_menu4_interface()
         if self.menuplace == 0:
            for event in pygame.event.get():
               if event.type == pygame.QUIT:
                  print("User asked to quit.")
                  self.running = False
               if event.type == pygame.MOUSEBUTTONUP: 
                  mousex, mousey = event.pos

                  #If left-click, determine if interface is being clicked;
                  #run the interface's function if it is.
                  if event.button == 1:
                     function, isinterface = self.check_interface((mousex, mousey),interfaces)
                     if isinterface:
                        eval(("self."+function))

         screen.fill(self.bgcolor)
         #Draw  Graphic Interfaces
         for i in interfaces:
            i.update(screen)
         for t in self.textlist:
            self.update_text_interface(t,screen)

         pygame.display.flip()
         fpsClock.tick(30)

   # Because __init__ cannot return values, this function is called upon
   # a mode change to return the values that the naval event handler needs.

   def menu_done(self):
      return self.running, self.boattype, self.scenario

   # These functions create the menu items which are appropriate
   # based on which menu is currently active.

   def update_text_interface(self,text,screen):
      screen.blit(text[0],text[1])

   def init_menu1_interface(self):
      interfaces = {}

      logo_box = interface((200,50),"logo", interfaces, (300,150),False)
      playgame_box = interface((100,400), "playgame()", interfaces, (150,75))

      self.menuplace = 0

      return interfaces

   def init_menu2_interface(self):
      self.textlist = []
      interfaces = {}

      arenatype_box = interface((40,300),'arenatype', interfaces, (150,50), False)
      boattype_box = interface((40,200),"boattype", interfaces, (150,50), False)
      arenatype_change_box = interface((450,312),'arenachange()',interfaces,(64,32))
      boattype_change_box = interface((450,212),'boattypechange()',interfaces,(64,32))
      proceed_box = interface((400,450),'proceed()',interfaces,(150,75))
      self.textlist.append([(self.font.render(str(self.boattype),1,(255,255,255))),(210,225)])
      self.textlist.append([(self.font.render(str(self.scenario),1,(255,255,255))),(210,325)])

      self.menuplace = 0

      return interfaces

   def init_menu3_interface(self):
      interfaces = {}

      self.textlist = []

      trireme_box = interface((200,200),"set_player_boat('trireme')", interfaces, (150,75))
      bireme_box = interface((400,200),"set_player_boat('bireme')", interfaces, (150,75))
      quadireme_box = interface((200,400), "set_player_boat('quadrireme')", interfaces, (150,75))
      quinquereme_box = interface((400,400),"set_player_boat('quinquereme')",interfaces, (150,75))

      self.menuplace = 0

      return interfaces  

   def init_menu4_interface(self):
      interfaces = {}
      self.textlist = []
      
      test_box = interface((200,200),"set_scenario('1v1')", interfaces, (150,75))
      arena_box = interface((400,200),"set_scenario('3v3')", interfaces, (150,75))
      arena2_box = interface((200,400), "set_scenario('2v6')", interfaces, (150,75))
      tutorial_box = interface((400,400),"set_scenario('Tutorial')",interfaces, (150,75))

      self.menuplace = 0

      return interfaces

   #These functions are all reactions to clicking menu items.

   def arenachange(self):
      self.menuplace = 4 

   def boattypechange(self):
      self.menuplace = 3

   def set_scenario(self,scenario):
      self.scenario = scenario
      self.menuplace = 2

   def set_player_boat(self,boat):
      self.boattype = boat
      self.menuplace = 2

   def playgame(self):
      self.menuplace = 2

   def proceed(self):
      global MODE
      MODE = "Naval"
      self.menuplace = 0

   def options(self):
      self.menuplace = 3    

def main():

    #This doesn't need to be a global at all, will change in future versions
    #This global as it exists defines which functions represent standard up
    #or down arrow images for the uniqueimagecheck function in class interface

    global STANDARDIMAGES
    STANDARDIMAGES = ["people_manage('bailers','up')","people_manage('bailers','down')",
                      "people_manage('dousers','up')","people_manage('dousers','down')",
                      "people_manage('fixers','up')","people_manage('fixers','down')",
                      "people_manage('sailors','up')","people_manage('sailors','down')",
                      "people_manage('fighters','up')","people_manage('fighters','down')",
                      "people_manage('rowers','up')","people_manage('rowers','down')"]

    # This global determines the mode of play.

    global MODE
    MODE = "Menu"

    # Initiate pygame and fps limiter clock
    pygame.init()
    pygame.font.init()
    pygame.mixer.pre_init(frequency=44100)
    pygame.mixer.init()

    fpsClock = pygame.time.Clock()

    # Draw screen
    winWidth, winHeight = 720, 576
    screen = pygame.display.set_mode((winWidth, winHeight)) 
    pygame.display.set_caption("")

    # Event Handler
    running = True
    while running:
      if MODE == "Menu":
         menu = menu_event_handler(screen, fpsClock)
         running, boattype, scenario = menu.menu_done()      
      elif MODE == "Naval":
         naval_menu = naval_event_handler(screen,fpsClock, boattype, scenario)
         naval_menu.menu_done()

    pygame.quit()

if __name__=="__main__":
    main()
