import random
from math import floor

from evaluate import evaluate


def generateRandomSolution(freeSpaces, totalShiftLength, numHours, numShifts):
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

    return shifts


def genareteSolution(freeSpaces,totalShiftLength, shiftLength, hoursBetween, maxWorking, maxOff, minWorking, minOff, numHours, numShifts):
    shifts = []
    offsets = []
    curWorking = 0
    curOff = 0
    curOffOffset = 0
    for i in range(numShifts):
        if i == 0:
            shiftStart = random.randint(0, freeSpaces)
            shifts.append(shiftStart)
            offsets.append(shiftStart)
            curWorking += 1
        else:
            start = shifts[i - 1] + totalShiftLength

            if curWorking >= maxWorking:
                start += 24 * minOff
            if curWorking < minWorking:
                end = start + min(23, (freeSpaces - sum(offsets)))
            else:
                end = start + (freeSpaces - sum(offsets))

            if end > numHours:
                end = numHours

            curOff = 0

            # REFACTOR TO THIS
            # r = choice([(1, 5), (9, 15), (21, 27)])
            # print(randint(*r))

            shiftStart = random.randint(start, end)
            offset = shiftStart - start
            if offset >= 24:
                curWorking = 0
                if offset < 24 * minOff:
                    offset = 24 * minOff
                    shiftStart = start + offset
            else:
                curWorking += 1

            offsets.append(offset)
            shifts.append(shiftStart)

    return shifts

def localSearchOneStep(totalShiftLength, shiftLength, hoursBetween, maxWorking, maxOff, minWorking, minOff, numHours):
    def localSearch(shifts):
        neighbors = []
        shifts = [round(x) for x in shifts]
        shifts.sort()
        for i in range(len(shifts)):
            if i == 0:
                if shifts[0] != 0:
                    neighbor = [shifts[0] - 1] + shifts[1:]
                    neighbors.append(neighbor)
            else:
                if shifts[i] - shifts[i - 1] > totalShiftLength:
                    neighbor = shifts[0:i] + [shifts[i] - 1] + shifts[i + 1:]
                    neighbors.append(neighbor)

            if i == len(shifts) - 1:
                if shifts[i] + totalShiftLength < numHours:
                    neighbor = shifts[0:i] + [shifts[i] - 1] + shifts[i + 1:]
                    neighbors.append(neighbor)
            else:
                if shifts[i + 1] - shifts[i] > totalShiftLength:
                    neighbor = shifts[0:i] + [shifts[i] + 1] + shifts[i + 1:]
                    neighbors.append(neighbor)

        return neighbors

        # evaluated = []
        # for neighbor in neighbors:
        #     fitness = evaluate(neighbor, shiftLength, hoursBetween, maxWorking, maxOff, minWorking, minOff, numHours)
        #     evaluated.append((neighbor, fitness))
        #
        # return sorted(evaluated, key=lambda tup: tup[1])

    return localSearch


