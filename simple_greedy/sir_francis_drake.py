from src.instance import Instance
from src.delivery import Delivery
from src.courier import Courier
import logging
from itertools import cycle
# max 180 min per route
# max 4 deliveries per courier

def sir_francis_drake(instance: Instance):
    """
    Optimized heuristic that assigns deliveries to the best courier based on travel time, time window constraints,
    and capacity limits.
    """
    # Sort deliveries by time window start
    sorted_deliveries = sorted(instance.deliveries, key=lambda delivery: delivery.time_window_start)

    # Iterate through all deliveries
    for delivery in sorted_deliveries:
        best_courier = None
        min_cost = float('inf')  # Store the minimum cost for insertion

        # Find the best courier based on the combination of travel time, time windows, and capacity
        for courier in instance.couriers:
            if rider_is_feasible(delivery, courier, instance):
                insertion_cost = calculate_insertion_cost(delivery, courier, instance)
                
                if insertion_cost < min_cost:
                    min_cost = insertion_cost
                    best_courier = courier

        # If a best courier is found, assign the delivery to that courier
        if best_courier:
            update_courier(best_courier, delivery, instance)
        else:
            logging.debug(f"Delivery {delivery.delivery_id} could not be assigned to any courier")


def calculate_insertion_cost(delivery: Delivery, courier: Courier, instance: Instance):
    """
    Calculate a cost metric for inserting the delivery into the courier's route based on:
    1. Travel time to the pickup location.
    2. How close the current time is to the delivery's time window start.
    3. Capacity left on the courier.
    4. Remaining available time for the courier.
    """
    delivery_time = instance.travel_time[delivery.pickup_loc][delivery.dropoff_loc]
    time_to_pickup = instance.travel_time[courier.location][delivery.pickup_loc]

    # Calculate penalties for nearing constraints
    capacity_penalty = max(0, 4 - courier.delivery_count) * 10  # Add a penalty if nearing max deliveries
    time_penalty = max(0, 180 - courier.time_consumed) / 10  # Add a penalty if nearing max time

    # Combine all factors into a single cost metric
    insertion_cost = time_to_pickup + delivery_time + capacity_penalty + time_penalty
    
    # Include time window penalty (courier should ideally arrive before the delivery's time window)
    if courier.time_consumed + time_to_pickup > delivery.time_window_start:
        time_window_penalty = (courier.time_consumed + time_to_pickup - delivery.time_window_start) * 5
        insertion_cost += time_window_penalty
    
    return insertion_cost


def rider_is_feasible(delivery: Delivery, courier: Courier, instance: Instance):
    delivery_time = instance.travel_time[delivery.pickup_loc][delivery.dropoff_loc]
    time_to_pickup = instance.travel_time[courier.location][delivery.pickup_loc]

    # Check if the courier can take the delivery without violating constraints
    if courier.time_consumed + delivery_time + time_to_pickup <= 180:  # Max travel time per route
        if courier.capacity >= delivery.capacity:  # Courier must have capacity for the delivery
            if courier.delivery_count < 4:  # Max deliveries per courier
                return True
    return False


def update_courier(courier: Courier, delivery: Delivery, instance: Instance):
    courier.delivery_count += 1

    # Update time consumed by the courier
    delivery_time = instance.travel_time[delivery.pickup_loc][delivery.dropoff_loc]
    time_to_pickup = instance.travel_time[courier.location][delivery.pickup_loc]
    courier.time_consumed += (delivery_time + time_to_pickup)

    # Update the courier's activities and location
    courier.activities.append(delivery.delivery_id)  # Add pickup
    courier.activities.append(delivery.delivery_id)  # Add dropoff

    # Update the courier's location to the dropoff location
    courier.location = delivery.dropoff_loc