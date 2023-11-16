class piece():
    def __init__(self):
        self.xmovement = []
        self.ymovement = []
        self.past = []
        self.xxmovement = []
        self.xymovement = []
        self.distance = 999
        self.jump = False
        self.promote = False
        self.team = 1   # 1 - white, 0 - black
        self.identifier = ''

    def m_add(self, move):
        self.past.append(move)

    def remove(self):
        return 0