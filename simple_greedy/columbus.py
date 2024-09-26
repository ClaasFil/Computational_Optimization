from src.instance import Instance
from src.delivery import Delivery
from src.courier import Courier
import logging

def columbus(instance: Instance):
    """
    Fast heuristic that assigns deliveries to couriers based on the earliest possible delivery time,
    considering capacity and time constraints, and appends deliveries at the end of the courier's route.
    """
    # Initialize couriers
    for courier in instance.couriers:
        courier.route = []
        courier.time_consumed = 0
        courier.delivery_count = 0
        courier.capacity_used = 0
        # Assuming couriers have an initial location attribute
        courier.location = courier.location

    # Sort deliveries by earliest time window start
    unassigned_deliveries = sorted(instance.deliveries, key=lambda d: d.time_window_start)

    # While there are unassigned deliveries
    while unassigned_deliveries:
        best_assignment = None
        earliest_delivery_time = float('inf')

        # For each unassigned delivery
        for delivery in unassigned_deliveries:
            # For each courier
            for courier in instance.couriers:
                if courier.delivery_count >= 4:
                    continue  # Courier cannot take more deliveries

                # Calculate the earliest time the courier can pick up the delivery
                time_to_pickup = instance.travel_time[courier.location][delivery.pickup_loc]
                arrival_at_pickup = courier.time_consumed + time_to_pickup

                # If arrival is before time window start, courier must wait
                if arrival_at_pickup < delivery.time_window_start:
                    arrival_at_pickup = delivery.time_window_start

                # Calculate time to deliver
                pickup_to_dropoff = instance.travel_time[delivery.pickup_loc][delivery.dropoff_loc]
                arrival_at_dropoff = arrival_at_pickup + pickup_to_dropoff

                # Total time increase for the courier
                total_time_increase = (arrival_at_dropoff - courier.time_consumed)

                # Check if adding this delivery would exceed courier's total route time
                if courier.time_consumed + total_time_increase > 180:
                    continue  # Exceeds maximum route time

                # Check if courier's capacity is sufficient
                if courier.capacity_used + delivery.capacity > courier.capacity:
                    continue  # Exceeds capacity

                # This assignment is feasible
                if arrival_at_dropoff < earliest_delivery_time:
                    earliest_delivery_time = arrival_at_dropoff
                    best_assignment = {
                        'delivery': delivery,
                        'courier': courier,
                        'arrival_at_pickup': arrival_at_pickup,
                        'arrival_at_dropoff': arrival_at_dropoff,
                        'time_to_pickup': time_to_pickup,
                        'pickup_to_dropoff': pickup_to_dropoff,
                        'total_time_increase': total_time_increase
                    }

        if best_assignment:
            # Assign the delivery to the courier
            delivery = best_assignment['delivery']
            courier = best_assignment['courier']

            # Update courier's route
            courier.route.append({
                'delivery_id': delivery.delivery_id,
                'pickup_loc': delivery.pickup_loc,
                'dropoff_loc': delivery.dropoff_loc,
                'arrival_at_pickup': best_assignment['arrival_at_pickup'],
                'arrival_at_dropoff': best_assignment['arrival_at_dropoff']
            })

            # Update courier's attributes
            courier.time_consumed += best_assignment['total_time_increase']
            courier.location = delivery.dropoff_loc
            courier.delivery_count += 1
            courier.capacity_used += delivery.capacity

            # Remove delivery from unassigned deliveries
            unassigned_deliveries.remove(delivery)
        else:
            # No feasible assignment found
            logging.debug("No feasible assignment found for remaining deliveries.")
            break  # Exit the loop

    # After all assignments, update courier activities
    for courier in instance.couriers:
        courier.activities = []
        for stop in courier.route:
            # Add pickup and dropoff activities
            courier.activities.append(stop['delivery_id'])  # Pickup
            courier.activities.append(stop['delivery_id'])  # Dropoff
