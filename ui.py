from typing import List
import craftingcalc

import xml.etree.ElementTree as ET

from tkinter import *
from tkinter import filedialog
from tkinter.ttk import *

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
  foundCrafts.sort(key=lambda t: (-craftingcalc.quality[t[0]], itemNames[t[0]]))

  for item in foundCrafts:
    itemList.insert(END, (itemNames[item[0]], "(" + str(craftingcalc.quality[item[0]]) + ")"))
  refreshCrafts()

def refreshCrafts(p = None):
  craftList.delete(0, END)
  selection = itemList.curselection()
  if selection:
    for recipe in foundCrafts[selection[0]][1]:
      craftList.insert(END, [labels[i][0] for i in recipe])

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

  count = Spinbox(win, to=8, command=refreshItemList)
  count.set(0)
  count.grid(row=i, column=1, sticky="EW")
  counts.append(count)

itemList = Listbox(win, selectmode=SINGLE, width=30)
itemList.grid(column=3,row=2, rowspan=25, sticky="NSEW")
itemList.bind("<<ListboxSelect>>", refreshCrafts)

craftList = Listbox(win, selectmode=SINGLE, width=60)
craftList.grid(column=4,row=2, rowspan=25, sticky="NSEW")

win.columnconfigure(3, weight=1)
win.columnconfigure(4, weight=2)
win.mainloop()