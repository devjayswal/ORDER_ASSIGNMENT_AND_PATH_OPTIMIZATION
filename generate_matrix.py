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

#module dependencies
from utils import *
from nearby_order import get_longest_coordinate,is_in_the_route



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



# here is the funtion to generate the matrix for the Assignment
def calculate_distance(coordnate1, coordnate2):
    
    [coord1] = coordnate1
    [coord2] = coordnate2
    """
    Calculate the Euclidean distance between two coordinates.
    """
    try:
        dist = np.sqrt((coord1[0] - coord2[0]) ** 2 + (coord1[1] - coord2[1]) ** 2)
        dist = round(dist, roundoff_digit)
        return dist
    except Exception as e:
        print(f"Error calculating distance: {e}")
        return 0

def ALL_in_time(rider):
    """
    Check if all orders are within the OTD limit for a rider.
    """
    if len(rider["CART"]) == 0:
        print("All in time function called and all in time, because cart is empty.")
        return True
    else:
        for order in rider["CART"]:
            if order["OTD"] > OTD:
                print("All in time function called and not all in time.")
                return False
        print("All in time function called and all in time.")
    return True


def get_max_in_the_matrix(matrix):
    """
    Find the maximum value in a matrix and its position.
    """
    try:
        max_value = -math.inf
        row_index = -1
        column_index = -1
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                if matrix[i][j] > max_value:
                    max_value = matrix[i][j]
                    row_index = i
                    column_index = j
        print(max_value, row_index, column_index)
        return max_value, row_index, column_index
    except Exception as e:
        
        print(f"Error finding max value in matrix: {e}")
        return None, None, None

def get_delivery_time(rider, order):
    print("get delivery time function called")
    orderid = order["ORDER_ID"]
    print("Order id", orderid)
    delivery_times = rider["delivery_times"]
    print("Delivery times", delivery_times)
    print(type(delivery_times))
    
    for item in delivery_times:
        print("item", item)
        if orderid in item:
            print("item keys", list(item.keys())[0])
            print("item values", list(item.values())[0])
            return list(item.values())[0]
    
    print("Delivery time not found")


def generate_matrixs(orders, riders):
    """
    Generate profit, OTD, and distance matrices for orders and riders.
    """
    profit_matrix = []
    OTD_matrix = []
    distance_matrix = []
    time_duration_matrix = []
    for j in range(len(riders)):
        rider_orig = riders[j]
        if len(rider_orig["CART"]) > 0:
            
            profit_row = []
            OTD_row = []
            distance_matrix_row = []
            time_duration_matrix_row = []
            
            
            for i in range(len(orders)):
                rider = copy.deepcopy(riders[j])
                print(f"Rider {rider['RIDER_ID']} has orders in the cart")
                order = copy.deepcopy(orders[i])
                rider_capacity = rider["rider_capacity"]
                if order["order_volume"] <= rider_capacity :
                    rider = append_order(order, rider)
                    profit = total_profit(rider)
                    if is_in_the_route(rider, order):
                        if profit > min_profit:
                            if ALL_in_time(rider) :
                                print("All in time",ALL_in_time(rider))
                                print(rider)
                                profit_row.append(round(profit, roundoff_digit))
                                OTD_row.append(round(get_min_OTD(rider["CART"]), roundoff_digit))
                                distance_matrix_row.append(round(rider["total_distance"], roundoff_digit))
                                time_duration_matrix_row.append(get_delivery_time(rider, order))
                            else:
                                profit_row.append(-5)
                                OTD_row.append(-5)
                                distance_matrix_row.append(-5)
                                time_duration_matrix_row.append(-5)
                        else:
                            profit_row.append(-5)
                            OTD_row.append(-5)
                            distance_matrix_row.append(-5)
                            time_duration_matrix_row.append(-5)
                    else:
                        profit_row.append(-5)
                        OTD_row.append(-5)
                        distance_matrix_row.append(-5)
                        time_duration_matrix_row.append(-5)
                else:
                    profit_row.append(-5)
                    OTD_row.append(-5)
                    distance_matrix_row.append(-5)
                    time_duration_matrix_row.append(-5)
                                    
            profit_matrix.append(profit_row)
            OTD_matrix.append(OTD_row)
            distance_matrix.append(distance_matrix_row)
            time_duration_matrix.append(time_duration_matrix_row)
            continue
        
        else:
            profit_row = []
            OTD_row = []
            distance_matrix_row = []
            time_duration_matrix_row = []
            order_index = 0
            for order in orders:
                rider = copy.deepcopy(riders[j])
                order = copy.deepcopy(order)
                order_index += 1
                print("order index",order_index)
                #order = orders[order]
                print("order",order)
                rider = append_order(order, rider)
                
                tot_profit = round(total_profit(rider), roundoff_digit)
                OTD = round(order["OTD"], roundoff_digit)
                distance= round(rider["total_distance"], roundoff_digit)
                Duration = get_delivery_time(rider, order)
                
                print("this is row value",OTD, tot_profit, distance, Duration)
                Duration = 0
                profit_row.append(tot_profit)
                OTD_row.append(OTD)
                distance_matrix_row.append(distance)
                time_duration_matrix_row.append(Duration)

            print("print profit row",profit_row)
            profit_matrix.append(profit_row)
            OTD_matrix.append(OTD_row)
            distance_matrix.append(distance_matrix_row)
            time_duration_matrix.append(time_duration_matrix_row)
        print("matrix updated")
    
    return profit_matrix, OTD_matrix, distance_matrix, time_duration_matrix



def print_matrix(matrix):
    """
    Print the matrix in a formatted way.
    """
    try:
        for row in matrix:
            for value in row:
                print(value, end=" ")
            print()
    except Exception as e:
        print(f"Error printing matrix: {e}")
