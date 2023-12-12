import math
import pyglet
from pyglet.window import key
import levels
import chess

display = pyglet.canvas.Display()
screen = display.get_default_screen()

WIDTH = 500
HEIGHT = 500

sprites = []

game = pyglet.window.Window(width=WIDTH, height=HEIGHT)
#game.set_fullscreen(True)

back_sprite = levels.background(game, "assets\\backgrounds\\chessboard.png", fit=True)
spacing_scale = back_sprite.width / 8
sprites.append(back_sprite)

game_board = chess.board()
game_board.reset()
c_piece = None

def pixel_to_index(pixel_pos: list):
    x1, y1 = pixel_pos
    x1 -= back_sprite.x
    y1 -= back_sprite.y
    p1 = y1 // spacing_scale
    p2 = x1 // spacing_scale
    return [7 - int(p1), int(p2)]

def index_to_pixel(index_pos: list):
    p1, p2 = index_pos
    p1 = 7 - p1
    y1 = p1 * spacing_scale
    x1 = p2 * spacing_scale
    x1 += back_sprite.x
    y1 += back_sprite.y
    return [int(x1), int(y1)]

@game.event
def on_mouse_press(x, y, button, modifiers):
    print(str(pixel_to_index([x,y])))

@game.event
def on_mouse_drag(x, y, dx, dy):
    pass

@game.event
def on_draw():
    game.clear()
    for sprite in sprites:
        sprite.draw()

for pos in game_board.piece_pos:
    x,y = pos
    px,py = index_to_pixel(pos)
    image = pyglet.image.load(game_board.chess_board[x][y].sprite())
    sprite = pyglet.sprite.Sprite(image, x=px, y=py)
    sprites.append(sprite)



pyglet.app.run()


