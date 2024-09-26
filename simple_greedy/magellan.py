from src.instance import Instance
from src.delivery import Delivery
from src.courier import Courier
import logging
from itertools import cycle
# max 180 min per route
# max 4 deliveries per courier

def magellan(instance: Instance):
    """
    Heuristic that assigns deliveries to the closest available courier based on their current location.
    """

    n = len(instance.couriers)
    m = len(instance.deliveries)

    # Sort deliveries from first available time to last
    sorted_deliveries = sorted(instance.deliveries, key=lambda delivery: delivery.time_window_start)

    # Loop through each delivery and assign it to the closest courier
    for delivery in sorted_deliveries:
        closest_courier = None
        min_travel_time = float('inf')
        
        # Find the closest courier to the delivery's pickup location
        for courier in instance.couriers:
            time_to_pickup = instance.travel_time[courier.location][delivery.pickup_loc]
            
            # Check if this courier can take the delivery
            if rider_is_feasible(delivery, courier, instance):
                # Find the courier with the minimum travel time to the pickup location
                if time_to_pickup < min_travel_time:
                    min_travel_time = time_to_pickup
                    closest_courier = courier
        
        # Assign the delivery to the closest feasible courier
        if closest_courier:
            update_courier(closest_courier, delivery, instance)
        else:
            logging.debug(f"Delivery {delivery.delivery_id} could not be assigned to any courier")


def rider_is_feasible(delivery: Delivery, courier: Courier, instance: Instance):
    delivery_time = instance.travel_time[delivery.pickup_loc][delivery.dropoff_loc]
    time_to_pickup = instance.travel_time[courier.location][delivery.pickup_loc]
    # Check if the courier has enough capacity, hasn't exceeded the travel time limit, and can take more deliveries
    if courier.time_consumed + delivery_time + time_to_pickup < instance.max_travel_time:
        if courier.capacity >= delivery.capacity:
            if courier.delivery_count < 4:
                return True
    return False


def update_courier(courier: Courier, delivery: Delivery, instance: Instance):
    courier.delivery_count += 1

    # Update the time consumed by the courier
    delivery_time = instance.travel_time[delivery.pickup_loc][delivery.dropoff_loc]
    time_to_pickup = instance.travel_time[courier.location][delivery.pickup_loc]
    courier.time_consumed += (delivery_time + time_to_pickup)

    # Update the courier's activities and location
    courier.activities.append(delivery.delivery_id)  # Add pickup
    courier.activities.append(delivery.delivery_id)  # Add dropoff

    # Update the courier's location to the dropoff location
    courier.location = delivery.dropoff_loc
