from src.read_data import *
from src.helper import *
from simple_greedy.simple_algorithm import *


# Entry point of the script
def main():
    
    location = os.path.dirname(os.path.abspath(__file__))
    

    #[logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL]
    setup_logging(log_level=logging.DEBUG, base_dir=location)  


    logging.debug(f"Starting to read instances")
    # Process all instances
    # all_instance_data = process_all_instances('./training_data', max_instances=1)

    # Process test intance
    dir = './training_data/2a230eaf-44a1-4705-9cd4-19ba7d4f4668'
    couriers, deliveries, travel_time = process_instance_folder(dir)
    instance = Instance(dir, couriers, deliveries, travel_time) 
    
    execute_simple_algorithm(instance)


    print("The End")


# Main execution
if __name__ == "__main__":
    main()

