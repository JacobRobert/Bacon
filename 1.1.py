import pyglet
from pyglet.gl import *
from pyglet.window import key
import random
import math


farmer_image = pyglet.resource.image("farmer.png")  #loads images
pig_image = pyglet.resource.image("pig.png")

def center_image(image):                    #changes the images anchors to the center of the image
    image.anchor_x = image.width/2
    image.anchor_y = image.height/2

center_image(farmer_image)
center_image(pig_image)

main_batch   = pyglet.graphics.Batch()      #makes a group of everything that will be drawn

game_width  = 1400      #Sets game window size
game_height = 700

game_window = pyglet.window.Window(game_width, game_height) #opens window
game_window.set_caption("Cow Tipper")

def distance(pt_1=(0,0), pt_2=(0,0)):   #finds distance between two points
    return math.sqrt(
        (pt_1[0] - pt_2[0]) ** 2 +
        (pt_1[1] - pt_2[1]) ** 2)

class PhysicalObject(pyglet.sprite.Sprite):     #basic object class

    def __init__(self, *args, **kwargs):
        super(PhysicalObject, self).__init__(*args, **kwargs)

        self.velocity_x, self.velocity_y = 0.0, 0.0
        self.rotation_speed = .1
        self.dead = False
        self.scale = 1
        
    def update(self, dt):
        self.x += self.velocity_x * dt  #moves object
        self.y += self.velocity_y * dt

        self.check_bounds()     
        self.totter()

    def check_bounds(self):         #if the object hits the edge of the window, the object reverses direction
        min_x = self.image.width/2
        min_y = self.image.height/2
        max_x = game_width - self.image.width/2
        max_y = game_height - self.image.height/2

        if self.x < min_x or self.x > max_x:
            self.velocity_x = self.velocity_x * -1
        if self.y < min_y or self.y > max_y:
            self.velocity_y = self.velocity_y * -1

    def totter(self):               #rotates the object as it moves, BROKEN
        if self.rotation > 20:
            self.rotation -= self.rotation_speed
        elif self.rotation  < 0:
            self.rotation += self.rotation_speed

    def collides_with(self, other_object):          #checks if 2 objects are touching
        collision_distance = self.image.width/2 + other_object.image.width/2
        actual_distance = distance(self.position, other_object.position)

        return (actual_distance <= collision_distance)

    def handle_collision_with(self, other_object):
        self.dead = True
        


class PlayerObject(PhysicalObject):

    def __init__(self, *args, **kwargs):
        super(PlayerObject, self).__init__(img=farmer_image,*args,**kwargs)

        self.speed = 400

        self.keys = dict(left=False, right=False, up=False, down=False)

    def on_key_press(self, symbol, modifiers): #checks what buttons are being pressed
        if symbol == key.UP:
            self.keys['up'] = True
        elif symbol == key.DOWN:
            self.keys['down'] = True
        elif symbol == key.LEFT:
            self.keys['left'] = True
        elif symbol == key.RIGHT:
            self.keys['right'] = True

    def on_key_release(self, symbol, modifiers):
        if symbol == key.UP:
            self.keys['up'] = False
        elif symbol == key.DOWN:
            self.keys['down'] = False
        elif symbol == key.LEFT:
            self.keys['left'] = False
        elif symbol == key.RIGHT:
            self.keys['right'] = False

    def update(self, dt):
        super(PlayerObject, self)

        if self.keys['left']:           #moves objects based on what keys are pressed
            self.x -= self.speed * dt
        if self.keys['right']:
            self.x += self.speed * dt
        if self.keys['up']:
            self.y += self.speed * dt
        if self.keys['down']:
            self.y -= self.speed * dt

        if self.x > game_width - 50:    #stops player from leaving the screen
            self.x -= self.speed * dt
        if self.x < 0:
            self.x += self.speed * dt
        if self.y > game_height:
            self.y -= self.speed * dt
        if self.y < 0:
            self.y += self.speed * dt

player = PlayerObject(x=400, y=300, batch=main_batch)   #places instance of player, adds player to the batch
player_position = player.x, player.y

def pigs(num_pigs):
    pigs = []
    for i in range(num_pigs):
        pig_x, pig_y = player_position      #checks if pig is spawning on the player
        while distance((pig_x, pig_y), player_position) < 300:
            pig_x = random.randint(1,game_width-100)    #randomly spawns pigs
            pig_y = random.randint(1,game_height-100)
        new_pig = PhysicalObject(img=pig_image, x=pig_x, y=pig_y, batch=main_batch)
        new_pig.velocity_x = random.random()*400    #gives each pig a random speed and direction
        new_pig.velocity_y = random.random()*400
        pigs.append(new_pig)    #adds pig to pigs
    return pigs


def update(dt):
    for obj in game_objects:    #updates all objects
        obj.update(dt)

    for pig in pigs:    #if pigs are dead they are removed from the drawing list
        for to_remove in [pig for pig in pigs if pig.dead]:
            to_remove.delete()
            pigs.remove(to_remove)

    for i in xrange(len(pigs)):     #checks collisions of player against every pig BROKEN 
        obj_1 = player
        obj_2 = pigs[i]

        if not obj_2.dead:
            if obj_2.collides_with(obj_1):
                obj_2.handle_collision_with(obj_1)

    


level_label = pyglet.text.Label(text="Level 1", x=400, y=575, anchor_x='center', batch=main_batch) #Level label


pigs = pigs(10)     #spawns 10 pigs


game_window.push_handlers(player)   #checks keystrokes

game_objects = [player] + pigs

@game_window.event
def on_draw():      #draws everything        
    
    pyglet.gl.glClearColor(34,139,34,255)
    game_window.clear()

    main_batch.draw()
    

pyglet.clock.schedule_interval(update, 1/120.0) #sets speed of graphics(dt)
    
pyglet.app.run()
