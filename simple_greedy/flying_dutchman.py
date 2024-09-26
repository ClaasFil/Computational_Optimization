from src.instance import Instance
import logging

def flying_dutchman(instance: Instance):

    # Idea of the algorithm:

    # Sort deliveries from first available time to last.

    # Then for each timestep t = 1,.....

    # Step 1: Assign the first of these sorted deliveries to the closest courier, then the second, etc. 
    # but only assign the delivery to the courier if they don't have to wait upon arrival, 
    # otherwise don't assign in this timestep yet,
    # and check capacity constraints in this assignment 
    # (don't exceed max stack capacity and max 4 deliveries total).
    
    # Step 2: If a courier has picked up a delivery and is idle, 
    # let them deliver the delivery in their stack with the nearest drop off location.

    # We do not guarantee a feasible solution,
    # 180min per route per courier might be violated.
    
    # Initialize algorithm parameters
    T = 10*sum(instance.travel_time[1][1:]) # upper bound on total time needed to deliver everything
    n = len(instance.couriers)
    m = len(instance.deliveries)
    available_couriers = [[courier.courier_id for courier in instance.couriers] for _ in range(T)]
    location_couriers = {courier.courier_id: courier.location for courier in instance.couriers}
    stack = {courier.courier_id: [] for courier in instance.couriers}
    stack_capacity = {courier.courier_id: 0 for courier in instance.couriers}
    n_deliveries = {courier.courier_id: 0 for courier in instance.couriers} # max 4
    # Sort deliveries from first available time to last
    # sorted_deliveries = sorted(instance.deliveries, key=lambda delivery.delivery_id: delivery.time_window_start)
    sorted_deliveries = sorted(instance.deliveries, key=lambda delivery: delivery.time_window_start)
    n_dropoff = 0

    # Execute the algorithm
    total_delivery_time = 0 # objective function value
    for t in range(T):

        # Step 1: Assign deliveries to the closest available courier that has enough capacity
        # if the delivery is ready by the time they would arrive, 
        # else don't assign in this timestep yet

        for i in range(len(available_couriers)):
            if i < len(sorted_deliveries):
                # Identify i'th delivery in sorted_deliveries
                # delivery = list(filter(lambda elem: elem.delivery_id == sorted_deliveries[i], instance.deliveries))[0]
                delivery = sorted_deliveries[i]
                # Identify closest available courier
                closest_courier_id = None
                closest_courier_distance = 10000
                for courier_id in available_couriers[t]:
                    travel_time = instance.travel_time[location_couriers[courier_id]][delivery.pickup_loc]
                    if travel_time < closest_courier_distance and stack_capacity[courier_id]+delivery.capacity <= 100 and n_deliveries[courier_id] < 4: #TODO CHANGE CAPACITY VAL
                        capacity_available = True if stack_capacity[courier_id]+delivery.capacity <= 100 else False
                        closest_courier_distance = travel_time
                        closest_courier_id = courier_id
                # Assign delivery to closest courier if they don't have to wait
                if closest_courier_distance > delivery.time_window_start - t - 1 and closest_courier_id is not None:
                    # Identify courier
                    courier = list(filter(lambda elem: elem.courier_id == closest_courier_id, instance.couriers))[0]
                    # Assign delivery to courier
                    courier.activities.append(delivery.delivery_id)
                    
                    # Update algorithm parameters:
                    # Courier is not available while it is traveling
                    for t_temp in range(t,t+closest_courier_distance+1):
                        available_couriers[t_temp].remove(courier.courier_id)
                    # Set courier location to pickup location
                    location_couriers[courier.courier_id] = delivery.pickup_loc
                    # Add delivery to courier stack
                    stack[courier.courier_id].append(delivery.delivery_id)
                    stack_capacity[courier.courier_id] += delivery.capacity
                    n_deliveries[courier_id] += 1
                    # Remove delivery from sorted_deliveries
                    sorted_deliveries.remove(delivery)

        # Step 2: let courier drop off closest of its stack if it is available
        for courier_id, stack_items in stack.items():
            if courier_id in available_couriers[t] and len(stack_items) > 0:
                # # Find first item in stack
                # delivery_id = stack_items[0] 
                # Identify closest dropoff # TODO can change to biggest capacity
                closest_delivery_id = None
                closest_delivery_distance = 10000
                for stack_item in stack_items:
                    # Identify delivery
                    delivery = list(filter(lambda elem: elem.delivery_id == stack_item, instance.deliveries))[0]
                    travel_time = instance.travel_time[location_couriers[courier_id]][delivery.dropoff_loc]
                    if travel_time < closest_delivery_distance:
                        closest_delivery_distance = travel_time
                        closest_delivery_id = stack_item
                delivery_id = closest_delivery_id

                # Identify courier
                courier = list(filter(lambda elem: elem.courier_id == courier_id, instance.couriers))[0]
                # Identify delivery
                delivery = list(filter(lambda elem: elem.delivery_id == delivery_id, instance.deliveries))[0]
                # Assign delivery to courier
                courier.activities.append(delivery.delivery_id)
                
                # Update algorithm parameters:
                # Courier is not available while it is traveling
                travel_time = instance.travel_time[location_couriers[courier_id]][delivery.dropoff_loc]
                for t_temp in range(t,t+travel_time+1): # TODO check if this is correct
                    available_couriers[t_temp].remove(courier.courier_id)
                # Set courier location to drop off location
                location_couriers[courier.courier_id] = delivery.dropoff_loc
                # Remove delivery from courier stack
                stack[courier.courier_id].remove(delivery.delivery_id)
                stack_capacity[courier.courier_id] -= delivery.capacity
                # Increase number of dropped off deliveries by 1
                n_dropoff += 1
        
        # Stopping condition 
        if n_dropoff == m:
            break
    
    # for courier in instance.couriers:
    #     print(courier.activities)
