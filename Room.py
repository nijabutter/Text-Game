class Room:
    def __init__(self, _name, monster=None, chestItems=[]):
        self.name = _name
        self.neighbours = []
        self.chestItems = []
        self.monster = monster
        if self.monster:
            self.clear = False
        else:
            self.clear = True