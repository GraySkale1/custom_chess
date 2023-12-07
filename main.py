import pyglet
from pyglet.window import key
import levels
import chess

display = pyglet.canvas.Display()
screen = display.get_default_screen()

WIDTH = screen.width
HEIGHT = screen.height

sprites = []

game = pyglet.window.Window(width=WIDTH, height=HEIGHT)
game.set_fullscreen(True)

@game.event
def on_draw():
    game.clear()
    for sprite in sprites:
        sprite.draw()
        
back_sprite = levels.background(game, "assets\\backgrounds\\chessboard.png", fit=True)
spacing_height = back_sprite.height / 8
spacing_width = back_sprite.width / 8

sprites.append(back_sprite)

game_board = chess.board()
game_board.reset()


pyglet.app.run()


