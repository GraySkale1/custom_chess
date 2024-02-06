import pyglet

class winner():
    """contains logic for rendering winner"""
    def __init__(self, screen:pyglet.window.Window, winner_name:str):
        self.screen = screen
        self.text = winner_name + ' has won!'

        self.label = pyglet.text.Label(self.text,
                          font_name='Times New Roman',
                          font_size=36,
                          x=self.screen.width//2, y=self.screen.height//2,
                          anchor_x='center', anchor_y='center')

    def on_draw(self):
        return [self.label]
    
    def on_mouse_press(self, x,y,button,modifiers):
        pass