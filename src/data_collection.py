from geopy.distance import geodesic
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
import googlemaps
from datetime import datetime

# Set up Google Maps Client
gmaps = googlemaps.Client(key='YOUR_API_KEY_HERE')

# Get the directions from Google Maps
def GetDirections(start_location, end_location):
    directions_result = gmaps.directions(
        start_location,
        end_location,
        mode="driving",
        departure_time=datetime.now()
    )
    return directions_result[0]['legs'][0]['steps']

# Extract highways and major roads
def ExtractHighwayNames(route):
    highway_names = []
    for step in route:
        instr = step['html_instructions'].lower()
        if 'highway' in instr or 'toll road' in instr or 'freeway' in instr:
            highway_names.append(step['html_instructions'])
    return highway_names

# Find potential fuel stops
def FindFuelStops(route):
    potential_fuel_stops = []
    for step in route:
        instr = step['html_instructions'].lower()
        if 'highway' in instr or 'toll road' in instr or 'freeway' in instr:
            for intersection in step['intersections']:
                for road in intersection['roads']:
                    road_name = road['name'].lower()
                    if 'gas' in road_name or 'petrol' in road_name or 'fuel' in road_name:
                        exit_name = f"{road['name']} on Exit {intersection['exit']}"
                        potential_fuel_stops.append((exit_name, intersection['location']))
    return potential_fuel_stops

# Calculate distances between fuel stops
def GetFuelStopDistances(start_location, end_location, potential_fuel_stops):
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
    
    return distances

# Calculate the time to reach the fuel stop from the exit ramp
# THIS IS WRONG BECAUSE OF THE EXIT_RAMP_LOCATION
def GetFuelStopTimes(potential_fuel_stops):
    time_to_fuel_stops = []
    for i in range(len(potential_fuel_stops)):
        # FIX exit_ramp_location VALUE
        exit_ramp_location = potential_fuel_stops[i][1]
        fuel_stop_location = potential_fuel_stops[i][1]

        directions_result = gmaps.directions(
            exit_ramp_location, 
            fuel_stop_location, 
            mode="driving", 
            departure_time=datetime.now()
        )

        time_exit_ramp_to_fuel_stop = directions_result[0]['legs'][0]['duration']['value']
        time_to_fuel_stops.append(time_exit_ramp_to_fuel_stop)

    return time_to_fuel_stops

# COULDN'T FIND AN ONLINE DATABASE OF API FOR THIS
# TRY PREDICTION OR WEB-SCRAPING
# Check out: https://www.tomtom.com/products/fuel-services/
def CalculateFuelPrice(stop):
    pass
    # IMPLEMENTATION HERE

def GetFuelPrices(potential_fuel_stops):
    fuel_prices = [CalculateFuelPrice(stop) for stop in potential_fuel_stops]
    return fuel_prices

# Parent function to handle data collection
def DataCollection(start_location, end_location):
    route = GetDirections(start_location, end_location)
    highway_names = ExtractHighwayNames(route)
    potential_fuel_stops = FindFuelStops(route)
    fuel_stop_dists = GetFuelStopDistances(start_location, end_location, potential_fuel_stops)
    time_to_fuel_stops = GetFuelStopTimes(potential_fuel_stops)
    fuel_prices = GetFuelPrices(potential_fuel_stops)

    return {
        "Route": route,
        "Highway Names": highway_names,
        "Potential Fuel Stops": potential_fuel_stops,
        "Fuel Stop Distances": fuel_stop_dists,
        "Time to Fuel Stops": time_to_fuel_stops,
        "Fuel Prices": fuel_prices
    }


def Main(start_location, end_location):
    # Collect Data
    data = DataCollection(start_location, end_location)

    # Format Information

    
    return data

Main()