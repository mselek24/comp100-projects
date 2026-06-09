from drone import Drone
from drone_exceptions import CargoLimitError

class DeliveryDrone(Drone):
    """
    A delivery drone that inherits from Drone.

    Attributes:
        cargo_capacity (float): The maximum cargo weight.
        current_cargo (float): The current cargo load (starts at 0).
    """

    def __init__(self, id: str, max_speed: int, current_location: tuple[float, float], cargo_capacity: float):
       super().__init__(id, max_speed, current_location)
       self.cargo_capacity =cargo_capacity
       self.current_cargo =0


    def load_cargo(self, weight: float) -> None:
        """
        Loads cargo if it doesn't exceed capacity.
        """
        if weight+self.current_cargo<=self.cargo_capacity:
            self.current_cargo+=weight
        else:
            raise CargoLimitError()
        # TODO: Check if the new weight can be added without exceeding the drone's capacity.
        # Update the load if possible.
        # (In Task 4, you will update this to raise a custom CargoLimitError if capacity is exceeded).
      


    def deliver_cargo(self) -> None:
       self.current_cargo=0
       print('Cargo delivered successfully!')


    def get_type(self) -> str:
        """
        Overrides the base method to return the specific type.
        """
        # TODO: Identify this drone specifically as a delivery drone.
        return "Delivery Drone"
