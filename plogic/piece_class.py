import os


class piece():
    def __init__(self):
        # by x and y movement I mean where the x and y pos from the 2d array's perspective.
        # so the y axis is inverted while x is normal on the board
        self.xmovement = []
        self.ymovement = []
        self.past = []
        self.xxmovement = []
        self.xymovement = []
        self.distance = 999
        self.jump = False
        self.team = 0   # 0 - white, 1 - black
        self.identifier = ''
        self.premote = False

    def m_add(self, move):
        self.past.append(move)

    def remove(self):
        return 0
    
    def promote(self):
        return 0
    
    def sprite(self):
        """returns path to image asscoiated with piece"""
        string = self.identifier.upper()
        if self.team == 0:
            string += 'W'
        else:
            string += 'B'

        if os.path.isfile(f'assets\\pieces\\{string}.png'):
            return f'assets\\pieces\\{string}.png'
        else:
            return 'assets\\misc\\default_texture.png'

        