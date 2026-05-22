from drone import Drone


class DroneHub(Drone):
    """
    A hub that manages a collection of drones.

    Attributes:
        name (str): The name of the drone hub.
        drones (list): A list of Drone objects.
    """

    def __init__(self, name: str):
        self.name=name
        self.drones=[]


    def add_drone(self, drone: Drone) -> None:
        self.drones.append(drone)


    def list_drones(self) -> None:
        for drone in self.drones:
            print(f"Drone ID: {drone.id} Type: {drone.get_type()}")


    def relocate_all_drones(self, new_location: tuple[float, float]) -> None:
        for drone in self.drones:
            drone.move_to(new_location)


    def __str__(self):
        result = f"\n--- DroneHub {self.name}: {len(self.drones)} drones docked ---"
        index = 0
        for drone in self.drones:
            result += f"\n[{index}]: {drone.id} {drone.get_type()}"
            index += 1
        result += "\n"
        return result