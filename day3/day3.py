import re

with open('day3.in', 'r') as f:
  lines = f.readlines()
  sumResults = 0
  for line in lines:
    results = re.findall(r'mul\((?P<first>[1-9][0-9]*)\,(?P<second>[1-9][0-9]*)\)', line)
    print(results)
    for a, b in results:
      sumResults += (int(a)*int(b))
  
  print(sumResults)


  # part2
  # add matches to 'do()' and 'don't()'s as well

  allTokens = []
  for line in lines:
    results = re.findall(r'mul\([1-9][0-9]*\,[1-9][0-9]*\)|do\(\)|don\'t\(\)', line)
    allTokens = [*allTokens, *results]

  print(allTokens)

  skipNext = False
  answerP2 = 0
  for token in allTokens:
    if token == 'do()':
      skipNext = False
      continue
    if token == 'don\'t()':
      skipNext = True
      continue

    if skipNext:
      continue

    result = re.match(r'mul\((?P<a>\d+)\,(?P<b>\d+)\)', token) 
    if result is None:
      print('match result is none for ', token)
      continue
    answerP2 += (int(result.group('a')) * int(result.group('b')))
  
  print('answer to P2: ', answerP2)
