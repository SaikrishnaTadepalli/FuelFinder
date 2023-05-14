# Bottom-Up Algorithm
# Requires More Testing to verify correctness

# (Experimental, suppose it takes 5 mins on average)
TIME_TO_REFUEL = 5

def Solve(FE, FC, B, N, distToNext, timeToNext, refuelTravelTime, unitMoneyCost):

    dp = [[float('inf')] * (FC + 1) for _ in range(N)]
    dp[0][FC] = 0

    for curLoc in range(N):
        for curAmntFuel in range(FC + 1):
            for refuelAmount in range(curAmntFuel + 1):
                fuelInTank = curAmntFuel - refuelAmount

                if fuelInTank < 0: continue

                curMnySpent = B - (FC - fuelInTank) * unitMoneyCost[curLoc]

                if curMnySpent < 0: continue

                timeTakenToRefuel = refuelAmount * refuelTravelTime[curLoc] + TIME_TO_REFUEL
                fuelInTank += refuelAmount

                if curLoc < N - 1:
                    fuelNeeded = distToNext[curLoc] / FE
                    if fuelInTank < fuelNeeded: continue

                    timeToNextCity = timeToNext[curLoc] + timeTakenToRefuel
                    nextFuel = fuelInTank - fuelNeeded

                    dp[curLoc + 1][nextFuel] = min(dp[curLoc + 1][nextFuel], dp[curLoc][curAmntFuel] + timeToNextCity)

    minTime = float('inf')
    fuelAdded = ""
    for fuel in range(FC + 1):
        if dp[N - 1][fuel] < minTime:
            minTime = dp[N - 1][fuel]
            fuelAdded = str(FC - fuel)

    return (minTime, fuelAdded)

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
