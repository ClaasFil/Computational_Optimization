from src.read_data import *
from src.helper import *
from src.instance import *
from simple_greedy.titanic import *
from src.output import *
import time
import copy
import concurrent.futures

from feasibility_checker import  check_single_instance

from simple_greedy.magellan import magellan
from simple_greedy.sir_francis_drake import sir_francis_drake
from simple_greedy.hannibal import hannibal
from simple_greedy.flying_dutchman import flying_dutchman

# Entry point of the script
def main():
    
    location = os.path.dirname(os.path.abspath(__file__))
    

    #[logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL]
    setup_logging(log_level=logging.INFO, base_dir=location)  


    logging.debug(f"Starting to read instances")
    # Process all instances
    all_instance_data = process_all_instances('./final_test_set', max_instances=100)

    # Process test intance
    scoreboard = {}
    feasbilty_counter = 0
    for i, each_instance in enumerate(all_instance_data):
        start_time = time.time()
        solved_instance, best_name = solve(each_instance)
        if solved_instance:
            feasbilty_counter += 1
            if best_name in scoreboard:
                scoreboard[best_name] += 1
            else:
                scoreboard[best_name] = 1
        else:
            logging.warning(f"Instance {each_instance.instance_name} could not be solved.")
        logging.info(f"Instance {i} solved successfully. Execution time: {time.time() - start_time} seconds")

    logging.info(f"Feasability rate: {feasbilty_counter}/{len(all_instance_data)}")
    # Log final scoreboard and feasibility count
    logging.info(f"Total feasible solutions found: {feasbilty_counter}/{len(all_instance_data)}")
    logging.info("Final Scoreboard:")
    for solver, count in scoreboard.items():
        logging.info(f"{solver}: {count} times best solution")


def run_heuristic(heuristic_func, instance, name):
    current_instance = copy.deepcopy(instance)
    heuristic_func(current_instance)
    output_path = output(current_instance)
    is_feasable, cost = check_single_instance(output_path)
    return name, is_feasable, cost, current_instance

def solve(each_instance):
    solved_instance = False
    best_solution = None
    best_cost = float('inf')
    best_name= "Not Solved"

    # Define the heuristics and their names
    heuristics = [
        (titanic, "Titanic"),
        (magellan, "Magellan"),
        (sir_francis_drake, "Sir Francis Drake"),
        (hannibal, "Hannibal"),
        (flying_dutchman, "Flying Dutchman")
    ]
    
    # Execute each heuristic sequentially
    for heuristic_func, name in heuristics:
        try:
            name, is_feasable, cost, solution_instance = run_heuristic(heuristic_func, each_instance, name)
            
            if is_feasable:
                solved_instance = True
                logging.info(f"{name} Feasible: {cost}")

                # Check if this solution has the best cost
                if cost < best_cost:
                    best_name = name
                    best_cost = cost
                    best_solution = solution_instance
                    best_name = name

        except Exception as exc:
            logging.error(f"{name} heuristic generated an exception: {exc}")

    if best_solution:
        output_path = output(best_solution)

    return solved_instance, best_name





# Main execution
if __name__ == "__main__":
    main()

