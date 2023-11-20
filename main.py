import pyglet
from pyglet.window import key
import levels

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
        
back_sprite = levels.background(game, "assets\\backgrounds\\chessboard.png", fit=1)
#button = pyglet.image.load("assets\\buttons\\menu_play.png")
#button_sprite = pyglet.sprite.Sprite(button)
#button_sprite.scale = 2
#button_sprite = levels.move(game, button_sprite, [0.5,0.5])

sprites.append(back_sprite)
#sprites.append(button_sprite)

pyglet.app.run()


