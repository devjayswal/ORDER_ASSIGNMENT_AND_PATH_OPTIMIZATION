import matplotlib.pyplot as plt

# Order data
orders = [
    {
        "ORDER_ID": "ORD002",
        "pickup_coordinates": [7.2347, 10.7418],
        "delivery_coordinates": [6.7634, 12.4487]
    },
    {
        "ORDER_ID": "ORD004",
        "pickup_coordinates": [7.2347, 10.7418],
        "delivery_coordinates": [7.7491, 9.5289]
    },
    {
        "ORDER_ID": "ORD001",
        "pickup_coordinates": [7.2347, 10.7418],
        "delivery_coordinates": [2.6792, 9.5842]
    },
    {
        "ORDER_ID": "ORD002",
        "pickup_coordinates": [7.2347, 10.7418],
        "delivery_coordinates": [12.6946, 9.0711]
    },
    {
        "ORDER_ID": "ORD003",
        "pickup_coordinates": [7.2347, 10.7418],
        "delivery_coordinates": [14.3056, 9.7244]
    },
    {
        "ORDER_ID": "ORD003",
        "pickup_coordinates": [7.2347, 10.7418],
        "delivery_coordinates": [11.144, 6.5248]
    },
    {
        "ORDER_ID": "ORD005",
        "pickup_coordinates": [7.2347, 10.7418],
        "delivery_coordinates": [12.5127, 5.157]
    }
]

# Separate pickup and delivery coordinates
pickup_coords = [order["pickup_coordinates"] for order in orders]
delivery_coords = [order["delivery_coordinates"] for order in orders]

# Route data (example)
route = [
    [5.7881, 13.3155],
    [7.2347, 10.7418],
    [7.7491, 9.5289],
    [12.6946, 9.0711],
    [14.3056, 9.7244],
    [12.5127, 5.157],
    [11.144, 6.5248],
    [2.6792, 9.5842],
    [6.7634, 12.4487],
    [5.7881, 13.3155]
]

# Separate route into latitude and longitude
route_lats, route_longs = zip(*route)

# Plotting
plt.figure(figsize=(12, 8))

# Plot route
plt.plot(route_lats, route_longs, marker='o', linestyle='-', color='b', label="Route Path")

# Plot pickup and delivery locations
for i, order in enumerate(orders):
    pickup_lat, pickup_long = order["pickup_coordinates"]
    delivery_lat, delivery_long = order["delivery_coordinates"]

    # Plot pickup location
    plt.plot(pickup_lat, pickup_long, marker='^', color='green', markersize=10)
    plt.text(pickup_lat, pickup_long, f'P{i+1}', fontsize=12, ha='right', color='green')

    # Plot delivery location
    plt.plot(delivery_lat, delivery_long, marker='s', color='red', markersize=10)
    plt.text(delivery_lat, delivery_long, f'D{i+1}', fontsize=12, ha='right', color='red')

plt.title("Delivery Routes with Pickup and Delivery Locations")
plt.xlabel("Latitude")
plt.ylabel("Longitude")
plt.grid(True)
plt.legend()
plt.show()
