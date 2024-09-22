import logging
class Arc:
    """Represents an individual arc between two vertices with an associated travel time."""
    def __init__(self, start_vertex, end_vertex, travel_time):
        self.start_vertex = start_vertex  # Starting vertex of the arc
        self.end_vertex = end_vertex      # Ending vertex of the arc
        if travel_time < 0:
            logging.error("Travel time cannot be negative")
            raise ValueError("Travel time cannot be negative")
        self.travel_time = travel_time    # Travel time from start_vertex to end_vertex

    def __repr__(self):
        return f"Arc({self.start_vertex}, {self.end_vertex}, TravelTime={self.travel_time})"






