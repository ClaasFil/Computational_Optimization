from src.delivery import Delivery
from src.courier import Courier
from src.arc import Arc
import numpy as np
from typing import List
import logging

# Define the Courier class
class Instance:
    def __init__(self, instance_name: str, couriers: List[Courier], deliveries: List[Delivery], travel_time):
        # Input variables

        self.instance_name = instance_name
        # K in Doc
        self.couriers = couriers
        # O in Doc
        self.deliveries = deliveries
        self.travel_time = travel_time
        self.max_travel_time = 180


        self.max_capacity = self.get_max_capacity()

        self.rider_starting_points = self.get_rider_starting_points()

        self.picup_locations = self.get_pickup_locations()

        self.dropoff_locations = self.get_dropoff_locations()

        self.all_locations = self.picup_locations.union(self.dropoff_locations, self.rider_starting_points)
        


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
    
