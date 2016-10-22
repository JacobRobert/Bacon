import pyglet

field_image = pyglet.resource.image("field.png")

main_batch = pyglet.graphics.Batch()

score_label = pyglet.text.Label(text="Highscores:",x=330, y=350,anchor_x='center', bold=True, font_size=55, color=(0,0,0,255),font_name = 'Monospac821 BT', batch=main_batch)

labels = []
positions = ['1st   : ','2nd   : ','3rd   : ','4th   : ','5th   : ','6th   : ','7th   : ','8th   : ','9th   : ','10th : ']
for i in range(10):
    label = pyglet.text.Label(x=600, y=(560-50*i), bold=True, font_size=35, color=(0,0,0,255), font_name = 'Monospac821 BT', batch=main_batch)
    labels.append(label)

window = pyglet.window.Window(1400, 700) #opens window
window.set_caption("HighScore")

def update(dt):
    with open('saves.txt', 'r') as f:
        lines = f.readlines()
        line_list = []
    for line in lines:
        linestr = line.strip()
        score_str, name = linestr.split(' ', 1)
        score = int(score_str)
        line_list.append((score, name))
    score_list = sorted(line_list,reverse=True)

    scores = 10
    if len(score_list) < 10:
        scores = len(score_list)

    for i in range(scores):
        score, name = score_list[i]
        labels[i].text = '{:4}{:5} {:<10}'.format(positions[i], score, name)

    f.close()

@window.event
def on_draw():
    field_image.blit(0,0)
    main_batch.draw()


pyglet.clock.schedule_interval(update, 1/120.0) #sets speed of graphics(dt)
pyglet.app.run()
