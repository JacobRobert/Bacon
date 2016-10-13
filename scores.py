import pyglet

field_image = pyglet.resource.image("field.png")

main_batch = pyglet.graphics.Batch()

score_label = pyglet.text.Label(text="Highscores:",x=300, y=600,anchor_x='center', bold=True, font_size=35, color=(0,0,0,255), batch=main_batch)
first_label = pyglet.text.Label(x=300, y=550,anchor_x='center', bold=True, font_size=35, color=(0,0,0,255), batch=main_batch)
secon_label = pyglet.text.Label(x=300, y=500,anchor_x='center', bold=True, font_size=35, color=(0,0,0,255), batch=main_batch)
third_label = pyglet.text.Label(x=300, y=450,anchor_x='center', bold=True, font_size=35, color=(0,0,0,255), batch=main_batch)
fourt_label = pyglet.text.Label(x=300, y=400,anchor_x='center', bold=True, font_size=35, color=(0,0,0,255), batch=main_batch)
fifth_label = pyglet.text.Label(x=300, y=350,anchor_x='center', bold=True, font_size=35, color=(0,0,0,255), batch=main_batch)
sixth_label = pyglet.text.Label(x=300, y=300,anchor_x='center', bold=True, font_size=35, color=(0,0,0,255), batch=main_batch)
seven_label = pyglet.text.Label(x=300, y=250,anchor_x='center', bold=True, font_size=35, color=(0,0,0,255), batch=main_batch)
eight_label = pyglet.text.Label(x=300, y=200,anchor_x='center', bold=True, font_size=35, color=(0,0,0,255), batch=main_batch)
ninth_label = pyglet.text.Label(x=300, y=150,anchor_x='center', bold=True, font_size=35, color=(0,0,0,255), batch=main_batch)
tenth_label = pyglet.text.Label(x=300, y=100,anchor_x='center', bold=True, font_size=35, color=(0,0,0,255), batch=main_batch)

window = pyglet.window.Window(1400, 700) #opens window
window.set_caption("HighScore")

@window.event
def on_draw():
    field_image.blit(0,0)
    main_batch.draw()

#def update():


pyglet.app.run()
