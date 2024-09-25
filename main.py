from src.read_data import *
from src.helper import *
from simple_greedy.titanic import *
from src.output import *
import time
from simple_greedy.gready_anna import *

# Entry point of the script
def main():
    
    location = os.path.dirname(os.path.abspath(__file__))
    

    #[logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL]
    setup_logging(log_level=logging.INFO, base_dir=location)  


    logging.debug(f"Starting to read instances")
    # Process all instances
    all_instance_data = process_all_instances('Computational_Optimization/training_data', max_instances=1)

    # Process test intance
    #dir = 'Computational_Optimization/training_data/2a230eaf-44a1-4705-9cd4-19ba7d4f4668'
    #couriers, deliveries, travel_time = process_instance_folder(dir)
    #instance = Instance(dir, couriers, deliveries, travel_time) 
    
    
    
    for (i,each_instance) in enumerate(all_instance_data):
        start_time = time.time()
        #logging.INFO(f"Executing simple algorithm for instance: {each_instance.instance_name}")
        #Maike
        #execute_simple_algorithm(each_instance)

        #anna
        each_instance = execute_greedy_algorithm(each_instance)





        #logging.INFO(f"Outputting results for instance: {each_instance.instance_name}")
        output(each_instance)
        logging.info(f"Execution time for instance {i}: {time.time() - start_time} seconds")


    print("The End")


# Main execution
if __name__ == "__main__":
    main()

