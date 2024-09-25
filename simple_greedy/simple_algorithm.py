from src.instance import Instance
import logging
# max 180 min per route
# max 4 deliveries per courier

def execute_simple_algorithm(instance: Instance):

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

    # Assign deliveries to drivers
    courier_id = 1
    for delivery in sorted_deliveries:
        # identify next delivery for our courier
        courier = list(filter(lambda elem: elem.courier_id == courier_id, instance.couriers))[0]
        # add pickup to acitivity list of courier
        courier.activities.append(delivery.delivery_id)
        # add drop off to activity list of courier
        courier.activities.append(delivery.delivery_id)
        courier_id += 1
        if courier_id > n:
            courier_id = 1
    for courier in instance.couriers:
        print(courier.activities)

    # DO NOT NEED TO RUN THE CODE BELOW FOR FEASIBILITY CHECKER 
    # just for checking 180min constraint and max4 deliveries constraint
    # and finding interpretable solution and objective function value

    # 180 min per route might be violated, it will indicate that
    # It will say that the solution is infeasible if there are more than 4 deliveries per courier

    # Assign deliveries to drivers
    assignments = {courier_id: [] for courier_id in range(1,n+1)} # dict {courier: list[deliveries]}
    courier_id = 1
    for delivery in sorted_deliveries:
        assignments[courier_id].append(delivery.delivery_id)
        courier_id += 1
        if courier_id > n:
            courier_id = 1

    # Check max. 4 deliveries per courier constraint
    for courier_id, delivery_lst in assignments.items():
        if len(delivery_lst) > 4:
            logging.error("Oops! Courier" + str(courier.courier_id) + "has to deliver more than 4 deliveries")
            raise Exception("So this is not a feasible solution.")

    # Find the solution provided by this assignment:
    # The total delivery time (objective funciton value) and the list of activities for each courier
    total_delivery_time = 0 # objective function value
    for courier in instance.couriers:
        total_t = 0
        courier_loc = courier.location
        for delivery_id in assignments[courier.courier_id]:
            # identify next delivery for our courier
            delivery = list(filter(lambda elem: elem.delivery_id == delivery_id, instance.deliveries))[0]
            # calculate travel time from couriers current location to pickup location
            total_t += max(total_t + instance.travel_time[courier_loc][delivery.pickup_loc], delivery.time_window_start)
            courier.activities.append(delivery.delivery_id)
            # caclulate travel time from pickup to delivery locatiion
            total_t += instance.travel_time[delivery.pickup_loc][delivery.dropoff_loc]
            courier.activities.append(delivery.delivery_id)
            # add this dropoff time to the total delivery time
            total_delivery_time += total_t
            # set current courier location to dropoff location
            courier_loc = delivery.dropoff_loc
        # Check 180min constraint
        if total_t > 180:
            logging.error("Oops! Route of driver" + str(courier.courier_id) + "is longer than 180 minutes")
            raise Exception("So this is not a feasible solution.")
        # # get delivery driver home
        # total_t += instance.travel_time[delivery.dropoff_loc][courier.location]

    return 0