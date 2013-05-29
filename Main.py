from time import *
import pygame
import math
import random

MISSILELIST = []
ROMANBOATLIST = []
CARTHAGINIANBOATLIST = []

class boat():

   # Set every single variable for the boat. If a 'c'
   # is before a word, it represents 'current', else
   # a 'c' after a word represents 'count'.

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
         self.acceleration = .01
         self.deceleration = .05

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
      self.firedamage = 0
      self.waterdamage = 0

      # Initiates dictionary of variables which are rendered as text objects

      self.textvariables = {}
      self.set_text()

   def set_text(self):
      self.textvariables["self.speed"] = [self.speed, (self.x+30,self.y)]
      self.textvariables["self.chull"] = [self.chull, (self.x,self.y)]
      self.textvariables["self.csail"] = [self.csail, (self.x,self.y - 10)]
      self.textvariables["self.cpeople"] = [self.cpeople, (5,5)]
      self.textvariables["self.crowers"] = [self.crowers, (121,529)]
      self.textvariables["self.cfixers"] = [self.cfixers, (2,529)]
      self.textvariables["self.cdousers"] = [self.cdousers, (2,481)]
      self.textvariables["self.cbailers"] = [self.cbailers, (2,433)]
      self.textvariables["self.csailors"] = [self.csailors, (121,433)]
      self.textvariables["self.cfighters"] = [self.cfighters, (121,481)]
      self.textvariables["self.carrows"] = [self.carrows, (self.x, self.y+30)]

   # Set default images as according to the boat's prefix

   def set_images(self, prefix):
      self.sailupimage = prefix + "sailup"
      self.saildownimage = prefix +"saildown"

      # Currently unused
      self.sinkimage = prefix + "sinkimage"

   # Creates appropriate count of missiles of appropriate kind
   # when the user fires out of either side of the boat.

   def fire(self, side):
      self.firingside = side

      # Checks to ensure there is a current weapon
      if self.cweapon == None:
         None
         # Currently unused
         # new_sound = error_sound(nope)
      else:

         # Sets appropriate kind of weapon as internal variable
         # 'weapon'

         if self.cweapon == "arrows":
            weapon = self.carrows
         elif self.cweapon == "javelin":
            weapon = self.cjavelin
         elif self.cweapon == "rocks":
            weapon = self.crocks

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
            new_missile = missile(self.cweapon,ammo_fired,self.window,self.angle,self.firingside,(self.x+(self.drawnimage.get_width() / 2),self.y+(self.drawnimage.get_height() / 2)),self.alliance)
            weapon -= ammo_fired

         elif weapon == 0:
            #new_sound = error_sound(nope)
            return None

         elif weapon <= self.cfighters and self.cweapon != "rocks":
            new_missile = missile(self.cweapon,weapon,self.window,self.angle,self.firingside,(self.x+(self.drawnimage.get_width() / 2),self.y+(self.drawnimage.get_height() / 2)),self.alliance)
            weapon = 0
         elif weapon <= self.cfighters and self.cweapon == "rocks":
            new_missile = missile(self.cweapon,1,self.window,self.angle,self.firingside,(self.x+(self.drawnimage.get_width() / 2),self.y+(self.drawnimage.get_height() / 2)),self.alliance)
            weapon -= 1
            

         # Resets appropriate weapon to the changed value as per
         # ammo_fired
         if self.cweapon == "arrows":
            self.carrows = weapon
         elif self.cweapon == "javelin":
            self.cjavelin = weapon
         elif self.cweapon == "rocks":
            self.crocks = weapon

   # This function takes damage upon being hit by anything

   def ishit(self,count,weapon):

      if weapon == "arrows":
         damage = 1
         prime_target = "sail"

      elif weapon == "javelin":
         damage = 3
         prime_target = "people"

      elif weapon == "rocks":
         damage = 45
         prime_target = "hull"

      else:
         damage = 10
         prime_target = "hull"

      tot_damage = count * damage

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

      # Destroys boat if boat's hull at 0 or less  

      if self.chull <= 0:
         self.destroy()

   # Removes and disposes of destroyed boats.
   # Will eventually use self.sinkimage

   def destroy(self):
      self.x = -50
      self.y = -50
      self.update()
      if self.alliance == "Roman":
         ROMANBOATLIST.remove(self)
      else:
         CARTHAGINIANBOATLIST.remove(self)
   
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
      elif self.angle >= 360:
         self.angle = self.angle - 360

   # CREDIT: Gummbum via pygame.org, replace function with something
   # self-written??
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
      if self.csail != self.sail:   
         self.fixingsail = True

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
      
   def update(self):

      # Hull repair

      if 0 < self.chull < self.hull:
         self.chull += self.cfixers / float(100)
         print self.chull
      if self.fixingsail == True:
         self.sail_change("down","total")
         self.row_change("down","total")
         print "fixing sail"
         self.csail += .5
         if self.csail == self.sail:
            self.fixingsail = False
            print "done fixing sail" 


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

      # Runs functions to update boat image and boat text interfaces
         
      self.load_image()
      self.drawnimage = self.change_image(self.baseimage,self.angle)
      self.window.blit(self.drawnimage, (self.x,self.y))
      self.set_text()

      if self.alliance == "Carthaginian":
         self.enemyAI()

   def enemyAI(self):
      if self.csail == 0:
         self.fixsail()
         return
      elif self.speed == 0:
         self.sail_change('up')
         self.row_change('up')
         return
      else:
         if self.cweapon == None:
            self.setweapon('arrows')
            return
         elif self.x > 640 and self.angle != 90:
            if self.angle != 270:
               self.turn('counterclockwise')
               return
         if self.y < 50 and self.angle != 180:
            if self.angle != 0:
               self.turn('counterclockwise')
               return
         elif self.x < 50 and self.angle != 90:
            if self.angle != 270:
               self.turn('counterclockwise')
               return
         elif self. y > 360 and self.angle != 180:
            if self.angle != 0:
               self.turn('counterclockwise')
               return
         else:
            for b in ROMANBOATLIST:
               if self.y - 5 < b.y < self.y + 5:
                  if self.angle == 270:
                     if b.x < self.x:
                        self.fire('left')
                     else: self.fire('right')
                     return
                  elif self.angle == 90:
                     if b.x < self.x:
                        self.fire('right')
                     else: self.fire('left')
                     return
               elif self.x - 5 < b.x < self.x + 5:
                  if self.angle == 180:
                     if b.y < self.y:
                        self.fire('right')
                     else: self.fire('left')
                     return
                  elif self.angle == 0:
                     if b.y < self.y:
                        self.fire('left')
                     else: self.fire('right')
                     return
               else:
                  if self.csail != self.cmaxsails or self.crows != self.cmaxrows:
                     self.sail_change('up')
                     self.row_change('up')
         
         
   
# Missile inherits Boat solely so that missile can use boat's 
# change_image function to rotate itself on being spawned

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

         if self.count == 0 or weapon == "rocks":
            self.count = 1
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
             self.speed = 4
             self.error = 4
             self.maxdeathtoll = 60

         self.deathtoll = 0
         MISSILELIST.append(self)

   def update(self):

         # Determines how considerably the missile will waver in its path, javelin
         # are perfectly accurate and will not have inaccuracy.

         if self.weapon != "javelin":
             inaccuracy = float(random.randint(-(self.error*5),(self.error*5)))/20
         else: inaccuracy = 0

         # Moves the missile as according to its angle and inaccuracy

         self.x += (math.cos(math.radians(self.angle)) * self.speed) + inaccuracy
         self.y += (math.sin(math.radians(self.angle)) * self.speed) + inaccuracy

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
                  b.ishit(self.count,self.weapon)

                  # Kills missile upon contact
                  self.deathtoll = self.maxdeathtoll-1

         self.window.blit(self.missileimage, (self.x,self.y))
         
         # Remove and dispose of the missile upon the missile reaching its maximum range   
         self.deathtoll += 1
         if self.deathtoll == self.maxdeathtoll:
            self.window.blit(self.missileimage, (-50,-50))
            MISSILELIST.remove(self)

#This class represents clickable graphical user interfaces

class interface():
    def __init__(self, (x,y), function, interfacelist, size=2, functional=True):
        self.x = x
        self.y = y
        self.functional = functional
        self.function = function

        # Adds self to interface list along with self's size for click checking

        interfacelist[self]=[[x,x+60],[y,y+(24*size)]]

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
        window.blit(self.drawnimage, (self.x,self.y))

# This function updates the text interface for the active player boat.

def update_text_interface(aboat, window,a_font):
   items = aboat.textvariables.items()
   for item in items:
      image = a_font.render(str(item[1][0]),1,(255,255,255))
      window.blit(image,item[1][1])
      
         
# This function initates the entire graphical user interface for the 
# player. Each interface has a given string 'function', boolean functional,
# and size (effectively height) default 2.

def init_naval_interface():
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
    
    return interfaces
        
# This function acts with left clicks to run the function of an interface
# when the interface is clicked given that 1) an interface is being clicked
# and 2) the interface is "functional=True"

def check_interface((x,y),interfacelist):
    interfaces = interfacelist.items()
    for item in interfaces:
        if item[0].functional:
            if item[1][0][0] <= x <= item[1][0][1]:
                if item[1][1][0] <= y <= item[1][1][1]:
                    return item[0].function, True
    return None, False

# Intended future functionality: when clicking on a boat, 
# take control of that boat.
def select_boat(boat):
    #PLACEHOLDER
    None

# Intended future use as a place to put the event handling code
# currently in main().
def event_handler():
    #PLACEHOLDER
    None

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

    # This global determines the mode of play. Currently functional only as Naval, 
    # later functionality includes Terrestrial and Pregame / Menu.

    global MODE
    MODE = "Naval"

    # Initiate pygame and fps limiter clock
    pygame.init()
    pygame.font.init()
    a_font = pygame.font.Font(None, 16)
    fpsClock = pygame.time.Clock()

    # Draw screen
    winWidth, winHeight = 720, 576
    screen = pygame.display.set_mode((winWidth, winHeight)) 
    pygame.display.set_caption("")
    bgcolor = pygame.Color(25,100,250)

    # Create current basic enemy and player boats
    aboat = boat("quadrireme", "Roman", (20,20), screen)
    enemy_boat = boat("trireme","Carthaginian", (360,360), screen)

    # Add boats to global boat-draw lists
    ROMANBOATLIST.append(aboat)
    CARTHAGINIANBOATLIST.append(enemy_boat)

    # Initiate GUI
    interfaces = init_naval_interface()

    # Event Handler
    running = True
    while running:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                print("User asked to quit.")
                running = False

            #Placeholder, may not be used    
            if event.type == pygame.MOUSEMOTION:
                mousex, mousey = event.pos

            #Determine mouse actions
            if event.type == pygame.MOUSEBUTTONUP: 
                mousex, mousey = event.pos

                #If left-click, determine if interface is being clicked;
                #run the interface's function if it is.
                if event.button == 1:
                    function, isinterface = check_interface((mousex, mousey),interfaces)
                    if isinterface:
                        if MODE == "Naval":
                            eval(("aboat." + function))

                # Placeholder, may not be used
                elif event.button == 2:
                    print "middle click"
                elif event.button == 3:
                    print "right click"

            # Determine what interface to run on keyboard input
            elif event.type == pygame.KEYUP:
                if event.key == 117:
                    aboat.row_change('up')
                elif event.key == 105:
                    aboat.turn('counterclockwise')
                elif event.key == 111:
                    aboat.turn('clockwise')
                elif event.key == 112:
                    aboat.sail_change('up')
                elif event.key == 106:
                    aboat.row_change('down')
                elif event.key == 107:
                    aboat.fire('left')
                elif event.key == 108:
                    aboat.fire('right')
                elif event.key == 59:
                    aboat.sail_change('down')
                elif event.key == 109:
                    aboat.setweapon('arrows')
                elif event.key == 44:
                    aboat.setweapon('javelin')
                elif event.key == ord("."):
                    aboat.setweapon('rocks')
                elif event.key == ord("/"):
                    aboat.fixsail()
                
        #Draw sea
        screen.fill(bgcolor)

        #Draw Terrain
                
        #Draw boats
        for b in ROMANBOATLIST:
            b.update()
        for b in CARTHAGINIANBOATLIST:
            b.update()

        #Draw Missiles
        for m in MISSILELIST:
            m.update()

        #Draw  Graphic Interfaces
        for i in interfaces:
            i.update(screen)

        #Draw text interfaces
        update_text_interface(aboat, screen, a_font)
                

        pygame.display.flip()
        fpsClock.tick(30)
    pygame.quit()

if __name__=="__main__":
    main()
