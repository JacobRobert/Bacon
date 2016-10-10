import pyglet
from pyglet.gl import *
from pyglet.window import key
import random
import math


farmer_image = pyglet.resource.image("farmer.png")  #loads images
pig_image = pyglet.resource.image("pig.png")
angry_pig_image = pyglet.resource.image("angrypig.png")
field_image = pyglet.resource.image("field.png")
game_over = pyglet.resource.image("game over.png")


def center_image(image):                    #changes the images anchors to the center of the image
    image.anchor_x = image.width/2
    image.anchor_y = image.height/2

center_image(farmer_image)
center_image(pig_image)

def distance(pt_1=(0,0), pt_2=(0,0)):   #finds distance between two points
    return math.sqrt(
        (pt_1[0] - pt_2[0]) ** 2 +
        (pt_1[1] - pt_2[1]) ** 2)

def spawn_pigs(num_pigs, image):    #Function that spawns pigs
    pigs = []
    for i in range(num_pigs):
        pig_x, pig_y = player_position      #checks if pig is spawning on the player
        while distance((pig_x, pig_y), player_position) < 300:
            pig_x = random.randint(100,game_width-120)    #spawns pigs at random locations
            pig_y = random.randint(100,game_height-120)
        pig_rotation = random.randint(-20,20)
        pig_scale = random.randint(7,13)/10.0
        new_pig = PhysicalObject(img=image, x=pig_x, y=pig_y, batch=main_batch, rotation=pig_rotation, scale=pig_scale)
        new_pig.velocity_x = random.random()*400    #gives each pig a random speed and direction
        new_pig.velocity_y = random.random()*400
        pigs.append(new_pig)    #adds pig to pigs
    return pigs

class PhysicalObject(pyglet.sprite.Sprite):     #basic object class (pig)

    def __init__(self, rotation=0, scale=1, *args, **kwargs):
        super(PhysicalObject, self).__init__(*args, **kwargs)

        self.velocity_x, self.velocity_y = 0.0, 0.0
        self.rotation_speed = 1
        self.dead = False
        self.scale = scale          #random size
        self.rot_dir = -1           #initial rotation direction
        self.rotation = rotation    #random initial rotation

    def update(self, dt):
        self.x += self.velocity_x * dt  #moves object
        self.y += self.velocity_y * dt

        self.check_bounds() #keeps object on the screen
        self.totter()       #rotates object

    def check_bounds(self):         #if the object hits the edge of the window, the object reverses direction
        min_x = self.image.width/2 + 80
        min_y = self.image.height/2 + 80
        max_x = game_width - self.image.width/2 - 80
        max_y = game_height - self.image.height/2 - 80

        if self.x < min_x or self.x > max_x:
            self.velocity_x = self.velocity_x * -1
        if self.y < min_y or self.y > max_y:
            self.velocity_y = self.velocity_y * -1

    def totter(self):               #rotates the object as it moves

        if self.rotation > 20:
            self.rot_dir = -1
        elif self.rotation  < -20:
            self.rot_dir = 1
        self.rotation += self.rot_dir * self.rotation_speed

    def collides_with(self, other_object):          #checks if 2 objects are touching
        collision_distance = self.image.width/2 + other_object.image.width/2
        actual_distance = distance(self.position, other_object.position)

        return (actual_distance <= collision_distance)

    def handle_collision_with(self, other_object):
        self.dead = True


class PlayerObject(PhysicalObject):     #creates player class

    def __init__(self, *args, **kwargs):
        super(PlayerObject, self).__init__(img=farmer_image,*args,**kwargs)

        self.speed = 200    #speed of movement
        self.score = 500   #Initial score

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

    def on_key_release(self, symbol, modifiers): #checks if buttons are released
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
        if self.x < self.image.width/2:
            self.x += self.speed * dt
        if self.y > game_height:
            self.y -= self.speed * dt
        if self.y < self.image.height/2:
            self.y += self.speed * dt

        if self.score > 0:
            self.score -= 1

    def handle_collision_with(self, other_object):
        self.score += 100

    def kill(self):
        self.dead = True

main_batch   = pyglet.graphics.Batch()      #makes a group of everything that will be drawn

game_width  = 1400      #Sets game window size
game_height = 700
game_window = pyglet.window.Window(game_width, game_height) #opens window
game_window.set_caption("Bacon")

player = PlayerObject(x=400, y=300, batch=main_batch)   #places instance of player, adds player to the batch
player_position = player.x, player.y
game_window.push_handlers(player)   #checks keystrokes

numpigs = 10    #sets # of pigs to spawn
pigs = spawn_pigs(numpigs, pig_image)           #spawns 10 pigs
angry_pigs = spawn_pigs(4, angry_pig_image)     #spawns 4 angry pigs
score_label = pyglet.text.Label(text=("Score:" + str(player.score)) , x=100, y=600, bold=True, font_size=25, color=(0,0,0,255), batch=main_batch) #Displays score
final_score_label = pyglet.text.Label(x=700, y=300,anchor_x='center', bold=True, font_size=35, color=(0,0,0,255), batch=main_batch) #displays Final Score

game_objects = [player] + pigs + angry_pigs #list of all updating objects

over = False
def update(dt):
    for obj in game_objects:    #updates all objects
        obj.update(dt)

    score_label.text = "Score:" + str(player.score)

    for to_remove in pigs:              #if pigs are dead they are removed from the drawing and updating lists list
        if to_remove.dead:
            to_remove.delete()
            pigs.remove(to_remove)
            game_objects.remove(to_remove)

    for i in range(len(pigs)):                  #checks collisions of player against every pig
        if not pigs[i].dead:
            if pigs[i].collides_with(player):
                pigs[i].handle_collision_with(player)
                player.handle_collision_with(pigs[i])

    for i in range(len(angry_pigs)):            #checks collisions between player and angry pigs
        if not player.dead:
            if angry_pigs[i].collides_with(player):
                player.kill()

    #if len(pigs) == 0 and over==False:              #Adds pigs if no catchable pigs are left
    #    new_pigs = spawn_pigs(10, pig_image)
    #    new_angry_pigs = spawn_pigs(4, pig_image)
    #    angry_pigs.append(new_angry_pigs)
    #    game_objects.append(angry_pigs)

    if player.dead == True and over == False:       #Checks if the player is dead and displays final score
        global over
        over = True
        final_score_label.text = "Final Score:" + str(player.score)

@game_window.event
def on_draw():               #draws everything
    game_window.clear()
    field_image.blit(0,0)
    main_batch.draw()

pyglet.clock.schedule_interval(update, 1/120.0) #sets speed of graphics(dt)
pyglet.app.run()            #Runs Loops
