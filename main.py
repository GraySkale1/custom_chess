import piece_class
import math
import pyglet
from pyglet.window import key
import levels
import chess

display = pyglet.canvas.Display()
screen = display.get_default_screen()

WIDTH = 500
HEIGHT = 500

game_sprites = []

game = pyglet.window.Window(width=WIDTH, height=HEIGHT)
#game.set_fullscreen(True)

back_sprite = levels.background(game, "assets\\backgrounds\\chessboard.png", fit=True)
spacing_scale = back_sprite.width / 8
game_sprites.append(back_sprite)

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

def piece_add(game_sprites_list:list):
    game_sprites_list = [game_sprites_list[0]]
    for pos in game_board.piece_pos:
        x,y = pos
        px,py = index_to_pixel(pos)
        if game_board.chess_board[x][y] != 0:
            image = pyglet.image.load(game_board.chess_board[x][y].sprite())
            sprite = pyglet.sprite.Sprite(image, x=px, y=py)
            sprite.scale = math.ceil(spacing_scale) / sprite.width
            game_sprites_list.append(sprite)
    return game_sprites_list

highlight = pyglet.image.load('assets\\misc\\yellow.jpg')
highlight = pyglet.sprite.Sprite(highlight)
highlight.scale_x = math.ceil(spacing_scale) / highlight.width
highlight.scale_y = math.ceil(spacing_scale) / highlight.height

increment = 0
@game.event
def on_mouse_press(x, y, button, modifiers):
    global past_piece
    global current_piece
    global increment
    global past
    global game_sprites

    p1, p2 = pixel_to_index([x,y])

    current_piece = game_board.chess_board[p1][p2]
    if increment == 0:
        past_piece = None
        increment += 1
        highlight.position = (index_to_pixel([p1,p2])[0], index_to_pixel([p1,p2])[1], highlight.z)
        game_sprites.insert(1, highlight)

    elif increment % 2 == 0:
        if past_piece != 0 and current_piece != 0:
            exe = 1
        else:
            exe = 0

        print(game_board.turn)
        vec = game_board._vector(past, pixel_to_index([x,y]))
        if issubclass(type(past_piece), piece_class.piece):
            move = chess.movement(start=past, vector=vec, exe=exe, team=(past_piece.team))
            game_board.execute(move)
        if highlight in game_sprites:
            game_sprites.remove(highlight)
        game_sprites = piece_add(game_sprites)
    else:
       highlight.position = (index_to_pixel([p1,p2])[0], index_to_pixel([p1,p2])[1], highlight.z)
       game_sprites.insert(1, highlight)
        
    past_piece = current_piece
    increment += 1
    
    print(c_piece, end=', ')
    past = pixel_to_index([x,y])
    print(past)
    


@game.event
def on_mouse_release(x, y, button, modifiers):
    pass

@game.event
def on_draw():
    game.clear()
    for sprite in game_sprites:
        sprite.draw()


game_sprites = piece_add(game_sprites)

pyglet.app.run()
