#include <iostream>
#include<vector>
#include<string>
#include<unordered_map>

using namespace std;

class Result {       
  public:             
    int timeToEnd;        
    string amntsFuelAdded;

    Result(int bestTime, string fuelAddedPath) {
        timeToEnd = bestTime;
        amntsFuelAdded = fuelAddedPath;
    }
};

int fuelEconomy;
int fuelCapacity;
int budget;
int numStops;
vector<int> distToNext;
vector<int> timeToNext;
vector<int> refuelTravelTime;
vector<int> unitMoneyCost;

const int TIME_TO_REFUEL = 5;

unordered_map<string, int> minTimeMap;
unordered_map<string, string> fuelAddedMap;

int ReadInt() {
    int num = 0;
    cin >> num;
    return num;
}

string GetKey(int curAmntFuel, int curMnySpent, int curLoc) {
    return to_string(curAmntFuel) + "," + to_string(curMnySpent) + "," + to_string(curLoc);
}

Result Recurse(int curAmntFuel, int curMnySpent, int curLoc) {
    string curKey = GetKey(curAmntFuel, curMnySpent, curLoc);

    if (curLoc == numStops - 1) {
        return Result(0, "0");
    }
        
    if (minTimeMap.find(curKey) != minTimeMap.end()) {
        return Result(minTimeMap[curKey], fuelAddedMap[curKey]);
    }

    Result res = Result(-2, "");

    int refuelAmount = 0;
    if (curAmntFuel < timeToNext[curLoc]) {
        refuelAmount = timeToNext[curLoc] - curAmntFuel;
    }

    while (curAmntFuel + refuelAmount <= fuelCapacity) {
        int moneySpentToRefuel = refuelAmount * unitMoneyCost[curLoc];
        int timeTakenToRefuel = refuelAmount + refuelTravelTime[curLoc] + TIME_TO_REFUEL;

        if (curMnySpent + moneySpentToRefuel > budget) { break; }

        int fuelInTank = curAmntFuel + refuelAmount;
        int timeToNextCity = timeToNext[curLoc] + timeTakenToRefuel;

        if ((fuelInTank * fuelEconomy - distToNext[curLoc]) < 0) {
            refuelAmount += 1;
            continue;
        }

        Result jumpRes = Recurse(
            fuelInTank - (distToNext[curLoc] / fuelEconomy),
            curMnySpent + moneySpentToRefuel,
            curLoc + 1
        );

        if (jumpRes.timeToEnd != -1) {
            if ((timeToNextCity + jumpRes.timeToEnd < res.timeToEnd) || res.timeToEnd == -2) {
                res = Result(
                    timeToNextCity + jumpRes.timeToEnd,
                    to_string(refuelAmount) + " " + jumpRes.amntsFuelAdded
                );
            }
        }

        refuelAmount += 1;
    }

    if (res.timeToEnd == -2) {
        res.timeToEnd == -1;
    }

    minTimeMap[curKey] = res.timeToEnd;
    fuelAddedMap[curKey] = res.amntsFuelAdded;

    return res;
}


int main() {
    cout << "Hello, World!" << endl;

    int fuelEconomy = ReadInt();
    int fuelCapacity = ReadInt();
    int budget = ReadInt();

    int numStops = ReadInt();

    for (int i = 0; i < numStops; i++) {
        distToNext.push_back(ReadInt());
    }

    for (int i = 0; i < numStops; i++) {
        distToNext.push_back(ReadInt());
    }

    for (int i = 0; i < numStops; i++) {
        distToNext.push_back(ReadInt());
    }

    for (int i = 0; i < numStops; i++) {
        distToNext.push_back(ReadInt());
    }
        
    Result res = Recurse(fuelCapacity, 0, 0);

    // Handle Return
}