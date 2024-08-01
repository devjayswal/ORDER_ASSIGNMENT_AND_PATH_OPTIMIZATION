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



#here the all utility functions are defined
from Optimize_route import optimize_route


def calculate_distance(coordinate1, coordinate2, roundoff_digit=2):
    """
    Calculate the Euclidean distance between two coordinates.
    """
    print("Calculating distance")
    print(f"coordinate1 = {coordinate1}")
    print(f"coordinate2 = {coordinate2}")
    
    coord1 = coordinate1[0]
    coord2 = coordinate2[0]
    
    print(f"coord1 = {coord1}")
    print(f"coord2 = {coord2}")
    
    dist = np.sqrt((coord1[0] - coord2[0]) ** 2 + (coord1[1] - coord2[1]) ** 2)
    dist = round(dist, roundoff_digit)
    
    return dist

def calculate_distance_for_delhivery_time(x,y):
    print("Calculating distance for delhivery time")
    distance = 0
    distance = distance + np.sqrt((x[0] - y[0]) ** 2 + (x[1] - y[1]) ** 2)
    
    return distance




def print_rider_details(riders):
    """
    Print details of all riders.
    """
    print(".........................../")
    for rider in riders:
        print(f'RIDER_ID = {rider["RIDER_ID"]}, Our Profit = {rider["our_profit"]}, Total Order Value = {rider["Total_order_value"]}, Total Distance = {rider["total_distance"]}, Total Orders = {len(rider["CART"])} ')
        for item in rider["delivery_times"]:
            key = list(item.keys())[0]
            print(f"Delhiver Time of Order id {key} is {item[key]}")
    print(".........................../")


def append_order(order_orig, rider_orig):
    # try:
    order=copy.deepcopy(order_orig)
    rider=copy.deepcopy(rider_orig)
    
    if len(rider["CART"])==0:
        print(f"Order {order['ORDER_ID']} appended to rider {rider['RIDER_ID']}")
        print("appending if case")
        rider["CART"].append(order)
        rider["route"] = [order["pickup_coordinates"],order["delivery_coordinates"]]
        rider["rider_order_status"].append("PICKUP")
        rider["coordinates"] = [[order["pickup_coordinates"],order["delivery_coordinates"]]]
        rider["rider_capacity"] -= order.get("order_volume", 0)
        order["Rider"] = rider["RIDER_ID"]
        rider["Total_order_value"] += order["Order_value"]
        rider["our_profit"] = round((rider["Total_order_value"] * our_cut),roundoff_digit) - rider["total_distance"] * avg_cost_per_km
        rider["total_distance"] = calculate_distance([rider["current_coordinates"]], [order["pickup_coordinates"]])+calculate_distance([order["pickup_coordinates"]], [order["delivery_coordinates"]])
        delhivery_time = calculate_delivery_time(rider)
        print("delhivery timemmmm",delhivery_time)
        rider["delivery_times"] = calculate_delivery_time(rider)
        return rider
    else:
        print("appending else case")
        rider["coordinates"].append([order["pickup_coordinates"],order["delivery_coordinates"]])
        rider["CART"].append(order)
        best_route_coordinates, min_distance, best_flags = optimize_route(rider)
        rider["route"] = best_route_coordinates  # Assign the best route to rider["route"]
        rider["rider_flags"] = best_flags
        rider["rider_order_status"].append("DELIVERY")
        order["Rider"] = rider["RIDER_ID"]
        print(f"Order {order['ORDER_ID']} appended to rider {rider['RIDER_ID']}")
        rider["rider_capacity"] -= order["order_volume"]
        rider["total_distance"] = min_distance
        rider["our_profit"] = round((rider["Total_order_value"] * our_cut),roundoff_digit) - rider["total_distance"] * avg_cost_per_km
        rider["Total_order_value"] += order["Order_value"]
        print([rider])
        delhivery_time = calculate_delivery_time(rider)
        print("delhivery time moon",delhivery_time)
        rider["delivery_times"] = calculate_delivery_time(rider)
        print_rider_details([rider])
        return rider
    # except KeyError as e:
    #     print(f"Error: Missing key {e} in rider or order dictionary")
    # except Exception as e:
    #     print(f"An error occurred while appending order: {e}")


def calculate_delivery_time(rider):
    print("Calculating delivery time")
    print("rider cart ",rider["CART"])
    delhivery_times = []
    delhivery_time = 0
    if len(rider["CART"]) == 0:
        print("No orders in the cart. and At that time this function need not to call something wrong")
        return delhivery_times
    if len(rider["CART"]) == 1:
        order = rider["CART"][0]
        pickup = order["pickup_coordinates"]
        delhivery = order["delivery_coordinates"]
        delhivery_time = (calculate_distance_for_delhivery_time(rider["current_coordinates"], pickup)/first_mile_speed)*60
        delhivery_time = delhivery_time + (calculate_distance_for_delhivery_time(pickup, delhivery)/last_mile_speed)*60
        delhivery_times.append({order["ORDER_ID"]:delhivery_time})
        return delhivery_times
    else:
        current_coordinates = rider["current_coordinates"]
        print("current coordinates",current_coordinates)
        orders = rider["CART"]
        print(f"Rider CART have :{len(orders)}")
        coordinats = rider["route"] 
        for order in orders:  
            pickup = order["pickup_coordinates"]
            delhivery = order["delivery_coordinates"]
            print(f"Coordinates:{coordinats}")
            print("current coordinates",current_coordinates)
            print(f"Pickup:{pickup}")
            print(f"Delhivery:{delhivery}")

            i = coordinats.index(pickup) 
            j = coordinats.index(delhivery)
            
            print("i = ",i)
            print("j = ",j)

            delhivery_time = delhivery_time + (calculate_distance_for_delhivery_time(current_coordinates, coordinats[i])/first_mile_speed)*60
            delhivery_time = delhivery_time + (calculate_distance_for_delhivery_time(coordinats[i], coordinats[j])/last_mile_speed)*60
            delhivery_times.append({order["ORDER_ID"]:delhivery_time})
        return delhivery_times




def get_min_OTD(orders):
    """
    Get the minimum OTD from a list of orders.
    """
    OTD = math.inf
    try:
        for order in orders:
            if order["OTD"] < OTD:
                OTD = order["OTD"]
        return OTD
    except Exception as e:
        print(f"Error getting min OTD: {e}")
        return 0


def total_profit(rider):
    tot_profit = 0
    """
    Calculate the total profit if rider pick this order .
    """
    try:
        if len(rider["CART"]) == 0:
            print("Total profit function called and cart is empty.")
            return tot_profit
        if len(rider["CART"]) == 1:
            revenue = rider["Total_order_value"]*our_cut
            order = rider["CART"][0]
            cost = calculate_distance([rider["current_coordinates"]], [order["pickup_coordinates"]]) * first_mile_cost
            cost = cost + calculate_distance([order["pickup_coordinates"]], [order["delivery_coordinates"]]) * last_mile_cost
            tot_profit = revenue - cost
            return tot_profit
        else:
            cost = 0 
            path = rider["route"]
            flags = rider["rider_flags"]
            revenue = rider["Total_order_value"]*our_cut
            for i in range(len(rider["rider_flags"])):
                if flags[i] == 0:
                    cost = cost + calculate_distance([path[i]],[path[i+1]]) * first_mile_cost
                elif flags[i] == 1:
                    cost = cost + calculate_distance([path[i]],[path[i+1]]) * last_mile_cost
                elif flags[i] == -1:
                    cost = cost + calculate_distance([path[i]],[path[i+1]]) * return_mile_cost
                else:
                    print("Invalid flag")
            tot_profit = revenue - cost
            return tot_profit

    except Exception as e:
        print(f"Error calculating profit: {e}")
        return 0
