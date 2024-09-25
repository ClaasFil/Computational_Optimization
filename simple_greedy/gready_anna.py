#from src import *
from src.instance import Instance
#def execute_greedy_algorithm(instance: Instance):
    # Sort pickups from first to latest available time

    #for t in range(sum(instance.travel_time)): #TODO change this max later
        #n = len(instance.couriers)

        #TO FIND AN INITIAL FEASIBLE SOLUTION
        #for c in instance.couriers:
            # Find nearest delivery (from first n) for each courier
            # Assign courier to delivery if t_start - t_travel <= 0 and record T[c]= t_(depot-pickup)+ t_(pickup-deliver)
        #Order in a crescent way the orders with respect to their pickup times 
            # (that have not already assigned)--> O*
        #Order couriers in a crescent way according to their times--> C*
        #Consider the first courier (c) of the list (C*):
            #for o in O*:
                #if quantity[o] < Capacity[c] --> assign o to c and calculate T
                #otherwise continue
        #Finally calculate the sum of all times (objective function value)

        #HOW TO IMPROVE THE QUALITY OF THE SOLUTION?
        # we can apply mutation and crossover and recalculate objective function value 

def sort_times_couriers(instance: Instance):
    sorted_orders_couriers = []
    for c in instance.couriers:
        list_time_orders = []
        for d in instance.deliveries:
            time_cd = abs(d.time_window_start - (instance.travel_time[c.location][d.pickup_loc] + instance.travel_time[d.pickup_loc][d.dropoff_loc]))
            list_time_orders.append([d.delivery_id,time_cd, d.capacity])
        sorted_list_time_orders = sorted(list_time_orders, key=lambda x: x[1])
    
        sorted_orders_couriers.append(sorted_list_time_orders)
    return sorted_orders_couriers


# Function to execute a greedy algorithm for the VRP
def execute_greedy_algorithm(instance: Instance):
    sorted_orders_couriers = sort_times_couriers(instance)

    # Dictionary to track which orders are assigned to which couriers
    courier_assignments = {courier.courier_id: [] for courier in instance.couriers}
    
    # Initialize total time (objective function value)
    total_time = 0
    residual_capacity = {}
    D = [d.delivery_id for d in instance.deliveries]
    c_indices = {c: c.courier_id - 1 for c in instance.couriers}
    check_order = {d: 0 for d in D}
    for c in instance.couriers:
        #courier_index = c.courier_id - 1
        residual_capacity[c.courier_id] = c.capacity
        for i in range(len(D)):
            delivery_id = D[i]     
            # Verifica se la capacità residua è sufficiente e se l'ordine non è già stato assegnato
            if (residual_capacity[c.courier_id] >= sorted_orders_couriers[c_indices[c]][i][2] and 
                check_order[delivery_id] == 0):
                
                # Assegna l'ordine al corriere
                courier_assignments[c.courier_id] = sorted_orders_couriers[c_indices[c]][i][0]
                total_time += sorted_orders_couriers[c.courier_id][i][1]
                
                # Sottrai la capacità utilizzata
                residual_capacity[c.courier_id] -= sorted_orders_couriers[c_indices[c]][i][2]
                
                # Segna l'ordine come assegnato
                check_order[delivery_id] = 1
            else:
                continue

    
    return courier_assignments, total_time