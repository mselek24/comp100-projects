from drone import Drone

class DeliveryDrone:
    """
    A delivery drone that inherits from Drone.

    Attributes:
        cargo_capacity (float): The maximum cargo weight.
        current_cargo (float): The current cargo load (starts at 0).
    """

    def __init__(self, id: str, max_speed: int, current_location: tuple[float, float], cargo_capacity: float):
        """
        Initializes a delivery drone. 
        Uses super() to initialize base attributes.
        """
        # TODO: Initialize the base attributes by calling the parent class constructor.
        # Then, set the specific attributes for a delivery drone, starting with an empty load.
        pass


    def load_cargo(self, weight: float) -> None:
        """
        Loads cargo if it doesn't exceed capacity.
        """
        # TODO: Check if the new weight can be added without exceeding the drone's capacity.
        # Update the load if possible.
        # (In Task 4, you will update this to raise a custom CargoLimitError if capacity is exceeded).
        pass


    def deliver_cargo(self) -> None:
        """
        Delivers the cargo and resets current load.
        """
        # TODO: Reset the drone's current cargo to indicate a successful delivery.
        # Print a confirmation message to the console.
        pass

    def get_type(self) -> str:
        """
        Overrides the base method to return the specific type.
        """
        # TODO: Identify this drone specifically as a delivery drone.
        return ""
