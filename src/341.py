
minTimeMap = {}
fuelAddedMap = {}

def GetKey(curAmntFuel, curMnySpent, curLoc):
    lst = [str(x) for x in [ curAmntFuel, curMnySpent, curLoc ]]
    return ','.join(lst)

def Solve(N, M, C, timeToNext, unitTimeCost, unitMoneyCost):
    def Recurse(curAmntFuel, curMnySpent, curLoc):
        curKey = GetKey(curAmntFuel, curMnySpent, curLoc)

        if (curLoc == N - 1):
            return (0, "0")
        
        if (curKey in minTimeMap):
            return (minTimeMap[curKey], fuelAddedMap[curKey])
        
        possibleRefuels = []

        refuelAmount = 0
        while (curAmntFuel + refuelAmount <= C):
            moneySpentToRefuel = refuelAmount * unitMoneyCost[curLoc]
            timeTakenToRefuel = refuelAmount * unitTimeCost[curLoc]

            if ((curMnySpent + moneySpentToRefuel) > M):
                break
            
            fuelInTank = curAmntFuel + refuelAmount
            timeToNextCity = timeToNext[curLoc] + timeTakenToRefuel

            if (fuelInTank - timeToNext[curLoc] < 0):
                refuelAmount += 1
                continue

            jumpRes = Recurse(
                fuelInTank - timeToNext[curLoc],
                curMnySpent + moneySpentToRefuel,
                curLoc + 1
            )

            if (jumpRes[0] != -1):
                possibleRefuels.append(
                    (
                        timeToNextCity + jumpRes[0], 
                        str(refuelAmount) + " " + jumpRes[1]
                    )
                )

            refuelAmount += 1
        
        if (len(possibleRefuels)):
            minItem = min(possibleRefuels, key=lambda x:x[0])

            minTimeMap[curKey] = minItem[0]
            fuelAddedMap[curKey] = minItem[1]
        else:
            minTimeMap[curKey] = -1
            fuelAddedMap[curKey] = ""
        
        return (minTimeMap[curKey], fuelAddedMap[curKey])

    return Recurse(C, 0, 0)

def Main():
    inputs = input().split(' ')
    N, M, C = int(inputs[0]), int(inputs[1]), int(inputs[2])

    inputs = input().split(' ')
    timeToNext = [int(i) for i in inputs]

    inputs = input().split(' ')
    unitTimeCost = [int(i) for i in inputs]

    inputs = input().split(' ')
    unitMoneyCost = [int(i) for i in inputs]

    res = Solve(N, M, C, timeToNext, unitTimeCost, unitMoneyCost)

    print(res[0])
    if (res[0] != -1):
        print(res[1])

Main()