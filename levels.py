import pyglet
def resize():
    pass



class level():
    def __init__(self, window:pyglet.window):
        #creates background
        self.sprites = []
        background = pyglet.image.load("assets\\misc\\default_texture.png")
        self.back_sprite = pyglet.sprite.Sprite(background)

        self.back_sprite.scale_x = window.width / self.back_sprite.width
        self.back_sprite.scale_y = window.height / self.back_sprite.height

        self.back_sprite.x = (window.width - self.back_sprite.width) / 2
        self.back_sprite.y = (window.height - self.back_sprite.height) / 2
    
    def objs():
        pass
