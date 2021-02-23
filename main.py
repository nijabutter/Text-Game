import json
import random
import os
from Entity import Entity
from Player import Player
from Room import Room
from Item import Item

def getClear():
    print("What would you like to use to clear the screen?")
    print("1. 'cls' (Windows)")
    print("2. 'clear' (Linux/Mac)")
    return "clear" if input(": ") == "2" else "cls"

if os.path.isfile("settings.txt"):
    with open("settings.txt") as f:
        contents = f.read()
        if contents == "clear" or contents == "cls":
            clear = contents
        else:
            print("Error reading settings.txt file - please choose clear option again")
            clear = getClear()
            with open("settings.txt", "w") as f:
                f.write(clear)
else:
    clear = getClear()            
    with open("settings.txt", "w") as f:
        f.write(clear)

monsters = json.loads(open("monsters.json", "r").read())
items = json.loads(open("items.json", "r").read())
player = Player("Bob")

'''
Each room has max of 3 other neighbours + the room that led into it
Go through all the room names:
    Make a new room
    1 in 10 chance it has a chest
    1 in 8 chacne for monster
    Pick random amount of neighbours
    For each neighbours recurse
    For each neighbour add self to neighbours list
'''


roomNames = [
    "The Kitchen",
    "The Living Room",
    "The Conservatory",
    "The Wine Cellar",
    "The Pantry",
    "The Garden",
    "The Basement",
    "The Fireplace",
    "The Master Bedroom",
    "The Spare Bedroom",
    "The Office",
    "The Library",
    "The Attic",
    "The Porch",
    "The Dining Room",
    "The Hallway",
    "The Landing",
    "The Painting Room",
    "The Airing cupboard"
]

entrance = Room("The Entrance")

roomsMade = 0

def createRoom(parent):
    global roomsMade
    maxRoomCount = 10
    if roomsMade >= maxRoomCount: # max room count in total
        return
    roomsMade += 1
    newRoom = Room(roomNames.pop())
    nCount = random.randint(0, (3 if roomsMade < maxRoomCount - 3 else maxRoomCount - roomsMade))
    for i in range(nCount):
        createRoom(newRoom)
    newRoom.neighbours.append(parent)
    parent.neighbours.append(newRoom)


createRoom(entrance)

# diningRoom = Room("The Dining Room")
# kitchen = Room("The Kitchen")
# lounge = Room("The Lounge")
# basement = Room("The Basement")
# garden = Room("The Garden")

#entrance.neighbours = [diningRoom, lounge]
# lounge.neighbours = [entrance, kitchen]
# kitchen.neighbours = [diningRoom, lounge]
# diningRoom.neighbours = [entrance, kitchen]
# kitchen.monster = Entity(monsters["easy"][random.randint(0, len(monsters)-1)])
player.currentRoom = entrance


# if random.randint(0, 10) > 7:
#     kitchen.chestItems = [Item(items["rare"][random.randint(0, len(items["rare"])-1)])]
# else:
#     kitchen.chestItems = [Item(items["common"][random.randint(0, len(items["common"])-1)])]

def getInfo():
    print("Inventory:")
    [print("-", item.name, "("+item.getStats()+")") for item in player.inventory]
    print("Current Weapon:", player.weapon.name, "(" + player.weapon.getStats() + ")")
    print("Health:", player.healthBar.get())
    print("Armour:", player.armour)
    print("You are currently in:", player.currentRoom.name)  
    print("Connected rooms:")
    [print("-", room.name) for room in player.currentRoom.neighbours]

def menu():
    choices = []
    optionsCount = 1
    if player.currentRoom.neighbours:
        for j, n in enumerate(player.currentRoom.neighbours):
            print(optionsCount, "Go " + ("back " if n is player.currentRoom.neighbours[-1] else "") + "to:", n.name)
            optionsCount += 1
            choices.append("player.setRoom(" + str(j) + ")")
    if player.currentRoom.clear and player.currentRoom.chestItems:
        print(optionsCount, "Open chest")
        optionsCount += 1
        choices.append("player.openChest()")
    
    print(optionsCount, "Get Player Info")
    choices.append("getInfo()")
    optionsCount += 1
    
    print(optionsCount, "Leave the house")
    choices.append("exit(0)")
    optionsCount += 1
    
    try:
        move = int(input("What would you like to do? (1-" + str(len(choices)) + ") " ))-1
        os.system(clear)
    except:
        os.system(clear)
        menu()
    else:
        if move >= 0 and move < len(choices):
            eval(choices[move])
        else:
            os.system(clear)
            menu()

def combatOptions():
    print("You are fighting:", player.currentRoom.monster.name)
    print("--- Enemy Info ---")
    player.currentRoom.monster.getInfo()
    print("--- Your Info ---")
    print("Health:", player.healthBar.get())
    print("Armour:", player.armour)
    optionsCount = 1
    choices = []
    print(optionsCount, "Attack")
    choices.append("player.attack(player.currentRoom.monster)")
    optionsCount += 1
    # go to other rooms while in combat
    # if player.currentRoom.neighbours:
    #     for j, n in enumerate(player.currentRoom.neighbours):
    #         print(optionsCount, "Go to:", n.name)
    #         optionsCount += 1
    #         choices.append("player.setRoom(" + str(j) + ")")
    print(optionsCount, "Leave the house")
    optionsCount += 1
    choices.append("exit(0)")
    try:
        move = int(input("What would you like to do? (1-" + str(len(choices)) + ") " ))-1
        os.system(clear)
    except:
        os.system(clear)
        combatOptions()
    else:
        if move >= 0 and move < len(choices):
            eval(choices[move])
        else:
            os.system("cls")
            combatOptions()

while True:
    if player.inCombat:
        combatOptions()
        if player.health == 0:
            break
    else:
        menu()
# TODO: bar charts??
print("--- Game Over ---")
print("Gold collected:", player.gold)
print("Skills:")
[print(skill, player.skills[skill]) for skill in player.skills]
if input("Would you like to play again (y) ? ").lower() == "y":
    print("restart")
