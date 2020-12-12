class Item:
    def __init__(self, data: dict):
        for key in data:
            setattr(self, key, data[key])
    
    def getStats(self):
        if self.type == "Weapon":
            return "Damage: " + str(self.damage)
        elif self.type == "Trinket":
            return "Value: " + str(self.value)