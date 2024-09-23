from src.read_data import *
from src.helper import *
# from greedy import execute_greedy_algorithm




# Entry point of the script
def main():
    
    location = os.path.dirname(os.path.abspath(__file__))


    #[logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL]
    setup_logging(log_level=logging.DEBUG, base_dir=location)  


    logging.debug(f"Stasrting to read instances")
    # Process all instances
    all_instance_data = process_all_instances('Computational_Optimization/training_data', max_instances=10)


    # Execute greedy algorithm to find feasible solution
    # for instance in all_instance_data:
    #     solution = execute_greedy_algorithm(instance)

    # Apply heuristic to improve solution


    print("The End")


# Main execution
if __name__ == "__main__":
    main()

