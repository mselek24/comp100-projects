class DroneError(Exception):
    """
    Base class for exceptions in this project.
    Inherits from the built-in Exception class.
    """
    pass

class DuplicateIDError:
    """
    Raised when a drone ID is already in use.
    """
    def __init__(self, drone_id):
        # TODO: Initialize the exception with a message: "Drone id {drone_id} already exists!"
        # Hint: Use super() to pass the message to the parent Exception class
        pass

class CargoLimitError:
    """
    Raised when the cargo exceeds the drone's capacity.
    """
    def __init__(self, message="Weight exceeds maximum capacity!"):
        # TODO: Initialize the exception with the provided message
        # Hint: Use super() to pass the message to the parent Exception class
        pass
