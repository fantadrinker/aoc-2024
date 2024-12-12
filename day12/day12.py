
def regionCost(region: list[tuple[int, int]]):
  # calculate the perimeter:
  return len(region) * regionPerimeters(region)

def regionCost2(region):
  return len(region) * regionSides(region)

def regionPerimeters(region: list[tuple[int, int]]):
  # (number of unique pairs that are adjacent to each other)
  adjacentUniquePairs = 0
  for i in range(len(region)):
    for j in range(i+1, len(region)):
      x1, y1 = region[i]
      x2, y2 = region[j]
      if x1 == x2 and abs(y1-y2) == 1:
        adjacentUniquePairs += 1
      if y1 == y2 and abs(x1-x2) == 1:
        adjacentUniquePairs += 1
  return 4 * len(region) - 2 * adjacentUniquePairs

def sortLocTuple(p1: tuple[int, int], p2: tuple[int, int]):
  x1, y1 = p1
  x2, y2 = p2
  return (x1 - x2) * (x1 + x2 + y1 + y2) + y1 - y2

def regionSides(region: list[tuple[int, int]]):
  # first get start and end x/y for the region, which is bounding box
  startX, startY = region[0]
  endX = -1
  endY = -1
  for member in region:
    x, y = member
    if x > endX:
      endX = x
    if y > endY:
      endY = y
    if x < startX:
      startX = x
    if y < startY:
      startY = y
  region.sort(key=lambda region: region[0] * 10000 + region[1])
  # then calculate number of sides in horizontal and vertical separately
  # top-down
  prevYs = set()
  currYs = set()
  currX, currY = region[0]
  topDownSides = [currX]
  currYs.add(currY)
  for memX, memY in region[1:]:
    if memX != currX:
      prevYs = currYs
      currYs = set()
      currX = memX
      currY = -100
    if memY not in prevYs and (memX != currX or memY != currY + 1):
      topDownSides.append(memX)
    if memY not in prevYs and memY != currY:
      currY = memY
    currYs.add(memY)
    
  print(f"topdown: {topDownSides}")

  # bottom-up
  region.sort(key=lambda region: 0 - region[0] * 10000 + region[1])
  prevYs = set()
  currYs = set()
  currX, currY = region[0]
  bottomUpSides = [currX]
  currYs.add(currY)
  for memX, memY in region[1:]:
    if memX != currX:
      prevYs = currYs
      currYs = set()
      currX = memX
      currY = -100
    if memY not in prevYs and (memX != currX or memY != currY + 1):
      bottomUpSides.append(memX)
    if memY not in prevYs and memY != currY:
      currY = memY
    currYs.add(memY)
  print(f"bottomUp: {bottomUpSides}")

  # left-right
  region.sort(key=lambda region: region[1] * 10000 + region[0])
  prevXs = set()
  currXs = set()
  currX, currY = region[0]
  leftRightSides = [currY]
  currXs.add(currX)
  for memX, memY in region[1:]:
    if memY != currY:
      prevXs = currXs
      currXs = set()
      currY = memY
      currX = -100
    if memX not in prevXs and (memY != currY or memX != currX + 1):
      leftRightSides.append(memY)
    if memX not in prevXs and memX != currX:
      currX = memX
    currXs.add(memX)
  print(f"leftRight: {leftRightSides}")

  # right-left
  region.sort(key=lambda region: 0 - region[1] * 10000 + region[0])
  prevXs = set()
  currXs = set()
  currX, currY = region[0]
  rightLeftSides = [currY]
  currXs.add(currX)
  for memX, memY in region[1:]:
    if memY != currY:
      prevXs = currXs
      currXs = set()
      currY = memY
      currX = -100
    if memX not in prevXs and (memY != currY or memX != currX + 1):
      rightLeftSides.append(memY)
    if memX not in prevXs and memX != currX:
      currX = memX
    currXs.add(memX)
  print(f"rightLeft: {rightLeftSides}")
  
  result = len(topDownSides) + len(bottomUpSides) + len(rightLeftSides) + len(leftRightSides)
  print(f"region {region} has {result} sides, x: {startX} -> {endX}, y: {startY} -> {endY}")
  return result

with open('day12.in', 'r') as f:
  lines = f.readlines()

  puzzle = []
  for line in lines:
    puzzle.append(list(line.strip()))
  
  print(puzzle)

  # explore all regions and return a list of all regions
  # example: { 'a': [(1,1), (1,2), ...]}
  allRegions: list[list[tuple[int, int]]] = []
  # a region is consisted of a set of connected coordinates
  # sample coordinate: (1,2,E)

  explored = set()
  exploreQueue = []
  for i in range(len(puzzle)):
    for j in range(len(puzzle[0])):
      exploreQueue.append((i,j))
  
  currentExploring = None
  currentRegion: list[tuple[int, int]] = []
  currentRegionExploreQueue: list[tuple[int, int]] = []
  while len(exploreQueue) > 0:
    if len(currentRegionExploreQueue) == 0:
      # move on to next region
      currentExploring = None

    (x, y) = exploreQueue.pop() if len(currentRegionExploreQueue) == 0 else currentRegionExploreQueue.pop()

    if (x,y) in explored:
      continue

    ch = puzzle[x][y]
    if ch != currentExploring:
      print(f"adding region of {currentExploring} to allRegions: {len(currentRegion)} ")
      currentExploring = ch
      if len(currentRegion) > 0:
        allRegions.append(currentRegion)
        currentRegion = []

    currentRegion.append((x,y))
    if x < len(puzzle) - 1 and puzzle[x+1][y] == ch:
      currentRegionExploreQueue.append((x+1, y))
    if x > 0 and puzzle[x-1][y] == ch:
      currentRegionExploreQueue.append((x-1, y))
    if y > 0 and puzzle[x][y-1] == ch:
      currentRegionExploreQueue.append((x, y-1))
    if y < len(puzzle) - 1 and puzzle[x][y+1] == ch:
      currentRegionExploreQueue.append((x, y+1))
    explored.add((x,y))
  
  allRegions.append(currentRegion)
  print(f"adding region of {currentExploring} to allRegions: {len(currentRegion)} ")

  print(f"found total of {len(allRegions)} regions")

  # then for each region calculate the size and perimeter length
  result = 0
  for region in allRegions:
    result += regionCost2(region)

  print(f"total cost: {result}")