import pyglet
from pyglet.window import key

display = pyglet.canvas.Display()
screen = display.get_default_screen()

WIDTH = screen.width
HEIGHT = screen.height

sprites = []

game = pyglet.window.Window(width=WIDTH, height=HEIGHT)

@game.event
def on_draw():
    game.clear()
    for sprite in sprites:
        sprite.draw()
        

background = pyglet.image.load("assets\\misc\\default_texture.png")
back_sprite = pyglet.sprite.Sprite(background)

back_sprite.scale_x = game.width / back_sprite.width
back_sprite.scale_y = game.height / back_sprite.height

back_sprite.x = (WIDTH - back_sprite.width) / 2
back_sprite.y = (HEIGHT - back_sprite.height) / 2

sprites.append(back_sprite)

pyglet.app.run()


