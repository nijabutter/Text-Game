import random
from ProgressBar import ProgressBar
from Item import Item
class Player():
    
    def __init__(self, _name):
        self.name = _name
        self.health = 100
        self.maxHealth = 100
        self.gold = 500
        self.armour = 20
        self.inCombat = False
        self.currentRoom = None
        self.weapon = Item({
            "name": "Wooden Sword",
            "type": "Weapon",
            "ranged": False,
            "damage": 10
        })
        self.healthBar = ProgressBar(maximum=self.maxHealth, value=self.health, width=20)
        self.skills = {
            "Archery": 0,
            "Melee": 10,
            "Luck": 0
        }
        self.inventory = [Item({"name": "Cloth", "type": "Trinket", "value": 2})]

    def setHealth(self, newHealth):
        if newHealth > self.maxHealth:
            newHealth = self.maxHealth
        elif newHealth < 0:
            newHealth = 0
        self.health = newHealth
        self.healthBar.value = newHealth

    def openChest(self):
        for item in self.currentRoom.chestItems:
            print("+", item.name, "(" + item.getStats() + ")")
            self.inventory.append(item)
        self.currentRoom.chestItems = []


    def setRoom(self, roomIndex):
        self.currentRoom = self.currentRoom.neighbours[roomIndex]
        print("You are now in:", self.currentRoom.name)
        if self.currentRoom.monster:
            self.inCombat = True
            print("You are in combat!")

    def attack(self, target):
        if self.weapon.ranged:
            hit = random.randint(0, 10) <= self.skills["Archery"]
        else:
            hit = random.randint(0, 10) <= self.skills["Melee"]
        if hit:
            target.hit(self.weapon.damage)
            
        else:
            print("Miss!")
        if target.health <= 0:
                print("You killed", target.name + "!")
                if target.drops:
                    if target.drops["rare"]:
                        if random.randint(0, 10) <= self.skills["Luck"]:
                            # rare item
                            chosenItem = Item(target.drops["rare"][random.randint(0, len(target.drops["rare"])-1)])
                        else:
                            # common item
                            chosenItem = Item(target.drops["common"][random.randint(0, len(target.drops["common"])-1)])
                    else:
                        chosenItem = Item(target.drops["common"][random.randint(0, len(target.drops["common"])-1)])
                    print("+", chosenItem.name, "(" + chosenItem.getStats() + ")")
                    self.inventory.append(chosenItem)
                gold = int(target.droppedGold + target.droppedGold * self.skills["Luck"] / 100)
                print("+", gold, "Gold")
                self.gold += gold
                self.inCombat = False
                self.currentRoom.monster = None
        else:
            target.attack(self)
        if self.health <= 0:
            # dead
            print("you have died!")
            self.inCombat = False
