# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import sys
import time
from math import ceil, floor
import matplotlib.pyplot as plt
import random
import numpy as np
import scipy.optimize as opt

from anneal import dual_annealing

from local import localSearchOneStep

def placeShifts(offsets, shiftLength, hoursBetween):
    shifts = []
    for i in range(len(offsets)):
        shifts.append(sum(offsets[:i + 1]) + shiftLength * i + hoursBetween * i)
    return shifts


def evaluate(shifts, shiftLength, hoursBetween, maxWorking, maxOff, minWorking, minOff, numHours, test=False):
    shifts = [round(x) for x in shifts]
    shifts.sort()
    prevShift = shifts[0]
    consecutiveWorkings = []
    consecutiveOffs = []
    if prevShift >= 24:
        consecutiveOffs = [floor(prevShift / 24)]

    working = 0
    off = 0
    penalty = 0
    for i in range(len(shifts) - 1):
        n = i + 1
        curShift = shifts[n]
        distanceBetween = curShift - prevShift - shiftLength - hoursBetween
        if test:
            print(n, curShift, distanceBetween)

        if working == 0:
            working = 1

        off = 0

        if distanceBetween < 0:
            penalty -= 5

        if distanceBetween < 24:
            working += 1
        else:
            if working != 0:
                consecutiveWorkings.append(working)
            working = 0
            if test:
                print("distanceBetween", distanceBetween)
            off = floor(distanceBetween / 24)
            if off != 0:
                if test:
                    print("off", off)
                consecutiveOffs.append(off)

        if n == len(shifts) - 1:
            off += floor((numHours - curShift - (shiftLength + hoursBetween)) / 24)
            if off < 0:
                off = 0
            if test:
                print("final off", off, numHours, curShift, numHours - curShift - (shiftLength))
            if off != 0:
                consecutiveOffs.append(off)
            if working == 0:
                working = 1
            consecutiveWorkings.append(working)

        prevShift = curShift

    if len(consecutiveWorkings) == 0:
        consecutiveWorkings.append(0)
    if len(consecutiveOffs) == 0:
        consecutiveOffs.append(0)

    for w in consecutiveWorkings:
        if w > maxWorking:
            if test:
                print('maxWorking')
            penalty -= 1
        if w < minWorking:
            if test:
                print('minWorking')
            penalty -= 1

    for o in consecutiveOffs:
        if o > maxOff:
            if test:
                print('maxOff')
            penalty -= 1
        if o < minOff:
            if test:
                print('minOff')
            penalty -= 1

    return -penalty

def ch():
    print("ch")


def cb(x, f, context):
    print(x)
    if f == 0:
        return True


def fancyAnneal(numShifts, totalShiftLength, freeSpaces, shiftLength, hoursBetween, maxWorking, maxOff, minWorking, minOff, numHours):
    shiftBounds = []
    for i in range(numShifts):
        shiftBounds.append((totalShiftLength * i, freeSpaces + totalShiftLength * i))

    def eqcons(x):
        shifts = [round(x0) for x0 in x]
        shifts.sort()
        arr = []
        for i in range(len(shifts)):
            if i == 0:
                arr.append(0)
            else:
                arr.append(x[i] - (x[0] + totalShiftLength))
        return np.array(arr)

    res = dual_annealing(
        local_search_options={
            "constraints": {
                'type': 'ineq',
                'fun': eqcons
            }
        },
        maxiter=10000,
        func=evaluate,
        args=(shiftLength, hoursBetween, maxWorking, maxOff, minWorking, minOff, numHours),
        bounds=shiftBounds,
        callback=cb
    )
    f = evaluate(res.x, shiftLength, hoursBetween, maxWorking, maxOff, minWorking, minOff, numHours)
    if f != 0:
        shifts = [round(x) for x in res.x]
        shifts.sort()
        print("WTF", f, shifts)
    return res.x


def bruteForce(numShifts, totalShiftLength, freeSpaces, shiftLength, hoursBetween, maxWorking, maxOff, minWorking, minOff, numHours):
    shiftBounds = []
    for i in range(numShifts):
        shiftBounds.append([totalShiftLength * i, freeSpaces + totalShiftLength * i])

    f = 99999999
    bestF = f
    bestShift = []
    iterCount = 0
    while f != 0 and iterCount < 1000000:
        shifts = []
        offsets = []
        for i in range(numShifts):
            if i == 0:
                shiftStart = random.randint(0, freeSpaces)
                shifts.append(shiftStart)
                offsets.append(shiftStart)
            else:
                start = shifts[i - 1] + totalShiftLength
                end = start + (freeSpaces - sum(offsets))
                if end > numHours:
                    end = numHours

                shiftStart = random.randint(start, end)
                offsets.append(shiftStart - start)
                shifts.append(shiftStart)

        f = evaluate(shifts, shiftLength, hoursBetween, maxWorking, maxOff, minWorking, minOff, numHours)
        if f < bestF:
            bestF = f
            bestShift = shifts
        if f == 0:
            break
        iterCount += 1


    if f != 0:
        print("WTF")
    print(iterCount, bestF, bestShift)


def main():
    print("test")
    numHours = 7 * 24
    numShifts = 5
    shiftLength = 8
    hoursBetween = 16
    maxWorking = 5
    maxOff = 3
    minWorking = 2
    minOff = 2

    totalShiftLength = shiftLength + hoursBetween

    occupiedSpaces = shiftLength * numShifts + hoursBetween * (numShifts - 1)
    freeSpaces = numHours - occupiedSpaces + 1
    print('freeSpaces', freeSpaces)
    bestShift = []
    numIteration = 0

    # [48, 72, 96, 120, 144]
    # [0, 24, 96, 120, 144]
    f = evaluate([69, 108, 141, 235, 266, 294, 329, 374, 476, 503, 537, 561, 608, 639, 681], shiftLength, hoursBetween, maxWorking, maxOff, minWorking, minOff, numHours, True)
    print(f)
    fitnesses = []
    iterations = []
    validShifts = 0

    # for n1 in range(freeSpaces):
    #     for n2 in range(freeSpaces):
    #         for n3 in range(freeSpaces):
    #             for n4 in range(freeSpaces):
    #                 for n5 in range(freeSpaces):
    #                     shifts = [
    #                         n1,
    #                         n2 + totalShiftLength,
    #                         n3 + totalShiftLength * 2,
    #                         n4 + totalShiftLength * 3,
    #                         n5 + totalShiftLength * 4
    #                     ]
    #                     fitness = evaluate(shifts, shiftLength, hoursBetween, maxWorking, maxOff, minWorking, minOff, numHours)
    #                     fitnesses.append(fitness)
    #                     iterations.append(numIteration)
    #                     numIteration += 1
    #                     if fitness == 0:
    #                         validShifts += 1
    #                         bestShift = (nurmIteration, fitness, shifts)
        # print(fitness)
    count = 1
    sumTime = 0
    bestS = []
    for i in range(count):
        tic = time.perf_counter()
        bestS = fancyAnneal(numShifts, totalShiftLength, freeSpaces, shiftLength, hoursBetween, maxWorking, maxOff, minWorking, minOff, numHours)
        toc = time.perf_counter()
        sumTime += toc - tic
    print(f"fancyAnneal in {sumTime/count:0.4f} seconds")

    print("bestS", bestS)
    print(localSearchOneStep(bestS, totalShiftLength, numHours))

    # sumTime = 0
    # for i in range(count):
    #     tic = time.perf_counter()
    #     bruteForce(numShifts, totalShiftLength, freeSpaces, shiftLength, hoursBetween, maxWorking, maxOff, minWorking, minOff, numHours)
    #     toc = time.perf_counter()
    #     sumTime += toc - tic
    # print(f"brute force in {sumTime/count:0.4f} seconds")

    # shiftBounds = []
    # for i in range(numShifts):
    #     shiftBounds.append([totalShiftLength * i, freeSpaces + totalShiftLength * i])
    #
    # for shiftBounds

    # print(bestShift, validShifts, numIteration)
    #
    # plt.bar(iterations, fitnesses)
    # # naming the x axis
    # plt.xlabel('iterations')
    # # naming the y axis
    # plt.ylabel('fitness')
    #
    # plt.show()
    # plt.savefig('graph.eps', format='eps')

    # print(numIteration)
    # print(min(fitnesses), max(fitnesses))
    # print(bestShift)
    # print(validShifts)
    # print(validShifts/numIteration)

if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
