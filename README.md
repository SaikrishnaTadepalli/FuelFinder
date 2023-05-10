# FuelFinder
FuelFinder is a Python-based command-line tool that helps drivers on long trips calculate the most efficient refueling strategy to reach their destination within a given budget. It collects data on car mileage, fuel tank capacity, and fuel prices/time costs for every stop along the route to determine the best plan for refueling stops.

## Getting Started

To use FuelFinder, you'll need to have Python 3.x installed on your machine. You can download it from the [official Python website](https://www.python.org/downloads/).

Once you have Python installed, you can clone the FuelFinder repository from GitHub:
```
git clone https://github.com/[SaikrishnaTadepalli]/FuelFinder.git
```

Finally, run the main.py file to start the program:
```
python main.py
```

## Features

- Calculates the most efficient refueling strategy to reach a destination within a given budget.
- Provides a detailed breakdown of the route and refueling plan, including how much fuel to refuel at each stop, and the total cost and time required.

## How it works

FuelFinder consists of two phases: data-collection and calculation. 

During the data-collection phase, FuelFinder gathers information on car mileage, fuel tank capacity, and fuel prices/time costs for every stop along the route. 

In the calculation phase, FuelFinder uses this data to determine the most efficient refueling strategy, leveraging dynamic and systems programming to implement an efficient algorithm and optimize performance using system resources

## Limitations

FuelFinder has a few limitations:

- It only considers highway exits for refueling stops.
- It assumes that the closest fuel stop to each exit is the best option.
- It does not take into account traffic conditions or road closures.
- It does not consider how weather conditions and terrain of route can affect the car's mileage and travel time.
- It does not take into account additional costs such as tolls, parking fees, and any other expenses that may arise during the trip.
- It does not account for lunch breaks, washroom breaks, and wait times at toll booths, borders etc.

## Futur Plans

In the future, we plan to add the following features to FuelFinder, in addition to patching up the limitations above:

- Adding support for routes within cities to the calculator.
- Allowing user's to select fuel preferences including what type of fuel and fuel providers.
- Integration with real-time traffic data to suggest the best route to take.
- Additional Support and optimization for electric vehicles, including charging times and costs.
- Integration with GPS data to suggest the best refueling stops based on the driver's location in real-time.

## Contributions

Contributions to FuelFinder are welcome! If you find a bug or have a suggestion for a new feature, please submit an issue on the GitHub repository.




