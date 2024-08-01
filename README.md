# ORDER_ASSIGNMENT_AND_PATH_OPTIMIZATION
this repo  contains a complex  algorithm and there source code  which are able to   maximize the profit of  dilhivery company

Main file  using_buffer_schedululing.py
function contains in this file

1. Assignment  funtion which assign the orders to riders
 python dependcuies
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
 
 module dependencies
 # importing the functions from other modules
    from test import generate_orders_and_riders
    from utils import print_rider_details, print_matrix, append_order
    from generate_matrix import generate_matrixs
    from utils import get_max_in_the_matrix




constraints which is maybe fixed in the algorithm


# Constants
OTD = 60  # Order Time Delivery limit in minutes
first_mile_speed = 25  # Speed to reach pickup location in km/h
last_mile_speed = 15   # Speed from pickup to delivery location in km/h
return_mile_speed = 40 # Speed to return from delivery location to origin in km/h
batch_size = 100  # Number of orders that can be assigned to a rider at once
first_mile_cost = 2 # Cost to reach pickup location in km
last_mile_cost = 5 # Cost to deliver from pickup location to delivery location in  /km
return_mile_cost = 1.5  # Cost to return from delivery location to origin in  /km
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




modoule  test.py  contains all the funtion which is used for testing function 
1.generate_orders_and_riders(num of orders, num of riders , num of locations)



module  generate_matrix.py  contains all the funtion which is used for generating matrix

1. generate_matrixs(orders , riders)

2. print_matrix(matrix) # print the matrix

3. get_max_in_the_matrix(matrix) # get the maximum value in the matrix

4. ALL_in_time(rider,order) # check the order is in time or not

5. get_distance(coordinate1 , coordinate2) # get the distance between two location

module utils.py contains all the utility function which is used in the main file

1. print_rider_details(rider) # print the rider details

2. append_order(rider, order) # append the order to the rider

3. calculate_distance(order, rider) # calculate the cost of the order

4. calculate_delhivery_time(rider,order) # calculate the delhivery time

5. get_min_OTD(rider,order) # get the minimum OTD of the rider 

6. total_profit(rider) # calculate the total profit of the rider

module  nearby_order.py contains all the function which is used for finding the nearby order

1.  get_longest_coordinate(coordinate) # get the longest coordinate

2. is_in_the_route(rider,order) # check the order is in the route or not


module Optimize_route.py contains all the function which is used for optimizing the route

1. optimize_route(rider) # optimize the route of the single rider

2. extract_coordinates(rider) # extract the coordinates of the rider

