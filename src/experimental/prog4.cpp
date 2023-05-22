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

int N, M, C;
vector<int> timesToNext;
vector<int> unitTimeCost;
vector<int> unitMoneyCost;

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

    if (curLoc == N - 1)
        return Result(0, "0");

    if (minTimeMap.find(curKey) != minTimeMap.end())
        return Result( minTimeMap[curKey], fuelAddedMap[curKey]);

    Result res = Result(100000, "");

    int refuelAmount = 0;
    if (curAmntFuel < timesToNext[curLoc]) {
        refuelAmount = timesToNext[curLoc] - curAmntFuel;
    }

    while (curAmntFuel + refuelAmount <= C) {
        int moneySpentToRefuel = refuelAmount * unitMoneyCost[curLoc];
        int timeTakenToRefuel = refuelAmount * unitTimeCost[curLoc];

        if (curMnySpent + moneySpentToRefuel > M) { break; }

        int fuelInTank = curAmntFuel + refuelAmount;
        int timeToNextCity = timesToNext[curLoc] + timeTakenToRefuel;

        Result jumpRes = Recurse(
            fuelInTank - timesToNext[curLoc],
            curMnySpent + moneySpentToRefuel,
            curLoc + 1
        );

        if (jumpRes.timeToEnd != -1) {
            if (timeToNextCity + jumpRes.timeToEnd < res.timeToEnd) {
                res = Result(
                    timeToNextCity + jumpRes.timeToEnd,
                    to_string(refuelAmount) + " " + jumpRes.amntsFuelAdded
                );
            }
        }

        refuelAmount += 1;
    }

    if (res.timeToEnd == 100000)
        res.timeToEnd = -1;

    minTimeMap[curKey] = res.timeToEnd;
    fuelAddedMap[curKey] = res.amntsFuelAdded;

    return res;
}

int main() {
    N = ReadInt(), M = ReadInt(), C = ReadInt();

    for (int i = 0; i < N - 1; i++) 
        timesToNext.push_back(ReadInt());
    
    for (int i = 0; i < N; i++)
        unitTimeCost.push_back(ReadInt());

    for (int i = 0; i < N; i++)
        unitMoneyCost.push_back(ReadInt());

    Result res = Recurse(C, 0, 0);

    cout << res.timeToEnd;
    if (res.timeToEnd != -1)
        cout << endl << res.amntsFuelAdded;

    return 0;
}
