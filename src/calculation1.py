'''
Input:

- Fuel Economy in KM/L (kmpl)
- Fuel Capacity in L (capacity)
- Budget (budget)

- Number of Stops (numStops)

- Distance from current stop to the next in KM (distToNext[])
- Time from current stop to the next in Minutes (timeToNext[])

- Time to get from the highway to the fuel station 
  and back onto the highway in Minutes(refuelTravelTime[])

- Unit Money Cost to refill per location in Dollars/Liter (unitMoneyCost[])
'''

minTimeMap = {}
fuelAddedMap = {}

# (Experimental, suppose it takes 5 mins on average)
TIME_TO_REFUEL = 5

def GetKey(curAmntFuel, curMnySpent, curLoc):
    lst = [str(x) for x in [ curAmntFuel, curMnySpent, curLoc ]]
    return ','.join(lst)

def Solve(FE, FC, B, N, distToNext,
           timeToNext, refuelTravelTime, unitMoneyCost):
    
    def Recurse(curAmntFuel, curMnySpent, curLoc):
        curKey = GetKey(curAmntFuel, curMnySpent, curLoc)

        if (curLoc == N - 1):
            return (0, "0")
        
        if (curKey in minTimeMap):
            return (minTimeMap[curKey], fuelAddedMap[curKey])
        
        possibleRefuels = []
        
        refuelAmount = 0
        while (curAmntFuel + refuelAmount <= FC):
            moneySpentToRefuel = refuelAmount * unitMoneyCost[curLoc]
            timeTakenToRefuel = refuelAmount * refuelTravelTime[curLoc] + TIME_TO_REFUEL

            if ((curMnySpent + moneySpentToRefuel) > B):
                break

            fuelInTank = curAmntFuel + refuelAmount
            timeToNextCity = timeToNext[curLoc] + timeTakenToRefuel

            if ((fuelInTank * FE - distToNext[curLoc]) < 0):
                refuelAmount += 1
                continue

            jumpRes = Recurse(
                fuelInTank - (distToNext[curLoc] / FE),
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
    
    return 0


def Main():
    inputs = input().split(' ')
    
    fuelEconomy = int(inputs[0])
    fuelCapacity = int(inputs[1])
    budget = int(inputs[2])

    numStops = int(inputs[3])

    inputs = input().split(' ')
    distToNext = [int(i) for i in inputs]

    inputs = input().split(' ')
    timeToNext = [int(i) for i in inputs]

    inputs = input().split(' ')
    refuelTravelTime = [int(i) for i in inputs]

    inputs = input().split(' ')
    unitMoneyCost = [int(i) for i in inputs]

    res = Solve(
        fuelEconomy, 
        fuelCapacity, 
        budget, 
        numStops, 
        distToNext, 
        timeToNext, 
        refuelTravelTime, 
        unitMoneyCost
    )

    print(res[0])
    if (res[0] != -1):
        print(res[1])

Main()