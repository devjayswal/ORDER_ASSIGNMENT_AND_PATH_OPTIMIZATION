# importing nessary libraries
import copy
import random
import numpy as np
import matplotlib.pyplot as plt
from itertools import permutations
import math
from math import radians, sin, cos, sqrt, atan2
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
import json

# importing the functions from other modules
from test import generate_orders_and_riders
from utils import print_rider_details,  append_order, calculate_distance, calculate_delivery_time,get_min_OTD,total_profit
from generate_matrix import generate_matrixs,get_max_in_the_matrix,print_matrix
from nearby_order import get_longest_coordinate,is_in_the_route
from Optimize_route import optimize_route, extract_coordinates


# Constants
OTD = 60  # Order Time Delivery limit in minutes
first_mile_speed = 25  # Speed to reach pickup location in km/h
last_mile_speed = 15   # Speed from pickup to delivery location in km/h
return_mile_speed = 40 # Speed to return from delivery location to origin in km/h
batch_size = 100  # Number of orders that can be assigned to a rider at once
first_mile_cost = 2 # Cost to reach pickup location in $/km
last_mile_cost = 5 # Cost to deliver from pickup location to delivery location in $/km
return_mile_cost = 1.5  # Cost to return from delivery location to origin in $/km
ellipse_a = 0.5 # Ellipse axes lengths a
ellipse_b = 0.5 # Ellipse axes lengths b
roundoff_digit = 4 # Round off digit for floating point numbers
avg_speed = 25 # average speed of the rider needs to be removed
our_cut = 0.08 # variable  from 8% to 15%
avg_cost_per_km = 2.5 # needs to be remove
rider_capacity = 20 # maybe variable rider to rider 
min_profit = -3 # minimum profit to assign an order to a rider needs to be 0
# if there are multiple order assigned  so then maximum percentage of bearable loss of total profit
maximum_percentage_of_bearable_loss_when_mulitple_orders_assign = 0.5 # 50% loss is bearable if mulitple orders are assigned to a rider at once

order_per_minute = 5 # order per minute
maximum_order_per_day = 1000 # maximum order per day
sleep_time = 10 # sleep time in seconds


  
def Assignment(orders, riders, assigned_orders, unassigned_orders):
    print("Assignment function called")
    """
    Assigns orders to riders based on maximum profit and updates the matrices accordingly.

    Args:
    orders (list): List of ordeavr dictionaries.
    riders (list): List of rider dictionaries.
    assigned_orders (list): List to store assigned orders.
    unassigned_orders (list): List to store unassigned orders.
    """
    iterations = 0
    while len(orders) > 0:
        #try:
        iterations += 1
        print(f"Iteration:.................. {iterations}")
        # Generate matrices for profit, OTD, and distance
        profit_matrix, OTD_matrix, distance_matrix, time_duration_matrix = generate_matrixs(orders, riders)
        print("Generated Matrices:")
        print("Profit Matrix:")
        print_matrix(profit_matrix)
        print("OTD Matrix:")
        print_matrix(OTD_matrix)
        print("Distance Matrix:")
        print_matrix(distance_matrix)
        print("Time Duration Matrix:")
        print_matrix(time_duration_matrix)
    
    
        # Get the maximum profit calculate_delivery_timeand corresponding indices
        max_profit, rider_index, order_index = get_max_in_the_matrix(profit_matrix)
        print(f"Max Profit: {max_profit}, Rider Index: {rider_index}, Order Index: {order_index}")
        if max_profit < min_profit:
            for order in orders:
                unassigned_orders.append(order)
            print(f"There are no orders where the profit is less than {min_profit} for all riders")
            return assigned_orders, unassigned_orders,riders
        print(f"Profit is positive : Max Profit: {max_profit}, Rider Index: {rider_index}, Order Index: {order_index}")
    
        # Check if indices are valid
        if rider_index != -1 and order_index != -1:
            print(f"Assigning order {orders[order_index]['ORDER_ID']} to rider {riders[rider_index]['RIDER_ID']}")
        
            # Append the order to the rider's route
            riders[rider_index] = append_order(orders[order_index], riders[rider_index])

            # Add the assigned order to the assigned_orders list and remove it from the orders list
            assigned_orders.append(orders[order_index])
            orders.pop(order_index)
            
            # Store the updated rider data in a JSON file
            with open('rider.json', 'a') as json_file:
                json.dump(riders[rider_index], json_file, indent=4)
            print(f"Rider data stored in rider.json after assigning order ")

            
        else:
            print("No valid assignment found. Moving to next iteration.")

    #except Exception as e:
        # print(f"Error in assignment process: {e}")
        # break
    print("All orders have been assigned.")
    print("Assigned Orders:")
    print(assigned_orders)
    print("Unassigned Orders:")
    print(unassigned_orders)
    return assigned_orders, unassigned_orders , riders

