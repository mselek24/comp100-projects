from drone_exceptions import DuplicateIDError
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
        if id in Drone.ids:
            raise  DuplicateIDError(id)
        
        else:
            Drone.ids.append(id)
        self.id=id
        self.max_speed=max_speed
        self.current_location=current_location
        self.type=self.get_type()
        
           
        # For now, you can use a simple print message or an assertion.
        # (In Task 4, you will replace this with a custom DuplicateIDError).
        
        # Once validated, update the global list and set the drone's personal attributes.
        


    def move_to(self, new_location: tuple[float, float]) -> None:
        self.current_location=new_location


    def get_type(self) -> str:
        """
        Returns the type of the drone.
        """
        # TODO: This method should return a string identifying this as a generic drone.
        return "Generic Drone"

    def __str__(self):
        """
        Returns a string representation of the drone.
        Format: "Drone ID: #D1001 Type: Delivery Drone"
        """
        # TODO: Return a descriptive string that includes the ID and the drone's type.
        return f'{self.id}: #D1001 Tyoe: {self.get_type} '
