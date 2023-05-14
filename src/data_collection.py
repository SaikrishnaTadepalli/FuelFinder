from geopy.distance import geodesic
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
import googlemaps
from datetime import datetime

# Set up Google Maps Client
gmaps = googlemaps.Client(key='YOUR_API_KEY_HERE')

# Gather Stuff Here
def DataCollection(start_location, end_location):
    # Get the directions from Google Maps
    directions_result = gmaps.directions(
        start_location, 
        end_location, 
        mode="driving", 
        departure_time=datetime.now()
    )

    # Extract the optimal route
    route = directions_result[0]['legs'][0]['steps']
    
    # Extract highways and major roads
    highway_names = []
    for step in route:
        instr = step['html_instructions'].lower()
        if 'highway' in instr or 'toll road' in instr or 'freeway' in instr:
            highway_names.append(step['html_instructions'])
    
    # Find potential fuel stops
    potential_fuel_stops = []
    for step in route:
        instr = step['html_instructions'].lower()
        if 'highway' in instr or 'toll road' in instr or 'freeway' in instr:
            for intersection in step['intersections']:
                for road in intersection['roads']:
                    road_name = road['name'].lower()
                    if 'gas' in road_name  or 'petrol' in road_name or 'fuel' in road_name:
                        exit_name = f"{road['name']} on Exit {intersection['exit']}"
                        potential_fuel_stops.append((exit_name, intersection['location']))
    
    # Find distance between fuel stops
    fuel_stop_dists = []
    for i in range(len(potential_fuel_stops) - 1):
        dist_result = gmaps.distance_matrix(
            potential_fuel_stops[i][1], 
            potential_fuel_stops[i+1][1], 
            mode="driving"
        )
        fuel_stop_dists.append(dist_result['rows'][0]['elements'][0]['distance']['value'])

    # Calculate distances from starting location to the first exit
    start_to_first_exit = gmaps.directions(
        start_location, 
        potential_fuel_stops[0][1], 
        mode="driving"
        )[0]['legs'][0]['distance']['value']
    dist_start_to_first_exit = start_to_first_exit[0]['legs'][0]['distance']['value']

    # Calculate distances between fuel stops
    distance_between_fuel_stops = []
    for i in range(len(potential_fuel_stops) - 1):
        start = potential_fuel_stops[i][1]
        end = potential_fuel_stops[i + 1][1]

        directions_result = gmaps.directions(
            start, 
            end, 
            mode="driving", 
            departure_time=datetime.now()
        )
        
        distance = directions_result[0]['legs'][0]['distance']['value']
        distance_between_fuel_stops.append(distance)

    # Calculate distance from the last exit to the ending location
    last_exit_to_end = gmaps.directions(
        potential_fuel_stops[-1][1], 
        end_location, 
        mode="driving"
    )
    dist_last_exit_to_end = last_exit_to_end[0]['legs'][0]['distance']['value']

    # Construct final distances array
    distances = [dist_start_to_first_exit] + distance_between_fuel_stops + [dist_last_exit_to_end]
    
    # Find the time taken to get to each fuel stop
    # THIS IS WRONG BECAUSE OF THE EXIT_RAMP_LOCATION
    time_to_fuel_stops = []
    for i in range(len(potential_fuel_stops)):
        # GET VALUE HERE
        exit_ramp_location = potential_fuel_stops[i][1]
        fuel_stop_location = potential_fuel_stops[i][1]

        # Calculate the time to reach the fuel stop from the exit ramp
        directions_result = gmaps.directions(exit_ramp_location, fuel_stop_location, mode="driving", departure_time=datetime.now())
        time_exit_ramp_to_fuel_stop = directions_result[0]['legs'][0]['duration']['value']

        time_to_fuel_stops.append(time_exit_ramp_to_fuel_stop)

    # Find the exit/stop names for each fuel stop
    exit_names = [fuel_stop[0] for fuel_stop in potential_fuel_stops]
    
    '''
    # Print the results
    print('Highway and major road names:')
    for name in highway_names:
        print(name)
        
    print('\nPotential fuel stops:')
    for stop in potential_fuel_stops:
        print(stop[0], stop[1])
        
    print('\nExit/Stop names for each fuel stop:')
    for name in exit_names:
        print(name)

    print('\nDistance between fuel stops:')
    print(distance_between_fuel_stops)

    print('\nTime to reach fuel stops:')
    print(time_to_fuel_stops)
    '''
    return [
        highway_names,
        potential_fuel_stops,
        distances,
        time_to_fuel_stops
    ]


# COULDN'T FIND AN ONLINE DATABASE OF API FOR THIS
# TRY PREDICTION OR WEB-SCRAPING
# Check out: https://www.tomtom.com/products/fuel-services/
def CalculateFuelPrice(stop):
    pass
    # IMPLEMENTATION HERE

def get_fuel_prices(potential_fuel_stops):
    fuel_prices = [CalculateFuelPrice(stop) for stop in potential_fuel_stops]
    return fuel_prices


def Main():
    # Get Information about Car
    # Get Information about Trip
    # Get Information about Fuel Prices

    # Format Information

    # Create file called 'trip_info'

    # Write Fuel Economy, Fuel Capacity, Trip Budget, and Number 
    # of Stops on 1 line each seperated by single spaces

    # Write distance from current stop to next stop for all stops
    # Write time from current stop to next stop for all stops

    # Write time taken from the highway to the fuel stop back 
    # to the highway for all stops

    # Write Cost of Fuel

    # End Data Collection Phase
    pass

Main()