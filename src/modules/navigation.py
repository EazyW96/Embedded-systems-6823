import asyncio
import time
from modules.obstacle_avoidance import ObstacleAvoidance
from modules.motor_control import MotorControl
from modules.sensor_manager import SensorManager

class Navigation:
    def __init__(self, motor: MotorControl, sensor: SensorManager):
        self.motor = motor
        self.sensor = sensor
        self.obstacle_avoidance = ObstacleAvoidance(sensor)
        self.photo_dir = "/home/ciaon/Embedded-systems-6823/ble_images"

    async def start_mission(self):
        """Main mission loop: obstacle avoidance + BLE search."""
        print("Starting autonomous navigation mission...")

        try:
            while True:
                # 1. Obstacle Avoidance
                action = self.obstacle_avoidance.decide_movement()

                if action == "move_forward":
                    self.motor.move_forward(speed=40)
                elif action == "turn_left":
                    self.motor.turn_left(speed=30)
                    await asyncio.sleep(0.5)
                    self.motor.move_forward()
                elif action == "turn_right":
                    self.motor.turn_right(speed=30)
                    await asyncio.sleep(0.5)
                    self.motor.move_forward()
                elif action == "move_backwards":
                    self.motor.move_backwards(speed=30)
                    await asyncio.sleep(0.5)
                    self.motor.move_forward()
                elif action == "stop":
                    self.motor.stop_car()

                # 2. BLE Detection
                beacon_found = await self.sensor.scan_for_beacon()
                if beacon_found:
                    print("Beacon found! Stopping and taking photo...")
                    self.motor.stop_car()
                    await asyncio.sleep(1)

                    from picamera2 import Picamera2
                    camera = Picamera2()
                    camera.configure(camera.create_still_configuration())
                    camera.start()
                    time.sleep(2)
                    timestamp = time.strftime("%Y%m%d-%H%M%S")
                    filename = f"{self.photo_dir}/beacon_detected_{timestamp}.jpg"
                    camera.capture_file(filename)
                    print(f"Photo saved at: {filename}")
                    camera.stop()

                    break

                await asyncio.sleep(0.1)

        except KeyboardInterrupt:
            print("Mission interrupted. Stopping car...")
            self.motor.stop_car()
