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
min_profit = 0 # minimum profit to assign an order to a rider needs to be 0
# if there are multiple order assigned  so then maximum percentage of bearable loss of total profit
maximum_percentage_of_bearable_loss_when_mulitple_orders_assign = 0.5 # 50% loss is bearable if mulitple orders are assigned to a rider at once



#Contain funtions which is used to test the model


def generate_orders_and_riders(order_num, rider_loc,resto_location):
    
    """
    Generate random orders and riders for testing purposes.
    """
    orders = []
    riders = []

    # Latitude and longitude bounds for the random generation
    min_order_price, max_order_price = 200,500
    min_lat, max_lat = 1, 15
    min_lon, max_lon = 1, 15

    # Fixed pickup coordinates
    print(resto_location)
    # Generate orders
    for i in range(order_num):
        
        order_id = f"ORD{i+1:03}"
        delivery_coordinates = [round(random.uniform(min_lat, max_lat), 4), round(random.uniform(min_lon, max_lon), 4)]
        orders.append({
            "ORDER_ID": order_id,
            "pickup_coordinates": random.choice(resto_location),
            "delivery_coordinates": delivery_coordinates,
            "Order_value": round(random.uniform(min_order_price, max_order_price), 2),
            "order_volume": random.randint(1, 5),
            "OTD" : random.randint(30, 60),
            "Rider" : None,
            "first_mile_distance": 0,
            "last_mile_distance": 0,
            "first_mile_time": 0,
            "last_mile_time": 0,
        })

    # Generate riders
    for i in range(len(rider_loc)):
        rider_id = f"RID{i+1:03}"
        riders.append({
            "RIDER_ID": rider_id,
            "current_coordinates": rider_loc[i],
            "rider_capacity": rider_capacity,
            "CART":[],
            "coordinates": [],
            "route": [],
            "rider_order_status": [],
            "rider_flags": [], #flags for the route 0 for pickup, 1 for delivery, -1 for return
            "our_profit": 0,
            "rider_order": [],
            "Total_order_value": 0,
            "total_distance": 0,
            "total_orders": 0,
            "delivery_times":[],
            
        })

    return orders, riders
