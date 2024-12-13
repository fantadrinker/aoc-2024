import sys
import re
import numpy as np
from numpy.linalg import LinAlgError
from scipy.linalg import solve


class ClawMachine:
    def __init__(self, prizeX, prizeY, buttonAX, buttonAY, buttonBX, buttonBY):
        self.prizeX = prizeX + 10000000000000
        self.prizeY = prizeY + 10000000000000
        self.buttonAX = buttonAX
        self.buttonAY = buttonAY
        self.buttonBX = buttonBX
        self.buttonBY = buttonBY
        self.buttonACost = 3
        self.buttonBCost = 1

    def solvePrize(self):
        # a * buttonAX + b * buttonBX = prizeX
        # a * buttonAY + b * buttonBY = prizeY
        # is there possible a, b?
        # equivalent matrix multiplication:
        # | ax, bx | * | a | = | prizeX |
        # | ay, by |   | b |   | prizeY |
        # | a | = | ax, bx |^-1 * | prizeX |
        # | b |   | ay, by |      | prizeY |
        # so if the first matrix is inversable, then there is a solution
        # if there are multiple solution, then the first and the second is
        # the same vector?
        try:
            buttonMatrix = np.array([[self.buttonAX, self.buttonBX],
                                    [self.buttonAY, self.buttonBY]])
            result = solve(buttonMatrix, [self.prizeX, self.prizeY])
            numA = round(result[0])
            numB = round(result[1])
            endX = numA * self.buttonAX + numB * self.buttonBX
            endY = numA * self.buttonAY + numB * self.buttonBY
            if endX == self.prizeX and endY == self.prizeY:
                return numA * self.buttonACost + numB * self.buttonBCost
            else:
                print("not possible to win, differences: ",
                      endX - self.prizeX, endY - self.prizeY)
                return 0
        except LinAlgError:
            print("matrix is singular", self.buttonAX,
                  self.buttonAY, self.buttonBX, self.buttonBY)
            return 0


def readXYFromLine(line: str):
    result = re.search(r'X[\+\=](?P<x>\d+), Y[\+\=](?P<y>\d+)', line)
    if not result:
        print(f"unable to get x, y from line {line}")
        return None, None

    return int(result.group('x')), int(result.group('y'))


def main():
    fileName = sys.argv[1]
    if len(sys.argv) <= 1:
        fileName = "test.in"

    with open(fileName, 'r') as f:
        lines = f.readlines()

        # define the structure of each machine
        prizeX = None
        prizeY = None
        buttonAX = None
        buttonBX = None
        buttonAY = None
        buttonBY = None
        result = 0
        for line in lines:
            if line == "\n":
                machine = ClawMachine(
                    prizeX, prizeY, buttonAX, buttonAY, buttonBX, buttonBY)
                # solve machine
                result += machine.solvePrize()
                continue
            defType = line.split(":")[0]
            match defType:
                case "Button A":
                    buttonAX, buttonAY = readXYFromLine(line)
                case "Button B":
                    buttonBX, buttonBY = readXYFromLine(line)
                case "Prize":
                    prizeX, prizeY = readXYFromLine(line)

        print("result: ", result)


if __name__ == "__main__":
    main()
