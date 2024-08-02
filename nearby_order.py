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

def get_longest_coordinate(rider):
    print("get_longest_coordinate function called")
    max_distance = 0
    longest_coordinate = []
    print(f"rider = {rider}")
    """
    Get the longest coordinate from a list of coordinates.
    """
    # try:
    route = rider["route"]
    print(f"route = {route}")
    longest_coordinate.append(route[0])
    longest_coordinate.append(route[-2])
    print("here.....",longest_coordinate)
    return longest_coordinate


def is_in_the_route(rider, order2, shape='ellipse', major_axis_length=5, minor_axis_length=5):
    
    """
    Check if the second order is within the route of the first order.
    
    Parameters:
    - rider: dict containing rider route information.
    - order2: dict containing order2 coordinates.
    - shape: 'ellipse' or 'circle', determines the shape used for checking.
    - major_axis_length: length of the major axis (only for ellipse).
    - minor_axis_length: length of the minor axis (only for ellipse).
    """

    def is_within_shape(center, point, major_axis, minor_axis):
        """
        Check if a point is within an ellipse or circle.
        """
        try:
            x, y = point
            h, k = center

            if shape == 'ellipse':
                # Ellipse equation
                result = ((x - h) ** 2 / (major_axis / 2) ** 2) + ((y - k) ** 2 / (minor_axis / 2) ** 2) <= 1
            elif shape == 'circle':
                # Circle equation
                result = ((x - h) ** 2 + (y - k) ** 2) <= (major_axis / 2) ** 2
            else:
                raise ValueError("Invalid shape type. Use 'ellipse' or 'circle'.")
            
            return result
        except Exception as e:
            print(f"Error checking shape: {e}")
            return False

    # try:
    if len(rider["CART"]) == 0:
        print("Rider's cart is empty.")
        return True
    else:
        print("is_in_the_route function called")

        logest_coordinate = get_longest_coordinate(rider)
        print(f"Rider Path longest coordinate: {logest_coordinate}")
        
        o1x1, o1y1 = logest_coordinate[0]
        o1x2, o1y2 = logest_coordinate[1]
        o2x1, o2y1 = order2["pickup_coordinates"]
        
        o1x = (o1x1 + o1x2) / 2
        o1y = (o1y1 + o1y2) / 2

        if shape == 'ellipse':
            if major_axis_length is None or minor_axis_length is None:
                raise ValueError("For ellipse, both major_axis_length and minor_axis_length must be provided.")
        elif shape == 'circle':
            if major_axis_length is None:
                raise ValueError("For circle, major_axis_length (which is the diameter) must be provided.")
            minor_axis_length = major_axis_length  # For circle, minor_axis_length is the same as major_axis_length
        
        major_axis_length = round(major_axis_length, 2)
        minor_axis_length = round(minor_axis_length, 2)
        
        flag1 = is_within_shape((o1x, o1y), (o2x1, o2y1), major_axis_length, minor_axis_length)
        print(f"{order2['ORDER_ID']} is within the route of {rider['RIDER_ID']} : {flag1}")
        
        return flag1
    # except Exception as e:
    #     print(f"Error checking route: {e}")
    return False
