from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError

import data_collection
import calculation

# Using for Address Verification
geolocator = Nominatim(user_agent="address_verification")
def verify_address(address):
    try:
        location = geolocator.geocode(address)

        if location is not None:
            return location
    except (GeocoderTimedOut, GeocoderServiceError):
        print("Error: Geocoding service timed out or encountered an error.")
    
    return False

def Main():
    # WELCOME MESSAGE HERE
    
    # Get Starting Location
    startingLocation = False
    while not startingLocation:
        address = input('What is your starting location? (Address, City, Provice/State, Country)\n>')
        startingLocation = verify_address(address)

    # Get Ending Location
    endingLocation = False
    while not endingLocation:
        address = input('What is your ending location? (Address, City, Provice/State, Country)\n>')
        endingLocation = verify_address(address)

    # Get Trip Budget
    budget = None
    while not budget or budget < 0:
        try:
            budget = float(input('\nWhat is your budget for this trip? (In Dollars)\n> '))
            if budget < 0: 
                print("Invalid input. Please enter a valid number.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    # ---------------------------------------------------------
    # UNABLE TO FIND CAR DATABASE RIGHT NOW. GET DATA FROM USER.
    # car = input('\nWhat is the Make and Model of your car? (Toyota Corolla, Honda Civic etc.)\n> ')

    # Get fuel capacity from user right now. Change later to an API call
    capacity = float(input('\nEnter Fuel Capacity: (in L)\n>'))
    # Get fuel economy from user right now. Change later to an API call
    fuelEconomy = float(input('\nEnter Fuel Economy: (in KM/L)\n>'))
    # ---------------------------------------------------------
    
    # Begin Data Collection Phase
    data = data_collection.Main(startingLocation, endingLocation)

    # Create file called 'trip_info' and write data to it
    file_path = "trip_info"
    file = open(file_path, "w")

    # Write Fuel Economy, Fuel Capacity, Trip Budget, and Number 
    # of Stops on 1 line each seperated by single spaces
    file.write(fuelEconomy + " " + capacity + " " + budget + " " + len(data["Potential Fuel Stops"]))
    
    # Write the names and locations of each potential stop
    line = " ".join([stop for stop in data["Potential Fuel Stops"]])
    file.write(line)

    # Write distance from current stop to next stop for all stops
    line = " ".join([dist for dist in data["Fuel Stop Distances"]])
    file.write(line)

    # Write time taken from the highway to the fuel stop back 
    # to the highway for all stops
    line = " ".join([time for time in data["Time to Fuel Stops"]])
    file.write(line)

    # Write Cost of Fuel
    line = " ".join([price for price in data["Fuel Prices"]])
    file.write(line)
    
    # End Data Collection Phase
    file.close()

    # Begin Calculation Phase

    calculation.Main()

Main()