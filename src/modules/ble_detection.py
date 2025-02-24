"""
BLE Detection Module.

This module processes BLE beacon signals by analyzing the Received Signal Strength Indicator (RSSI)
to estimate the beacon's direction and proximity, assisting the navigation module in course correction.
"""

import math
import asyncio
import bleak
import BleakScanner
import BleakClient
import time

class BLEBeaconDetector:
    def __init__(self, target_uuid = None):
        self.target__uuid = target_uuid
        self.beacon_data = {}               # Stores Beacon data 
        self.rssi_history_length = 5        # Will be altered as necessary

    async def scan_beacons (self, scan_time = 5.0):
        devices = await BleakScanner.discover(timeout = scan_time)
        timestamp = time.time()

        for device in devices:
            if self.target_uuid is None or (device.metadata and device.metadata.get("uuids") and self.target_uuid.lower() in [str(u).lower() for u in device.metada["uuids"]]):
                if device.address not in self.beacon_data:
                    self.beacon_data[device.address] = {"rssi": [], "timestamps": []}

                self.beacon_data[device.address]["rssi"].append(device.rssi)
                self.beacon_data[device.address]["timestamps"].append(timestamp)

                # Establish parameters to only keep recent RSSIs
                if len(self.beacon_data[device.address]["rssi"]) > self.rssi_history_length:
                    self.beacon_data[device.address]["rssi"].pop(0)
                    self.beacon_data[device.address]["timestamps"].pop(0)

    def estimate_proximity(self, address):
        if address in self.beacon_daata and self.beacon_data[address]["rssi"]:
            avg_rssi = sum(self.beacon._data[address]["rssi"]) / len(self.beacon_data[address]["rssi"])

            # Distance thresholds (Will be altered as needed)
            if avg_rssi > -60:
                return "Close"
            elif avg_rssi > -80:
                return "Medium Distance"
            else:
                return "Far Away"
        else:
            return "Signal Location Distance Unknown"
    
    def estimate_direction(self, address, reference_rssi = None):
        if address in self.beacon_data and len(self.beacon_data[address]["rssi"]) > 1:
            rssi_values = self.beacon_data[address]["rssi"]
            current_rssi = rssi_values[-1]
            previous_rssi = rssi_values[-2]

            if reference_rssi is None:
                reference_rssi = previous_rssi

            # Thresholds will be altered as required
            if current_rssi > reference_rssi + 5:
                return "Approaching Current Location"
            elif current_rssi < reference_rssi - 5:
                return "Moving Away from Current Location"
            else:
                return "Not Moving"
        else:
            return "Unknown Status"
        