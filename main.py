import json
import random
import os
from Entity import Entity
from Player import Player
from Room import Room
from Item import Item
monsters = json.loads(open("monsters.json", "r").read())
items = json.loads(open("items.json", "r").read())
player = Player("Bob")

entrance = Room("The Entrance")
diningRoom = Room("The Dining Room")
kitchen = Room("The Kitchen")
lounge = Room("The Lounge")
basement = Room("The Basement")
garden = Room("The Garden")

entrance.neighbours = [diningRoom, lounge]
lounge.neighbours = [entrance, kitchen]
kitchen.neighbours = [diningRoom, lounge]
diningRoom.neighbours = [entrance, kitchen]
kitchen.monster = Entity(monsters["easy"][random.randint(0, len(monsters)-1)])
player.currentRoom = entrance

if random.randint(0, 10) > 7:
    kitchen.chestItems = [Item(items["rare"][random.randint(0, len(items["rare"])-1)])]
else:
    kitchen.chestItems = [Item(items["common"][random.randint(0, len(items["common"])-1)])]

def getInfo():
    print("Inventory:")
    [print("-", item.name, "("+item.getStats()+")") for item in player.inventory]
    print("Current Weapon:", player.weapon.name, "(" + player.weapon.getStats() + ")")
    print("Health:", player.healthBar.get())
    print("Armour:", player.armour)
    print("You are currently in:", player.currentRoom.name)  
    print("Connected rooms:")
    [print("-", room.name) for room in player.currentRoom.neighbours]

def roomsMenu():
    optionCount = 1
    print(optionCount, "Stay here")
    for room in player.currentRoom.neighbours:
        print(optionCount, room.name)
    choice = input("Where would you like to go?")
    if choice == "1":
        return
    else:
        try:
            choice = int(choice)
        except:
            roomsMenu()
        else:
            if choice > 0:
                if choice > len(player.currentRoom.neighbours):
                    roomsMenu()
                player.moveRoom(player.currentRoom.neighbours[choice-1])
            else:
                roomsMenu()

    
def menu():
    choices = []
    optionsCount = 1
    if player.currentRoom.neighbours:
        for j, n in enumerate(player.currentRoom.neighbours):
            print(optionsCount, "Go to:", n.name)
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
        os.system("cls")
    except:
        os.system("cls")
        menu()
    else:
        if move >= 0 and move < len(choices):
            eval(choices[move])
        else:
            os.system("cls")
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
        os.system("cls")
    except:
        os.system("cls")
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
print("--- Game Over ---")
print("Gold collected:", player.gold)
print("Skills:")
[print(skill, player.skills[skill]) for skill in player.skills]
if input("Would you like to play again (y) ? ").lower() == "y":
    print("restart")