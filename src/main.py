import asyncio
import time
import os
from modules.sensor_manager import SensorManager

# Set up photo directory
PHOTO_DIR = "/home/ciaon/Embedded-systems-6823/src/ble_images"
os.makedirs(PHOTO_DIR, exist_ok=True)

# Set your BLE MAC address
ble_mac = "14:1B:A0:17:11:83"

async def main():
    loop = asyncio.get_running_loop()  # ? Get the current event loop
    sensor = SensorManager(target_mac=ble_mac, photo_dir=PHOTO_DIR, loop=loop)
    sensor.start_all_threads()
    task_queue = sensor.task_queue

    try:
        while True:
            priority, task = await task_queue.get()
            task()

    except KeyboardInterrupt:
        print("Stopping car.")
    finally:
        sensor.camera.stop()
        sensor.motors.stop_car()

if __name__ == "__main__":
    asyncio.run(main())
