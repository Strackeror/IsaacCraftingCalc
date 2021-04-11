import xml.etree.ElementTree as ET
import struct

class Rng:
  def __init__(self):
    self.seed = 0x77777770
    self.shifts = (0, 0, 0)

  def next(self):
    num = self.seed
    num ^= (num >> self.shifts[0]) & 0xffffffff
    num ^= (num << self.shifts[1]) & 0xffffffff
    num ^= (num >> self.shifts[2]) & 0xffffffff
    num = num & 0xffffffff
    self.seed = num
    return num

  def nextFloat(self):
    mult = struct.unpack(">f", bytes([0x2f, 0x7f, 0xff, 0xfe]))[0]
    return self.next() * mult


craftingShifts = [
    (0x00000001, 0x00000005, 0x00000010),
    (0x00000001, 0x00000005, 0x00000013),
    (0x00000001, 0x00000009, 0x0000001D),
    (0x00000001, 0x0000000B, 0x00000006),
    (0x00000001, 0x0000000B, 0x00000010),
    (0x00000001, 0x00000013, 0x00000003),
    (0x00000001, 0x00000015, 0x00000014),
    (0x00000001, 0x0000001B, 0x0000001B),
    (0x00000002, 0x00000005, 0x0000000F),
    (0x00000002, 0x00000005, 0x00000015),
    (0x00000002, 0x00000007, 0x00000007),
    (0x00000002, 0x00000007, 0x00000009),
    (0x00000002, 0x00000007, 0x00000019),
    (0x00000002, 0x00000009, 0x0000000F),
    (0x00000002, 0x0000000F, 0x00000011),
    (0x00000002, 0x0000000F, 0x00000019),
    (0x00000002, 0x00000015, 0x00000009),
    (0x00000003, 0x00000001, 0x0000000E),
    (0x00000003, 0x00000003, 0x0000001A),
    (0x00000003, 0x00000003, 0x0000001C),
    (0x00000003, 0x00000003, 0x0000001D),
    (0x00000003, 0x00000005, 0x00000014),
    (0x00000003, 0x00000005, 0x00000016),
    (0x00000003, 0x00000005, 0x00000019),
    (0x00000003, 0x00000007, 0x0000001D),
    (0x00000003, 0x0000000D, 0x00000007),
    (0x00000003, 0x00000017, 0x00000019),
    (0x00000003, 0x00000019, 0x00000018),
    (0x00000003, 0x0000001B, 0x0000000B),
    (0x00000004, 0x00000003, 0x00000011),
    (0x00000004, 0x00000003, 0x0000001B),
    (0x00000004, 0x00000005, 0x0000000F),
    (0x00000005, 0x00000003, 0x00000015),
    (0x00000005, 0x00000007, 0x00000016),
    (0x00000005, 0x00000009, 0x00000007),
    (0x00000005, 0x00000009, 0x0000001C),
    (0x00000005, 0x00000009, 0x0000001F),
    (0x00000005, 0x0000000D, 0x00000006),
    (0x00000005, 0x0000000F, 0x00000011),
    (0x00000005, 0x00000011, 0x0000000D),
    (0x00000005, 0x00000015, 0x0000000C),
    (0x00000005, 0x0000001B, 0x00000008),
    (0x00000005, 0x0000001B, 0x00000015),
    (0x00000005, 0x0000001B, 0x00000019),
    (0x00000005, 0x0000001B, 0x0000001C),
    (0x00000006, 0x00000001, 0x0000000B),
    (0x00000006, 0x00000003, 0x00000011),
    (0x00000006, 0x00000011, 0x00000009),
    (0x00000006, 0x00000015, 0x00000007),
    (0x00000006, 0x00000015, 0x0000000D),
    (0x00000007, 0x00000001, 0x00000009),
    (0x00000007, 0x00000001, 0x00000012),
    (0x00000007, 0x00000001, 0x00000019),
    (0x00000007, 0x0000000D, 0x00000019),
    (0x00000007, 0x00000011, 0x00000015),
    (0x00000007, 0x00000019, 0x0000000C),
    (0x00000007, 0x00000019, 0x00000014),
    (0x00000008, 0x00000007, 0x00000017),
    (0x00000008, 0x00000009, 0x00000017),
    (0x00000009, 0x00000005, 0x0000000E),
    (0x00000009, 0x00000005, 0x00000019),
    (0x00000009, 0x0000000B, 0x00000013),
    (0x00000009, 0x00000015, 0x00000010),
    (0x0000000A, 0x00000009, 0x00000015),
    (0x0000000A, 0x00000009, 0x00000019),
    (0x0000000B, 0x00000007, 0x0000000C),
    (0x0000000B, 0x00000007, 0x00000010),
    (0x0000000B, 0x00000011, 0x0000000D),
    (0x0000000B, 0x00000015, 0x0000000D),
    (0x0000000C, 0x00000009, 0x00000017),
    (0x0000000D, 0x00000003, 0x00000011),
    (0x0000000D, 0x00000003, 0x0000001B),
    (0x0000000D, 0x00000005, 0x00000013),
    (0x0000000D, 0x00000011, 0x0000000F),
    (0x0000000E, 0x00000001, 0x0000000F),
    (0x0000000E, 0x0000000D, 0x0000000F),
    (0x0000000F, 0x00000001, 0x0000001D),
    (0x00000011, 0x0000000F, 0x00000014),
    (0x00000011, 0x0000000F, 0x00000017),
    (0x00000011, 0x0000000F, 0x0000001A)
]

craftingWeights = [
    0x00000000, # 0 None

    # Hearts
    0x00000001, # 1 Red heart
    0x00000004, # 2 Soul Heart
    0x00000005, # 3 Black Heart
    0x00000005, # 4 Eternal Heart
    0x00000005, # 5 Gold Heart
    0x00000005, # 6 Bone Heart
    0x00000001, # 7 Rotten Heart

    # Pennies
    0x00000001, # 8 Penny
    0x00000003, # 9 Nickel
    0x00000005, # 10 Dime
    0x00000008, # 11 Lucky Penny

    # Keys
    0x00000002, # 12 Key
    0x00000005, # 13 Golden Key
    0x00000005, # 14 Charged Key

    # Bombs
    0x00000002, # 15 Bomb
    0x00000006, # 16 Golden Bomb
    0x0000000A, # 17 Giga Bomb

    # Batteries
    0x00000002, # 18 Micro Battery
    0x00000004, # 19 Lil' Battery
    0x00000008, # 20 Mega Battery


    # Usables
    0x00000002, # 21 Card
    0x00000002, # 22 Pill
    0x00000004, # 23 Rune
    0x00000004, # 24 Dice Shard
    0x00000002, # 25 Cracked Key
    0x00000001
]

qualityBoundsList = [
  (34, (4, 4)),
  (30, (3, 4)),
  (26, (2, 4)),
  (22, (1, 4)),
  (18, (1, 3)),
  (14, (1, 2)),
  (8, (0, 2)),
  (0, (0, 1)),
]

xmlItemPools = ET.fromstring(open("itempools.xml").read())

pools = []
for pool in xmlItemPools.findall("Pool"):
  name = pool.get("Name")
  itemList = []
  for item in pool.findall("Item"):
    itemList.append((int(item.get("Id")), float(item.get("Weight"))))
  pools.append((name, itemList))


xmlItemMetadata = ET.fromstring(open("items_metadata.xml").read())
quality = {}
for item in xmlItemMetadata.findall("item"):
  quality[int(item.get("id"))] = int(item.get("quality"))


def tryCraft(pickups):
  rng = Rng()
  pickupCounts = [0] * 30
  pickupWeightTotal = 0

  for pickupId in pickups:
    pickupCounts[pickupId] += 1
    pickupWeightTotal += craftingWeights[pickupId]

  for idx, count in enumerate(pickupCounts):
    for _ in range(count):
      rng.shifts = craftingShifts[idx]
      rng.next()

  rng.shifts = (1, 21, 20)


  poolWeights = [
      (0, 1.),
      (1, 2.),
      (2, 2.),
      (4, pickupCounts[4] * 10.),
      (3, pickupCounts[3] * 10.),
      (5, pickupCounts[6] * 5.),
      (8, pickupCounts[5] * 10.),
      (12, pickupCounts[7] * 10.),
      (9, pickupCounts[25] * 10.),
  ]

  combined = 0
  for i in [1, 8, 12, 15]:
    combined += pickupCounts[i]
  if (combined == 0):
    poolWeights += [(26, pickupCounts[23] * 10.)]


  itemWeights = [0.] * (max(quality.keys()) + 1)
  weightTotal = 0.

  for poolIdx, poolWeight in poolWeights:
    if poolWeight <= 0:
      continue
    
    qualityCheckVal = pickupWeightTotal
    if poolIdx in [3, 4, 5]:
      qualityCheckVal -= 5

    qualityBounds = (0, 0)
    for min, bounds in qualityBoundsList:
      if qualityCheckVal > min:
        qualityBounds = bounds
        break
    
    pool = pools[poolIdx]
    for itemIdx, itemWeight in pool[1]:
      itemQuality = quality[itemIdx]
      if itemQuality < qualityBounds[0] or itemQuality > qualityBounds[1]:
        continue
      
      finalWeight = poolWeight * itemWeight
      itemWeights[itemIdx] += finalWeight
      weightTotal += finalWeight
    

  target = rng.nextFloat() * weightTotal
  for itemIdx, weight in enumerate(itemWeights):
    target -= weight
    if (target < 0):
      return itemIdx

  return 25




