import os
import csv
import argparse
import logging
from src.delivery import Delivery
from src.courier import Courier


from src.instance import Instance


# Function to load couriers from CSV using the csv module
def load_couriers_from_csv(filepath):
    couriers = []
    with open(filepath, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            courier = Courier(
                courier_id=int(row['ID']),
                location=int(row['Location']),
                capacity=int(row['Capacity'])
            )
            couriers.append(courier)
    return couriers


# Function to load deliveries from CSV using the csv module
def load_deliveries_from_csv(filepath):
    deliveries = []
    with open(filepath, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            delivery = Delivery(
                delivery_id=int(row['ID']),
                capacity=int(row['Capacity']),
                pickup_loc=int(row['Pickup Loc']),
                time_window_start=int(row['Time Window Start']),
                pickup_stacking_id=int(row['Pickup Stacking_Id']),
                dropoff_loc=int(row['Dropoff Loc'])
            )
            deliveries.append(delivery)
    return deliveries


# Function to load travel time matrix from CSV
def load_travel_time_from_csv(filepath):
    travel_time = []
    with open(filepath, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == 'Locations':
                travel_time.append([val for val in row])
            else:
                travel_time.append([int(val) for val in row])  # Convert the row values to integers, skip the location index (first column)
    return travel_time


# Function to process each instance folder and look for couriers.csv, deliveries.csv, and traveltime.csv
def process_instance_folder(instance_folder_path):
    couriers_file = None
    deliveries_file = None
    travel_time_file = None

    # Search for files in the instance folder
    for filename in os.listdir(instance_folder_path):
        if 'couriers.csv' in filename:
            couriers_file = os.path.join(instance_folder_path, filename)
        elif 'deliveries.csv' in filename:
            deliveries_file = os.path.join(instance_folder_path, filename)
        elif 'traveltimes.csv' in filename:
            travel_time_file = os.path.join(instance_folder_path, filename)

    # Ensure all necessary files are found
    if not couriers_file:
        raise FileNotFoundError(f"Missing couriers.csv file in folder: {instance_folder_path}")

    if not deliveries_file:
        raise FileNotFoundError(f"Missing deliveries.csv file in folder: {instance_folder_path}")

    if not travel_time_file:
        raise FileNotFoundError(f"Missing traveltimes.csv file in folder: {instance_folder_path}")


    # Load couriers, deliveries, and travel time matrix from the instance
    couriers = load_couriers_from_csv(couriers_file)
    deliveries = load_deliveries_from_csv(deliveries_file)
    travel_time = load_travel_time_from_csv(travel_time_file)

    return couriers, deliveries, travel_time


# Main function to loop through all instance folders
def process_all_instances(parent_folder, max_instances=None):
    logging.debug(f"Processing all instances in folder: {parent_folder}")
    all_instances = []
    

    # Loop through each instance folder in the parent directory
    for instance_folder in os.listdir(parent_folder):
        if max_instances and len(all_instances) < max_instances:
            instance_folder_path = os.path.join(parent_folder, instance_folder)

            # Check if it's a directory (instance folder)
            if os.path.isdir(instance_folder_path):
                logging.debug(f"Processing instance: {instance_folder}")
                try:
                    couriers, deliveries, travel_time = process_instance_folder(instance_folder_path)
                    instance = Instance(instance_folder, couriers, deliveries, travel_time) 
                    # Add this instance's couriers, deliveries, and travel time matrix to the overall list
                    all_instances.append(instance)
                    
                except FileNotFoundError as e:
                    logging.error(f"Error processing instance: {instance_folder}. {e}")
    if max_instances:
        logging.info(f"Processed {len(all_instances)} instances out of {max_instances} requested.")
    else:
        logging.info(f"Processed {len(all_instances)} instances.")

    return all_instances


"""# Entry point of the script
def main():
    # Parse the command-line arguments
    parser = argparse.ArgumentParser(description="Process couriers, deliveries, and travel time matrices from multiple instances.")
    parser.add_argument('parent_folder', type=str, help='Path to the parent folder containing all instance folders')

    args = parser.parse_args()

    # Process all instances
    all_instance_data = process_all_instances(args.parent_folder)


# Main execution
if __name__ == "__main__":
    main()"""
