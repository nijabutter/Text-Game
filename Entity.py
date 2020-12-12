from ProgressBar import ProgressBar
import random
class Entity:
    def __init__(self, data: dict):
        for key in data:
            setattr(self, key, data[key])
        self.healthBar = ProgressBar(maximum=self.maxHealth, value=self.health, width=20)
    
    def setHealth(self, newHealth):
        if newHealth > self.maxHealth:
            newHealth = self.maxHealth
        elif newHealth < 0:
            newHealth = 0
        self.health = newHealth
        self.healthBar.value = newHealth
    
    def getInfo(self):
        print("Health:", self.healthBar.get())
        print("Armour:", self.armour)
    def attack(self, target):
        if random.randint(0, 10) <= 2:
            print(self.name, "misses!")
        else:
            # hit
            newDmg = (self.damage - self.damage * target.armour / 100)
            if target.armour > 0:
                target.armour -= 1
            target.setHealth(target.health - newDmg)
            print(self.name, self.attacks[random.randint(0, len(self.attacks)-1)], "and deals", newDmg, "damage!")

    def hit(self, damage):
        newDmg = (damage - damage * self.armour / 100)
        self.setHealth(self.health - newDmg)
        if self.armour > 0:
            self.armour -= 1
        print("You deal", newDmg, "damage!")
