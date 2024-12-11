
with open('day10.in', 'r') as f:
  lines = f.readlines()

  # construct the map as 2 d array
  topMap = []

  for line in lines:
    digits = [int(x) for x in list(line.strip())]
    topMap.append(digits)
  
  print(topMap)

  # first find all trailheads
  trailHeadLocs = []
  for i, row in enumerate(topMap):
    for j, item in enumerate(row):
      if item == 0:
        trailHeadLocs.append((i, j))
  print(3, trailHeadLocs)

  # then for each trailhead, calculate the number of 
  # peaks it can reach
  totalTotalTrails = 0
  for trailHeadLoc in trailHeadLocs:
    startX, startY = trailHeadLoc
    reachablePeaks = set()
    exploreQueue = [(startX, startY)]
    while len(exploreQueue) > 0:
      x, y= exploreQueue.pop()
      h = topMap[x][y]
      if h == 9 and (x,y) not in reachablePeaks:
        reachablePeaks.add((x,y))
        continue
      if x > 0 and topMap[x-1][y] == h + 1:
        exploreQueue.append((x-1, y))
      if y < len(topMap) - 1 and topMap[x][y+1] == h+1:
        exploreQueue.append((x, y+1))
      if x < len(topMap) - 1 and topMap[x+1][y] == h+1:
        exploreQueue.append((x+1, y))
      if y > 0 and topMap[x][y-1] == h+1:
        exploreQueue.append((x, y-1))
    
    # deduplicate
    print(f"for trailHead at ({startX}, {startY}) there are {len(reachablePeaks)} trails to the top")

    totalTotalTrails += len(reachablePeaks)
  print(4, totalTotalTrails)

  # part 2
  totalTotalTrails = 0
  for trailHeadLoc in trailHeadLocs:
    startX, startY = trailHeadLoc
    totalTrailCount = 0
    exploreQueue = [(startX, startY)]
    while len(exploreQueue) > 0:
      x, y= exploreQueue.pop()
      h = topMap[x][y]
      if h == 9:
        totalTrailCount += 1
        continue
      if x > 0 and topMap[x-1][y] == h + 1:
        exploreQueue.append((x-1, y))
      if y < len(topMap) - 1 and topMap[x][y+1] == h+1:
        exploreQueue.append((x, y+1))
      if x < len(topMap) - 1 and topMap[x+1][y] == h+1:
        exploreQueue.append((x+1, y))
      if y > 0 and topMap[x][y-1] == h+1:
        exploreQueue.append((x, y-1))
    
    # deduplicate
    print(f"for trailHead at ({startX}, {startY}) there are {totalTrailCount} trails to the top")

    totalTotalTrails += totalTrailCount
  print(5, totalTotalTrails)
