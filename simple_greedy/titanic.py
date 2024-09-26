from src.instance import Instance
from src.delivery import Delivery
from src.courier import Courier
import logging
from itertools import cycle
# max 180 min per route
# max 4 deliveries per courier

def titanic(instance: Instance):

    # Idea of the algorithm:
    # Sort deliveries from first available time to last.
    # Assign the first of these sorted deliveries to first courier, second to second, etc., 
    # and keep louping over couriers until all deliveries are assigned.
    # We do not stack, so keeping track of capacities is not necessary.
    # We do not guarantee a feasible solution,
    # 180min per route and max4 deliveries per courier might be violated.
    


    n = len(instance.couriers)
    m = len(instance.deliveries)

    # Sort deliveries from first available time to last
    sorted_deliveries = sorted(instance.deliveries, key=lambda delivery: delivery.time_window_start)

    courier_dict = {courier.courier_id: courier for courier in instance.couriers}
    
    # Get the number of couriers
    n = len(courier_dict)

    # Use an itertools.cycle to cycle through couriers in a round-robin fashion
    courier_cycle = cycle(courier_dict.values())

    for delivery in sorted_deliveries:
        assigned = False  # Flag to track if delivery was assigned to any courier in this iteration
        
        # Check all couriers to see if anyone can take the delivery within max_travel_time
        for _ in range(n):  # Loop through the couriers in a round-robin cycle
            courier = next(courier_cycle)  # Get the next courier in the cycle
            
            
            
            if rider_is_feasible(delivery, courier, instance):
                # Assign the delivery to the courier
                # Update the courier's attributes
                courier.delivery_count += 1

                #update the time consumed by the courier
                delivery_time = instance.travel_time[delivery.pickup_loc][delivery.dropoff_loc]
                time_to_pickup = instance.travel_time[courier.location][delivery.pickup_loc]
                courier.time_consumed += (delivery_time + time_to_pickup)

                # Update the courier's activities and location
                courier.activities.append(delivery.delivery_id)  # Add pickup
                courier.activities.append(delivery.delivery_id)  # Add dropoff

                # Update the courier's location
                courier.location = delivery.dropoff_loc  # Update courier's location to dropoff location

                # Mark the delivery as assigned
                assigned = True  # Mark delivery as assigned
                break  # Exit the courier loop once the delivery is assigned
            #else:
            #    logging.debug(f"Courier {courier.courier_id} cannot take delivery {delivery.delivery_id}")
        
        # If no courier could take this delivery, break out of the loop
        if not assigned:
            logging.debug(f"Delivery {delivery.delivery_id} could not be assigned to any courier")
            break


def rider_is_feasible(delivery: Delivery, courier: Courier, instance: Instance):
    delivery_time = instance.travel_time[delivery.pickup_loc][delivery.dropoff_loc]
    time_to_pickup = instance.travel_time[courier.location][delivery.pickup_loc]
    if courier.time_consumed + delivery_time + time_to_pickup < instance.max_travel_time:
        if courier.capacity >= delivery.capacity:
            if courier.delivery_count < 4:
                return True
    return False