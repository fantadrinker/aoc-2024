from io import TextIOWrapper
import sys


def readPuzzle(input: list[str]) -> tuple[list[list[str]], tuple[int, int]]:
    playerX = 0
    playerY = 0
    endLine = 0
    for i, line in enumerate(input):
        if line == '\n':
            endLine = i
            break
        for j, ch in enumerate(list(line)):
            if ch == '@':
                playerX = i
                playerY = j

    return [list(line) for line in input[:endLine]], (playerX, playerY)


def transformPuzzle(puzzle: list[list[str]]) -> tuple[list[list[str]], tuple[int, int]]:
    # transform puzzle from p1 to p2
    playerX = 0
    playerY = 0
    newPuzzle = []
    for i, line in enumerate(puzzle):
        newLine = []
        for j, ch in enumerate(list(line)):
            match ch:
                case 'O':
                    newLine += ["[", "]"]
                case '@':
                    newLine += ["@", "."]
                    playerX = i
                    playerY = j * 2
                case '#':
                    newLine += ["#", "#"]
                case '.':
                    newLine += [".", "."]
        newPuzzle.append(newLine)
    return newPuzzle, (playerX, playerY)


def readInstructions(input: list[str]) -> list[str]:
    foundLineBreak = False
    result = []
    for line in input:
        if foundLineBreak:
            result += list(line)
        if line == "\n":
            foundLineBreak = True
    return result


def move(puzzle: list[list[str]], loc: tuple[int, int], direction: str) -> tuple[int, int]:
    # try to propogate the move to the intended direction
    print(f"trying to move {loc} to the {direction}")
    x, y = loc
    if puzzle[x][y] == '.' or puzzle[x][y] == '#':
        return loc
    nextX = x
    nextY = y
    match direction:
        case '^':
            nextX -= 1
        case 'v':
            nextX += 1
        case '>':
            nextY += 1
        case '<':
            nextY -= 1

    moved = False
    nextTile = puzzle[nextX][nextY]
    match nextTile:
        case '.':
            # overwrite
            puzzle[nextX][nextY] = puzzle[x][y]
            puzzle[x][y] = '.'
            moved = True
        case 'O':
            if move(puzzle, (nextX, nextY), direction) != (nextX, nextY):
                # overwrite
                puzzle[nextX][nextY] = puzzle[x][y]
                puzzle[x][y] = '.'
                moved = True
    return loc if not moved else (nextX, nextY)


def moveP2(puzzle: list[list[str]], loc: tuple[int, int, int], direction: str) -> tuple[int, int]:
    # different cases:
    # left, right: trivial ..[][]@.[][]..
    # up, down: not so trivial:
    # case 1: []..[]
    #         .@....
    #          ^
    # case 2: ..[]..
    #         .@....
    #          ^
    # try to propogate the move to the intended direction
    print(f"trying to move {loc} to the {direction}")
    x, y1, y2 = loc
    if puzzle[x][y1] == '.' or puzzle[x][y1] == '#':
        return x, y1
    nextX = x
    nextY1 = y1
    nextY2 = y2
    match direction:
        case '^':
            nextX -= 1
        case 'v':
            nextX += 1
        case '>':
            nextY1 += 1
            nextY2 += 1
        case '<':
            nextY -= 1

    moved = False
    nextTile = puzzle[nextX][nextY]
    match nextTile:
        case '.':
            # overwrite
            puzzle[nextX][nextY] = puzzle[x][y]
            puzzle[x][y] = '.'
            moved = True
        case 'O':
            if move(puzzle, (nextX, nextY), direction) != (nextX, nextY):
                # overwrite
                puzzle[nextX][nextY] = puzzle[x][y]
                puzzle[x][y] = '.'
                moved = True
    return loc if not moved else (nextX, nextY)


def printPuzzle(puzzle: list[list[str]]):
    for line in puzzle:
        print(''.join(line))


def puzzleScore(puzzle: list[list[str]]):
    score = 0
    for i, line in enumerate(puzzle):
        for j, ch in enumerate(line):
            if ch == 'O':
                score += (100 * i + j)
    return score


def solvePuzzle(fh: TextIOWrapper):
    # first read in puzzle map
    lines = fh.readlines()
    puzzle, playerLoc = readPuzzle(lines)
    # then read instructions
    instructions = readInstructions(lines)

    # p1:
    # then execute instructions, and then get all coordinates
    for dir in instructions:
        playerLoc = move(puzzle, playerLoc, dir)
        print("current puzzle after direction ", dir)
        printPuzzle(puzzle)

    # finally calculate the score
    score = puzzleScore(puzzle)
    print(f"total score for puzzle p1 is {score}")

    # part 2
    # first tranform the puzzle

    freshPuzzle, _ = readPuzzle(lines)
    p2Puzzle, playerLoc = transformPuzzle(freshPuzzle)

    for dir in instructions:
        playerLoc = moveP2(p2Puzzle, playerLoc, dir)
        print("current puzzle after direction ", dir)
        printPuzzle(puzzle)

    return 0


def main():
    with open(sys.argv[1], 'r') as fh:
        print(solvePuzzle(fh))


if __name__ == "__main__":
    main()
