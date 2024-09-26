from src.read_data import *
from src.helper import *
from simple_greedy.titanic import *
from src.output import *
import time
from simple_greedy.gready_anna import *
import copy

from feasibility_checker import feasability_chack_all, check_single_instance

from simple_greedy.magellan import magellan
from simple_greedy.sir_francis_drake import sir_francis_drake

# Entry point of the script
def main():
    
    location = os.path.dirname(os.path.abspath(__file__))
    

    #[logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL]
    setup_logging(log_level=logging.INFO, base_dir=location)  


    logging.debug(f"Starting to read instances")
    # Process all instances
    all_instance_data = process_all_instances('Computational_Optimization/training_data', max_instances=1000)

    # Process test intance
    #dir = 'Computational_Optimization/training_data/2a230eaf-44a1-4705-9cd4-19ba7d4f4668'
    #couriers, deliveries, travel_time = process_instance_folder(dir)
    #instance = Instance(dir, couriers, deliveries, travel_time) 
    
    
    feasbilty_counter = 0
    for (i,each_instance) in enumerate(all_instance_data):
        solved_instance = False
        start_time = time.time()
        #logging.INFO(f"Executing simple algorithm for instance: {each_instance.instance_name}")
        #Maike
        logging.info(f"-----------")
        current_instance = copy.deepcopy(each_instance)
        titanic(current_instance)
        output_path = output(current_instance)
        is_feasable, cost = check_single_instance(output_path)
        if is_feasable:
            solved_instance = True
            logging.info(f"Titanic Feasable: {cost}")

        current_instance = copy.deepcopy(each_instance)
        magellan(current_instance)
        output_path = output(current_instance)
        is_feasable, cost = check_single_instance(output_path)
        if is_feasable:
            solved_instance = True
            logging.info(f"Magellan Feasable: {cost}")

        current_instance = copy.deepcopy(each_instance)
        sir_francis_drake(current_instance)
        output_path = output(current_instance)
        is_feasable, cost = check_single_instance(output_path)
        if is_feasable:
            solved_instance = True
            logging.info(f"Sir Francis Drake Feasable: {cost}")
        
        
        #anna
        #each_instance = execute_greedy_algorithm(each_instance)





        #logging.INFO(f"Outputting results for instance: {each_instance.instance_name}")
        output_path = output(each_instance)
        logging.info(f"Execution time for instance {i}: {time.time() - start_time} seconds")

        #is_feasable, cost = check_single_instance(output_path)
        if solved_instance:
            feasbilty_counter += 1

    logging.info(f"Feasability rate: {feasbilty_counter}/{len(all_instance_data)}")

    #feasability_chack_all()
    print("The End")


# Main execution
if __name__ == "__main__":
    main()

