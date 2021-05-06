from typing import List
import craftingcalc

import xml.etree.ElementTree as ET

from tkinter import *
from tkinter import filedialog
from tkinter.ttk import *

import json

xmlItems = ET.fromstring(open("items.xml").read())
itemNames = {}
for item in xmlItems:
  if item.tag in ["passive", "active", "familiar"]:
    itemNames[int(item.get("id"))] = item.get("name")



def buildPickupList(currentPickups, remainingPickups, currentPickup, craftedDict):
  if len(currentPickups) == 8:
    item = craftingcalc.tryCraft(currentPickups)
    if item not in craftedDict:
      craftedDict[item] = []
    craftedDict[item].append(currentPickups)
    return
  
  for tryPickup in range(currentPickup, 25):
    if remainingPickups[tryPickup] > 0:
      remainingPickups[tryPickup] -= 1
      buildPickupList(currentPickups + [tryPickup], remainingPickups, tryPickup, craftedDict)
      remainingPickups[tryPickup] += 1

def findItems(availablePickups, minPickups):
  craftedDict = {}
  currentPickups = []

  for idx,count in enumerate(minPickups):
    for _ in range(count):
      currentPickups.append(idx)
  if len(currentPickups) <= 8:
    buildPickupList(currentPickups, availablePickups, 1, craftedDict)
  return craftedDict
  
foundCrafts = []


labels = [
  ("",),
  ("Heart", "Ht"),
  ("Soul Heart", "SHt"),
  ("Black Heart", "BlHt"),
  ("Eternal Heart", "EtHt"),
  ("Gold Heart", "GlHt"),
  ("Bone Heart", "BnHt"),
  ("Rotten Heart", "RtHt"),
  ("Penny", "Pn"),
  ("Nickel", "Nc"),
  ("Dime", "Dm"),
  ("Lucky Penny", "LPn"),
  ("Key", "K"),
  ("Gold Key", "GK"),
  ("Charged Key", "CK"),
  ("Bomb", "Bm"),
  ("Gold Bomb", "GBm"),
  ("Mega Bomb", "MBm"),
  ("Micro Battery", "MBt"),
  ("Lil' Battery", "LBt"),
  ("Mega Battery", "MBt"),
  ("Card", "Crd"),
  ("Pill", "Pll"),
  ("Rune", "Run"),
  ("Dice Shard", "Dic"),
  ("Cracked Key", "Crk")
]


special_items = [
  ('BRK', [
    # Drop on damage
    "Fanny Pack",
    "Piggy Bank",
    "Old Bandage",
    "Gimpy",

    # Healing
    "Maggy's Bow",
    "Charm of the Vampire",
    "Placenta",
    "Yum Heart",

    # More stuff
    "Sack Head",
    "Humbleing Bundle",
    "BOGO Bombs",
    "Options?",
    "Mom's Key",
    "D20",
    "Lucky Foot",

    # More rooms
    "X-Ray Vision",
    "Red Key",

    # Money
    "Restock",
    "Steam Sale",
    "A Dollar",
    "IV Bag",

    # Blood Donation Machine spam
    "Virgo",
    "Book of Shadows",

    # Get more completion marks
    "Clicker",
    "R Key",
    "Goat Head",
    "Mama Mega!",
  ]),

  # Active item aids
  ("ACT", [
    "Car Battery",
    "Habit",
    "9 Volt",
    "Jumper Cables",
    "Schoolbag",
    "Void",
    "Sharp Plug",
  ]),

  # Trinkets
  ("TRK", [
    "Marbles",
    "Smelter",
    "Mom's Box",
  ]),

  # Generates drops on room clear
  ("DRP", [
    "Sack of Pennies",
    "Sack of Sacks",
    "Little C.H.A.D.",
    "Lil Chest",
    "Mystery Sack",
    "Rune Bag",
    "Bomb Bag",
    "The Relic",
    "Charged Baby",
    "Acid Baby",
  ]),

  ("PCK", [
    # One-time pickups
    "Box",
    "Pandora's Box",
    "Mystery Gift",
    "Marrow",
    "Mom's Coin Purse",
    "Battery Pack",
    "Chaos",
    "Dad's Lost Coin",

    # Periodic pickups
    "Crystal Ball",
    "The Book of Sin"
  ]),

  # Good items with low quality
  ("LOQ", [
    "Dead Cat",
    "The Halo",
  ]),

  # Defense items
  ("DEF", [
    "Gnawed Leaf",
    "The Soul",
    "Halo of Flies",
    "Sacrificial Dagger",
    "Cube of Meat",
    "Ball of Bandages",
    "Guardian Angel",
    "Sworn Protector", # (actually on hit)
    "Bot Fly",
    "Psy Fly",
    "Saturnus",
    "The Swarm",
  ]),

  # Flight
  ("FLY", [
    "A Pony",
    "White Pony",
    "Dead Dove",
    "Fate",
    "Holy Grail",
    "Lord of the Pit",
    "Spirit of the Night",
    "Transcendence",
    "Dogma",
    "Revelation",
  ]),
]

itemsByName = {}
for i, name in itemNames.items():
  itemsByName[name] = i

special_quality = {}
for i, group in enumerate(special_items):
  quality = len(special_items) - i
  group_name = group[0]
  for name in group[1]:
    special_quality[itemsByName[name]] = (quality, group_name)

def refreshItemList():
  itemList.delete(0, END)
  availablePickups = [0]
  craftingPickups = [0]
  for count in counts:
    availablePickups.append(int(count.get()))

  for crafting in craftings:
    craftingPickups.append(int(crafting.get()))


  global foundCrafts
  calculatedCrafts = findItems(availablePickups, craftingPickups)
  foundCrafts = [(id, recipes) for id, recipes in calculatedCrafts.items()]
  foundCrafts.sort(key=lambda t: (
    -special_quality.get(t[0], (0, ''))[0],
    -craftingcalc.quality[t[0]],
    itemNames[t[0]]
  ))
  for id, recipes in foundCrafts:
    recipes.sort(key=lambda recipe: sum([craftingcalc.craftingWeights[i] for i in recipe]))

  for item in foundCrafts:
    itemList.insert(END, (special_quality.get(item[0], (0, ''))[1], itemNames[item[0]], "(" + str(craftingcalc.quality[item[0]]) + ")"))
  refreshCrafts()

def refreshCrafts(p = None):
  craftList.delete(0, END)
  selection = itemList.index(ANCHOR)
  if selection < len(foundCrafts):
    for recipe in foundCrafts[selection][1]:
      craftList.insert(END, [labels[i][0] for i in recipe])

def craftItem(p = None):
  itemSelection = itemList.index(ANCHOR)
  craftSelection = craftList.index(ANCHOR)
  if itemSelection < len(foundCrafts) and craftSelection < len(foundCrafts[itemSelection][1]):
    recipe = foundCrafts[itemSelection][1][craftSelection]
    for pickup in recipe:
      if int(craftings[pickup - 1].get()) > 0:
        craftings[pickup - 1].set(int(craftings[pickup - 1].get()) - 1)
      else:
        counts[pickup - 1].set(int(counts[pickup - 1].get()) - 1)
    refreshItemList()

def reset():
  for count in counts:
    count.set(0)
  
  for crafting in craftings:
    crafting.set(0)
  refreshItemList()


win = Tk()

counts = []
craftings = []

Label(win, text="Pickup").grid(row=0, column=0)
Label(win, text="Available").grid(row=0, column=1)
Label(win, text="Crafting").grid(row=0, column=2)

Button(win, text="Reset", command=reset).grid(row=0, column =3)

for i in range(1, 25):
  label = Label(win, text=labels[i][0])
  label.grid(row=i, column=0, sticky="W")

  crafting = Spinbox(win, to=8, command=refreshItemList)
  crafting.set(0)
  crafting.grid(row=i, column=2, sticky="EW")
  craftings.append(crafting)

  count = Spinbox(win, to=99, command=refreshItemList)
  count.set(0)
  count.grid(row=i, column=1, sticky="EW")
  counts.append(count)

itemList = Listbox(win, selectmode=SINGLE, width=30)
itemList.grid(column=3,row=2, rowspan=25, sticky="NSEW")
itemList.bind("<<ListboxSelect>>", refreshCrafts)

craftList = Listbox(win, selectmode=SINGLE, width=60)
craftList.grid(column=4,row=2, rowspan=25, sticky="NSEW")
craftList.bind('<Double-Button-1>', craftItem)

win.columnconfigure(3, weight=1)
win.columnconfigure(4, weight=2)
for i in range(1, 25):
  win.rowconfigure(i, weight=1)

try:
  data = json.load(open("state.json"))
  for i in range(1, 25):
    counts   [i - 1].set(data[0][i - 1])
    craftings[i - 1].set(data[1][i - 1])
  refreshItemList()
except FileNotFoundError:
  pass

def save():
  data = [[], []]
  for i in range(1, 25):
    data[0].append(int(counts[i - 1].get()))
    data[1].append(int(craftings[i - 1].get()))
  json.dump(data, open("state.json", "w"))
  win.destroy()

win.protocol("WM_DELETE_WINDOW", save)
win.mainloop()
