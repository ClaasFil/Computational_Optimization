from src.instance import Instance
from src.courier import Courier


# generate output for the optimization problem

def output(instance:Instance):

    all_couriers = instance.couriers
    for each in all_couriers:
        print(f"Courier Activities: {each.activities}")
        print("\n")


    pass