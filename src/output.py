from src.instance import Instance
from src.courier import Courier
import logging
import csv
import os


# generate output for the optimization problem

def output(instance:Instance):

    couriers = instance.couriers

    output_dir = "./res/"
    os.makedirs(output_dir, exist_ok=True)

    # Define the full file path
    file_path = os.path.join(output_dir, f"{instance.instance_name}.csv")

    if os.path.exists(file_path):
        os.remove(file_path)

    with open(file_path, mode="w", newline="") as file:
        #

        writer = csv.writer(file)

        #if not exsisting add the header as ID
        writer.writerow(["ID"])
        
        # Write each courier's ID and delivery sequence
        for courier in couriers:
            if courier.activities:
                # The sequence includes pickup and dropoff (so delivery IDs appear twice)
                row = [courier.courier_id] + courier.activities 
            else:
                # If no deliveries, just output the courier ID
                row = [courier.courier_id]
            
            # Write the row to the CSV file
            writer.writerow(row)