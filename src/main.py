import asyncio
import time
import os
from modules.motor_control import MotorControl
from modules.sensor_manager import SensorManager
from modules.navigation import Navigation

PHOTO_DIR = "/home/ciaon/Embedded-systems-6823/ble_images"
os.makedirs(PHOTO_DIR, exist_ok=True)

TARGET_MAC = "14:1B:A0:17:11:83"

async def main():
    motor = MotorControl()
    sensor = SensorManager(target_mac=TARGET_MAC)
    navigation = Navigation(motor, sensor)

    try:
        await navigation.start_mission()
    except KeyboardInterrupt:
        print("Shutdown requested.")
    finally:
        motor.cleanup()
        sensor.cleanup_ultrasonic()
        print("Cleanup complete.")

if __name__ == "__main__":
    asyncio.run(main())
