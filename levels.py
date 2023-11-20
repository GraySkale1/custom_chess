import pyglet

def move(window:pyglet.window, sprite:pyglet.sprite.Sprite, pos:list):
    """places sprites with percentages instead of pixel position \n
    pos = [x, y]"""
    sprite.x = (window.width - sprite.width) * pos[0]
    sprite.y = (window.height - sprite.height) * pos[1]

    return sprite

def background(window:pyglet.window, img_PATH, fit=0):
    """Returns sprite correctly sized to fit window\n
    fit = 1 means that scale will not be changed"""
    background = pyglet.image.load(img_PATH)
    back_sprite = pyglet.sprite.Sprite(background)

    if fit == 0:
        back_sprite.scale.x = window.width / back_sprite.width
        back_sprite.scale.y = window.height / back_sprite.height
    else:
        back_sprite.scale = min(window.width / back_sprite.width, window.height / back_sprite.height)

    return move(window, back_sprite, [0.5,0.5])


class menu():
    def __init__(self, window):
        back_sprite = background(window, "assets\\backgrounds\\menu.png")
        back_sprite = levels.background(game, "assets\\backgrounds\\menu.png")
        button = pyglet.image.load("assets\\buttons\\menu_play.png")
        button_sprite = pyglet.sprite.Sprite(button)

