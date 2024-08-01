# importing necessary libraries
import copy
import random
import numpy as np
import matplotlib.pyplot as plt
from itertools import permutations
import math
from math import radians, sin, cos, sqrt, atan2
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse

def remove_duplicates(input_list):
    # Convert the list to a set of tuples to remove duplicates, then convert back to list of lists
    return [list(t) for t in set(tuple(i) for i in input_list)]

def extract_coordinates(rider):
    """
    Extract pickup and delivery coordinates from riders' routes.

    Args:
    rider (list): List of rider dictionaries containing their routes.

    Returns:
    tuple: Two lists containing pickup coordinates and delivery coordinates.
    """
    pickup_coords = []
    delivery_coords = []
    try:
        coordinates = rider["coordinates"]
        for coor_pair in coordinates:
            pickup, delivery = coor_pair
            pickup_coords.append(pickup)
            delivery_coords.append(delivery)
        
        # Removing duplicates if needed
        pickup_coords = remove_duplicates(pickup_coords)
        delivery_coords = remove_duplicates(delivery_coords)
        
        return pickup_coords, delivery_coords

    except Exception as e:
        print(f"Error extracting coordinates: {e}")
        return [], []

def calculate_distance(coord1, coord2):
    """
    Calculate the Euclidean distance between two points.

    Args:
    coord1 (list): The first coordinate [x, y].
    coord2 (list): The second coordinate [x, y].

    Returns:
    float: The Euclidean distance between the two points.
    """
    dist = np.sqrt((coord1[0] - coord2[0]) ** 2 + (coord1[1] - coord2[1]) ** 2)
    return round(dist, 2)

def calculate_route_distance(route, coordinates):
    """
    Calculate the total distance of a given route.

    Args:
    route (list): The order of visiting points.
    coordinates (list): List of coordinates corresponding to the route points.

    Returns:
    float: The total distance of the route.
    """
    distance = 0
    for i in range(len(route) - 1):
        coord1 = coordinates[route[i]]
        coord2 = coordinates[route[i + 1]]
        distance += calculate_distance(coord1, coord2)
    
    return distance

def optimize_route(rider):
    """
    Optimize the route for a rider to minimize the travel distance.

    Args:
    rider (dict): A dictionary containing rider information including coordinates.

    Returns:
    tuple: Best route coordinates, minimum distance, and flags indicating the type of route.
    """
    all_coords = []
    current_location = [rider["current_coordinates"]]
    pickup_coords, delivery_coords = extract_coordinates(rider)
    
    all_coords.extend(current_location)
    all_coords.extend(pickup_coords)
    all_coords.extend(delivery_coords)
    
    pickup_count = len(pickup_coords)
    delivery_count = len(delivery_coords)
    min_distance = float('inf')
    best_route = None
    best_flags = None
    pickup_indices = list(range(1, pickup_count + 1))
    delivery_indices = list(range(pickup_count + 1, pickup_count + delivery_count + 1))
    
    for pickup_permutation in permutations(pickup_indices):
        for delivery_permutation in permutations(delivery_indices):
            route = [0] + list(pickup_permutation) + list(delivery_permutation) + [0]
            flags = []  # Start with the current location (initial point, no flag)
            items_in_cart = 0  # Track items in cart
            
            for i in range(1, len(route) - 1):
                if route[i] in pickup_indices:
                    if items_in_cart == 0:
                        flags.append(0)  # First mile (picking up first order)
                    else:
                        flags.append(1)  # Last mile (already has items, this is additional pickup)
                    items_in_cart += 1  # After pickup, increment cart count
                elif route[i] in delivery_indices:
                    flags.append(1)  # Last mile (delivering order)
                    items_in_cart -= 1  # After delivery, decrement cart count
            
            # Add flag for return to home if cart is empty
            if items_in_cart == 0:
                flags.append(-1)  # Return mile
            else:
                flags.append(1)  # Still delivering something on the way home

            distance = calculate_route_distance(route, all_coords)
            print(f"Route: {route}, Flags: {flags}, Distance: {distance}")
            if distance < min_distance:
                min_distance = distance
                best_route = route
                best_flags = flags
    print(f"Best Route: {best_route}, Min Distance: {min_distance}, Flags: {best_flags}")
    best_route_coordinates = [all_coords[i] for i in best_route]
    
    return best_route_coordinates, min_distance, best_flags

