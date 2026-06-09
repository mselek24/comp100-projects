from drone import Drone


class SurveyDrone(Drone):
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
        super().__init__(id, max_speed, current_location)
        self.camera_quality = camera_quality
        self.survey_data = []


    def scan_area(self, area_coordinates: list) -> None:
        """
        Simulates scanning an area.
        """
        # TODO: Store the provided area coordinates in the drone's survey data.
        # Print a message indicating the scan was completed.
       
        for coordinate in area_coordinates:
            self.survey_data.append(coordinate)
        print("Survey completed!")


    def get_type(self) -> str:
        return "Survey Drone"
