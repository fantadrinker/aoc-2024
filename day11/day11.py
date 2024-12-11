import math

class Node:
  def __init__(self, value: int, next = None):
    self.value = value
    self.next = next
    self.length = 0
  
  def getLength(self) -> int:
    count = 0
    currNode = self
    while currNode is not None:
      currNode = currNode.next
      count += 1
    return count

def listToNodes(stones: list[int]) -> Node|None:
  if len(stones) == 0:
    return None
  firstNode = Node(stones[0])
  prevNode = firstNode
  for stone in stones[1:]:
    nextNode = Node(stone)
    prevNode.next = nextNode
    prevNode = nextNode
  return firstNode




def blinkTransform(stones: list[int]) -> list[int]:
  i = 0
  while i < len(stones):
    if stones[i] == 0:
      stones[i] = 1
    elif math.floor(math.log10(stones[i])) % 2 == 1:
      # break stone in half
      numDigits = math.floor(math.log10(stones[i])) + 1
      # print(f"total num of digits for {stones[i]} is ")
      secondHalf = math.floor(stones[i] % math.pow(10, numDigits / 2))
      firstHalf = math.floor((stones[i] - secondHalf) / math.pow(10, numDigits/2))
      stones[i] = firstHalf
      stones.insert(i+1, secondHalf)
      i += 1
    else:
      stones[i] *= 2024
    i += 1
  return stones

def blinkTransformNodes(stones: Node | None) -> Node | None:
  currNode = stones
  while currNode is not None:
    currValue = currNode.value
    if currNode.value == 0:
      currNode.value = 1
    elif math.floor(math.log10(currValue)) % 2 == 1:
      # break stone in half
      numDigits = math.floor(math.log10(currValue)) + 1
      # print(f"total num of digits for {stones[i]} is ")
      secondHalf = math.floor(currValue % math.pow(10, numDigits / 2))
      firstHalf = math.floor((currValue - secondHalf) / math.pow(10, numDigits/2))
      currNode.value = firstHalf
      # stones.insert(i+1, secondHalf)
      newNode = Node(secondHalf, currNode.next)
      currNode.next = newNode
      currNode = currNode.next
    else:
      currNode.value = currValue * 2024
    currNode = currNode.next
  return stones


with open('day11.in', 'r') as f:
  line = f.readline()

  stones = [int(x) for x in line.split(' ')]

  # for i in range(25):
  #   stones = blinkTransform(stones)
  #   print(f"after {i+1} transforms, the number of stones becomes: {len(stones)}")
  
  # part 2:
  # stoneNodes = listToNodes(stones)
  # for i in range(25):
  #   stoneNodes = blinkTransformNodes(stoneNodes)
  #   if stoneNodes is None:
  #     print('nodes are none')
  #     continue
  #   print(f"after {i+1} transforms, the number of stones becomes: {stoneNodes.getLength()}")


  totalLength = 0
  stones = [(stone, 0) for stone in stones]
  originalLength = len(stones)
  # stones.reverse()
  originalProcessed = 0
  while len(stones) > 0:
    topStone, blinks = stones.pop()
    totalLength += 1

    for i in range(blinks, 50):
      if topStone == 0:
        topStone = 1
      elif math.floor(math.log10(topStone)) % 2 == 1:
        # break stone in half
        numDigits = math.floor(math.log10(topStone)) + 1
        # print(f"total num of digits for {stones[i]} is ")
        secondHalf = math.floor(topStone % math.pow(10, numDigits / 2))
        firstHalf = math.floor((topStone - secondHalf) / math.pow(10, numDigits/2))
        topStone = secondHalf
        stones.append((firstHalf, i+1))
      else:
        topStone *= 2024
    #print(topStone)
    if blinks == 0:
      originalProcessed += 1
      print(f"{originalProcessed} out of {originalLength} processed")

  print(f"totalLength is {totalLength}")