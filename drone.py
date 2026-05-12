class Drone:
    """
    A base class for all drones.

    Attributes:
        ids (list): Class variable to store all unique drone IDs.
        id (str): The unique identifier for the drone.
        max_speed (int): The maximum speed of the drone (km/h).
        current_location (tuple[float, float]): The current location of the drone (latitude, longitude).
    """

    # TODO: Initialize a class-level variable to keep track of all drone IDs that have been created.
    ids = []

    def __init__(self, id: str, max_speed: int, current_location: tuple[float, float]):
        """
        Initializes a drone with the given attributes.
        """
        # TODO: Ensure the provided ID does not already exist in the global list of IDs.
        # For now, you can use a simple print message or an assertion.
        # (In Task 4, you will replace this with a custom DuplicateIDError).
        
        # Once validated, update the global list and set the drone's personal attributes.
        pass


    def move_to(self, new_location: tuple[float, float]) -> None:
        """
        Updates the current location of the drone.
        """
        # TODO: Update the drone's position to the coordinates provided.
        pass


    def get_type(self) -> str:
        """
        Returns the type of the drone.
        """
        # TODO: This method should return a string identifying this as a generic drone.
        return ""

    def __str__(self):
        """
        Returns a string representation of the drone.
        Format: "Drone ID: #D1001 Type: Delivery Drone"
        """
        # TODO: Return a descriptive string that includes the ID and the drone's type.
        return ""
