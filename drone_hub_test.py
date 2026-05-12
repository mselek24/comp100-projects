import unittest
import sys
from io import StringIO

from drone import Drone
from delivery_drone import DeliveryDrone
from survey_drone import SurveyDrone
from drone_hub import DroneHub


class TestDroneHub(unittest.TestCase):
    def setUp(self):
        Drone.ids = []

    def test_1(self):
        hub = DroneHub("Central Fleet")
        self.assertEqual(hub.name, "Central Fleet", "DroneHub name was not set correctly.")
        self.assertEqual(hub.drones, [], "DroneHub 'drones' list should be initialized to an empty list.")
        self.assertTrue(isinstance(hub.drones, list), "DroneHub 'drones' attribute should be a list.")

    def test_2(self):
        hub = DroneHub("Central Fleet")
        hub.add_drone(Drone("#D1001", 100, (34.0522, -118.2437)))
        self.assertEqual(len(hub.drones), 1, "add_drone did not add the drone to the hub's drones list.")
        self.assertEqual(hub.drones[0].id, "#D1001", "The drone added to the hub has the wrong ID.")
        self.assertEqual(hub.drones[0].max_speed, 100, "The drone added to the hub has the wrong max_speed.")
        self.assertEqual(hub.drones[0].current_location, (34.0522, -118.2437), "The drone added to the hub has the wrong current_location.")
        self.assertTrue(isinstance(hub.drones[0], Drone), "The item added to 'drones' list should be a Drone object.")
        self.assertEqual(hub.drones[0].get_type(), "Generic Drone", "get_type() for base Drone should be 'Generic Drone'.")

    def test_3(self):
        hub = DroneHub("Central Fleet")
        hub.add_drone(Drone("#D1001", 100, (34.0522, -118.2437)))
        hub.add_drone(Drone("#D1002", 100, (34.0522, -118.2437)))
        self.assertEqual(len(hub.drones), 2, "add_drone failed to add multiple drones.")
        self.assertEqual(hub.drones[0].id, "#D1001", "The first drone in the hub has the wrong ID.")
        self.assertEqual(hub.drones[1].id, "#D1002", "The second drone in the hub has the wrong ID.")

    def test_4(self):
        hub = DroneHub("Central Fleet")
        hub.add_drone(DeliveryDrone("#D1001", 100, (34.0522, -118.2437), 100))
        hub.add_drone(SurveyDrone("#S1001", 100, (34.0522, -118.2437), "HD"))
        self.assertEqual(len(hub.drones), 2, "add_drone failed to add subclasses of Drone (DeliveryDrone and SurveyDrone).")
        self.assertEqual(hub.drones[0].id, "#D1001", "The DeliveryDrone in the hub has the wrong ID.")
        self.assertEqual(hub.drones[1].id, "#S1001", "The SurveyDrone in the hub has the wrong ID.")
        self.assertEqual(hub.drones[0].get_type(), "Delivery Drone", "get_type() for DeliveryDrone should be 'Delivery Drone'.")
        self.assertEqual(hub.drones[1].get_type(), "Survey Drone", "get_type() for SurveyDrone should be 'Survey Drone'.")

    def test_5(self):
        expected_lines = [
            "Drone ID: #D1001 Type: Delivery Drone",
            "Drone ID: #S1001 Type: Survey Drone"
        ]
        captured_output = StringIO()
        sys_stdout_backup = sys.stdout
        sys.stdout = captured_output
        try:
            hub = DroneHub("Central Fleet")
            hub.add_drone(DeliveryDrone("#D1001", 100, (34.0522, -118.2437), 100))
            hub.add_drone(SurveyDrone("#S1001", 100, (34.0522, -118.2437), "HD"))
            hub.list_drones()
        finally:
            sys.stdout = sys_stdout_backup
        actual_lines = captured_output.getvalue().strip().split("\n")
        self.assertEqual(actual_lines, expected_lines, "list_drones output format is incorrect. Each line should be 'Drone ID: <id> Type: <type>'.")

    def test_6(self):
        hub = DroneHub("Central Fleet")
        d1 = DeliveryDrone("#D1001", 100, (34.0, -118.0), 100)
        d2 = SurveyDrone("#S1001", 100, (34.0, -118.0), "HD")
        hub.add_drone(d1)
        hub.add_drone(d2)
        
        new_loc = (50.0, -120.0)
        hub.relocate_all_drones(new_loc)

        # The drones should still be in the hub and moved to the new location
        self.assertEqual(len(hub.drones), 2, "Drones list length should not change after relocation.")
        self.assertEqual(d1.current_location, new_loc, "relocate_all_drones did not move the DeliveryDrone correctly.")
        self.assertEqual(d2.current_location, new_loc, "relocate_all_drones did not move the SurveyDrone correctly.")

    def test_7_str_representation(self):
        hub = DroneHub("Central Fleet")
        hub.add_drone(DeliveryDrone("#D1001", 100, (0, 0), 100))
        hub.add_drone(SurveyDrone("#S1001", 80, (0, 0), "HD"))
        expected = (
            "\n--- DroneHub Central Fleet: 2 drones docked ---\n"
            "[0]: #D1001 Delivery Drone\n"
            "[1]: #S1001 Survey Drone\n"
        )
        self.assertEqual(str(hub), expected, "DroneHub __str__ implementation is incorrect. Please check the instructions for the required format.")


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestDroneHub)
    result = unittest.TextTestRunner().run(suite)
    total_tests_run = result.testsRun
    total_failures = len(result.failures) + len(result.errors)
    total_passed = total_tests_run - total_failures
    print(f"Test Passed: {total_passed}/{total_tests_run}")