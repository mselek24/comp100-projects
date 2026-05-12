from delivery_drone import DeliveryDrone
from survey_drone import SurveyDrone
from drone_hub import DroneHub
from drone_exceptions import CargoLimitError, DuplicateIDError


print("--- Phase 1: Creating Drones ---")
hub = DroneHub("Central Fleet")
drone1 = DeliveryDrone("#D1001", 100, (0.0, 0.0), 100.0)
drone2 = SurveyDrone("#S1001", 80, (0.0, 0.0), "HD")

print(f"Created {drone1.get_type()} with ID {drone1.id}")
print(f"Created {drone2.get_type()} with ID {drone2.id}")

print("\n--- Phase 2: Specific Drone Actions ---")
print("Loading 10kg into Delivery Drone...")
drone1.load_cargo(10.0)
print("Delivering cargo...")
drone1.deliver_cargo()

print("\nScanning area with Survey Drone...")
drone2.scan_area([(0, 0), (10, 10), (20, 20), (30, 30)])

print("\n--- Phase 3: Handling Errors ---")
drone4 = DeliveryDrone("#D1002", 180, (0, 0), 45.0)
print(f"Trying to load 50kg into drone with capacity {drone4.cargo_capacity}...")
try:
    drone4.load_cargo(50.0)
except CargoLimitError as e:
    print(f"Caught expected error: {e}")

print("\nTrying to create a drone with an existing ID '#D1001'...")
try:
    drone5 = DeliveryDrone("#D1001", 120, (0, 0), 50.0)
except DuplicateIDError as e:
    print(f"Caught expected error: {e}")

print("\n--- Phase 4: Hub Management ---")
hub.add_drone(drone1)
hub.add_drone(drone2)
hub.add_drone(drone4)

print(f"Listing all drones in hub '{hub.name}':")
hub.list_drones()

print("\nTesting Hub __str__:")
print(hub)

print("--- Phase 5: Bulk Relocation ---")
new_loc = (50.0, -120.0)
print(f"Relocating all drones to {new_loc}...")
hub.relocate_all_drones(new_loc)

print("\nVerifying location of first drone...")
print(f"Drone {drone1.id} location: {drone1.current_location}")