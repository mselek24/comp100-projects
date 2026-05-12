import unittest
from drone import Drone



class TestDrone(unittest.TestCase):
    def setUp(self):
        # Clear class-level ID list before each test
        Drone.ids = []
        self.drone = Drone("#D1001", 100, (34.0522, -118.2437))

    def test_1_initialization(self):
        self.assertEqual(self.drone.id, "#D1001", "Drone ID was not set correctly in __init__.")
        self.assertEqual(self.drone.max_speed, 100, "Drone max_speed was not set correctly in __init__.")
        self.assertEqual(self.drone.current_location, (34.0522, -118.2437), "Drone current_location was not set correctly in __init__.")

    def test_2_move_to(self):
        new_location = (40.7128, -74.0060)
        self.drone.move_to(new_location)
        self.assertEqual(self.drone.current_location, new_location, "move_to did not update current_location correctly.")

    def test_3_get_type(self):
        self.assertEqual(self.drone.get_type(), "Generic Drone", "get_type for the base Drone class should return 'Generic Drone'.")

    def test_4_location_type(self):
        self.assertIsInstance(self.drone.current_location, tuple, "current_location should be a tuple.")
        self.assertEqual(len(self.drone.current_location), 2, "current_location should have 2 elements (latitude, longitude).")
        # Checking if coordinates are numbers
        self.assertTrue(isinstance(self.drone.current_location[0], (int, float)), "Latitude should be a number.")
        self.assertTrue(isinstance(self.drone.current_location[1], (int, float)), "Longitude should be a number.")

    def test_5_ids_class_variable(self):
        # The ID should be in the class variable
        self.assertIn("#D1001", Drone.ids, "New drone ID was not added to the class variable 'ids'.")
        self.assertEqual(len(Drone.ids), 1, "The 'ids' list should contain exactly one ID after creating one drone.")

    def test_6_duplicate_id_assertion(self):
        # This import is inside the method so Task 1 tests still run before Task 4 is started
        from drone_exceptions import DuplicateIDError
        with self.assertRaises(DuplicateIDError, msg="DuplicateIDError was not raised when creating a drone with an existing ID.") as cm:
            duplicate = Drone("#D1001", 80, (0, 0))
        self.assertEqual(str(cm.exception), "Drone id #D1001 already exists!", "DuplicateIDError message is incorrect.")


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestDrone)
    result = unittest.TextTestRunner().run(suite)
    total_tests_run = result.testsRun
    total_failures = len(result.failures) + len(result.errors)
    total_passed = total_tests_run - total_failures
    print(f"Test Passed: {total_passed}/{total_tests_run}")