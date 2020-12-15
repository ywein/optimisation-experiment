# This is a sample Python script.

import random
# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import time
from math import floor

import numpy as np

from anneal import dual_annealing
from local import generateRandomSolution, localSearchOneStep, genareteSolution
from evaluate import evaluate
from tabu import tabu_search

def placeShifts(offsets, shiftLength, hoursBetween):
    shifts = []
    for i in range(len(offsets)):
        shifts.append(sum(offsets[:i + 1]) + shiftLength * i + hoursBetween * i)
    return shifts




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
    # f = evaluate([69, 108, 141, 235, 266, 294, 329, 374, 476, 503, 537, 561, 608, 639, 681], shiftLength, hoursBetween, maxWorking, maxOff, minWorking, minOff, numHours, True)
    # print(f)
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
    # for i in range(count):
    #     tic = time.perf_counter()
    #     bestS = fancyAnneal(numShifts, totalShiftLength, freeSpaces, shiftLength, hoursBetween, maxWorking, maxOff, minWorking, minOff, numHours)
    #     toc = time.perf_counter()
    #     sumTime += toc - tic
    # print(f"fancyAnneal in {sumTime/count:0.4f} seconds")

    # randS = generateRandomSolution(freeSpaces, totalShiftLength, numHours, numShifts)
    # print(localSearchOneStep(totalShiftLength, shiftLength, hoursBetween, maxWorking, maxOff, minWorking, minOff, numHours)(randS))
    #
    eval = evaluate(shiftLength, hoursBetween, maxWorking, maxOff, minWorking, minOff, numHours, True)
    # localSearch = localSearchOneStep(totalShiftLength, shiftLength, hoursBetween, maxWorking, maxOff, minWorking, minOff, numHours)
    #
    # bestS = tabu_search(randS, 500000, 10000, localSearch, eval)
    # print(bestS)

    testS = genareteSolution(freeSpaces, totalShiftLength, shiftLength, hoursBetween, maxWorking, maxOff, minWorking, minOff, numHours, numShifts)
    print(testS, eval(testS))

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
