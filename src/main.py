from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError

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

    print('\nHere is the final data:')
    print(startingLocation)
    print(endingLocation)
    print(budget)
    print(capacity)
    print(fuelEconomy)
    
    # Begin Data Collection Phase
    # (Data Collection Phase ends)

    # Begin Calculation Phase
    # (Calculation Phase ends)

print('==================================================\n')
Main()
print('\n==================================================')