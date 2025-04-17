import time
import RPi.GPIO as GPIO
from bleak import BleakScanner
from modules.ble_detection import BLEBeaconDetector

class SensorManager:
    def __init__(self, trig_pin=27, echo_pin=22, target_uuid=None, target_mac=None):
        self.trig_pin = trig_pin
        self.echo_pin = echo_pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.trig_pin, GPIO.OUT)
        GPIO.setup(self.echo_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        self.ble_detector = BLEBeaconDetector(target_uuid=target_uuid, target_mac=target_mac)

    def get_ultrasonic_distance(self, num_readings=3):
        distances = []
        try:
            for _ in range(num_readings):
                # Trigger ultrasonic pulse
                GPIO.output(self.trig_pin, True)
                time.sleep(0.00001)
                GPIO.output(self.trig_pin, False)

                timeout = time.time() + 0.05  # 50ms timeout

                # Wait for echo pin to go HIGH
                while True:
                    val = GPIO.input(self.echo_pin)
                    if val is None:
                        print("[DEBUG] echo_pin read as None while waiting for HIGH")
                        return -1
                    if val == 1:
                        pulse_start = time.time()
                        break
                    if time.time() > timeout:
                        print("[DEBUG] Timeout waiting for echo HIGH")
                        return -1

                # Wait for echo pin to go LOW
                while True:
                    val = GPIO.input(self.echo_pin)
                    if val is None:
                        print("[DEBUG] echo_pin read as None while waiting for LOW")
                        return -1
                    if val == 0:
                        pulse_end = time.time()
                        break
                    if time.time() > timeout:
                        print("[DEBUG] Timeout waiting for echo LOW")
                        return -1

                duration = pulse_end - pulse_start
                distance = round(duration * 17150, 2)
                distances.append(distance)

            avg_distance = sum(distances) / len(distances) if distances else -1
            print(f"[DEBUG] Ultrasonic distance: {avg_distance} cm")
            return avg_distance

        except Exception as e:
            print(f"[ERROR] Ultrasonic read failed: {e}")
            return -1

    async def react_to_ble_and_take_photo(self, motor, head, camera, photo_dir):
        await self.ble_detector.scan_beacons()
        beacons = self.ble_detector.beacon_data

        if not beacons:
            print("No BLE beacons detected.")
            motor.stop_car()
            return

        # Get the strongest beacon (average RSSI)
        strongest = max(beacons.items(), key=lambda b: sum(b[1]["rssi"]) / len(b[1]["rssi"]))
        addr, data = strongest
        rssi = sum(data["rssi"]) / len(data["rssi"])
        proximity = self.ble_detector.estimate_proximity(addr)
        direction = self.ble_detector.estimate_direction(addr)

        print(f"Beacon: {addr} | RSSI: {rssi:.2f} | Proximity: {proximity} | Direction: {direction}")

        if rssi > -60:
            motor.move_forward(50)
        elif direction == "Approaching":
            motor.move_forward(30)
        elif direction == "Moving Away":
            motor.move_backwards(30)
        else:
            motor.stop_car()

        # Take picture if beacon is close
        if proximity == "Close":
            print("Taking photo...")
            filename = f"{photo_dir}/auto_ble_{int(time.time())}.jpg"
            camera.capture_file(filename)
            print(f"Saved photo: {filename}")

    def cleanup_ultrasonic(self):
        print("Ultrasonic Cleanup")
        # GPIO.cleanup()
