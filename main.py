from src.read_data import *
from src.helper import *
import sys
import time
#import xpress as xp



# Entry point of the script
def main():
    print("Python interpreter in use:", sys.executable)
    print("Python version:", sys.version)
    
    location = os.path.dirname(os.path.abspath(__file__))
    

    #[logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL]
    setup_logging(log_level=logging.DEBUG, base_dir=location)  


    logging.debug(f"Starting to read instances")
    # Process all instances

    #start timing 
    start_time_preprocessing = time.time()
    all_instance_data = process_all_instances('Computational_Optimization/training_data', max_instances=1)
    end_time_preprocessing = time.time()
    logging.info(f"Preprocessing time: {end_time_preprocessing - start_time_preprocessing}")

    #process each Instance
    for each_instance in all_instance_data:
        logging.info(f"Processing instance: {each_instance.instance_name}")

        each_instance.model_instance()
        

    logging.info(f"The end of the script")


# Main execution
if __name__ == "__main__":
    main()

