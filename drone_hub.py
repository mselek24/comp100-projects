from drone import Drone


class DroneHub:
    """
    A hub that manages a collection of drones.

    Attributes:
        name (str): The name of the drone hub.
        drones (list): A list of Drone objects.
    """

    def __init__(self, name: str):
        """
        Initializes the drone hub.
        """
        # TODO: Set the name for the hub and initialize an empty list to manage its fleet of drones.
        pass


    def add_drone(self, drone: Drone) -> None:
        """
        Adds a drone to the hub's fleet.
        """
        # TODO: Register a new drone object into the hub's list of managed drones.
        pass


    def list_drones(self) -> None:
        """
        Prints each drone's information.
        """
        # TODO: Iterate through the managed drones and display each one's details to the console.
        pass


    def relocate_all_drones(self, new_location: tuple[float, float]) -> None:
        """
        Moves all drones in the hub to a new location.
        """
        # TODO: Coordinate a mass move by updating the location of every drone in the fleet.
        pass


    def __str__(self):
        """
        Returns a summary of the hub and its docked drones.
        """
        # TODO: Return a multi-line string showing the hub's status and a numbered list of all drones currently docked.
        # Ensure the output matches the required format shown in the instructions.
        return ""