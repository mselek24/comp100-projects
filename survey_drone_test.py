import unittest
import sys
from io import StringIO

from survey_drone import SurveyDrone
from drone import Drone


class TestSurveyDrone(unittest.TestCase):
    def setUp(self):
        Drone.ids = []

    def test_1_initialization(self):
        drone = SurveyDrone(id="#S1001", max_speed=100, current_location=(34.0522, -118.2437), camera_quality="HD")
        self.assertEqual(drone.id, "#S1001", "SurveyDrone ID was not set correctly.")
        self.assertEqual(drone.max_speed, 100, "SurveyDrone max_speed was not set correctly.")
        self.assertEqual(drone.current_location, (34.0522, -118.2437), "SurveyDrone current_location was not set correctly.")
        self.assertEqual(drone.camera_quality, "HD", "SurveyDrone camera_quality was not set correctly.")
        self.assertEqual(drone.survey_data, [], "SurveyDrone survey_data should be initialized to an empty list.")

    def test_2_single_scan(self):
        expected_output = "Survey completed!"
        captured_output = StringIO()
        sys_stdout_backup = sys.stdout
        sys.stdout = captured_output
        try:
            drone = SurveyDrone("#S1001", 100, (34.0522, -118.2437), "HD")
            coords = [(34.0522, -118.2437)] * 3
            drone.scan_area(coords)
        finally:
            sys.stdout = sys_stdout_backup
        self.assertEqual(captured_output.getvalue().strip(), expected_output, "scan_area did not print the correct confirmation message.")
        self.assertEqual(drone.survey_data, coords, "scan_area did not store the coordinates correctly in survey_data.")

    def test_3_multiple_scans(self):
        expected_output = "Survey completed!\nSurvey completed!"
        captured_output = StringIO()
        sys_stdout_backup = sys.stdout
        sys.stdout = captured_output
        try:
            drone = SurveyDrone("#S1001", 100, (34.0522, -118.2437), "4K")
            first = [(34.0522, -118.2437)] * 3
            second = [(37.4, -122.1), (-42.4, 174.3), (34.0522, -118.2437)]
            drone.scan_area(first)
            drone.scan_area(second)
        finally:
            sys.stdout = sys_stdout_backup
        self.assertEqual(captured_output.getvalue().strip(), expected_output, "scan_area did not print the correct confirmation messages for multiple scans.")
        self.assertEqual(drone.survey_data, first + second, "scan_area should extend survey_data with new coordinates.")

    def test_4_get_type(self):
        drone = SurveyDrone("#S1001", 100, (34.0522, -118.2437), "4K")
        self.assertEqual(drone.get_type(), "Survey Drone", "get_type() should return 'Survey Drone' for SurveyDrone.")


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestSurveyDrone)
    result = unittest.TextTestRunner().run(suite)
    total_tests_run = result.testsRun
    total_failures = len(result.failures) + len(result.errors)
    total_passed = total_tests_run - total_failures
    print(f"Test Passed: {total_passed}/{total_tests_run}")