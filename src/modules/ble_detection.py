"""
BLE Detection Module.
Scans for nearby BLE devices, tracks RSSI, and estimates proximity/direction.
"""
import time
import asyncio
from bleak import BleakScanner

class BLEBeaconDetector:
    def __init__(self, target_uuid=None, target_mac=None):
        self.target_uuid = target_uuid
        self.target_mac = target_mac.lower() if target_mac else None
        self.beacon_data = {}
        self.rssi_history_length = 5

    async def scan_beacons(self, scan_time=5.0):
        devices = await BleakScanner.discover(timeout=scan_time)
        timestamp = time.time()
        for device in devices:
            name = device.name or "Unknown"
            address = device.address.lower()
            uuids = device.metadata.get("uuids", []) if device.metadata else []

            if (
                self.target_mac and address == self.target_mac
            ) or (
                self.target_uuid and self.target_uuid.lower() in [str(u).lower() for u in uuids]
            ):
                if address not in self.beacon_data:
                    self.beacon_data[address] = {"rssi": [], "timestamps": []}
                self.beacon_data[address]["rssi"].append(device.rssi)
                self.beacon_data[address]["timestamps"].append(timestamp)
                if len(self.beacon_data[address]["rssi"]) > self.rssi_history_length:
                    self.beacon_data[address]["rssi"].pop(0)
                    self.beacon_data[address]["timestamps"].pop(0)

    def estimate_proximity(self, address):
        if address in self.beacon_data and self.beacon_data[address]["rssi"]:
            avg_rssi = sum(self.beacon_data[address]["rssi"]) / len(self.beacon_data[address]["rssi"])
            if avg_rssi > -60:
                return "Close"
            elif avg_rssi > -80:
                return "Medium Distance"
            else:
                return "Far Away"
        else:
            return "Signal Distance Unknown"

    def estimate_direction(self, address, reference_rssi=None):
        if address in self.beacon_data and len(self.beacon_data[address]["rssi"]) > 1:
            rssi_values = self.beacon_data[address]["rssi"]
            current_rssi = rssi_values[-1]
            previous_rssi = rssi_values[-2]
            if reference_rssi is None:
                reference_rssi = previous_rssi
            if current_rssi > reference_rssi + 5:
                return "Approaching"
            elif current_rssi < reference_rssi - 5:
                return "Moving Away"
            else:
                return "Stationary"
        else:
            return "Unknown"

# Test Scanner
async def main():
    # Use your MAC address here
    target_mac = "14:1B:A0:17:11:83"
    detector = BLEBeaconDetector(target_mac=target_mac)

    while True:
        await detector.scan_beacons(scan_time=5.0)
        for address, data in detector.beacon_data.items():
            print(f" [Tracked Beacon] {address}")
            print(f"  RSSI History: {data['rssi']}")
            print(f"  Proximity: {detector.estimate_proximity(address)}")
            print(f"  Direction: {detector.estimate_direction(address)}")
        await asyncio.sleep(2)

if __name__ == "__main__":
    asyncio.run(main())
