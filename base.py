from piece_class import piece


            
class pawn(piece):
    def __init__(self):
        super().__init__()
        self.ymovement = [lambda y: 0 if y < 0 and self.team == 0 else 999, lambda y: 0 if y > 0 and self.team == 1 else 999]
        self.xxmovement = [lambda x: -abs(x) if self.team == 0 else 999, lambda x: abs(x) if self.team == 1 else 999]
        self.distance = 2
        self.promote = True
        self.identifier = 'p'

    def m_add(self, move_desc):
        super().m_add(move_desc)
        self.distance = 1

class rook(piece):
    def __init__(self):
        super().__init__()
        self.xmovement = [lambda x: 0]
        self.ymovement = [lambda y: 0]
        self.identifier = 'r'

class bishop(piece):
    def __init__(self):
        super().__init__()
        self.xmovement = [lambda x: x, lambda x: -x]
        self.identifier = 'b'

class knight(piece):
    def __init__(self):
        super().__init__()
        self.xmovement = [lambda x: x*2, lambda x: -x*2]
        self.ymovement = [lambda y: y*2, lambda y: -y*2]
        self.distance = 1
        self.jump = True
        self.identifier = 'n'