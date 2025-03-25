"""
Sensor Manager Module.

This module is responsible for initializing and managing all sensors,
including the camera, ultrasonic sensor, and BLE module.
It provides a unified interface for retrieving sensor data in real time.
"""
from Ultrasonic import *
import time
import RPi.GPIO as GPIO
import cv2
import asyncio
import bleak
from bleak import BleakScanner, BleakClient
from ble_detection import BLEBeaconDetector

class SensorManager:
    def __init__(self, trig_pin = 17, echo_pin = 18, camera_index = 0, target_uuid = None):
        #Initializes all the sensors
        self.trig_pin = trig_pin
        self.echo_pin = echo_pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.trig_pin, GPIO.OUT)
        GPIO.setup(self.echo_pin, GPIO.IN)

        # Initialize Camera
        self.cap = cv2.VideoCapture(camera_index)
        if not self.cap.isOpened():
            raise IOError("Cannot Start Camera")
        
        # Initialize BLE
        self.target_uuid = target_uuid
        self.beacon_data = {}
        self.rssi_history_length = 5
    
    def get_ultrasonic_distance(self, num_readings = 5):
        # Return distance from the sensor
        try:
            distances = []
            for _ in range(num_readings):
                GPIO.output(self.trig_pin, True)
                time.sleep(0.00001)
                GPIO.output(self.trig_pin, False)
            
                pulse_start = time.time()
                pulse_end = time.time()

                while GPIO.input(self.echo_pin) == 0:
                    pulse_start = time.time()

                while GPIO.input(self.echo_pin) == 1:
                    pulse_end = time.time()

                pulse_duration = pulse_end - pulse_start
                distance = pulse_duration * 17150
                distance = round(distance, 2)
                distance.append(distance)
                return sum(distances) / num_readings
        except Exception as e:
                print(f"Ultrasonic Error: {e}")
                return - 1 # Error Return Value
    
    def capture_camera_frame(self):
        ret, frame = self.capt.read()
        if ret:
            return frame
        else: 
            return None
        
    async def scan_ble_beacons (self, scan_time = 5.0):
        # Scan for beacons using BLE detection functions
        await self.ble_detector.scan_beacons(scan_time = scan_time)

    def estimate_ble_proximity(self, address):
        # Scan for BLE beacon and return proximity
        return self.ble_detector.estimate_proximity(address)

    def estimate_ble_direction(self, address):
        # Determine the BLE beacon direction
        return self.ble_detector.estimate_direction(address)

    def test_ultrasonic_loop(self):
        try:
            while True:
                distance = self.get_ultrasonic_distance()  #Get the distance value
                print(f"Ultrasonic Distance: {distance}) CM")
                time.sleep(1)
        except KeyboardInterrupt:
            print ;("End of Program")

    def cleanup_ultrasonic(self):
        GPIO.cleanup()

    def cleanup_camera(self):
        try:
            self.cap.release()
            cv2.destroyAllWindows()
        except:
            print("Camera Cleanup Failed")

async def main():
    sensor_manager = SensorManager(target_uuid = "6A4E3E10-6678-11E3-949A-0800200C9A66")
    try:
        while True:
            # Ultrasonic Call
            distance = sensor_manager.get_ultrasonic_distance()
            print(f"Ultrasonic Distance: {distance}) CM")

            # Camera Call
            frame = sensor_manager.capture_camera_frame()
            if frame is not None:
                cv2.imshow('Camera Feed' , frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break


    # BLE Call
        await sensor_manager.scan_ble_beacons()
        for address, data in sensor_manager.ble_detector.beacon_data.items():
            print(f" Beacon Address: {address}")
            print(f" RSSI: {data['rssi']}")
            print(f" Estimated Proximity: {sensor_manager.estimate_ble_proximity(address)}")
            print(f" Estimated Direction: {sensor_manager.estimate_ble_direction(address)}")
        
        await asyncio.sleep(1) #Scan for beacon every 2 seconds (will most likely need to be changed)

    except KeyboardInterrupt:
        print("Program Terminated")
    finally:
        sensor_manager.cleanup_ultrasonicd()
        sensor_manager.cleanup_camera()

if __name__ == "__main__":
    asyncio.run(main())