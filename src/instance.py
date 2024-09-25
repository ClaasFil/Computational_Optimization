from .delivery import Delivery
from .courier import Courier
from .arc import Arc



import numpy as np
from typing import List
import logging
import xpress as xp


# Define the Courier class
class Instance:
    def __init__(self, instance_name: str, couriers: List[Courier], deliveries: List[Delivery], travel_time):
        # Input parameters

        self.instance_name = instance_name
        # K in Doc
        self.couriers = couriers
        # O in Doc
        self.deliveries = deliveries
        self.travel_time = np.array(travel_time)

        # determent parameters

        # Max capacity of all couriers
        # Q_max in Doc
        self.max_capacity = self.get_max_capacity()
        logging.debug(f"Max capacity of all couriers: {self.max_capacity}")

        #Starting point of riders
        # S in Doc
        self.rider_starting_points = self.get_rider_starting_points()
        logging.debug(f"Found {len(self.rider_starting_points)} rider starting points")

        # Pickup locations
        # P in Doc
        self.picup_locations = self.get_pickup_locations()
        logging.debug(f"Found {len(self.picup_locations)} pickup locations")

        # Dorpoff locations
        # D in Doc
        self.dropoff_locations = self.get_dropoff_locations()
        logging.debug(f"Found {len(self.dropoff_locations)} dropoff locations")

        # all locations/ vertices
        # V in Doc
        self.all_locations = self.picup_locations.union(self.dropoff_locations, self.rider_starting_points)
        logging.debug(f"Found {len(self.all_locations)} locations")
        


        # Creat arcs
        logging.debug(f"Creating arcs")

        
        # A1 in Doc
        logging.debug(f"Creating arcs for A1")
        self.A1 = set()
        self.A1 = self.create_arcs_A1(self.rider_starting_points, self.picup_locations)

        #A2 in Doc
        logging.debug(f"Creating arcs for A2")
        self.A2 = set()
        self.A2 = self.create_arcs_A2(self.picup_locations, self.dropoff_locations)


        #A3 in Doc
        logging.debug(f"Creating arcs for A3")
        self.A3 = set()
        self.A3 = self.create_arcs_A3(self.dropoff_locations, self.rider_starting_points)

        #A4 in Doc
        logging.debug(f"Creating arcs for A4")
        self.A4 = set()
        self.A4 = self.create_arcs_A4(self.rider_starting_points)

        #A5 no Doc
        logging.debug(f"Creating arcs for A5")
        self.A5 = set()
        self.A5 = self.create_arcs_A5(self.picup_locations, self.picup_locations)

        #A6 no Doc
        logging.debug(f"Creating arcs for A6")
        self.A6 = set()
        self.A6 = self.create_arcs_A5(self.dropoff_locations, self.dropoff_locations)

    def model_instance(self):
        p = xp.problem(self.instance_name)

        U = len(self.rider_starting_points)
        V = len(self.picup_locations) + len(self.dropoff_locations)
        K = len(self.picup_locations) + len(self.dropoff_locations)
        x_uvk = xp.var(vartype=xp.binary, shape=(U, V, K), name='x_uvk')


        t_v = xp.add_variables( len(self.picup_locations) + len(self.dropoff_locations) + len(self.rider_starting_points), vartype=xp.continuous)
        
        pass



    def create_arcs_A1(self, starting_set, ending_set):
        # pointing one direction from depot to pickup point
        arcs = set()
        for each_start in starting_set:
            for each_end in ending_set:
                #logging.debug(f"Creating arc from {each_start} to {each_end}")
                #logging.debug(f"Travel time: {self.travel_time[each_start][each_end]}")
                arcs.add(Arc(each_start, each_end, int(self.travel_time[each_start][each_end])))
                

        logging.debug(f"Created {len(arcs)} arcs")
        if len(arcs) != len(starting_set) * len(ending_set):
            logging.error("Number of arcs created is not equal to the number of rider starting points times the number of pickup locations with loops")

        return arcs


    def create_arcs_A2(self, starting_set, ending_set):
        # pointing one direction from pick up point to drop off 
        # both directions 
        arcs = set()
        for each_start in starting_set:
            for each_end in ending_set:
                arcs.add(Arc(each_start, each_end, int(self.travel_time[each_start][each_end])))
                arcs.add(Arc(each_end, each_start, int(self.travel_time[each_start][each_end])))


                

        logging.debug(f"Created {len(arcs)} arcs")
        if len(arcs) != 2* (len(starting_set) * len(ending_set)) :
            logging.error("A2 arcs not setup properly sould be 2 times the number of pickup locations times the number of dropoff locations ")
        return arcs

    def create_arcs_A3(self, starting_set, ending_set):
        # pointing one direction from drop off to depot 
        # one directions 
        arcs = set()
        for each_start in starting_set:
            for each_end in ending_set:
                arcs.add(Arc(each_start, each_end, int(self.travel_time[each_start][each_end])))

                

        logging.debug(f"Created {len(arcs)} arcs")
        if len(arcs) !=  (len(starting_set) * len(ending_set)) :
            logging.error("A3 arcs not setup properly sould be the number of dropoff locations times the number of rider starting points")

        return arcs
    

    def create_arcs_A4(self, starting_set):
        # pointing one direction from drop off to depot 
        # one directions 
        arcs = set()
        for each_start in starting_set:
            arcs.add(Arc(each_start, each_start, int(self.travel_time[each_start][each_start])))

                

        logging.debug(f"Created {len(arcs)} arcs")
        if len(arcs) !=  len(starting_set)  :
            logging.error("A4 arcs not setup properly sould be the number of rider starting points")

        return arcs

    def create_arcs_A5(self, starting_set, ending_set):
        # pointing one direction from pickup off to other pickup off 
        # both directions 
        # no loop
        arcs = set()
        for each_start in starting_set:
            for each_end in ending_set:
                if each_start != each_end:
                    arcs.add(Arc(each_start, each_end, int(self.travel_time[each_start][each_end])))
                    arcs.add(Arc(each_end, each_start, int(self.travel_time[each_start][each_end])))

        
                

        logging.debug(f"Created {len(arcs)} arcs")
        if len(arcs) !=  2*(len(starting_set) * len(ending_set) - len(starting_set))  :
            logging.error(f"arcs not setup properly. sould be {2*(len(starting_set) * len(ending_set) - len(starting_set))} but created {len(arcs)}")

        return arcs



    def __repr__(self):
        return (f"Instance(Name={self.instance_name}, Couriers={len(self.couriers)}, "
                f"Deliveries={len(self.deliveries)}, TravelTimeMatrix={len(self.travel_time)}x{len(self.travel_time[0])}, "
                f"VarType={self.vartype})")
    

    def get_max_capacity(self):
        # Q_max in Doc
        # Find the maximum capacity among couriers
        if len(self.couriers) == 0:
            logging.error("Trying to get max capacity from an empty list of couriers")
            return 0  # Return 0 if no couriers are available
        return max(courier.capacity for courier in self.couriers)
    
    def get_pickup_locations(self):
        # Use a set to get unique pickup locations
        return set(delivery.pickup_loc for delivery in self.deliveries)
    

    def get_rider_starting_points(self):
        # Use a set to get unique pickup locations
        return set(courier.location for courier in self.couriers)
    
    def get_dropoff_locations(self):
        # Use a set to get unique dropoff locations
        return set(delivery.dropoff_loc for delivery in self.deliveries)