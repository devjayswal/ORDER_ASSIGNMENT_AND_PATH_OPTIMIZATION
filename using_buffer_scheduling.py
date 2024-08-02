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
import time

# importing the functions from other modules
from test import generate_orders_and_riders
from utils import print_rider_details,  append_order, calculate_distance, calculate_delivery_time,get_min_OTD,total_profit
from generate_matrix import generate_matrixs,get_max_in_the_matrix,print_matrix
from nearby_order import get_longest_coordinate,is_in_the_route
from Optimize_route import optimize_route, extract_coordinates
from Assignment import Assignment

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
sleep_time = 5 # sleep time in seconds

rider_num = 10

assigned_orders = []
unassigned_orders = []


total_resto = 5
total_attended_orders = 0
min_lat, max_lat = 1, 15
min_lon, max_lon = 1, 15


resto_location=[
        [round(random.uniform(min_lat, max_lat), 4), round(random.uniform(min_lon, max_lon), 4)]
        for _ in range(total_resto)
    ]
rider_loc=[
        [round(random.uniform(min_lat, max_lat), 4), round(random.uniform(min_lon, max_lon), 4)]
        for _ in range(rider_num)
    ]

print("resto location",resto_location)

orders1, riders1 = generate_orders_and_riders(order_per_minute,rider_loc,resto_location)
assinged =0
order2 = []
order2.extend(orders1)
total_assigned_orders =0
iter = 0
while maximum_order_per_day > 0:
    maximum_order_per_day -= order_per_minute
    total_attended_orders += order_per_minute
    iter += 1

    # Run the assignment function
    new_assigned_orders, unassigned_orders, riders = Assignment(order2, riders1, assigned_orders, unassigned_orders)

    print(f"ITERATION: {iter}")
    print("Assigned Orders in this iter:")
    print(len(new_assigned_orders))
    # Update assigned_orders list by appending new assignments
    
    assigned_orders.extend(new_assigned_orders)

    print(f"Order remain in unassigned orders: {len(unassigned_orders)} + New orders: {order_per_minute} = {len(unassigned_orders) + order_per_minute}")
    print(f"Total Attended Orders: {total_attended_orders}")
    
    # Total assigned orders across all iterations
    total_assigned_orders = len(assigned_orders)
    print("Total Assigned Orders:")
    print(total_assigned_orders)
    

    
    print("Unassigned Orders in this iter:")
    print(len(unassigned_orders))

    # Generate new orders
    orders, riders = generate_orders_and_riders(order_per_minute, rider_loc, resto_location)
    
    # Prepare orders for the next iteration
    order2 = orders + unassigned_orders

    unassigned_orders = []

    # Print rider details
    print_rider_details(riders1)
    
    # Pause for the next iteration
    time.sleep(sleep_time)
