from drone import Drone


class SurveyDrone:
    """
    A survey drone that inherits from Drone.

    Attributes:
        camera_quality (str): The quality of the camera (e.g., "4K").
        survey_data (list): A list to store results of scans.
    """

    def __init__(self, id: str, max_speed: int, current_location: tuple[float, float], camera_quality: str):
        """
        Initializes a survey drone.
        Uses super() to initialize base attributes.
        """
        # TODO: Initialize the base attributes using the parent class constructor.
        # Set the camera quality and initialize an empty collection for survey data.
        pass


    def scan_area(self, area_coordinates: list) -> None:
        """
        Simulates scanning an area.
        """
        # TODO: Store the provided area coordinates in the drone's survey data.
        # Print a message indicating the scan was completed.
        pass


    def get_type(self) -> str:
        """
        Overrides the base method to return the specific type.
        """
        # TODO: Identify this drone specifically as a survey drone.
        return ""
