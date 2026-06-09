class DroneError(Exception):
    pass

class DuplicateIDError(Exception):
    def __init__(self, drone_id):
        super().__init__(f"Drone id {drone_id} already exists!")

class CargoLimitError(Exception):
    def __init__(self, message="Weight exceeds maximum capacity!"):
        super().__init__(message)
        

