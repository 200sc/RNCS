from time import *
import pygame
import math
import random

MISSILELIST = []
ROMANBOATLIST = []
CARTHAGINIANBOATLIST = []

class boat():
   def __init__(self,type,alliance,(x,y),window):
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
         self.sail = 35
         self.people = 50
         self.catapult = False
         self.rocks = 0
         self.set_images("bi")
         self.acceleration = .2
         self.deceleration = .2
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
      self.arrows = self.people * 2
      self.carrows = self.arrows
      self.javelin = self.people 
      self.cjavelin = self.javelin
      self.crocks = self.rocks
      self.cweapon = None
      self.angle = 0
      self.fixingsail = False
      self.firingside = None
      self.type = type
      self.alliance = alliance
      self.x = x
      self.y = y
      self.rowname = ""
      self.sailname = self.saildownimage
      self.load_image()
      self.drawnimage = pygame.image.load("data/"+self.saildownimage+".gif")
      self.rect = self.baseimage.get_rect()
      self.imageangle = self.angle
      self.max_speed = None
      self.speed = 0
      self.window = window
   def set_images(self, prefix):
      self.sailupimage = prefix + "sailup"
      self.saildownimage = prefix +"saildown"           
      self.sinkimage = prefix + "sinkimage"
   def fire(self, side):
      self.firingside = side
      if self.cweapon == None:
         None
         #new_sound = error_sound(nope)
      elif self.cweapon:
         if self.cweapon == "arrows":
            weapon = self.carrows
         elif self.cweapon == "javelin":
            weapon = self.cjavelin
         elif self.cweapon == "rocks":
            weapon = self.crocks
         if weapon > self.cfighters:
            if self.cfighters > 25:
               ammo_fired = 25
            else: ammo_fired = self.cfighters
            new_missile = missile(self.cweapon,ammo_fired,self.window,self.angle,self.firingside,(self.x+32,self.y+32),self.alliance)
            weapon -= ammo_fired
         elif weapon == 0:
            #new_sound = error_sound(nope)
            return None
         elif weapon <= self.cfighters:
            new_missile = missile(self.cweapon,weapon,self.window,self.angle,self.firingside,(self.x+32,self.y+32),self.alliance)
            weapon = 0
         if self.cweapon == "arrows":
            self.carrows = weapon
         elif self.cweapon == "javelin":
            self.cjavelin = weapon
         elif self.cweapon == "rocks":
            self.crocks = weapon

   def setweapon(self,weapon):
      self.cweapon = weapon
   def turn(self,direction):
      mod = 15
      if direction == "clockwise":
         self.angle = self.angle + mod
      elif direction == "counterclockwise":
         self.angle = self.angle - mod
      if self.angle < 0:
         self.angle = self.angle + 360
      elif self.angle > 360:
         self.angle = self.angle - 360

   # CREDIT: Gummbum via pygame.org, replace function with something
   # self-written??
   def change_image(self,image,angle = None):
      rect = image.get_rect()
      rotated_image = pygame.transform.rotate(image, -angle)
      rotated_rect = rect.copy()
      rotated_rect.center = rotated_image.get_rect().center
      rotated_image = rotated_image.subsurface(rotated_rect).copy()
      return rotated_image
   
   def fixsail(self):
      if self.csail != self.sail:   
         self.fixingsail = True
         self.sail_change("down","total")
         self.row_change("down","total")
         while self.fixingsail == True:
            print "fixing sail"
            #[time?, wait]
            self.csail += 1
            if self.csail == self.sail:
               self.fixingsail = False
               print "done fixing sail"

   def sail_change(self,direction,amount=1):
      if self.csail != 0:
         if amount == "total" and direction == "down":
            while self.csailsout != 0:
               #[time?, wait]
               self.csailsout -= 1
         elif amount == "total" and direction == "up":
            while self.csailsout != self.cmaxsails:
               #[time?, wait]
               self.csailsout += 1
         else:
            if self.csailsout < self.cmaxsails and direction == "up":
               #[time?, wait]
               self.csailsout += amount
            elif self.csailsout > 0 and direction == "down":
               self.csailsout -= amount
         if self.csailsout == 0:
            self.sailname = self.saildownimage
         else:
            self.sailname = self.sailupimage
         
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
         
   def people_manage(self,person,direction,magnitude=1):
      if direction == "up":
         if self.cidlers >= magnitude * 5:
            change = magnitude*5
         else:
            change = self.cidlers
            if change == 0:
               print "cidlers = 0"
               return
         cperson = eval("self.c"+person)
         if cperson <= self.people - change:
            cperson += change
            self.cidlers -= change
            self.update_person(person,cperson)
            print self.cidlers
            print eval("self.c"+person)
      

      else:
         if self.cidlers <= self.people - magnitude * 5:
            cperson = eval("self.c"+person)
            if cperson == 0:
               print "cperson = 0"
               return
            else:
               if cperson - magnitude*5 < 0:
                  change = -(cperson - magnitude*5)
                  cperson = 0
               else:
                  change = magnitude*5
                  cperson -= change
               self.cidlers += change
               self.update_person(person,cperson)
               print self.cidlers
               print eval("self.c"+person)
      self.update_max_speed()
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
      
         
      
   def load_image(self):
      self.baseimage = pygame.image.load("data/"+self.sailname+self.rowname+".gif")

   def write(self, element):
      self.window.blit(element, 1, (255,255,255)) 
      
   def update(self):
      if self.crows or self.csailsout:
         self.max_speed = (self.crows + (self.csailsout * 2)) * .75
         accelerating = True
      else:
         accelerating = False   
      if self.max_speed:
         if self.speed <= self.max_speed and accelerating:
            self.speed += self.acceleration
         elif self.speed > 0 and not accelerating:
            self.speed -= self.deceleration
         elif self.speed > self.max_speed + self.deceleration:
            self.speed -= self.deceleration
         elif self.speed < 0:
            self.speed = 0
         self.x += math.cos(math.radians(self.angle)) * self.speed
         self.y += math.sin(math.radians(self.angle)) * self.speed
      self.load_image()
      self.drawnimage = self.change_image(self.baseimage,self.angle)
      self.window.blit(self.drawnimage, (self.x,self.y))
      
class missile(boat):
   def __init__(self,weapon,count,window,angle,firingside,(x,y),alliance):
         self.alliance = alliance
         self.num = count / 5
         print self.num
         if count < 26:
            self.count = count
         else:
            self.count = 25
         if self.num < 5:
            self.count = self.num * 5
         if self.count == 0:
            self.missileimage = pygame.image.load("data/"+weapon+".gif")
         else: 
            self.missileimage = pygame.image.load("data/"+weapon+str(self.count)+".gif")
         if firingside == "left":
             self.angle = angle - 90
         elif firingside == "right":
             self.angle = angle + 90
         self.missileimage = self.change_image(self.missileimage,self.angle+180)
         self.weapon = weapon
         self.x,self.y = (x,y)
         self.window = window
         self.speed = None
         if self.weapon == "javelin":
             self.speed = 4
             self.error = 0
             self.maxdeathtoll = 30
         elif self.weapon == "arrows":
             self.speed = 8
             self.error = 2
             self.maxdeathtoll = 60
         else: 
             self.speed = 2
             self.error = 4
             self.maxdeathtoll = 60
         self.deathtoll = 0
         MISSILELIST.append(self)

   def update(self):
         if self.weapon != "javelin":
             inaccuracy = float(random.randint(-(self.error*5),(self.error*5)))/20
         else: inaccuracy = 0
         self.x += (math.cos(math.radians(self.angle)) * self.speed) + inaccuracy
         self.y += (math.sin(math.radians(self.angle)) * self.speed) + inaccuracy
         if self.alliance == "Roman":
            if enemy_boat.x < self.x < (enemy_boat.x + enemy_boat.drawnimage.get_width()):
               print "got this far too"
               if enemy_boat.y < self.y < (enemy_boat.y + enemy_boat.drawnimage.get_height()):
                  print "it's a hit"
            #for b in CARTHAGINIANBOATLIST:
            #   print "got this far"
            #   if b.x < self.x < (b.x + b.drawnimage.get_width()):
            #      print "got this far too"
            #      if b.y < self.y < (b.y + b.drawnimage.get_height()):
            #         print "it's a hit"
         else:
            for b in ROMANBOATLIST:
               print "got this far"
               if b.x < self.x < (b.x + b.drawnimage.get_width()):
                  print "got this far too"
                  if b.y < self.y < (b.y + b.drawnimage.get_height()):
                     print "it's a hit"
         self.window.blit(self.missileimage, (self.x,self.y))
            
         self.deathtoll += 1
         if self.deathtoll == self.maxdeathtoll:
            self.window.blit(self.missileimage, (-50,-50))
            MISSILELIST.remove(self)

