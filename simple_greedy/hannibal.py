from src.instance import Instance
from src.delivery import Delivery
from src.courier import Courier
import logging

def hannibal(instance: Instance):
    """
    Heuristic that assigns deliveries to couriers based on the minimal time difference between
    the courier's travel time to complete the delivery and the delivery's time window start.
    """

    # Initialize couriers
    for courier in instance.couriers:
        courier.route = []
        courier.time_consumed = 0
        courier.delivery_count = 0
        courier.capacity_used = 0
        # Couriers start at their initial location
        courier.location = courier.location

    # Keep track of unassigned deliveries
    unassigned_deliveries = set(instance.deliveries)

    # For each courier, compute a sorted list of deliveries based on time_cd
    courier_delivery_lists = {}
    for courier in instance.couriers:
        delivery_list = []
        for delivery in unassigned_deliveries:
            # Compute time_cd: absolute difference between delivery's time window start
            # and total travel time from courier's location to pickup and then to dropoff
            time_to_pickup = instance.travel_time[courier.location][delivery.pickup_loc]
            time_pickup_to_dropoff = instance.travel_time[delivery.pickup_loc][delivery.dropoff_loc]
            total_travel_time = time_to_pickup + time_pickup_to_dropoff
            time_cd = abs(delivery.time_window_start - total_travel_time)
            delivery_list.append((delivery, time_cd))
        # Sort the delivery list for this courier
        sorted_delivery_list = sorted(delivery_list, key=lambda x: x[1])
        courier_delivery_lists[courier] = sorted_delivery_list

    # For each courier, attempt to assign deliveries from their sorted list
    for courier in instance.couriers:
        deliveries_assigned = 0
        while deliveries_assigned < 4 and courier.time_consumed < 180:
            # Get the next delivery from the courier's sorted list
            if not courier_delivery_lists[courier]:
                break  # No more deliveries to assign
            delivery, time_cd = courier_delivery_lists[courier].pop(0)
            if delivery not in unassigned_deliveries:
                continue  # Delivery has already been assigned

            # Check if the courier can feasibly deliver this order
            time_to_pickup = instance.travel_time[courier.location][delivery.pickup_loc]
            arrival_at_pickup = courier.time_consumed + time_to_pickup
            # Courier must arrive at or after the delivery's time_window_start
            if arrival_at_pickup < delivery.time_window_start:
                arrival_at_pickup = delivery.time_window_start

            # Calculate time to dropoff
            pickup_to_dropoff = instance.travel_time[delivery.pickup_loc][delivery.dropoff_loc]
            arrival_at_dropoff = arrival_at_pickup + pickup_to_dropoff

            # Total time increase for the courier
            total_time_increase = arrival_at_dropoff - courier.time_consumed

            # Check if adding this delivery would exceed the courier's total route time
            if courier.time_consumed + total_time_increase > 180:
                continue  # Exceeds maximum route time

            # Check if courier's capacity is sufficient
            if courier.capacity_used + delivery.capacity > courier.capacity:
                continue  # Exceeds capacity

            # Assign the delivery to the courier
            courier.route.append({
                'delivery_id': delivery.delivery_id,
                'pickup_loc': delivery.pickup_loc,
                'dropoff_loc': delivery.dropoff_loc,
                'arrival_at_pickup': arrival_at_pickup,
                'arrival_at_dropoff': arrival_at_dropoff
            })

            # Update courier's attributes
            courier.time_consumed += total_time_increase
            courier.location = delivery.dropoff_loc
            courier.delivery_count += 1
            courier.capacity_used += delivery.capacity

            # Mark the delivery as assigned
            unassigned_deliveries.remove(delivery)

            deliveries_assigned += 1

        # After assignments, update courier activities
        courier.activities = []
        for stop in courier.route:
            # Add pickup and dropoff activities
            courier.activities.append(stop['delivery_id'])  # Pickup
            courier.activities.append(stop['delivery_id'])  # Dropoff

    # Log unassigned deliveries
    if unassigned_deliveries:
        logging.debug(f"The following deliveries could not be assigned: {[d.delivery_id for d in unassigned_deliveries]}")
