import time
import asyncio
from modules.ble_detection import BLEBeaconDetector
from modules.obstacle_avoidance import ObstacleAvoidance
from modules.motor_control import MotorControl
from modules.head_movement import HeadMovement
from picamera2 import Picamera2

class SensorManager:
    def __init__(self, target_mac, photo_dir, loop):
        self.motors = MotorControl()
        self.head = HeadMovement()
        self.camera = Picamera2()
        self.photo_dir = photo_dir

        self.camera.configure(self.camera.create_still_configuration())
        self.camera.start()
        time.sleep(2)

        self.ble_detector = BLEBeaconDetector(target_mac, photo_dir, loop)
        self.ble_detector.motors = self.motors
        self.ble_detector.camera = self.camera

        self.task_queue = self.ble_detector.task_queue

        self.ble_detector.avoidance = ObstacleAvoidance(loop=loop)
        self.ble_detector.avoidance.init_obstacle_thread(self.task_queue, self.motors)

    def start_all_threads(self):
        print("[SENSOR MANAGER] Starting BLE detection thread")
        self.ble_detector.start_all_threads()
