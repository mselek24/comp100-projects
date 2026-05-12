import unittest
import sys
from io import StringIO

from delivery_drone import DeliveryDrone
from drone import Drone



class TestDeliveryDrone(unittest.TestCase):
    def setUp(self):
        Drone.ids = []  # Reset class-level IDs to avoid duplicate ID assertion failures

    def test_1_initialization(self):
        drone = DeliveryDrone("#D1001", 100, (34.0522, -118.2437), 100)
        self.assertEqual(drone.id, "#D1001", "DeliveryDrone ID was not set correctly.")
        self.assertEqual(drone.max_speed, 100, "DeliveryDrone max_speed was not set correctly.")
        self.assertEqual(drone.current_location, (34.0522, -118.2437), "DeliveryDrone current_location was not set correctly.")
        self.assertEqual(drone.cargo_capacity, 100, "DeliveryDrone cargo_capacity was not set correctly.")
        self.assertEqual(drone.current_cargo, 0, "DeliveryDrone current_cargo should be initialized to 0.")

    def test_2_load_cargo_within_capacity(self):
        drone = DeliveryDrone("#D1001", 100, (0, 0), 100)
        drone.load_cargo(50)
        self.assertEqual(drone.current_cargo, 50, "current_cargo was not updated correctly after loading within capacity.")

    def test_3_load_cargo_exact_capacity(self):
        drone = DeliveryDrone("#D1001", 100, (0, 0), 100)
        drone.load_cargo(100)
        self.assertEqual(drone.current_cargo, 100, "current_cargo should be equal to capacity when loading exactly the capacity.")

    def test_4_load_cargo_exceeds_capacity(self):
        # This import is inside the method so earlier tasks still run before Task 4 is started
        from drone_exceptions import CargoLimitError
        drone = DeliveryDrone("#D1001", 100, (0.0, 0.0), 100.0)
        with self.assertRaises(CargoLimitError, msg="CargoLimitError was not raised when loading exceeds capacity.") as cm:
            drone.load_cargo(150.0)
        self.assertEqual(str(cm.exception), "Weight exceeds maximum capacity!", "CargoLimitError message is incorrect.")

    def test_5_load_cargo_incrementally_exceeds_capacity(self):
        # This import is inside the method so earlier tasks still run before Task 4 is started
        from drone_exceptions import CargoLimitError
        drone = DeliveryDrone("#D1001", 100, (0.0, 0.0), 100.0)
        drone.load_cargo(50.0)
        with self.assertRaises(CargoLimitError, msg="CargoLimitError was not raised when combined weight exceeds capacity.") as cm:
            drone.load_cargo(60.0)
        self.assertEqual(str(cm.exception), "Weight exceeds maximum capacity!", "CargoLimitError message is incorrect.")

    def test_6_deliver_cargo(self):
        expected_output = "Cargo delivered successfully!"
        captured_output = StringIO()
        sys_stdout_backup = sys.stdout
        sys.stdout = captured_output
        try:
            drone = DeliveryDrone("#D1001", 100, (0, 0), 100)
            drone.load_cargo(50)
            drone.deliver_cargo()
        finally:
            sys.stdout = sys_stdout_backup
        self.assertEqual(captured_output.getvalue().strip(), expected_output, "deliver_cargo did not print the correct confirmation message.")
        self.assertEqual(drone.current_cargo, 0, "current_cargo should be reset to 0 after delivery.")

    def test_7_get_type(self):
        drone = DeliveryDrone("#D1001", 100, (0, 0), 100)
        self.assertEqual(drone.get_type(), "Delivery Drone")


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestDeliveryDrone)
    result = unittest.TextTestRunner().run(suite)
    total_tests_run = result.testsRun
    total_failures = len(result.failures) + len(result.errors)
    total_passed = total_tests_run - total_failures
    print(f"Test Passed: {total_passed}/{total_tests_run}")