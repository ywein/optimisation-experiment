from math import floor


def evaluate(shiftLength, hoursBetween, maxWorking, maxOff, minWorking, minOff, numHours, test=False):
    def eval(shifts):
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

    return eval