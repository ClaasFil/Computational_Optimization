import logging


class Arc:
    """Represents an individual arc between two vertices with an associated travel time."""
    def __init__(self, start_vertex, end_vertex, travel_time):
        self.start_vertex = start_vertex  # Starting vertex of the arc
        self.end_vertex = end_vertex      # Ending vertex of the arc
        if travel_time < 0:
            logging.error(f"Travel time is {travel_time} but should be negative")
            raise ValueError("Travel time cannot be negative")
        self.travel_time = travel_time    # Travel time from start_vertex to end_vertex

    def __repr__(self):
        return f"Arc({self.start_vertex}, {self.end_vertex}, TravelTime={self.travel_time})"



def find_arriving_arcs(starting_node, arcs):
    """
    Given a starting node and a set of arcs, return all arcs that start from the given node.
    
    :param starting_node: The node from which the arcs should start
    :param arcs: A set of Arc objects
    :return: A list of Arc objects that start from the starting_node
    """
    return [arc for arc in arcs if arc.start_vertex == starting_node]


def find_leaving_arcs(ending_node, arcs):
    """
    Given an ending node and a set of arcs, return all arcs that end at the given node.
    
    :param ending_node: The node at which the arcs should end
    :param arcs: A set of Arc objects
    :return: A list of Arc objects that end at the ending_node
    """
    return [arc for arc in arcs if arc.end_vertex == ending_node]

