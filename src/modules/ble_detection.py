import threading, time, bluetooth, asyncio
from collections import defaultdict

class BLEBeaconDetector:
    def __init__(self, target_mac, photo_dir, loop):
        self.target_mac = target_mac
        self.photo_dir = photo_dir
        self.loop = loop
        self.task_queue = asyncio.Queue()
        self.beacon_data = defaultdict(lambda: {"rssi": [], "timestamps": []})
        self.motors = self.camera = self.sensor = self.avoidance = None
        self.running = True

    def start_all_threads(self):
        threading.Thread(target=self.scan_beacons, daemon=True).start()

    def scan_beacons(self):
        print("[BLE] Scanning for beacons...")
        while self.running:
            try:
                for addr, _ in bluetooth.discover_devices(duration=5, lookup_names=True):
                    if addr == self.target_mac:
                        rssi = self.get_rssi_for_device(addr)
                        if rssi:
                            d = self.beacon_data[addr]
                            d["rssi"].append(rssi)
                            d["timestamps"].append(time.time())
                            if len(d["rssi"]) > 5:
                                d["rssi"].pop(0), d["timestamps"].pop(0)
                            asyncio.run_coroutine_threadsafe(
                                self.task_queue.put((1, lambda: self.react_to_ble_and_take_photo(
                                    self.beacon_data, self.motors, self.camera, self.photo_dir
                                ))), self.loop
                            )
            except Exception as e:
                print(f"[BLE] Scan error: {e}")
            time.sleep(1)

    def get_rssi_for_device(self, addr): return -65

    def _avg_rssi(self, r): return sum(r) / len(r) if r else -999

    def estimate_proximity(self, r): return (
        "Close" if r > -60 else "Medium Distance" if r > -80 else "Far Away"
    )

    def estimate_direction(self, r): return (
        "Approaching" if len(r) >= 2 and r[-1] > r[-2] else "Moving Away"
    )

    def react_to_ble_and_take_photo(self, beacons, motor, camera, photo_dir):
        print("[QUEUE] Running BLE task")
        addr, d = max(beacons.items(), key=lambda b: self._avg_rssi(b[1]["rssi"]))
        rssi = self._avg_rssi(d["rssi"])
        prox = self.estimate_proximity(rssi)
        direction = self.estimate_direction(d["rssi"])
        print(f"Beacon: {addr} | RSSI: {rssi:.2f} | Proximity: {prox} | Direction: {direction}")

        if self.avoidance and self.avoidance.check_and_avoid(motor):
            print("[BLE] Retrying task after avoidance...")
            asyncio.run_coroutine_threadsafe(
                self.task_queue.put((1, lambda: self.react_to_ble_and_take_photo(
                    beacons, motor, camera, photo_dir
                ))), self.loop
            )
            return

        if rssi > -60 or direction == "Approaching":
            motor.move_forward(speed=700)
        elif direction == "Moving Away":
            motor.turn_right(speed=2000)
            time.sleep(3)
            motor.stop_car()
            time.sleep(0.1)
            motor.move_forward(speed=700)
        else:
            motor.stop_car()

        if prox == "Close":
            motor.stop_car()
            print("Taking photo...")
            camera.capture_file(f"{photo_dir}/auto_ble_{int(time.time())}.jpg")
