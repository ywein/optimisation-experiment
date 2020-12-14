

def localSearchOneStep(shifts, totalShiftLength, numHours):
    neighbors = []
    print(shifts)
    for i in range(len(shifts)):
        if i == 0:
            if shifts[0] != 0:
                neighbors.append([shifts[0] - 1] + shifts[1:])
        else:
            if shifts[i] - shifts[i - 1] > totalShiftLength:
                neighbors.append(shifts[0:i - 1] + [shifts[i] - 1] + shifts[i:])

        print(neighbors)

        if i == len(shifts) - 1:
            if shifts[i] + totalShiftLength < numHours:
                neighbors.append(shifts[0:i - 1] + [shifts[i] + 1])
        else:
            if shifts[i + 1] - shifts[i] > totalShiftLength:
                neighbors.append(shifts[0:i - 1] + [shifts[i] + 1] + shifts[i:])

        print(neighbors)


