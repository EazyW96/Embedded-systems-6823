"""
Motor Control Module.

This module converts movement commands into actions by controlling the DC motors and servo mechanisms.
It includes functions for moving forward, backward, turning, and can incorporate PID control for smoother operations.
"""
import RPi.GPIO as GPIO
import time
from servo_control import Servo
from sensor_manager import SensorManager
from typing import Dict, Optional

class MotorControl:
    def __init__(self, left_motor_pins = (17, 18, 27), right_motor_pins = (22, 23, 24), servo_pin = 25):
        # Initializes the motor and servo with proper pin configurations
        # (May have to alter as testing begins)
        self.left_motor_pins = left_motor_pins
        self.right_motor_pins = right_motor_pins
        self.servo_pin = servo_pin

        GPIO.setmode(GPIO.BCM)

        # Motor 
        GPIO.setup(left_motor_pins[0], GPIO.OUT)
        GPIO.setup(left_motor_pins[1], GPIO.OUT)
        GPIO.setup(left_motor_pins[2], GPIO.OUT)
        GPIO.setup(right_motor_pins[0], GPIO.OUT)
        GPIO.setup(right_motor_pins[1], GPIO.OUT)
        GPIO.setup(right_motor_pins[2], GPIO.OUT)

        self.left_pwm =  GPIO.PWM(left_motor_pins[2], 100)
        # PWM frequency set to 100 Hz (Alter as needed)
        self.right_pwm = GPIO.PWM(right_motor_pins[2], 100)
        self.left_pwm.start(0)
        self.right_pwm.start(0)

        # Instantiate Servo
        self.servo = Servo()

    def move_motor(self, left_direction, right_direction, speed = 50):
        GPIO.output(self.left_motor_pins[0], left_direction[0])
        GPIO.output(self.left_motor_pins[1], left_direction[1])
        GPIO.output(self.right_motor_pins[0], right_direction[0])
        GPIO.output(self.right_motor_pins[1], right_direction[1])
        self.left_pwm.ChangeDutyCycle(speed)
        self.right_pwm.ChangeDutyCycle(speed)


    # Establish movement parameters(speed and pin settins may require alteration)
    def move_forward(self, speed = 50):
       self.move_motor((GPIO.HIGH, GPIO.LOW), (GPIO.HIGH, GPIO.LOW), speed) 

    def move_backwards(self, speed = 50):
        self.move_motor((GPIO.LOW, GPIO.HIGH), (GPIO.LOW, GPIO.HIGH), speed) 

    def turn_left(self, speed = 25):
        self.move_motor((GPIO.LOW, GPIO.HIGH), (GPIO.HIGH, GPIO.LOW), speed) 
    
    def turn_right(self, speed = 25):
        self.move_motor((GPIO.HIGH, GPIO.LOW), (GPIO.LOW, GPIO.HIGH), speed)

    def stop_car(self):
        self.left_pwm.ChangeDutyCycle(0)
        self.right_pwm.ChangeDutyCycle(0)

    def set_servo_angle(self, channel: str, angle: int, error: int = 10):
        # Set the servo to the correct angle  
        self.servo.set_servo_angle(channel, angle, error)
    
    async def react_to_beacons(self, beacon_data: Dict[str, dict[str, Optional[str | int | float]]]):
        # Beacon addresses are added to a string for easier reading
        # Also, react to beacons and controls car direction
        await self.sensor_manager.scan_ble_beacons()
        beacon_data = self.sensor_manager.ble_detector.beacon_data
        if not beacon_data:
            print ("No beacons detected")
            self.stop_car()
            return

        # Logic to have the car approach the strongest beacon signal
        # (Values may require adjustment)
        strongest_beacon_address = max(beacon_data, key = lambda address: sum(beacon_data[address]["rssi"]) / len(beacon_data[address]["rssi"]))
        strongest_beacon = beacon_data[strongest_beacon_address]
        avg_rssi = sum(strongest_beacon["rssi"]) / len(strongest_beacon["rssi"])
        proximity = self.sensor_manager.estimate_ble_proximity(strongest_beacon_address)
        direction = self.sensor_manager.estimate_ble_direction(strongest_beacon_address)

        if avg_rssi > -60:
            print(f"Strong Signal, Move Forward. Proximity to Beacon: {proximity}, Direction: {direction}")
            self.move_forward(speed = 70)
        elif direction == "Approaching Beacon Location":
            print(f"Approaching Beacon. Proximity: {proximity}, Direction: {direction}")
            self.move_forward(speed = 50)
        elif direction == "Moving away from Beacon":
            print(f"Moving away from Beacon Location. Proximity: {proximity}, Direction: {direction}")
            self.move_backwards(speed = 50)
        elif direction == "Left":
            print(f"Beacon is to the left. Proximity: {proximity}, Direction: {direction}")
            self.turn_left(speed = 40)
        elif direction == "Right":
            print(f"Beacon is to the right. Proximity: {proximity}, Direction: {direction}")
            self.turn_right(speed = 40)
        elif proximity == "Close":
            print(f"Beacon is Close. Proximity: {proximity}, Direction: {direction}")
            self.stop_car()
        elif proximity == "Beacon is further away":
            print(f"Beacon is Further away. Proximity: {proximity}, Direction: {direction}")
            self.move_forward(speed = 30)
        elif proximity == "Beacon is Far":
            print(f"Beacon is Far. Proximity: {proximity}, Direction: {direction}")
            self.move_forward(speed = 70)
        else: 
            print(f"Beacon not Found")
            self.stop_car()
    
    def cleanup(self):
        # Clean pins for effective resource management
        self.left_pwm.stop()
        self.right_pwm.stop()
        GPIO.cleanup()

if __name__ == "__main__":
    import asyncio
    controller = MotorControl(target_uuid = "6A4E3E10-6678-11E3-949A-0800200C9A66")

    async def main():
        try:
            while True:
                await controller.react_to_beacons()
                time.sleep(1)
        except KeyboardInterrupt:
            print("Program Terminated")
        finally:
            controller.cleanup()
            controller.sensor_manager.cleanup_ultrasonic()
            controller.sensor_manager.cleanup_camera()

    asyncio.run(main)