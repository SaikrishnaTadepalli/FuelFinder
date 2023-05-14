import googlemaps
from datetime import datetime

# Set up the Google Maps client
gmaps = googlemaps.Client(key='YOUR_API_KEY')

# Define the start and end locations
start_location = '25 OceanPearl Crescent, Whitby, ON, Canada'
end_location = '252 Phillip Street West, Waterloo, ON, Canada'

# Get the directions from Google Maps
directions_result = gmaps.directions(start_location, end_location, mode="driving", departure_time=datetime.now())

# Extract the optimal route
route = directions_result[0]['legs'][0]['steps']

# Extract the highway and major road names
highway_names = []
for step in route:
    if 'highway' in step['html_instructions'].lower() or 'toll road' in step['html_instructions'].lower() or 'freeway' in step['html_instructions'].lower():
        highway_names.append(step['html_instructions'])

# Find the potential fuel stops
potential_fuel_stops = []
for step in route:
    if 'highway' in step['html_instructions'].lower() or 'toll road' in step['html_instructions'].lower() or 'freeway' in step['html_instructions'].lower():
        for intersection in step['intersections']:
            for road in intersection['roads']:
                if 'gas' in road['name'].lower() or 'petrol' in road['name'].lower() or 'fuel' in road['name'].lower():
                    exit_name = f"{road['name']} on Exit {intersection['exit']}"
                    potential_fuel_stops.append((exit_name, intersection['location']))

# Find the distance between fuel stops
distance_between_fuel_stops = []
for i in range(len(potential_fuel_stops)-1):
    dist_result = gmaps.distance_matrix(potential_fuel_stops[i][1], potential_fuel_stops[i+1][1], mode="driving")
    distance_between_fuel_stops.append(dist_result['rows'][0]['elements'][0]['distance']['value'])

# Find the time taken to get to each fuel stop
time_to_fuel_stops = []
for i in range(len(potential_fuel_stops)):
    time_result = gmaps.directions(start_location, potential_fuel_stops[i][1], mode="driving", departure_time=datetime.now())
    time_to_fuel_stops.append(time_result[0]['legs'][0]['duration']['value'])

# Find the exit/stop names for each fuel stop
exit_names = []
for fuel_stop in potential_fuel_stops:
    exit_names.append(fuel_stop[0])

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
