
from pyvrp import Model,read
from pyvrp.plotting import (
    plot_coordinates,
    plot_instance,
    plot_result,
    plot_route_schedule,
)
from pyvrp.stop import MaxIterations, MaxRuntime
import copy
import random
import numpy as np
import matplotlib.pyplot as plt
import math

# Constants
OTD = 60  # Order Time Delivery limit in minutes
first_mile_speed = 20  # Speed to reach pickup location in km/h
last_mile_speed = 25   # Speed from pickup to delivery location in km/h
return_mile_speed = 30 # Speed to return from delivery location to origin in km/h
batch_size = 100  # Number of orders that can be assigned to a rider at once
first_mile_cost = 2 
last_mile_cost = 5
return_mile_cost = 1.5
ellipse_a = 0.5
ellipse_b = 0.5
roundoff_digit = 3
avg_speed = 25
our_cut = 0.08
avg_cost_per_km = 2.83

assigned_orders = []
unassigned_orders = []


# # Functions
def ALL_in_time(rider, order):
    
    return True

def get_longest_coordinate(coordinate):
    print("get_longest_coordinate function called")
    max_distance = 0
    longest_coordinate = []
    """
    Get the longest coordinate from a list of coordinates.
    """
    try:
        for coors in coordinate:
            (p,d) = coors
            distance = calculate_distance(p, d)
            if distance > max_distance:
                longest_coordinate = [p,d]
                max_distance = distance     
                longest_coordinate = coors
        return longest_coordinate
        
    except Exception as e:
        print(f"Error getting longest coordinate: {e}")
        return None

def get_duration(distance):
    print("get_duration function called")
    print(distance)
    """
    Get the duration in minutes from a given distance.
    """
    try:
        duration = distance / avg_speed * 60
        return round(duration, roundoff_digit)
    except Exception as e:
        print(f"Error getting duration: {e}")
        return 0

def get_max_distance(rider):
    print("get_max_distance function called")
    print(rider)
    """
    Get the maximum distance from a list of coordinates.
    """
    try:
        print(rider)
        route ,max_distance  = optimize_route(rider)
        print(f"max_distance: {max_distance}")
        return max_distance
    except Exception as e:
        print(f"Error getting max distance: {e}")
        return None

def get_max_profit(orders,distance):
    """
    Get the maximum profit from a list of orders.
    """
    try:
        profit = 0
        cost = distance * avg_cost_per_km
        for order in orders:
            profit += order["Order_value"] * our_cut - cost
        profit = round(profit, roundoff_digit)
        print(f"Profit: {profit}")
        return profit
    except Exception as e:
        print(f"Error getting profit: {e}")
        return 0

def extract_coordinates(rider):
    print("extract_coordinates function called")
    """
    Extract pickup and delivery coordinates from riders' routes.

    Args:
    rider (list): List of rider dictionaries containing their routes.

    Returns:
    tuple: Two lists containing pickup coordinates and delivery coordinates.
    """
    def remove_duplicates(input_list):
        # Convert the list to a set of tuples to remove duplicates, then convert back to list of lists
        return [list(t) for t in set(tuple(i) for i in input_list)]

    pickup_coords = []
    delivery_coords = []

    try:
        rider = rider[0]
        print(rider)
        routes = rider["route"]
        for route in range(len(routes)):
            pickup, delivery = routes[route]
            pickup_coords.append(pickup)
            delivery_coords.append(delivery)
        # Removing duplicates if needed
        pickup_coords = remove_duplicates(pickup_coords)
        delivery_coords = remove_duplicates(delivery_coords)
        return pickup_coords, delivery_coords

    except Exception as e:
        print(f"Error extracting coordinates: {e}")
        return [], []

def generate_orders_and_riders(order_num, rider_num):
    """
    Generate random orders and riders for testing purposes.
    """
    orders = []
    riders = []

    # Latitude and longitude bounds for the random generation
    min_order_price, max_order_price = 200, 1000
    min_lat, max_lat = 1, 10
    min_lon, max_lon = 1, 10

    # Fixed pickup coordinates

    # Generate orders
    for i in range(order_num):
        pickup_coordinates = [round(random.uniform(min_lat, max_lat), roundoff_digit), round(random.uniform(min_lon, max_lon), roundoff_digit)]
        order_id = f"ORD{i+1:03}"
        delivery_coordinates = [round(random.uniform(min_lat, max_lat), 4), round(random.uniform(min_lon, max_lon), 4)]
        orders.append({
            "ORDER_ID": order_id,
            "pickup_coordinates": pickup_coordinates,
            "delivery_coordinates": delivery_coordinates,
            "Order_value": round(random.uniform(min_order_price, max_order_price), 2),
            "order_volume": random.randint(1, 5),
            "OTD" : random.randint(30, 60),
            "Rider" : None,
        })

    # Generate riders
    for i in range(rider_num):
        rider_id = f"RID{i+1:03}"
        riders.append({
            "RIDER_ID": rider_id,
            "current_coordinates": [round(random.uniform(min_lat, max_lat), 4), round(random.uniform(min_lon, max_lon), 4)],
            "rider_capacity": 20,
            "CART":[],
            "route": [],
            "rider_order_status": [],
            "rider_path": [],
            "rider_order": [],
            "our_profit": 0
        })

    return orders, riders

def calculate_distance(coord1, coord2):
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

def calculate_delivery_time(pickup_coord, delivery_coord, rider_coord):
    print("calculate_delivery_time function called")
    print(pickup_coord)
    """
    Calculate the total delivery time including the time to reach the pickup location
    and the time from pickup to delivery location.
    """
    try:
        first_mile_time = calculate_distance(rider_coord, pickup_coord) / first_mile_speed * 60
        last_mile_time = calculate_distance(pickup_coord, delivery_coord) / last_mile_speed * 60
        return first_mile_time + last_mile_time
    except Exception as e:
        print(f"Error calculating delivery time: {e}")
        return 0

def total_profit(order, rider):
    """
    Calculate the total profit from delivering an order.
    """
    try:
        cost = (first_mile_cost * calculate_distance(rider["current_coordinates"], order["pickup_coordinates"]) +
                last_mile_cost * calculate_distance(order["pickup_coordinates"], order["delivery_coordinates"]))
        total_profit = order["Order_value"] * 0.08 - cost
        total_profit = round(total_profit, roundoff_digit)
        return total_profit
    except Exception as e:
        print(f"Error calculating profit: {e}")
        return 0

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

def generate_matrixs(orders_orig, riders_orig):
    print("generate_matrixs function called")
    """
    Generate profit, OTD, and distance matrices for orders and riders.
    """
    riders = copy.deepcopy(riders_orig)
    orders = copy.deepcopy(orders_orig)
    distance_matrix = []
    OTD_matrix = []
    profit_matrix = []
    time_duration_matrix = []
    
    try:
        for rider in riders:
            if len(rider["CART"]):
                print(f"Rider {rider['RIDER_ID']} has orders in the cart")
                cart_orders = rider["CART"]
                profit_row = []
                OTD_row = []
                distance_matrix_row = []
                time_duration_matrix_row = []
                rider_capacity = rider["rider_capacity"]
                
                logest_coordinate = get_longest_coordinate(rider["route"])
                
                distance = get_max_distance(rider)
                Duration = get_duration(distance)
                OTD = get_min_OTD(rider["CART"])
                profit = get_max_profit(rider["CART"],distance)
                print(f"Distance: {distance}, Duration: {Duration}, OTD: {OTD}, Profit: {profit}")
                
                for order in orders:
                    if(order["order_volume"] <= rider_capacity):
                        if( is_in_the_route(logest_coordinate, order)):
                            if (total_profit(order, rider) > -5):
                                 if(ALL_in_time(rider,order)):
                                     append_order(order, rider)
                                     OTD_row.append(get_min_OTD(rider["CART"]))
                                     profit_row.append(get_max_profit(rider["CART"],distance))
                                     distance_matrix_row.append(get_max_distance(rider))
                                     time_duration_matrix_row.append(get_duration(get_max_distance(rider)))
                                     
                profit_matrix.append(profit_row)
                OTD_matrix.append(OTD_row)
                distance_matrix.append(distance_matrix_row)
                time_duration_matrix.append(time_duration_matrix_row)
                continue
            profit_row = []
            OTD_row = []
            distance_matrix_row = []
            time_duration_matrix_row = []
            for order in orders:
                OTD_row.append(order["OTD"])
                profit_row.append(total_profit(order, rider))
                distance_matrix_row.append(calculate_distance(rider["current_coordinates"], order["pickup_coordinates"]))
                time_duration_matrix_row.append(0)
            profit_matrix.append(profit_row)
            OTD_matrix.append(OTD_row)
            distance_matrix.append(distance_matrix_row)
            time_duration_matrix.append(time_duration_matrix_row)
    except Exception as e:
        print(f"Error generating matrices: {e}")
    
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

def is_in_the_route(logest_coordinate, order2):
    print("is_in_the_route function called")
    """
    Check if the second order is within the route of the first order.
    """
    def is_within_ellipse(center, point, a, b):
        print("is_within_ellipse function called")
        """
        Check if a point is within an ellipse defined by center and axes lengths.
        """
        try:
            x, y = point
            h, k = center
            result = ((x - h) ** 2 / a ** 2) + ((y - k) ** 2 / b ** 2) <= 1
            return result
        except Exception as e:
            print(f"Error checking ellipse: {e}")
            return False
    
    try:
        o1x1, o1y1 = logest_coordinate[0]
        o1x2, o1y2 = logest_coordinate[1]
        o2x1, o2y1 = order2["pickup_coordinates"]
        
        o1x = (o1x1 + o1x2) / 2
        o1x=round(o1x, roundoff_digit)
        o1y = (o1y1 + o1y2) / 2
        o1y=round(o1y, roundoff_digit)
        major_axis_length = calculate_distance((o1x1, o1y1), (o1x2, o1y2)) / 2
        major_axis_length=round(major_axis_length, roundoff_digit)
        minor_axis_length = major_axis_length / 2
        minor_axis_length=round(minor_axis_length, roundoff_digit)
        
        
        flag1 = is_within_ellipse((o1x, o1y), (o2x1, o2y1), major_axis_length, minor_axis_length)
        print(f"Order 2 is within the route of Order 1: {flag1}")
        return flag1
    except Exception as e:
        print(f"Error checking route: {e}")
        return False

def append_order(order, rider):
    print("append_order function called")
    """
    Append an order to a rider's route and update the rider's status.
    """
    try:
        if rider["rider_capacity"] < order["order_volume"]:
            print(f"Error: Rider {rider['RIDER_ID']} doesn't have enough capacity for order {order['ORDER_ID']}")
            return rider
        rider["route"].append((order["pickup_coordinates"], order["delivery_coordinates"]))
        rider["rider_order"].append(order["ORDER_ID"])
        rider["CART"].append(order)
        rider["rider_capacity"] -= order.get("order_volume", 0)
        order["Rider"] = rider["RIDER_ID"]
        rider["our_profit"] += total_profit(order, rider)
        if len(rider["CART"]) > 1:
            rider["rider_path"],distance = optimize_route(rider)
            print(f"Rider {rider['RIDER_ID']} path: {rider['rider_path']}")
        print(f"Order {order['ORDER_ID']} appended to rider {rider['RIDER_ID']}")
    except KeyError as e:
        print(f"Error: Missing key {e} in rider or order dictionary")
    except Exception as e:
        print(f"An error occurred while appending order: {e}")

    return rider

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
        return max_value, row_index, column_index
    except Exception as e:
        print(f"Error finding max value in matrix: {e}")
        return None, None, None


# def optimize_route(rider):
#     print("optimize_route function called")
#     print(rider)
#     """
#     Optimize the route using the OR-Tools library.
#     Returns the sequence of coordinates to visit and the total distance.
#     """
#     print("Optimizing route...")
#     pickup_coords, delivery_coords = extract_coordinates([rider])
#     print(pickup_coords)
#     print(delivery_coords)
    
#     print("coordinates extracted")
#     try:
#         def euclidean_distance(xy1, xy2):
#             return np.linalg.norm(np.array(xy1) - np.array(xy2))
        
#         def create_data_model():
#             data = {}
#             all_coords = pickup_coords + delivery_coords
#             data['distance_matrix'] = [[euclidean_distance(i, j) for j in all_coords] for i in all_coords]
#             data['num_vehicles'] = 1
#             data['depot'] = 0
#             data['pickups_deliveries'] = []
#             for i, pickup in enumerate(pickup_coords):
#                 data['pickups_deliveries'].append((i, len(pickup_coords) + i))
#             return data, all_coords

#         data, all_coords = create_data_model()
#         manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),
#                                                  data['num_vehicles'],
#                                                  data['depot'])
#         routing = pywrapcp.RoutingModel(manager)
        
#         def distance_callback(from_index, to_index):
#             from_node = manager.IndexToNode(from_index)
#             to_node = manager.IndexToNode(to_index)
#             return int(data['distance_matrix'][from_node][to_node] * 1000)  # Convert to integer
        
#         transit_callback_index = routing.RegisterTransitCallback(distance_callback)
#         routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)
        
#         for pickup, delivery in data['pickups_deliveries']:
#             routing.AddPickupAndDelivery(manager.NodeToIndex(pickup), manager.NodeToIndex(delivery))
#             routing.solver().Add(routing.VehicleVar(manager.NodeToIndex(pickup)) == routing.VehicleVar(manager.NodeToIndex(delivery)))
        
#         search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        
#         search_parameters.first_solution_strategy = (
#             routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)
#         # print(".../")
#         # print(search_parameters)
#         # """
#         this line raising issue
#         # solution = routing.SolveWithParameters(search_parameters)
#         # """
#         # print(solution)
#         # print(".../")
#         if solution:
#             index = routing.Start(0)
#             route_coords = []
#             route_distance = 0
#             while not routing.IsEnd(index):
#                 node_index = manager.IndexToNode(index)
#                 route_coords.append(all_coords[node_index])
#                 previous_index = index
#                 index = solution.Value(routing.NextVar(index))
#                 route_distance += distance_callback(previous_index, index)
            
#             # Add the last point
#             node_index = manager.IndexToNode(index)
#             route_coords.append(all_coords[node_index])
            
#             # Convert distance back to float (it was multiplied by 1000 earlier)
#             route_distance = route_distance / 1000
            
#             print(f"Optimized route coordinates: {route_coords}")
#             print(f"Total distance: {route_distance}")
            
#             return route_coords, route_distance
#         else:
#             print('No solution found!')
#             return None, None

#     except Exception as e:
#         print(f"Error optimizing route: {e}")
#         return None, None

def optimize_route(rider):
    """ Now optimizeing the route using pyvrp library"""
    print("optimize_route function called")
    print(rider)
    pickup_coords, delivery_coords = extract_coordinates([rider])
    print(pickup_coords)
    print(delivery_coords)
    print("coordinates extracted")
    coordinates = []
    coordinates.append(rider["current_coordinates"])
    for i in range(len(pickup_coords)):
        coordinates.append(pickup_coords[i])
        coordinates.append(delivery_coords[i])
    print(coordinates)
    # Create distance matrix
    def get_distance_and_duration_matrix(coords):
        size = len(coords)
        matrix = np.zeros((size, size))
        for i in range(size):
            for j in range(size):
                if i != j:
                    matrix[i][j] = np.sqrt((coords[i][0] - coords[j][0])**2 + (coords[i][1] - coords[j][1])**2)
                    dist = matrix[i][j]
        return dist_matrix,duration_matrix
    
    distance_matrix = distance_matrix(coordinates)
    print(distance_matrix)
    
    
    
    
    
    
    
    # Create the model
    m = Model()
    # model = pyvrp.VehicleRoutingProblem(distance_matrix, num_vehicles=1, depot=0)
    
    # Define pickups and deliveries
    pickups_deliveries = [(1, 2), (3, 4)]
    # Add pickup and delivery constraints
    for pickup, delivery in pickups_deliveries:
        model.add_pickup_and_delivery(pickup, delivery)
        
    solution = model.solve()
    
    if solution:
        route = solution.routes[0]
        min_distance = solution.total_distance

        # Print the route
        route_coords = [coordinates[i] for i in route]
        print("Optimal Route Coordinates:")
        print(route_coords)

        print("Minimum Distance:")
        print(min_distance)
    else:
        print("No solution found.")

    


def Assignment(orders, riders, assigned_orders, unassigned_orders):
    print("Assignment function called")
    """
    Assigns orders to riders based on maximum profit and updates the matrices accordingly.

    Args:
    orders (list): List of order dictionaries.
    riders (list): List of rider dictionaries.
    assigned_orders (list): List to store assigned orders.
    unassigned_orders (list): List to store unassigned orders.
    """
    
    while len(orders) > 0:
        try:
            # Generate matrices for profit, OTD, and distance
            profit_matrix, OTD_matrix, distance_matrix, time_duration_matrix = generate_matrixs(orders, riders)
        
            # Print matrices
            print("Profit Matrix:")
            print_matrix(profit_matrix)
            print("OTD Matrix:")
            print_matrix(OTD_matrix)
            print("Distance Matrix:")
            print_matrix(distance_matrix)
            print("Time Duration Matrix:")
            print_matrix(time_duration_matrix)
        
            # Get the maximum profit and corresponding indices
            max_profit, rider_index, order_index = get_max_in_the_matrix(profit_matrix)
            print(f"Max Profit: {max_profit}, Rider Index: {rider_index}, Order Index: {order_index}")
            if max_profit <= -5:
                for order in orders:
                    unassigned_orders.append(order)
                print("There are no orders where the profit is less than -5 for all riders")
                return assigned_orders, unassigned_orders
            print(f"Max Profit: {max_profit}, Rider Index: {rider_index}, Order Index: {order_index}")
        
            # Check if indices are valid
            if rider_index != -1 and order_index != -1:
                print(f"Assigning order {orders[order_index]['ORDER_ID']} to rider {riders[rider_index]['RIDER_ID']}")
            
                # Append the order to the rider's route
                append_order(orders[order_index], riders[rider_index])

                # Add the assigned order to the assigned_orders list and remove it from the orders list
                assigned_orders.append(orders[order_index])
                orders.pop(order_index)
                        
                # Print the updated profit matrix
            else:
                print("No valid assignment found. Moving to next iteration.")
    
        except Exception as e:
            print(f"Error in assignment process: {e}")
            break
    print("All orders have been assigned.")
    print("Assigned Orders:")
    print(assigned_orders)
    print("Unassigned Orders:")
    print(unassigned_orders)
    return assigned_orders, unassigned_orders

# Example use case
orders, riders = generate_orders_and_riders(10, 3)
order_orig = copy.deepcopy(orders)
rider_orig = copy.deepcopy(riders)
assigned_orders,unassigned_orders= Assignment(orders, riders, assigned_orders, unassigned_orders)


print("Assigned Orders:")
print(len(assigned_orders))
print("Unassigned Orders:")
print(len(unassigned_orders))


# optimized_route, total_distance = optimize_route(riders[0])

