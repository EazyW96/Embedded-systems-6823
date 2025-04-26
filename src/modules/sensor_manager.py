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
                GPIO.output(self.trig_pin, True)
                time.sleep(0.00001)
                GPIO.output(self.trig_pin, False)

                timeout = time.time() + 0.05

                while True:
                    if GPIO.input(self.echo_pin):
                        pulse_start = time.time()
                        break
                    if time.time() > timeout:
                        return -1

                while True:
                    if not GPIO.input(self.echo_pin):
                        pulse_end = time.time()
                        break
                    if time.time() > timeout:
                        return -1

                duration = pulse_end - pulse_start
                distance = round(duration * 17150, 2)
                distances.append(distance)

            avg_distance = sum(distances) / len(distances) if distances else -1
            return avg_distance

        except Exception as e:
            print(f"[ERROR] Ultrasonic read failed: {e}")
            return -1

    async def scan_for_beacon(self):
        """Scan for BLE beacon."""
        await self.ble_detector.scan_beacons()
        beacons = self.ble_detector.beacon_data

        if not beacons:
            return False

        strongest = max(beacons.items(), key=lambda b: sum(b[1]["rssi"]) / len(b[1]["rssi"]))
        addr, data = strongest
        rssi = sum(data["rssi"]) / len(data["rssi"])

        print(f"[BLE Detection] Address: {addr} | RSSI: {rssi:.2f}")

        if rssi > -65:
            return True
        else:
            return False

    def cleanup_ultrasonic(self):
        print("Ultrasonic Cleanup")
        # GPIO.cleanup()
