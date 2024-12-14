from io import TextIOWrapper
import re
import sys
from pynput.keyboard import Listener

PUZZLE_WIDTH = 101
PUZZLE_HEIGHT = 103


class Robot:
    def __init__(self, posX: int, posY: int, vx: int, vy: int):
        self.posX = posX
        self.posY = posY
        self.vx = vx
        self.vy = vy

    def advance(self):
        self.posX, self.posY = positionAfterXSecs(self, 1)


def positionAfterXSecs(robot: Robot, x: int) -> tuple[int, int]:
    return (robot.posX + x * robot.vx) % PUZZLE_WIDTH, (robot.posY + x * robot.vy) % PUZZLE_HEIGHT


def solve(puzzle: list[Robot]):
    # given a list of robots, what are their positions after 100 seconds?
    allPoses = [positionAfterXSecs(robot, 100) for robot in puzzle]

    # first print out the puzzle
    resultsByQuadron = [0, 0, 0, 0]
    for x, y in allPoses:
        print(x, y)
        # which quadron are they in?
        if x < (PUZZLE_WIDTH - 1) / 2 and y < (PUZZLE_HEIGHT - 1) / 2:
            resultsByQuadron[0] += 1
        if x > (PUZZLE_WIDTH - 1) / 2 and y < (PUZZLE_HEIGHT - 1) / 2:
            resultsByQuadron[1] += 1
        if x < (PUZZLE_WIDTH - 1) / 2 and y > (PUZZLE_HEIGHT - 1) / 2:
            resultsByQuadron[2] += 1
        if x > (PUZZLE_WIDTH - 1) / 2 and y > (PUZZLE_HEIGHT - 1) / 2:
            resultsByQuadron[3] += 1

    return resultsByQuadron[0] * resultsByQuadron[1] * resultsByQuadron[2] * resultsByQuadron[3]


def advanceAllRobotsAndPrintPuzzle(robots: list[Robot]):
    for robot in robots:
        robot.advance()
    printPuzzle(robots)


def printPuzzle(puzzle: list[Robot]):
    gameMap = [[0] * PUZZLE_WIDTH] * PUZZLE_HEIGHT
    # populate map
    for robot in puzzle:
        gameMap[robot.posY][robot.posX] += 1

    # print map only if majority of spaces are empty?
    for row in gameMap:
        print(''.join(['.' if i == 0 else '*' for i in row]))


def solveP2(puzzle: list[Robot]):
    # need to do an infinite loop, for each loop print the next step of all robots
    with Listener(on_release=lambda key: advanceAllRobotsAndPrintPuzzle(puzzle)) as listener:
        printPuzzle(puzzle)
        listener.join()


def parseFile(fh: TextIOWrapper):
    # each line is p=12,34 v=56,-78
    lines = fh.readlines()
    robots: list[Robot] = []
    for line in lines:
        robotInfo = line.strip().split(' ')

        if len(robotInfo) < 2:
            print(f"{line} cannot be parsed")
            continue
        initPosMatch = re.search(r'p\=(?P<x>-?\d+),(?P<y>-?\d+)', robotInfo[0])
        velocityMatch = re.search(
            r'v\=(?P<x>-?\d+),(?P<y>-?\d+)', robotInfo[1])
        if initPosMatch is None or velocityMatch is None:
            print(f"unable to parse input {line}")
            continue
        robots.append(Robot(int(initPosMatch.group('x')), int(initPosMatch.group(
            'y')), int(velocityMatch.group('x')), int(velocityMatch.group('y'))))
    return robots


def __main__():
    with open(sys.argv[1], 'r') as fh:
        puzzle = parseFile(fh)
        # answer = solve(puzzle)

        # print(answer)
        solveP2(puzzle)


if __name__ == "__main__":
    __main__()
